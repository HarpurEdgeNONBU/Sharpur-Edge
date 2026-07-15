# Archive Manager (Desktop GUI)

A local desktop app for managing the Sharpur Edge magazine archive without a terminal.

## Install (one time)

```bash
py -m pip install -r manager/requirements.txt
```

## Run

```bash
py manager/run.py
```

## What it does

- **Dashboard** — see every issue; delete safely (removes PDF, cover, pages, page JSON, and the magazines.json entry, all-or-nothing).
- **Add Issue** — drop a PDF, fill the form, click Generate. Produces page WebPs, a cover, the page-text JSON, and the magazines.json entry.
- **Explorer** — read-only integrity check (missing covers/pages/JSON, page-count mismatches).
- **Git** — optional Pull / Commit / Push.

Settings live in `manager/config/config.yaml` (output folders, image DPI/quality, categories).

Everything is keyed off `issue_id`. The terminal script `scripts/generate-webp.py` still works and now shares the same core logic.
