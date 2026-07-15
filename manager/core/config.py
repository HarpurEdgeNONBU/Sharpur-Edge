from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

DEFAULT_CONFIG = {
    "root": "",
    "output": {
        "pages_dir": "library/pages",
        "covers_dir": "library/covers",
        "data_dir": "library/page-text",
        "pdfs_dir": "library/pdfs",
    },
    "image": {"format": "webp", "page_dpi": 300, "cover_dpi": 200, "quality": 82},
    "categories": ["Fall Issue", "Spring Issue"],
}


@dataclass
class ImageConfig:
    format: str
    page_dpi: int
    cover_dpi: int
    quality: int


@dataclass
class Config:
    root: str
    pages_dir: str
    covers_dir: str
    data_dir: str
    pdfs_dir: str
    image: ImageConfig
    categories: list[str]


def _default_config_path() -> Path:
    # manager/core/config.py -> manager/config/config.yaml
    return Path(__file__).resolve().parent.parent / "config" / "config.yaml"


def load_config(path: Path | None = None) -> Config:
    path = Path(path) if path is not None else _default_config_path()
    data: dict = {}
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

    output = {**DEFAULT_CONFIG["output"], **(data.get("output") or {})}
    image = {**DEFAULT_CONFIG["image"], **(data.get("image") or {})}
    return Config(
        root=data.get("root", DEFAULT_CONFIG["root"]) or "",
        pages_dir=output["pages_dir"],
        covers_dir=output["covers_dir"],
        data_dir=output["data_dir"],
        pdfs_dir=output["pdfs_dir"],
        image=ImageConfig(
            format=image["format"],
            page_dpi=int(image["page_dpi"]),
            cover_dpi=int(image["cover_dpi"]),
            quality=int(image["quality"]),
        ),
        categories=list(data.get("categories") or DEFAULT_CONFIG["categories"]),
    )
