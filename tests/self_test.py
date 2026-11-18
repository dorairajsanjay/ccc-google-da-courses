#!/usr/bin/env python3
"""Proves run_checks.py catches real breakage. Copies the site to a temp folder,
applies one sabotage at a time, and confirms the checks FAIL each time.

    python3 tests/self_test.py
"""
import os, re, shutil, subprocess, sys, tempfile, zipfile

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def edit(path, old, new):
    t = open(path).read()
    assert old in t, (path, old)
    open(path, "w").write(t.replace(old, new, 1))

def corrupt_package(root):
    p = os.path.join(root, "downloads/regular")
    f = os.path.join(p, sorted(os.listdir(p))[0])
    open(f, "wb").write(b"not a zip")

def add_placeholder_to_package(root):
    p = os.path.join(root, "downloads/cpl")
    f = os.path.join(p, sorted(os.listdir(p))[0])
    tmp = f + ".tmp"
    with zipfile.ZipFile(f) as zin, zipfile.ZipFile(tmp, "w") as zout:
        for n in zin.namelist():
            data = zin.read(n)
            if n.endswith(".html"):
                data = data.replace(b"</body>", b"<p>[NOTEBOOKLM_PODCAST_URL]</p></body>", 1)
            zout.writestr(n, data)
    os.replace(tmp, f)

SABOTAGE = {
    "deleted a course package": lambda r: os.remove(os.path.join(r, "downloads/cpl", sorted(os.listdir(os.path.join(r, "downloads/cpl")))[0])),
    "corrupted a course package": corrupt_package,
    "unfilled placeholder inside a course": add_placeholder_to_package,
    "broken internal link": lambda r: edit(os.path.join(r, "index.html"), 'href="courses.html"', 'href="course.html"'),
    "out-of-scope tool mention": lambda r: edit(os.path.join(r, "faq.html"), "Industry partners such as Google", "Gemini and NotebookLM"),
    "wrong CPL unit total": lambda r: edit(os.path.join(r, "cpl.html"), '<span class="num">17</span>', '<span class="num">14</span>'),
    "download button pointing at old version": lambda r: edit(os.path.join(r, "courses.html"), "-v3.1.imscc", "-v3.0.imscc"),
}

def run(root):
    return subprocess.run([sys.executable, "-I", os.path.join(root, "tests/run_checks.py")],
                          capture_output=True, text=True)

def main():
    base = run(SITE)
    if base.returncode != 0:
        print("Baseline checks fail; fix those first.\n" + base.stdout[-2000:])
        sys.exit(1)
    caught = 0
    for name, sabotage in SABOTAGE.items():
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "site")
            shutil.copytree(SITE, root, ignore=shutil.ignore_patterns(".git"))
            sabotage(root)
            r = run(root)
            fails = [l for l in r.stdout.splitlines() if l.startswith("FAIL")]
            ok = r.returncode != 0 and fails
            caught += bool(ok)
            print(f"{'CAUGHT ' if ok else 'MISSED '} {name}: {fails[0][6:110] if fails else 'no failure reported'}")
    print(f"\n{caught}/{len(SABOTAGE)} sabotage cases caught")
    sys.exit(0 if caught == len(SABOTAGE) else 1)

if __name__ == "__main__":
    main()
