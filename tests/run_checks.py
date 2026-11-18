#!/usr/bin/env python3
"""Release checks for the CCC Industry Certificate Pathways site.

Run before every publish:

    python3 tests/run_checks.py            # offline checks (fast, no network)
    python3 tests/run_checks.py --online   # also checks every external link
    python3 tests/run_checks.py --live https://dorairajsanjay.github.io/ccc-google-da-courses/
                                           # also checks the deployed site's pages and downloads

Exit code 0 = safe to publish. Any FAIL line = do not publish.
"""
import hashlib, json, os, re, sys, zipfile
from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag, unquote

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imscc_check import check_package  # noqa: E402

# ── What the site promises. Change these only when the catalog really changes. ──
PAGES = ["index.html", "courses.html", "cpl.html", "rollout.html",
         "partners.html", "getting-started.html", "faq.html"]
REGULAR_COURSES = ["DA-101", "DA-102", "DA-103", "DA-104", "DA-105",
                   "DA-201", "DA-202", "DA-203", "DA-204", "DA-205"]
CPL_COURSES = [c for c in REGULAR_COURSES if c != "DA-205"]  # capstone has no CPL
CPL_UNITS = 5 * 1 + 4 * 3  # five 1-unit + four 3-unit CPL courses = 17

# Out-of-scope or must-never-appear text (site pages, scripts, and course packages).
BANNED = {
    r"\bgemini\b": "Google AI tools are out of scope",
    r"notebook\s?lm": "Google AI tools are out of scope",
    r"google workspace": "Google AI tools are out of scope",
    r"digital center": "tools-rollout partner page is out of scope",
    r"\bibm\b|skillsbuild": "IBM is not to be named on the site",
    r"@gmail\.com": "use institutional email addresses only",
    r"to be announced|\bTBD\b|lorem ipsum|\bTODO\b": "unfinished placeholder text",
}
# Bracketed fill-in fields allowed on purpose (faculty customize these after import).
ALLOWED_BRACKETS = {"[Your College]", "[Instructor Name]", "[Semester]",
                    "[instructor-email@college.edu]", "[Email]", "[Office Hours]",
                    "[Semester Year]"}
# External hosts that block automated checks but work in a browser.
BOT_BLOCKED = {"www.linkedin.com", "www.instagram.com"}

results = {"pass": 0, "fail": 0, "warn": 0}


def report(ok, msg, warn=False):
    if ok:
        results["pass"] += 1
        return
    key = "warn" if warn else "fail"
    results[key] += 1
    print(f"{'WARN' if warn else 'FAIL'}  {msg}")


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.text, self.title = [], set(), [], ""
        self.scripts, self._in, self.imgs_no_alt = [], None, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.links.append(("a", a["href"], a))
        if tag == "link" and "href" in a:
            self.links.append(("link", a["href"], a))
        if tag in ("script", "img") and "src" in a:
            self.links.append((tag, a["src"], a))
        if tag == "script" and "src" in a:
            self.scripts.append(a["src"])
        if tag == "img" and not a.get("alt"):
            self.imgs_no_alt += 1
        if tag in ("title", "script", "style"):
            self._in = tag

    def handle_endtag(self, tag):
        if tag == self._in:
            self._in = None

    def handle_data(self, data):
        if self._in == "title":
            self.title += data
        elif self._in is None:
            self.text.append(data)


def parse(path):
    p = Page()
    p.feed(open(path, encoding="utf-8").read())
    p.visible = re.sub(r"\s+", " ", " ".join(p.text))
    return p


def fetch(url, method="HEAD"):
    """HTTP status via curl (uses the system certificate store; present on macOS and CI)."""
    import subprocess
    cmd = ["curl", "-s", "-o", "/dev/null", "-L", "--max-time", "25",
           "-A", "Mozilla/5.0 (site-check)", "-w", "%{http_code}", url]
    if method == "HEAD":
        cmd.insert(1, "-I")
    out = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
    code = int(out) if out.isdigit() else 0
    if method == "HEAD" and code in (0, 403, 405):
        return fetch(url, "GET")
    return code if code else "no response"


