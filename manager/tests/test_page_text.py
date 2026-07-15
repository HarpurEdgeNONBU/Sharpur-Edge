import json
from manager.core.paths import IssuePaths
from manager.core import page_text as pt


def test_load_missing_returns_empty(fixture_root, fixture_config):
    assert pt.load_page_text(fixture_root, fixture_config, "nope-2026") == []


def test_save_then_load_roundtrip(fixture_root, fixture_config):
    entries = [
        {"title": "Page 1", "text": "Line one\nLine two", "captions": "a cover"},
        {"title": "Page 2", "text": "", "captions": ""},
    ]
    pt.save_page_text(fixture_root, fixture_config, "iss-2026", entries)
    assert pt.load_page_text(fixture_root, fixture_config, "iss-2026") == entries


def test_save_writes_readable_json_with_real_newlines(fixture_root, fixture_config):
    pt.save_page_text(fixture_root, fixture_config, "iss-2026",
                      [{"title": "Page 1", "text": "a\nb", "captions": ""}])
    raw = IssuePaths(fixture_root, "iss-2026", fixture_config).page_data.read_text(encoding="utf-8")
    assert '"text": "a\\nb"' in raw  # valid JSON escaping, produced by the writer not the user


def test_for_edit_pads_to_page_count(fixture_root, fixture_config):
    pt.save_page_text(fixture_root, fixture_config, "iss-2026",
                      [{"title": "Page 1", "text": "kept", "captions": ""}])
    rows = pt.page_text_for_edit(fixture_root, fixture_config, "iss-2026", 3)
    assert len(rows) == 3
    assert rows[0]["text"] == "kept"
    assert rows[1] == {"title": "Page 2", "text": "", "captions": ""}
    assert rows[2] == {"title": "Page 3", "text": "", "captions": ""}


def test_for_edit_truncates_extra(fixture_root, fixture_config):
    pt.save_page_text(fixture_root, fixture_config, "iss-2026",
                      [{"title": "Page 1", "text": "", "captions": ""},
                       {"title": "Page 2", "text": "", "captions": ""}])
    rows = pt.page_text_for_edit(fixture_root, fixture_config, "iss-2026", 1)
    assert len(rows) == 1


def test_load_malformed_json_returns_empty(fixture_root, fixture_config):
    path = IssuePaths(fixture_root, "iss-2026", fixture_config).page_data
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not valid json", encoding="utf-8")
    assert pt.load_page_text(fixture_root, fixture_config, "iss-2026") == []
