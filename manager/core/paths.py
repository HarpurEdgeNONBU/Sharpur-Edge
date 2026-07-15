from __future__ import annotations

from pathlib import Path

from manager.core.config import Config


def get_root(config: Config) -> Path:
    if config.root:
        return Path(config.root).resolve()
    # manager/core/paths.py -> parent of manager/
    return Path(__file__).resolve().parent.parent.parent


def magazines_json(root: Path, config: Config) -> Path:
    return Path(root) / "library" / "magazines.json"


class IssuePaths:
    def __init__(self, root: Path, issue_id: str, config: Config):
        self.root = Path(root)
        self.issue_id = issue_id
        self.config = config

    @property
    def pdf(self) -> Path:
        return self.root / self.config.pdfs_dir / f"{self.issue_id}.pdf"

    @property
    def cover(self) -> Path:
        return self.root / self.config.covers_dir / f"{self.issue_id}.{self.config.image.format}"

    @property
    def pages_dir(self) -> Path:
        return self.root / self.config.pages_dir / self.issue_id

    def page_image(self, n: int) -> Path:
        return self.pages_dir / f"page-{n}.{self.config.image.format}"

    @property
    def page_data(self) -> Path:
        return self.root / self.config.data_dir / f"{self.issue_id}.json"
