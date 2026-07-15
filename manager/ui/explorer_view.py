from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import customtkinter as ctk

from manager.core import file_manager as fm
from manager.core.paths import IssuePaths


def _open_folder(path: Path):
    path = Path(path)
    if not path.exists():
        return
    if sys.platform.startswith("win"):
        os.startfile(str(path))  # noqa: S606
    elif sys.platform == "darwin":
        subprocess.run(["open", str(path)])
    else:
        subprocess.run(["xdg-open", str(path)])


class ExplorerView(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=12)
        ctk.CTkLabel(header, text="File Explorer / Integrity",
                     font=("", 22, "bold")).pack(side="left")
        ctk.CTkButton(header, text="Rescan", command=self.refresh).pack(side="right")
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.pack(fill="both", expand=True, padx=16, pady=8)
        self.refresh()

    def refresh(self):
        for child in self.list_frame.winfo_children():
            child.destroy()
        statuses = fm.scan_integrity(self.app.root_path, self.app.config_obj)
        if not statuses:
            ctk.CTkLabel(self.list_frame, text="No issues found.").pack(pady=20)
            return
        for s in statuses:
            row = ctk.CTkFrame(self.list_frame)
            row.pack(fill="x", pady=4)
            ok = not s.problems
            dot = "OK" if ok else "!"
            color = "#5cb85c" if ok else "#e06666"
            ctk.CTkLabel(row, text=dot, text_color=color, width=30).pack(side="left")
            info = f"{s.title}  ({s.issue_id})  pages {s.page_count_actual}/{s.page_count_expected}"
            if s.problems:
                info += "  —  " + "; ".join(s.problems)
            ctk.CTkLabel(row, text=info, anchor="w").pack(side="left", fill="x", expand=True)
            p = IssuePaths(self.app.root_path, s.issue_id, self.app.config_obj)
            ctk.CTkButton(row, text="Open folder", width=100,
                          command=lambda pp=p: _open_folder(pp.pages_dir)).pack(side="right", padx=6)
