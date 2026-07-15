#!/usr/bin/env python3
"""Thin CLI wrapper around manager.core. Kept for terminal users.

Run from the project root:

    python scripts/generate-webp.py magazines/my-magazine.pdf

Rendering logic now lives in manager/core (single source of truth).
"""
import argparse
import sys
from pathlib import Path

# Make the repo root importable so `manager` is a package.
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from manager.core.config import load_config
from manager.core.generator import generate_issue
from manager.core.json_builder import slugify


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a magazine PDF to WebP assets.")
    parser.add_argument("pdf", help="Path to a magazine PDF, e.g. magazines/issue.pdf")
    parser.add_argument("--id", dest="issue_id", help="Override the generated issue ID.")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"\nERROR: File not found: {pdf_path}\n")
        sys.exit(1)

    config = load_config()
    issue_id = args.issue_id or slugify(pdf_path.stem)
    metadata = {
        "issue_id": issue_id,
        "title": "Your Title Here",
        "year": "2026",
        "category": "Fall Issue",
        "description": "Short description.",
    }

    def progress(step: str, current: int, total: int) -> None:
        if step == "pages":
            print(f"   Page {current}/{total}", end="\r")
        else:
            print(f"{step}...")

    print(f"\nPDF: {pdf_path}\nID: {issue_id}\n")
    result = generate_issue(pdf_path, metadata, config, progress_cb=progress)

    if not result.success:
        print(f"\nERROR: {result.error}\n")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("magazines.json entry (already added — edit the placeholder text):\n")
    print(result.json_snippet)
    print("=" * 60 + "\nDone.\n")


if __name__ == "__main__":
    main()
