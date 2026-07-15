import json
from manager.core.paths import IssuePaths
from manager.core.generator import generate_issue, GenerateResult
from manager.core import file_manager as fm


def test_generate_issue_happy_path(tiny_pdf, fixture_root, fixture_config):
    steps = []
    meta = {
        "issue_id": "sample-issue-2026", "title": "Sample", "year": "2026",
        "category": "Fall Issue", "description": "desc",
    }
    result = generate_issue(
        tiny_pdf, meta, fixture_config, root=fixture_root,
        progress_cb=lambda step, cur, total: steps.append(step),
    )
    assert isinstance(result, GenerateResult)
    assert result.success is True
    p = IssuePaths(fixture_root, "sample-issue-2026", fixture_config)
    assert p.pdf.exists()
    assert p.cover.exists()
    assert p.page_image(1).exists() and p.page_image(2).exists()
    assert p.page_data.exists()
    page_data = json.loads(p.page_data.read_text(encoding="utf-8"))
    assert len(page_data) == 2
    mags = fm.read_magazines(fixture_root, fixture_config)
    assert mags[-1]["id"] == "sample-issue-2026"
    assert mags[-1]["pageCount"] == 2
    assert "read" in steps and "cover" in steps and "json" in steps
    assert '"sample-issue-2026"' in result.json_snippet


def test_generate_preserves_existing_page_data(tiny_pdf, fixture_root, fixture_config):
    p = IssuePaths(fixture_root, "keep-2026", fixture_config)
    p.page_data.parent.mkdir(parents=True, exist_ok=True)
    p.page_data.write_text(json.dumps([{"title": "Page 1", "text": "KEEP", "captions": ""}]), encoding="utf-8")
    meta = {"issue_id": "keep-2026", "title": "K", "year": "2026", "category": "Fall Issue", "description": ""}
    generate_issue(tiny_pdf, meta, fixture_config, root=fixture_root)
    data = json.loads(p.page_data.read_text(encoding="utf-8"))
    assert data[0]["text"] == "KEEP"