def check_pages():
    print("── Pages, navigation, and internal links")
    parsed, external = {}, set()
    for name in PAGES:
        path = os.path.join(SITE, name)
        report(os.path.exists(path), f"{name}: page missing")
        if not os.path.exists(path):
            continue
        p = parsed[name] = parse(path)
        html = open(path, encoding="utf-8").read()
        report(p.title.strip() != "", f"{name}: missing <title>")
        report('id="site-header"' in html and 'id="site-footer"' in html,
               f"{name}: missing shared header/footer placeholder")
        report("js/components.js" in p.scripts, f"{name}: does not load js/components.js")
        report('name="viewport"' in html, f"{name}: missing mobile viewport meta tag")
        report(p.imgs_no_alt == 0, f"{name}: {p.imgs_no_alt} image(s) without alt text")

    nav = open(os.path.join(SITE, "js/components.js"), encoding="utf-8").read()
    for href in re.findall(r"href: '([^']+)'", nav):
        report(href in PAGES, f"navigation links to unknown page {href}")
    for name in PAGES:
        report(f"'{name}'" in nav, f"{name} is not in the site navigation", warn=True)
    nav_links = re.findall(r'<a href="(https?://[^"]+)"', nav)
    external.update(nav_links)

    for name, p in parsed.items():
        for kind, href, attrs in p.links:
            if href.startswith(("mailto:", "tel:")):
                report(re.match(r"mailto:[^@\s]+@[^@\s]+\.\w+$", href) is not None,
                       f"{name}: malformed email link {href}")
                continue
            if href.startswith(("http://", "https://")):
                external.add(href)
                continue
            report(href not in ("#", ""), f"{name}: empty link ({kind}) {attrs}")
            target, frag = urldefrag(href)
            target = unquote(target) or name
            full = os.path.normpath(os.path.join(SITE, target))
            report(os.path.exists(full), f"{name}: broken link -> {href}")
            if frag and target.endswith(".html") and target in parsed:
                report(frag in parsed[target].ids, f"{name}: missing anchor #{frag} in {target}")
    return parsed, external


def check_downloads(parsed):
    print("── Course downloads")
    manifest_path = os.path.join(SITE, "downloads/manifest.json")
    report(os.path.exists(manifest_path), "downloads/manifest.json missing (run tools/sync_packages.py)")
    if not os.path.exists(manifest_path):
        return None
    m = json.load(open(manifest_path))
    pk = m["packages"]
    have = {(e["course"], e["variant"]) for e in pk}
    for c in REGULAR_COURSES:
        report((c, "regular") in have, f"no downloadable package for {c}")
    for c in CPL_COURSES:
        report((c, "cpl") in have, f"no downloadable CPL package for {c}")
    report(len(pk) == len(REGULAR_COURSES) + len(CPL_COURSES),
           f"expected {len(REGULAR_COURSES) + len(CPL_COURSES)} packages, manifest has {len(pk)}")
    report(len({e['version'] for e in pk}) == 1, "packages have mixed versions")

    for e in pk:
        path = os.path.join(SITE, e["file"])
        if not os.path.exists(path):
            report(False, f"{e['file']} listed in manifest but missing")
            continue
        data = open(path, "rb").read()
        report(hashlib.sha256(data).hexdigest() == e["sha256"],
               f"{e['file']}: changed since last sync (re-run tools/sync_packages.py)")
        errors, warnings, info = check_package(path)
        for x in errors:
            report(False, f"{e['file']}: {x}")
        for x in warnings:
            report(False, f"{e['file']}: {x}")
        expect = f"{e['course']}:"
        report((info.get("title") or "").startswith(expect),
               f"{e['file']}: course title {info.get('title')!r} does not match {e['course']}")
        z = zipfile.ZipFile(path)
        body = " ".join(z.read(n).decode("utf-8", "replace") for n in z.namelist()
                        if n.endswith((".html", ".xml")))
        for pat, why in BANNED.items():
            if pat.startswith(r"\bibm"):
                continue  # course evidence lists may name other certificates
            hit = re.search(pat, body, re.I)
            report(hit is None, f"{e['file']}: contains '{hit.group(0) if hit else ''}' ({why})")
        for ph in set(re.findall(r"\[[^\]\[<>]{3,40}\]", re.sub(r"<[^>]+>", " ", body))):
            if re.fullmatch(r"\[[A-Z0-9_]{4,}\]", ph):
                report(False, f"{e['file']}: unfilled build placeholder {ph}")

    bundle = os.path.join(SITE, m["bundle"])
    report(os.path.exists(bundle), f"bundle {m['bundle']} missing")
    if os.path.exists(bundle):
        names = set(zipfile.ZipFile(bundle).namelist())
        expected = {e["file"].split("downloads/", 1)[1] for e in pk}
        report(names == expected, f"bundle contents differ from manifest: {sorted(names ^ expected)[:4]}")

    # Every download button points at the right package, and every package has a button.
    linked = set()
    for name in PAGES:
        html = open(os.path.join(SITE, name), encoding="utf-8").read()
        for tag in re.findall(r"<a [^>]*data-course=[^>]*>", html):
            c = re.search(r'data-course="([^"]+)"', tag).group(1)
            v = re.search(r'data-variant="([^"]+)"', tag).group(1)
            href = re.search(r'href="([^"]+)"', tag).group(1)
            want = next((e["file"] for e in pk if e["course"] == c and e["variant"] == v), None)
            report(href == want, f"{name}: {c} {v} button points to {href}, expected {want}")
            linked.add((c, v))
        for tag in re.findall(r"<a [^>]*data-bundle[^>]*>", html):
            report(f'href="{m["bundle"]}"' in tag, f"{name}: 'download all' link is stale")
        for v in re.findall(r"<span data-version>([^<]*)</span>", html):
            report(v == f"v{m['version']}", f"{name}: shows version {v}, packages are v{m['version']}")
    for key in have:
        report(key in linked, f"package {key} has no download button on the site")
    return m


