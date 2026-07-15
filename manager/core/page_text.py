from __future__ import annotations

import json
from pathlib import Path

from manager.core.config import Config
from manager.core.paths import IssuePaths
from manager.core.file_manager import write_json_atomic
from manager.core.json_builder import build_page_data_template


def load_page_text(root: Path, config: Config, issue_id: str) -> list[dict]:
    path = IssuePaths(root, issue_id, config).page_data
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
    return data if isinstance(data, list) else []


def page_text_for_edit(root: Path, config: Config, issue_id: str, page_count: int) -> list[dict]:
    existing = load_page_text(root, config, issue_id)
    template = build_page_data_template(page_count)
    rows: list[dict] = []
    for n in range(page_count):
        base = template[n]
        if n < len(existing) and isinstance(existing[n], dict):
            e = existing[n]
            rows.append({
                "title": e.get("title") or base["title"],
                "text": e.get("text", ""),
                "captions": e.get("captions", ""),
            })
        else:
            rows.append(base)
    return rows


def save_page_text(root: Path, config: Config, issue_id: str, entries: list[dict]) -> None:
    path = IssuePaths(root, issue_id, config).page_data
    write_json_atomic(path, entries)
