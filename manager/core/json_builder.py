from __future__ import annotations

import re

from manager.core.config import Config


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def build_page_data_template(num_pages: int) -> list[dict]:
    return [
        {"title": f"Page {n}", "text": "", "captions": ""}
        for n in range(1, num_pages + 1)
    ]


def build_magazines_entry(
    issue_id: str, metadata: dict, page_count: int, config: Config
) -> dict:
    fmt = config.image.format
    return {
        "id": issue_id,
        "title": metadata.get("title", ""),
        "year": str(metadata.get("year", "")),
        "category": metadata.get("category", ""),
        "pageCount": page_count,
        "pdf": f"{config.pdfs_dir}/{issue_id}.pdf",
        "cover": f"{config.covers_dir}/{issue_id}.{fmt}",
        "description": metadata.get("description", ""),
    }
