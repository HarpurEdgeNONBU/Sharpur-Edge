from __future__ import annotations

import customtkinter as ctk

from manager.core import file_manager as fm
from manager.core import page_text as pt
from manager.core.paths import IssuePaths
from manager.ui.widgets import load_thumbnail


class PageTextView(ctk.CTkFrame):
    def __init__(self, master, app, issue_id: str | None = None):
        super().__init__(master)
        self.app = app
        self._mags = fm.read_magazines(app.root_path, app.config_obj)
        self._mags_by_id = {m.get("id", ""): m for m in self._mags}
        self._rows: list[dict] = []
        self._idx = 0
        self._issue_id = None
        self._build_ui()
        preselect = issue_id or (self._mags[0].get("id", "") if self._mags else None)
        if preselect:
            self.load_issue(preselect)
        else:
            self.status_label.configure(text="No issues yet.")

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=12)
        ctk.CTkLabel(header, text="Page Text", font=("", 22, "bold")).pack(side="left")

        self._titles = [m.get("title", m.get("id", "")) for m in self._mags]
        self.selector = ctk.CTkOptionMenu(
            header, values=self._titles or ["(no issues)"], command=self._on_select
        )
        self.selector.pack(side="left", padx=12)
        if not self._mags:
            self.selector.configure(state="disabled")

        self.save_btn = ctk.CTkButton(header, text="Save", command=self._save)
        self.save_btn.pack(side="right")
        self.status_label = ctk.CTkLabel(header, text="")
        self.status_label.pack(side="right", padx=12)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        left = ctk.CTkFrame(body)
        left.pack(side="left", fill="y", padx=(0, 8))
        self.image_label = ctk.CTkLabel(left, text="(no image)", width=360, height=480)
        self.image_label.pack(padx=8, pady=8)

        right = ctk.CTkFrame(body)
        right.pack(side="left", fill="both", expand=True, padx=(8, 0))

        nav_row = ctk.CTkFrame(right, fg_color="transparent")
        nav_row.pack(fill="x", padx=8, pady=8)
        self.prev_btn = ctk.CTkButton(nav_row, text="< Prev", width=80, command=self._prev)
        self.prev_btn.pack(side="left")
        self.page_label = ctk.CTkLabel(nav_row, text="Page 0 of 0")
        self.page_label.pack(side="left", expand=True)
        self.next_btn = ctk.CTkButton(nav_row, text="Next >", width=80, command=self._next)
        self.next_btn.pack(side="left")

        self.completeness_label = ctk.CTkLabel(
            right,
            text="",
            anchor="w",
            justify="left",
            text_color="#d6b85a",
        )
        self.completeness_label.pack(fill="x", padx=8, pady=(0, 8))

        title_row = ctk.CTkFrame(right, fg_color="transparent")
        title_row.pack(fill="x", padx=8, pady=(0, 8))
        ctk.CTkLabel(title_row, text="Title", width=90, anchor="w").pack(side="left")
        self.title_entry = ctk.CTkEntry(title_row)
        self.title_entry.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(right, text="Text", anchor="w").pack(fill="x", padx=8)
        self.text_box = ctk.CTkTextbox(right, height=180)
        self.text_box.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        ctk.CTkLabel(right, text="Captions", anchor="w").pack(fill="x", padx=8)
        self.captions_box = ctk.CTkTextbox(right, height=120)
        self.captions_box.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def _on_select(self, title: str):
        for m in self._mags:
            if m.get("title", m.get("id", "")) == title:
                self.load_issue(m.get("id", ""))
                return

    def load_issue(self, issue_id: str):
        mag = self._mags_by_id.get(issue_id)
        if mag is None:
            self.status_label.configure(text=f"Issue not found: {issue_id}")
            return
        self._issue_id = issue_id
        page_count = int(mag.get("pageCount", 0))
        self._rows = pt.page_text_for_edit(
            self.app.root_path, self.app.config_obj, issue_id, page_count
        )
        self._idx = 0
        title = mag.get("title", issue_id)
        if title in self._titles:
            self.selector.set(title)
        self.status_label.configure(text="")
        self._show_page()

    def _flush(self):
        if not self._rows:
            return
        row = self._rows[self._idx]
        row["title"] = self.title_entry.get()
        row["text"] = self.text_box.get("1.0", "end-1c")
        row["captions"] = self.captions_box.get("1.0", "end-1c")

    def _show_page(self):
        n = len(self._rows)
        self.title_entry.delete(0, "end")
        self.text_box.delete("1.0", "end")
        self.captions_box.delete("1.0", "end")

        if n == 0:
            self.page_label.configure(text="Page 0 of 0")
            self.completeness_label.configure(text="")
            self.image_label.configure(image=None, text="(no image)")
            return

        row = self._rows[self._idx]
        self.title_entry.insert(0, row.get("title", ""))
        self.text_box.insert("1.0", row.get("text", ""))
        self.captions_box.insert("1.0", row.get("captions", ""))
        self.page_label.configure(text=f"Page {self._idx + 1} of {n}")

        p = IssuePaths(self.app.root_path, self._issue_id, self.app.config_obj)
        thumb = load_thumbnail(p.page_image(self._idx + 1), size=(360, 480))
        if thumb is not None:
            self.image_label.configure(image=thumb, text="")
        else:
            self.image_label.configure(image=None, text="(no image)")
        self._update_completeness()

    def _prev(self):
        if not self._rows:
            return
        self._flush()
        self._idx = max(0, self._idx - 1)
        self._show_page()

    def _next(self):
        if not self._rows:
            return
        self._flush()
        self._idx = min(len(self._rows) - 1, self._idx + 1)
        self._show_page()

    def _save(self):
        if not self._rows or not self._issue_id:
            return
        self._flush()
        self._update_completeness()
        issue_id = self._issue_id
        rows = [dict(r) for r in self._rows]

        def work():
            pt.save_page_text(self.app.root_path, self.app.config_obj, issue_id, rows)

        def done(result, err):
            if err:
                self.status_label.configure(text=f"FAILED: {err}", text_color="#e06666")
            else:
                self.status_label.configure(text="Saved.", text_color="#5cb85c")

        self.app.run_bg(work, done)

    def _update_completeness(self):
        missing_text = self._missing_pages("text")
        missing_captions = self._missing_pages("captions")
        if not missing_text and not missing_captions:
            self.completeness_label.configure(
                text="Accessibility text complete for this issue.",
                text_color="#5cb85c",
            )
            return

        parts = []
        if missing_text:
            parts.append(f"Missing text: {self._format_pages(missing_text)}")
        if missing_captions:
            parts.append(f"Missing captions: {self._format_pages(missing_captions)}")
        self.completeness_label.configure(text=" | ".join(parts), text_color="#d6b85a")

    def _missing_pages(self, field: str) -> list[int]:
        return [
            index + 1
            for index, row in enumerate(self._rows)
            if not str(row.get(field, "")).strip()
        ]

    @staticmethod
    def _format_pages(pages: list[int]) -> str:
        if len(pages) <= 12:
            return ", ".join(str(page) for page in pages)
        shown = ", ".join(str(page) for page in pages[:12])
        return f"{shown}, +{len(pages) - 12} more"
