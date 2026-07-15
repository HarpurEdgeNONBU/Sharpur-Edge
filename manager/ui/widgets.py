from __future__ import annotations

from pathlib import Path
from typing import Callable

import customtkinter as ctk
from PIL import Image

TRASH_ICON = Path(__file__).resolve().parent.parent / "assets" / "icons" / "trash.png"


def load_thumbnail(path: Path, size=(160, 210)):
    try:
        img = Image.open(path)
        return ctk.CTkImage(light_image=img, dark_image=img, size=size)
    except Exception:
        return None


def _trash_image(size=(20, 20)):
    try:
        img = Image.open(TRASH_ICON)
        return ctk.CTkImage(light_image=img, dark_image=img, size=size)
    except Exception:
        return None


class IssueCard(ctk.CTkFrame):
    def __init__(self, master, magazine: dict, thumb, on_delete: Callable[[dict], None],
                 on_edit: Callable[[dict], None] | None = None):
        super().__init__(master, corner_radius=10)
        self.magazine = magazine
        self._on_edit = on_edit

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=8, pady=(8, 0))
        trash_img = _trash_image()
        del_btn = ctk.CTkButton(
            top, text="" if trash_img else "Delete", image=trash_img, width=28,
            fg_color="transparent", hover_color="#5a1f1f",
            command=lambda: on_delete(magazine),
        )
        del_btn.pack(side="right")
        if on_edit is not None:
            ctk.CTkButton(top, text="Edit text", width=72,
                          command=lambda: on_edit(magazine)).pack(side="left")

        if thumb is not None:
            cover = ctk.CTkLabel(self, image=thumb, text="")
            cover.pack(padx=8, pady=4)
        else:
            cover = ctk.CTkLabel(self, text="(no cover)", width=160, height=210)
            cover.pack(padx=8, pady=4)

        title = ctk.CTkLabel(self, text=magazine.get("title", ""), font=("", 14, "bold"))
        title.pack(padx=8)
        year = ctk.CTkLabel(self, text=str(magazine.get("year", "")))
        year.pack()
        issue_id = ctk.CTkLabel(self, text=magazine.get("id", ""), text_color="gray")
        issue_id.pack(pady=(0, 8))

        if on_edit is not None:
            for widget in (self, cover, title, year, issue_id):
                widget.bind("<Button-1>", lambda _event, mag=magazine: on_edit(mag))
                try:
                    widget.configure(cursor="hand2")
                except Exception:
                    pass


class DropZone(ctk.CTkFrame):
    def __init__(self, master, on_file: Callable[[str], None]):
        super().__init__(master, corner_radius=10, border_width=2)
        self.on_file = on_file
        self.label = ctk.CTkLabel(self, text="Drop a PDF here\nor", justify="center")
        self.label.pack(pady=(24, 6))
        ctk.CTkButton(self, text="Browse...", command=self._browse).pack(pady=(0, 24))
        self._register_dnd()

    def _browse(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.on_file(path)

    def _register_dnd(self):
        try:
            from tkinterdnd2 import DND_FILES
            self.drop_target_register(DND_FILES)
            self.dnd_bind("<<Drop>>", self._on_drop)
        except Exception:
            # tkinterdnd2 not available or root not TkinterDnD; Browse still works.
            pass

    def _on_drop(self, event):
        try:
            paths = list(self.tk.splitlist(event.data))
        except Exception:
            paths = [event.data.strip().strip("{}")]
        for path in paths:
            if path.lower().endswith(".pdf"):
                self.on_file(path)
                return


class ConfirmDeleteModal(ctk.CTkToplevel):
    def __init__(self, master, magazine: dict, targets: list[str], require_title: bool, on_confirm):
        super().__init__(master)
        self.title("Confirm delete")
        self.geometry("460x420")
        self.magazine = magazine
        self.on_confirm = on_confirm
        self.require_title = require_title

        name = magazine.get("title", magazine.get("id", ""))
        ctk.CTkLabel(self, text=f'Delete "{name}"?', font=("", 16, "bold")).pack(pady=12)
        ctk.CTkLabel(self, text="This will permanently delete:").pack(anchor="w", padx=16)
        for t in targets:
            ctk.CTkLabel(self, text=f"  - {t}", text_color="gray").pack(anchor="w", padx=16)

        self.entry = None
        if require_title:
            ctk.CTkLabel(self, text=f'Type "{name}" to confirm:').pack(anchor="w", padx=16, pady=(12, 2))
            self.entry = ctk.CTkEntry(self, width=380)
            self.entry.pack(padx=16)

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(pady=16)
        ctk.CTkButton(btns, text="Cancel", command=self.destroy).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Delete", fg_color="#a83232", hover_color="#7a2020",
                      command=self._confirm).pack(side="left", padx=6)
        self.transient(master)
        self.grab_set()

    def _confirm(self):
        if self.require_title:
            name = self.magazine.get("title", self.magazine.get("id", ""))
            if self.entry.get().strip() != name:
                self.bell()
                return
        self.destroy()
        self.on_confirm(self.magazine)
