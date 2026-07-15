import subprocess
import pytest
from manager.core import git_manager as gm


def _git(root, *args):
    subprocess.run(["git", *args], cwd=str(root), check=True,
                   capture_output=True, text=True)


def test_is_available():
    assert gm.is_available() is True  # git is installed in this environment


def test_is_repo_false_then_true(tmp_path):
    assert gm.is_repo(tmp_path) is False
    _git(tmp_path, "init")
    assert gm.is_repo(tmp_path) is True


def test_status_and_commit(tmp_path):
    _git(tmp_path, "init")
    _git(tmp_path, "config", "user.email", "t@t.com")
    _git(tmp_path, "config", "user.name", "T")
    (tmp_path / "a.txt").write_text("hi", encoding="utf-8")
    st = gm.status(tmp_path)
    assert st.ok and "a.txt" in st.output
    res = gm.commit(tmp_path, "add a")
    assert res.ok
    st2 = gm.status(tmp_path)
    assert "a.txt" not in st2.output
