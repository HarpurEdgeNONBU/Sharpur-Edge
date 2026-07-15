from pathlib import Path
import textwrap
from manager.core.config import load_config, Config


def test_load_defaults_when_keys_missing(tmp_path):
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text("categories:\n  - Only One\n", encoding="utf-8")
    cfg = load_config(cfg_file)
    assert isinstance(cfg, Config)
    assert cfg.pages_dir == "library/pages"
    assert cfg.covers_dir == "library/covers"
    assert cfg.data_dir == "library/page-text"
    assert cfg.pdfs_dir == "library/pdfs"
    assert cfg.image.page_dpi == 300
    assert cfg.image.cover_dpi == 200
    assert cfg.image.quality == 82
    assert cfg.image.format == "webp"
    assert cfg.categories == ["Only One"]


def test_load_full_file(tmp_path):
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text(textwrap.dedent("""
        root: "/some/root"
        output:
          pages_dir: "p"
          covers_dir: "c"
          data_dir: "d"
        image:
          format: "webp"
          page_dpi: 150
          cover_dpi: 100
          quality: 70
        categories:
          - "Fall Issue"
          - "Spring Issue"
    """), encoding="utf-8")
    cfg = load_config(cfg_file)
    assert cfg.root == "/some/root"
    assert cfg.pages_dir == "p"
    assert cfg.image.page_dpi == 150
    assert cfg.categories == ["Fall Issue", "Spring Issue"]
