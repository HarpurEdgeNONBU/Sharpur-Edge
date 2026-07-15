from __future__ import annotations

import re
from pathlib import Path

import customtkinter as ctk

from manager.core import file_manager as fm
from manager.core import pdf_processor
from manager.core.generator import generate_issue
from manager.core.json_builder import slugify
from manager.ui.widgets import DropZone

ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
STEP_LABELS = {"read": "Reading PDF", "pages": "Rendering pages",
               "cover": "Exporting cover", "json": "Writing JSON"}


class AddIssueView(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.pdf_path: Path | None = None

        ctk.CTkLabel(self, text="Add New Issue", font=("", 22, "bold")).pack(
            anchor="w", padx=16, pady=12)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=16)

        left = ctk.CTkFrame(body)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.drop = DropZone(left, on_file=self._on_file)
        self.drop.pack(fill="x", pady=8)
        self.file_label = ctk.CTkLabel(left, text="No file selected", text_color="gray")
        self.file_label.pack(anchor="w")

        self.form = ctk.CTkFrame(left)
        self.form.pack(fill="x", pady=8)
        self.fields: dict[str, ctk.CTkEntry] = {}
        for label in ("issue_id", "title", "year", "description"):
            row = ctk.CTkFrame(self.form, fg_color="transparent")
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text=label, width=90, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(row)
            entry.pack(side="left", fill="x", expand=True)
            self.fields[label] = entry
        cat_row = ctk.CTkFrame(self.form, fg_color="transparent")
        cat_row.pack(fill="x", pady=3)
        ctk.CTkLabel(cat_row, text="category", width=90, anchor="w").pack(side="left")
        self.category = ctk.CTkOptionMenu(cat_row, values=self.app.config_obj.categories)
        self.category.pack(side="left")

        self.validation = ctk.CTkLabel(left, text="", text_color="#e06666")
        self.validation.pack(anchor="w")
        self.generate_btn = ctk.CTkButton(left, text="Generate", command=self._generate)
        self.generate_btn.pack(anchor="w", pady=8)
        self.progress = ctk.CTkProgressBar(left)
        self.progress.set(0)
        self.progress.pack(fill="x", pady=4)
        self.step_label = ctk.CTkLabel(left, text="")
        self.step_label.pack(anchor="w")

        # Output panel
        right = ctk.CTkFrame(body)
        right.pack(side="left", fill="both", expand=True, padx=(8, 0))
        ctk.CTkLabel(right, text="Output", font=("", 16, "bold")).pack(anchor="w", padx=8, pady=6)
        self.status_label = ctk.CTkLabel(right, text="")
        self.status_label.pack(anchor="w", padx=8)
        self.output_box = ctk.CTkTextbox(right)
        self.output_box.pack(fill="both", expand=True, padx=8, pady=6)
        ctk.CTkButton(right, text="Copy JSON to clipboard", command=self._copy).pack(
            anchor="e", padx=8, pady=(0, 8))

    def _on_file(self, path: str):
        self.pdf_path = Path(path)
        try:
            pages = pdf_processor.page_count(self.pdf_path)
        except Exception:
            pages = "?"
        self.file_label.configure(text=f"{self.pdf_path.name}  ({pages} pages)")
        self.fields["issue_id"].delete(0, "end")
        self.fields["issue_id"].insert(0, slugify(self.pdf_path.stem))
        self.fields["title"].delete(0, "end")
        self.fields["title"].insert(0, self.pdf_path.stem.replace("-", " ").title())

    def _validate(self) -> str | None:
        if not self.pdf_path:
            return "Select a PDF first."
        issue_id = self.fields["issue_id"].get().strip()
        if not ID_RE.match(issue_id):
            return "issue_id must be lowercase, hyphen-separated, URL-safe."
        if fm.issue_exists(self.app.root_path, self.app.config_obj, issue_id):
            return f"issue_id '{issue_id}' already exists."
        if not self.fields["title"].get().strip():
            return "Title is required."
        return None

    def _generate(self):
        err = self._validate()
        if err:
            self.validation.configure(text=err)
            return
        self.validation.configure(text="")
        self.generate_btn.configure(state="disabled")
        self.progress.set(0)

        metadata = {
            "issue_id": self.fields["issue_id"].get().strip(),
            "title": self.fields["title"].get().strip(),
            "year": self.fields["year"].get().strip(),
            "category": self.category.get(),
            "description": self.fields["description"].get().strip(),
        }
        pdf_path = self.pdf_path

        def progress(step, current, total):
            frac = (current / total) if total else 0
            self.app.post(lambda v, e: self._show_step(step, frac), None)

        def work():
            return generate_issue(pdf_path, metadata, self.app.config_obj,
                                  root=self.app.root_path, progress_cb=progress)

        self.app.run_bg(work, self._on_done)

    def _show_step(self, step, frac):
        self.step_label.configure(text=STEP_LABELS.get(step, step))
        self.progress.set(frac)

    def _on_done(self, result, err):
        self.generate_btn.configure(state="normal")
        if err or (result and not result.success):
            msg = str(err) if err else result.error
            self.status_label.configure(text=f"FAILED: {msg}", text_color="#e06666")
            return
        self.progress.set(1)
        self.status_label.configure(text="SUCCESS", text_color="#5cb85c")
        lines = ["Files written:"] + [f"  {f}" for f in result.files_written]
        lines += ["", "magazines.json entry:", result.json_snippet]
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", "\n".join(lines))

    def _copy(self):
        text = self.output_box.get("1.0", "end").strip()
        self.clipboard_clear()
        self.clipboard_append(text)
