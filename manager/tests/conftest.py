import json
from pathlib import Path

import fitz
import pytest


@pytest.fixture
def tiny_pdf(tmp_path) -> Path:
    doc = fitz.open()
    for i in range(2):
        page = doc.new_page(width=200, height=300)
        page.insert_text((20, 40), f"Page {i + 1}")
    out = tmp_path / "sample-issue.pdf"
    doc.save(str(out))
    doc.close()
    return out


@pytest.fixture
def fixture_root(tmp_path) -> Path:
    root = tmp_path / "archive"
    (root / "library" / "pdfs").mkdir(parents=True)
    (root / "library" / "covers").mkdir()
    (root / "library" / "pages").mkdir()
    (root / "library" / "page-text").mkdir()
    (root / "library" / "magazines.json").write_text("[]\n", encoding="utf-8")
    return root


@pytest.fixture
def fixture_config(fixture_root):
    from manager.core.config import load_config
    cfg_file = fixture_root / "config.yaml"
    cfg_file.write_text('root: "%s"\n' % fixture_root.as_posix(), encoding="utf-8")
    return load_config(cfg_file)
