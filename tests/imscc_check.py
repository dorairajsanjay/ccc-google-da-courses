"""Structural validation of Canvas .imscc course packages."""
import re, sys, zipfile, xml.etree.ElementTree as ET
from urllib.parse import unquote

PLACEHOLDER_RE = re.compile(r'\[(NOTEBOOKLM[A-Z_]*|[A-Z][A-Z_]{3,}_URL|TODO|TBD)\]')

def check_package(path):
    """Return (errors, warnings, info) for one .imscc file."""
    errors, warnings, info = [], [], {}
    try:
        z = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        return [f"not a valid zip archive"], [], info
    bad = z.testzip()
    if bad:
        errors.append(f"corrupt member in archive: {bad}")
    names = set(z.namelist())
    if 'imsmanifest.xml' not in names:
        return errors + ["missing imsmanifest.xml"], warnings, info
    try:
        root = ET.fromstring(z.read('imsmanifest.xml'))
    except ET.ParseError as e:
        return errors + [f"imsmanifest.xml does not parse: {e}"], warnings, info
    ns = {'c': root.tag.split('}')[0].strip('{')} if root.tag.startswith('{') else {}
    p = 'c:' if ns else ''
    title = root.find(f'.//{p}organization/{p}item/{p}title', ns) if ns else None
    lom_title = None
    for el in root.iter():
        if el.tag.endswith('}string') and el.text and lom_title is None:
            lom_title = el.text.strip()
    info['title'] = lom_title
    resources = root.findall(f'.//{p}resource', ns)
    info['resources'] = len(resources)
    if not resources:
        errors.append("manifest lists no resources")
    missing = []
    for r in resources:
        for f in r.findall(f'{p}file', ns):
            href = unquote(f.get('href', ''))
            if href and href not in names:
                missing.append(href)
    if missing:
        errors.append(f"{len(missing)} manifest file(s) missing from archive, e.g. {missing[:3]}")
    # content checks on html/xml bodies
    placeholders = set()
    empty_pages = []
    for n in names:
        if n.endswith(('.html', '.xml')) and n != 'imsmanifest.xml':
            body = z.read(n).decode('utf-8', 'replace')
            placeholders.update(PLACEHOLDER_RE.findall(body))
            if n.endswith('.html') and len(re.sub(r'<[^>]+>|\s', '', body)) < 20:
                empty_pages.append(n)
    if placeholders:
        warnings.append(f"unfilled content placeholders: {sorted(placeholders)}")
    if empty_pages:
        warnings.append(f"{len(empty_pages)} near-empty page(s), e.g. {empty_pages[:2]}")
    info['files'] = len(names)
    return errors, warnings, info

if __name__ == '__main__':
    rc = 0
    for path in sys.argv[1:]:
        e, w, i = check_package(path)
        status = 'FAIL' if e else ('WARN' if w else 'OK')
        print(f"{status:4} {path.split('/')[-1]}  title={i.get('title')!r} resources={i.get('resources')}")
        for x in e: print('     ERROR:', x)
        for x in w: print('     warn :', x)
        rc |= bool(e)
    sys.exit(rc)
