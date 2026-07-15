import json
import pytest

from manager.core.paths import IssuePaths, magazines_json
from manager.core import file_manager as fm


def _entry(issue_id, pages=2):
    return {
        "id": issue_id, "title": "T", "year": "2026", "category": "Fall Issue",
        "pageCount": pages, "pdf": f"library/pdfs/{issue_id}.pdf",
        "cover": f"library/covers/{issue_id}.webp", "description": "d",
    }


def _make_issue_files(root, config, issue_id, pages=2):
    p = IssuePaths(root, issue_id, config)
    p.pdf.write_bytes(b"%PDF-1.4 fake")
    p.cover.write_bytes(b"webp")
    p.pages_dir.mkdir(parents=True, exist_ok=True)
    for n in range(1, pages + 1):
        p.page_image(n).write_bytes(b"webp")
    p.page_data.write_text("[]", encoding="utf-8")


def test_upsert_and_read(fixture_root, fixture_config):
    fm.upsert_magazines_entry(fixture_root, fixture_config, _entry("a-2026"))
    fm.upsert_magazines_entry(fixture_root, fixture_config, _entry("b-2026"))
    fm.upsert_magazines_entry(fixture_root, fixture_config, {**_entry("a-2026"), "title": "New"})
    mags = fm.read_magazines(fixture_root, fixture_config)
    assert [m["id"] for m in mags] == ["a-2026", "b-2026"]
    assert mags[0]["title"] == "New"


def test_delete_issue_all_or_nothing(fixture_root, fixture_config):
    _make_issue_files(fixture_root, fixture_config, "a-2026")
    fm.upsert_magazines_entry(fixture_root, fixture_config, _entry("a-2026"))
    report = fm.delete_issue(fixture_root, fixture_config, "a-2026")
    p = IssuePaths(fixture_root, "a-2026", fixture_config)
    assert not p.pdf.exists()
    assert not p.cover.exists()
    assert not p.pages_dir.exists()
    assert not p.page_data.exists()
    assert fm.read_magazines(fixture_root, fixture_config) == []
    assert "library/pdfs/a-2026.pdf" in "\n".join(report.removed)


def test_delete_unknown_id_raises(fixture_root, fixture_config):
    with pytest.raises(ValueError):
        fm.delete_issue(fixture_root, fixture_config, "does-not-exist")


def test_scan_integrity_flags_missing(fixture_root, fixture_config):
    # entry claims 2 pages but we create only the entry + 1 page, no cover
    fm.upsert_magazines_entry(fixture_root, fixture_config, _entry("gap-2026", pages=2))
    p = IssuePaths(fixture_root, "gap-2026", fixture_config)
    p.pages_dir.mkdir(parents=True, exist_ok=True)
    p.page_image(1).write_bytes(b"webp")
    statuses = fm.scan_integrity(fixture_root, fixture_config)
    s = next(x for x in statuses if x.issue_id == "gap-2026")
    assert s.has_cover is False
    assert s.page_count_actual == 1
    assert any("cover" in prob.lower() for prob in s.problems)
    assert any("page" in prob.lower() for prob in s.problems)


def test_scan_integrity_detects_orphan(fixture_root, fixture_config):
    # A pages folder + cover with NO magazines.json entry = orphan.
    from manager.core.paths import IssuePaths
    p = IssuePaths(fixture_root, "orphan-xyz-2099", fixture_config)
    p.pages_dir.mkdir(parents=True, exist_ok=True)
    p.page_image(1).write_bytes(b"webp")
    p.cover.write_bytes(b"webp")
    statuses = fm.scan_integrity(fixture_root, fixture_config)
    orphan = next((s for s in statuses if s.issue_id == "orphan-xyz-2099"), None)
    assert orphan is not None
    assert any("orphan" in prob.lower() for prob in orphan.problems)
    assert orphan.page_count_actual == 1
