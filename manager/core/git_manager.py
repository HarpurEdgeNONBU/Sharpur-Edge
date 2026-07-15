from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GitResult:
    ok: bool
    output: str


def _run(root: Path, *args: str) -> GitResult:
    try:
        proc = subprocess.run(
            ["git", *args], cwd=str(root), capture_output=True, text=True
        )
        out = (proc.stdout + proc.stderr).strip()
        return GitResult(proc.returncode == 0, out)
    except FileNotFoundError:
        return GitResult(False, "git is not installed")


def is_available() -> bool:
    try:
        subprocess.run(["git", "--version"], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False


def is_repo(root: Path) -> bool:
    res = _run(Path(root), "rev-parse", "--is-inside-work-tree")
    return res.ok and res.output.strip() == "true"


def status(root: Path) -> GitResult:
    return _run(Path(root), "status", "--short", "--branch")


def pull(root: Path) -> GitResult:
    return _run(Path(root), "pull")


def commit(root: Path, message: str) -> GitResult:
    add = _run(Path(root), "add", "-A")
    if not add.ok:
        return add
    return _run(Path(root), "commit", "-m", message)


def push(root: Path) -> GitResult:
    return _run(Path(root), "push")
