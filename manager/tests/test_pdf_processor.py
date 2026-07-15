from PIL import Image
from manager.core.pdf_processor import open_document, page_count, render_page_to_webp


def test_page_count(tiny_pdf):
    assert page_count(tiny_pdf) == 2


def test_render_page_to_webp(tiny_pdf, tmp_path):
    doc = open_document(tiny_pdf)
    out = tmp_path / "page-1.webp"
    render_page_to_webp(doc[0], 100, out, quality=82)
    doc.close()
    assert out.exists()
    with Image.open(out) as img:
        assert img.format == "WEBP"
        assert img.width > 0 and img.height > 0
