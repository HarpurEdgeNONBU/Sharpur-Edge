from __future__ import annotations

import json
import os
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from manager.core.config import Config
from manager.core.paths import IssuePaths, magazines_json


def write_json_atomic(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def read_magazines(root: Path, config: Config) -> list[dict]:
    path = magazines_json(root, config)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def issue_exists(root: Path, config: Config, issue_id: str) -> bool:
    return any(m.get("id") == issue_id for m in read_magazines(root, config))


def upsert_magazines_entry(root: Path, config: Config, entry: dict) -> None:
    mags = read_magazines(root, config)
    for i, m in enumerate(mags):
        if m.get("id") == entry["id"]:
            mags[i] = entry
            break
    else:
        mags.append(entry)
    write_json_atomic(magazines_json(root, config), mags)


def remove_magazines_entry(root: Path, config: Config, issue_id: str) -> bool:
    mags = read_magazines(root, config)
    new = [m for m in mags if m.get("id") != issue_id]
    if len(new) == len(mags):
        return False
    write_json_atomic(magazines_json(root, config), new)
    return True


@dataclass
class DeleteReport:
    issue_id: str
    removed: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)


def delete_issue(root: Path, config: Config, issue_id: str) -> DeleteReport:
    if not issue_exists(root, config, issue_id):
        raise ValueError(f"Issue not found in magazines.json: {issue_id}")

    p = IssuePaths(root, issue_id, config)
    report = DeleteReport(issue_id=issue_id)

    file_targets = [p.pdf, p.cover, p.page_data]
    for target in file_targets:
        rel = _rel(root, target)
        if target.exists():
            target.unlink()
            report.removed.append(rel)
        else:
            report.missing.append(rel)

    if p.pages_dir.exists():
        shutil.rmtree(p.pages_dir)
        report.removed.append(_rel(root, p.pages_dir) + "/")
    else:
        report.missing.append(_rel(root, p.pages_dir) + "/")

    if remove_magazines_entry(root, config, issue_id):
        report.removed.append("library/magazines.json entry")
    return report


def _rel(root: Path, target: Path) -> str:
    try:
        return target.relative_to(root).as_posix()
    except ValueError:
        return str(target)


@dataclass
class IssueStatus:
    issue_id: str
    title: str
    has_cover: bool
    has_pages: bool
    page_count_expected: int
    page_count_actual: int
    has_page_data: bool
    problems: list[str] = field(default_factory=list)


def scan_integrity(root: Path, config: Config) -> list[IssueStatus]:
    statuses: list[IssueStatus] = []
    known_ids: set[str] = set()
    for m in read_magazines(root, config):
        issue_id = m.get("id", "")
        known_ids.add(issue_id)
        p = IssuePaths(root, issue_id, config)
        expected = int(m.get("pageCount", 0))
        actual = 0
        if p.pages_dir.exists():
            actual = len(list(p.pages_dir.glob(f"page-*.{config.image.format}")))
        has_cover = p.cover.exists()
        has_pages = p.pages_dir.exists() and actual > 0
        has_page_data = p.page_data.exists()

        problems: list[str] = []
        if not has_cover:
            problems.append("Missing cover")
        if not p.pages_dir.exists():
            problems.append("Missing pages folder")
        elif actual == 0:
            problems.append("Pages folder is empty")
        elif actual != expected:
            problems.append(f"Page count mismatch (expected {expected}, found {actual})")
        if not has_page_data:
            problems.append("Missing page JSON")

        statuses.append(IssueStatus(
            issue_id=issue_id, title=m.get("title", ""), has_cover=has_cover,
            has_pages=has_pages, page_count_expected=expected,
            page_count_actual=actual, has_page_data=has_page_data, problems=problems,
        ))

    # Orphan detection: pages folders / cover images with no magazines.json entry.
    orphan_ids: set[str] = set()
    pages_root = root / config.pages_dir
    if pages_root.exists():
        for d in pages_root.iterdir():
            if d.is_dir() and d.name not in known_ids:
                orphan_ids.add(d.name)
    covers_root = root / config.covers_dir
    if covers_root.exists():
        for f in covers_root.glob(f"*.{config.image.format}"):
            if f.stem not in known_ids:
                orphan_ids.add(f.stem)
    for oid in sorted(orphan_ids):
        p = IssuePaths(root, oid, config)
        actual = 0
        if p.pages_dir.exists():
            actual = len(list(p.pages_dir.glob(f"page-*.{config.image.format}")))
        statuses.append(IssueStatus(
            issue_id=oid, title="(orphan)", has_cover=p.cover.exists(),
            has_pages=p.pages_dir.exists() and actual > 0, page_count_expected=0,
            page_count_actual=actual, has_page_data=p.page_data.exists(),
            problems=["Orphan: no magazines.json entry"],
        ))
    return statuses
