from pathlib import Path
from manager.core.config import load_config
from manager.core.paths import get_root, magazines_json, IssuePaths


def _cfg(tmp_path):
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text('root: "%s"\n' % tmp_path.as_posix(), encoding="utf-8")
    return load_config(cfg_file)


def test_get_root_uses_config(tmp_path):
    cfg = _cfg(tmp_path)
    assert get_root(cfg) == tmp_path


def test_issue_paths_derive_from_id(tmp_path):
    cfg = _cfg(tmp_path)
    root = get_root(cfg)
    p = IssuePaths(root, "mentor-magic-fall-2026", cfg)
    assert p.pdf == root / "library" / "pdfs" / "mentor-magic-fall-2026.pdf"
    assert p.cover == root / "library" / "covers" / "mentor-magic-fall-2026.webp"
    assert p.pages_dir == root / "library" / "pages" / "mentor-magic-fall-2026"
    assert p.page_image(3) == root / "library" / "pages" / "mentor-magic-fall-2026" / "page-3.webp"
    assert p.page_data == root / "library" / "page-text" / "mentor-magic-fall-2026.json"


def test_magazines_json_path(tmp_path):
    cfg = _cfg(tmp_path)
    assert magazines_json(get_root(cfg), cfg) == tmp_path / "library" / "magazines.json"
