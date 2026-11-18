#!/usr/bin/env python3
"""Copy the latest built course packages into downloads/ and point every
download button at them.

Usage:  python3 tools/sync_packages.py [BUILD_DIR]

BUILD_DIR defaults to the course build system's organized output
(imscc-output/v2/v3/imscc, containing regular/ and cpl/).

What it does:
  1. Replaces downloads/regular and downloads/cpl with the packages in BUILD_DIR
  2. Builds downloads/CCC-Data-Analytics-All-Courses-vX.Y.zip (all packages)
  3. Writes downloads/manifest.json (course, variant, file, bytes, sha256, version)
  4. Rewrites the href of every <a data-course=".." data-variant=".."> link and
     every <a data-bundle> link in the site's HTML pages
Run tests/run_checks.py afterwards.
"""
import hashlib, json, os, re, shutil, sys, zipfile

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_BUILD = os.path.expanduser(
    "~/dev/ccc/google-certs-tools/docs/google-data-analytics-focus-group-jan-2025/imscc-output/v2/v3/imscc")
NAME_RE = re.compile(r"CCC-Google-(DA-\d{3})(_cpl)?-.*-v(\d+\.\d+)\.imscc$")

def main():
    build = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BUILD
    dl = os.path.join(SITE, "downloads")
    entries, versions = [], set()
    for variant in ("regular", "cpl"):
        src_dir = os.path.join(build, variant)
        files = sorted(f for f in os.listdir(src_dir) if f.endswith(".imscc"))
        if not files:
            sys.exit(f"no .imscc files in {src_dir}")
        dst_dir = os.path.join(dl, variant)
        shutil.rmtree(dst_dir, ignore_errors=True)
        os.makedirs(dst_dir)
        for f in files:
            m = NAME_RE.match(f)
            if not m:
                sys.exit(f"unexpected package name: {f}")
            code, is_cpl, ver = m.group(1), bool(m.group(2)), m.group(3)
            if is_cpl != (variant == "cpl"):
                sys.exit(f"{f} is in the wrong folder ({variant})")
            versions.add(ver)
            shutil.copy2(os.path.join(src_dir, f), os.path.join(dst_dir, f))
            data = open(os.path.join(dst_dir, f), "rb").read()
            entries.append({"course": code, "variant": variant,
                            "file": f"downloads/{variant}/{f}", "bytes": len(data),
                            "sha256": hashlib.sha256(data).hexdigest(), "version": ver})
    if len(versions) != 1:
        sys.exit(f"mixed package versions in build: {sorted(versions)}")
    version = versions.pop()

    for old in os.listdir(dl):
        if old.startswith("CCC-Data-Analytics-All-Courses-"):
            os.remove(os.path.join(dl, old))
    bundle = f"downloads/CCC-Data-Analytics-All-Courses-v{version}.zip"
    with zipfile.ZipFile(os.path.join(SITE, bundle), "w", zipfile.ZIP_DEFLATED) as z:
        for e in entries:
            z.write(os.path.join(SITE, e["file"]), arcname=e["file"].split("downloads/", 1)[1])
    json.dump({"version": version, "bundle": bundle, "packages": entries},
              open(os.path.join(dl, "manifest.json"), "w"), indent=2)

    lookup = {(e["course"], e["variant"]): e["file"] for e in entries}
    link_re = re.compile(r'<a ([^>]*?)data-course="(DA-\d{3})" data-variant="(regular|cpl)"([^>]*)>')
    for page in sorted(p for p in os.listdir(SITE) if p.endswith(".html")):
        path = os.path.join(SITE, page)
        html = open(path).read()
        def fix(m):
            key = (m.group(2), m.group(3))
            if key not in lookup:
                sys.exit(f"{page}: no package for {key}")
            attrs = re.sub(r'href="[^"]*"', f'href="{lookup[key]}"', m.group(0))
            return attrs
        new = link_re.sub(fix, html)
        new = re.sub(r'<a [^>]*\bdata-bundle\b[^>]*>',
                     lambda m: re.sub(r'href="[^"]*"', f'href="{bundle}"', m.group(0)), new)
        new = re.sub(r'(<span data-version>)[^<]*(</span>)', rf'\g<1>v{version}\g<2>', new)
        if new != html:
            open(path, "w").write(new)
            print(f"updated links in {page}")
    print(f"synced {len(entries)} packages, version {version}, bundle {bundle}")

if __name__ == "__main__":
    main()