def check_content(parsed, manifest):
    print("── Content rules and consistency")
    texts = {n: p.visible for n, p in parsed.items()}
    texts["js/components.js"] = open(os.path.join(SITE, "js/components.js"), encoding="utf-8").read()
    for name, text in texts.items():
        for pat, why in BANNED.items():
            hit = re.search(pat, text, re.I)
            report(hit is None, f"{name}: contains '{hit.group(0) if hit else ''}' ({why})")
        for ph in set(re.findall(r"\[[^\]\[]{2,40}\]", text)):
            report(ph in ALLOWED_BRACKETS, f"{name}: unexpected bracketed placeholder {ph}")

    if manifest:
        n_reg = sum(1 for e in manifest["packages"] if e["variant"] == "regular")
        n_cpl = len(manifest["packages"]) - n_reg
        total = n_reg + n_cpl
        for name, text in texts.items():
            for num in re.findall(r"\b(\d+) (?:ready-to-adopt |faculty-built )?(?:Canvas )?courses\b", text, re.I):
                if int(num) > 5:
                    report(int(num) in (total, n_reg),
                           f"{name}: says '{num} courses' but there are {total} packages ({n_reg} regular)")
            for num in re.findall(r"(?<!Tier )\b(\w+) CPL (?:course variants|courses)\b", text):
                val = {"nine": 9}.get(num.lower(), int(num) if num.isdigit() else None)
                if val is not None:
                    report(val == n_cpl, f"{name}: says '{num} CPL courses' but there are {n_cpl}")
        cpl = texts.get("cpl.html", "")
        stat = re.search(r"(\d+) Units Available", cpl, re.I)
        report(stat is not None and int(stat.group(1)) == CPL_UNITS,
               f"cpl.html: 'Units Available' should be {CPL_UNITS}")


def check_external(urls):
    print(f"── External links ({len(urls)})")
    for u in sorted(urls):
        host = re.match(r"https?://([^/]+)", u).group(1)
        code = fetch(u)
        ok = isinstance(code, int) and code < 400
        if ok:
            report(True, "")
        elif host in BOT_BLOCKED or code == 429:
            # Social sites and rate limiters refuse automated checks but work in a browser.
            report(False, f"external link {u} -> {code} (blocks automated checks; verify by hand if this persists)", warn=True)
        else:
            report(False, f"external link {u} -> {code}")


def check_live(base, manifest):
    print(f"── Live site {base}")
    base = base if base.endswith("/") else base + "/"
    for name in PAGES:
        code = fetch(urljoin(base, name), "GET")
        report(code == 200, f"live {name} -> {code}")
    for path in [e["file"] for e in manifest["packages"]] + [manifest["bundle"]]:
        code = fetch(urljoin(base, path.replace("(", "%28").replace(")", "%29")), "GET")
        report(code == 200, f"live download {path} -> {code}")


def main():
    args = sys.argv[1:]
    parsed, external = check_pages()
    manifest = check_downloads(parsed)
    check_content(parsed, manifest)
    if "--online" in args:
        check_external(external)
    if "--live" in args and manifest:
        check_live(args[args.index("--live") + 1], manifest)
    print(f"\n{results['pass']} passed, {results['fail']} failed, {results['warn']} warnings")
    if results["fail"]:
        print("DO NOT PUBLISH: fix the FAIL lines above.")
        sys.exit(1)
    print("All checks passed. Safe to publish.")


if __name__ == "__main__":
    main()
