from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image

WEBP_METHOD = 6


def open_document(pdf_path: Path):
    return fitz.open(str(pdf_path))


def page_count(pdf_path: Path) -> int:
    doc = fitz.open(str(pdf_path))
    try:
        return len(doc)
    finally:
        doc.close()


def render_page_to_webp(
    page, dpi: int, output_path: Path, quality: int, lossless: bool = False
) -> None:
    matrix = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=matrix, alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    save_options = {"lossless": lossless, "method": WEBP_METHOD}
    if not lossless:
        save_options["quality"] = quality
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path), "WEBP", **save_options)
