from __future__ import annotations

import customtkinter as ctk

from manager.core import file_manager as fm
from manager.core.paths import IssuePaths
from manager.ui.widgets import IssueCard, ConfirmDeleteModal, load_thumbnail

# Approximate horizontal footprint of one card (thumbnail + text + padding).
# Used to decide how many columns fit the current window width.
CARD_WIDTH = 200


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self._cards: list[IssueCard] = []
        self._cols = 0
        self._resize_job = None

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=12)
        ctk.CTkLabel(header, text="All Issues", font=("", 22, "bold")).pack(side="left")
        ctk.CTkButton(header, text="Refresh", command=self.refresh).pack(side="right")

        self.grid_frame = ctk.CTkScrollableFrame(self)
        self.grid_frame.pack(fill="both", expand=True, padx=16, pady=8)
        # Reflow the columns whenever the frame is resized so cards always fit.
        # Use add=True so CustomTkinter keeps its own scroll-region updater.
        self.grid_frame.bind("<Configure>", self._on_resize, add=True)
        self.refresh()

    def refresh(self):
        for card in self._cards:
            card.destroy()
        self._cards = []
        for child in self.grid_frame.winfo_children():
            child.destroy()

        mags = fm.read_magazines(self.app.root_path, self.app.config_obj)
        if not mags:
            ctk.CTkLabel(self.grid_frame, text="No issues yet. Use 'Add Issue'.").pack(pady=20)
            return

        for mag in mags:
            p = IssuePaths(self.app.root_path, mag.get("id", ""), self.app.config_obj)
            thumb = load_thumbnail(p.cover)
            card = IssueCard(self.grid_frame, mag, thumb, self._ask_delete, on_edit=self._edit_text)
            self._cards.append(card)

        self._cols = 0  # force a fresh layout
        self._relayout()

    def _on_resize(self, event):
        # Debounce: only relayout once the resizing settles.
        if self._resize_job is not None:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(120, self._relayout)

    def _relayout(self):
        self._resize_job = None
        if not self._cards:
            return
        width = self.grid_frame.winfo_width()
        cols = max(1, width // CARD_WIDTH)
        if cols == self._cols:
            return
        self._cols = cols
        for i, card in enumerate(self._cards):
            card.grid(row=i // cols, column=i % cols, padx=10, pady=10, sticky="n")
        # Distribute width evenly across the active columns; clear the rest.
        for c in range(cols):
            self.grid_frame.grid_columnconfigure(c, weight=1)
        for c in range(cols, cols + 8):
            self.grid_frame.grid_columnconfigure(c, weight=0)
        self.grid_frame.after_idle(self._update_scroll_region)

    def _update_scroll_region(self):
        canvas = getattr(self.grid_frame, "_parent_canvas", None)
        if canvas is not None:
            canvas.configure(scrollregion=canvas.bbox("all"))

    def _ask_delete(self, magazine: dict):
        issue_id = magazine.get("id", "")
        p = IssuePaths(self.app.root_path, issue_id, self.app.config_obj)
        targets = [
            p.pdf.relative_to(self.app.root_path).as_posix(),
            p.cover.relative_to(self.app.root_path).as_posix(),
            p.pages_dir.relative_to(self.app.root_path).as_posix() + "/",
            p.page_data.relative_to(self.app.root_path).as_posix(),
            "library/magazines.json entry",
        ]
        ConfirmDeleteModal(self.app, magazine, targets, require_title=True,
                           on_confirm=self._do_delete)

    def _edit_text(self, magazine: dict):
        self.app.open_page_text(magazine.get("id", ""))

    def _do_delete(self, magazine: dict):
        issue_id = magazine.get("id", "")

        def work():
            return fm.delete_issue(self.app.root_path, self.app.config_obj, issue_id)

        def done(result, err):
            self.refresh()

        self.app.run_bg(work, done)
