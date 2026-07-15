from manager.core.config import load_config
from manager.core.json_builder import (
    slugify,
    build_page_data_template,
    build_magazines_entry,
)


def test_slugify():
    assert slugify("Mentor Magic FINAL final.pdf") == "mentor-magic-final-final-pdf"
    assert slugify("  Spring_2027!! ") == "spring-2027"
    assert slugify("The Arts Issue") == "the-arts-issue"


def test_page_data_template():
    tmpl = build_page_data_template(2)
    assert tmpl == [
        {"title": "Page 1", "text": "", "captions": ""},
        {"title": "Page 2", "text": "", "captions": ""},
    ]


def test_magazines_entry(tmp_path):
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text("categories:\n  - Fall Issue\n", encoding="utf-8")
    cfg = load_config(cfg_file)
    entry = build_magazines_entry(
        "humanities-fall-2026",
        {"title": "Humanities", "year": "2026", "category": "Fall Issue", "description": "hi"},
        18,
        cfg,
    )
    assert entry == {
        "id": "humanities-fall-2026",
        "title": "Humanities",
        "year": "2026",
        "category": "Fall Issue",
        "pageCount": 18,
        "pdf": "library/pdfs/humanities-fall-2026.pdf",
        "cover": "library/covers/humanities-fall-2026.webp",
        "description": "hi",
    }
