# CCC Industry Certificate Pathways

A static site about California Community Colleges courses, built by faculty, that turn industry certificates (starting with Google Career Certificates) into college credit. Faculty can download every course as a Canvas .imscc package.

Scope: courses, CPL, content development, and the statewide rollout. AI productivity tools are out of scope on purpose, and the checks enforce it.

## Layout
- `index, courses, cpl, rollout, partners, getting-started, faq .html`: the pages
- `js/components.js`: the shared header, navigation, and footer
- `downloads/`: course packages, `manifest.json`, and the all-courses bundle. Generated; never edit by hand.
- `docs/`: faculty reference documents
- `tools/sync_packages.py`: pulls the latest built packages in and updates every download link
- `tests/run_checks.py`: release checks. `tests/self_test.py` proves the checks catch breakage.

## Updating the courses
1. Change the course content in the build system (`imscc-output/v2`, see the ccc-da-courses skill). Bump `PACKAGE_VERSION` in `imscc_lib.py`, then run `python3 build_all.py`.
2. `python3 tools/sync_packages.py`
3. `python3 tests/run_checks.py --online`. Every check must pass.
4. Commit and push. GitHub Actions re-runs the checks, deploys only if they pass, and then checks the live site and every download.

## Updating page text
Edit the HTML and run `python3 tests/run_checks.py`. The checks catch broken links, missing downloads, banned or out-of-scope terms, leftover placeholders, and course counts that don't match the packages.
