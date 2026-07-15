from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from manager.core.config import Config
from manager.core.paths import IssuePaths, get_root
from manager.core import pdf_processor, json_builder, file_manager

ProgressCb = Optional[Callable[[str, int, int], None]]


@dataclass
class GenerateResult:
    success: bool
    issue_id: str
    files_written: list[str] = field(default_factory=list)
    entry: dict = field(default_factory=dict)
    json_snippet: str = ""
    error: Optional[str] = None


def _emit(cb: ProgressCb, step: str, current: int, total: int) -> None:
    if cb is not None:
        cb(step, current, total)


def generate_issue(
    pdf_path, metadata: dict, config: Config, root: Path | None = None,
    progress_cb: ProgressCb = None,
) -> GenerateResult:
    pdf_path = Path(pdf_path)
    issue_id = metadata["issue_id"]
    root = Path(root) if root is not None else get_root(config)
    p = IssuePaths(root, issue_id, config)
    written: list[str] = []

    try:
        _emit(progress_cb, "read", 0, 1)
        if not pdf_path.exists() or pdf_path.suffix.lower() != ".pdf":
            raise ValueError(f"Not a PDF file: {pdf_path}")
        doc = pdf_processor.open_document(pdf_path)
        try:
            num_pages = len(doc)
            _emit(progress_cb, "read", 1, 1)

            # Copy source PDF into the archive if it isn't already there.
            p.pdf.parent.mkdir(parents=True, exist_ok=True)
            if pdf_path.resolve() != p.pdf.resolve():
                shutil.copy2(pdf_path, p.pdf)
                written.append(f"{config.pdfs_dir}/{issue_id}.pdf")

            p.pages_dir.mkdir(parents=True, exist_ok=True)
            for i, page in enumerate(doc):
                n = i + 1
                pdf_processor.render_page_to_webp(
                    page, config.image.page_dpi, p.page_image(n), config.image.quality
                )
                written.append(f"{config.pages_dir}/{issue_id}/page-{n}.{config.image.format}")
                _emit(progress_cb, "pages", n, num_pages)

            _emit(progress_cb, "cover", 0, 1)
            p.cover.parent.mkdir(parents=True, exist_ok=True)
            pdf_processor.render_page_to_webp(
                doc[0], config.image.cover_dpi, p.cover, config.image.quality
            )
            written.append(f"{config.covers_dir}/{issue_id}.{config.image.format}")
            _emit(progress_cb, "cover", 1, 1)
        finally:
            doc.close()

        _emit(progress_cb, "json", 0, 1)
        if not p.page_data.exists():
            file_manager.write_json_atomic(
                p.page_data, json_builder.build_page_data_template(num_pages)
            )
            written.append(f"{config.data_dir}/{issue_id}.json")

        entry = json_builder.build_magazines_entry(issue_id, metadata, num_pages, config)
        file_manager.upsert_magazines_entry(root, config, entry)
        written.append("library/magazines.json (entry)")
        _emit(progress_cb, "json", 1, 1)

        snippet = json.dumps(entry, indent=2, ensure_ascii=False)
        return GenerateResult(True, issue_id, written, entry, snippet, None)
    except Exception as exc:  # noqa: BLE001 - surface any failure to the UI
        return GenerateResult(False, issue_id, written, {}, "", str(exc))
