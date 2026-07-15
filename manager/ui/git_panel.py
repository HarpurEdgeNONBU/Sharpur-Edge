from __future__ import annotations

import customtkinter as ctk

from manager.core import git_manager as gm


class GitPanel(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        ctk.CTkLabel(self, text="Git", font=("", 22, "bold")).pack(anchor="w", padx=16, pady=12)

        available = gm.is_available()
        is_repo = available and gm.is_repo(self.app.root_path)
        if not available:
            ctk.CTkLabel(self, text="git is not installed. Install Git to enable this panel.",
                         text_color="#e06666").pack(anchor="w", padx=16)
            return
        if not is_repo:
            ctk.CTkLabel(self, text="This archive folder is not a git repository.",
                         text_color="#e06666").pack(anchor="w", padx=16)

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(fill="x", padx=16, pady=8)
        ctk.CTkButton(btns, text="Pull latest", command=lambda: self._run(gm.pull)).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Commit changes", command=self._commit).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Push to GitHub", command=lambda: self._run(gm.push)).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Status", command=lambda: self._run(gm.status)).pack(side="left", padx=6)

        self.commit_msg = ctk.CTkEntry(self, placeholder_text="Commit message")
        self.commit_msg.pack(fill="x", padx=16)
        self.output = ctk.CTkTextbox(self)
        self.output.pack(fill="both", expand=True, padx=16, pady=8)
        for widget in btns.winfo_children():
            if not is_repo:
                widget.configure(state="disabled")

    def _run(self, fn):
        def work():
            return fn(self.app.root_path)

        def done(result, err):
            text = str(err) if err else (result.output or "(no output)")
            self.output.insert("end", text + "\n")

        self.app.run_bg(work, done)

    def _commit(self):
        msg = self.commit_msg.get().strip() or "Update archive"

        def work():
            return gm.commit(self.app.root_path, msg)

        def done(result, err):
            text = str(err) if err else (result.output or "committed")
            self.output.insert("end", text + "\n")

        self.app.run_bg(work, done)
