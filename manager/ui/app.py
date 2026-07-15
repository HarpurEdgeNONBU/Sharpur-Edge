from __future__ import annotations

import queue
import threading
from typing import Callable

import customtkinter as ctk

from manager.core.config import load_config
from manager.core.paths import get_root

# CustomTkinter's automatic DPI-scaling loop temporarily drops the window alpha
# to 0.15 while re-measuring scaling and restores it to 1 afterwards, with no
# try/finally. If a scaling callback raises in between (a stale callback for a
# widget destroyed during a dashboard refresh, or a just-closed modal), the
# restore is skipped and the main window stays translucent. Disabling the loop
# removes that failure mode. Must run before any CTk window is created.
ctk.deactivate_automatic_dpi_awareness()

try:
    from tkinterdnd2 import TkinterDnD
    _DND_BASE = TkinterDnD.Tk
    _HAS_DND = True
except Exception:
    _DND_BASE = ctk.CTk
    _HAS_DND = False


class App(_DND_BASE):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("Sharpur Edge Archive Manager")
        self.geometry("1100x720")

        self.config_obj = load_config()
        self.root_path = get_root(self.config_obj)
        icon_path = self.root_path / "manager" / "assets" / "icons" / "admin.ico"
        if icon_path.exists():
            try:
                self.iconbitmap(str(icon_path))
            except Exception:
                pass
        self._results: "queue.Queue" = queue.Queue()
        self._views: dict = {}

        nav = ctk.CTkFrame(self, width=180, corner_radius=0)
        nav.pack(side="left", fill="y")
        nav.pack_propagate(False)
        ctk.CTkLabel(nav, text="Archive\nManager", font=("", 18, "bold")).pack(pady=20)
        for name in ("Dashboard", "Add Issue", "Page Text", "Explorer", "Git"):
            ctk.CTkButton(nav, text=name, command=lambda n=name: self.show_view(n)).pack(
                fill="x", padx=12, pady=4
            )

        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)

        self.after(100, self._poll_results)
        self.show_view("Dashboard")

    def show_view(self, name: str):
        for child in self.content.winfo_children():
            child.destroy()
        if name == "Dashboard":
            from manager.ui.dashboard_view import DashboardView
            DashboardView(self.content, self).pack(fill="both", expand=True)
        elif name == "Add Issue":
            from manager.ui.add_issue_view import AddIssueView
            AddIssueView(self.content, self).pack(fill="both", expand=True)
        elif name == "Page Text":
            from manager.ui.page_text_view import PageTextView
            PageTextView(self.content, self).pack(fill="both", expand=True)
        elif name == "Explorer":
            from manager.ui.explorer_view import ExplorerView
            ExplorerView(self.content, self).pack(fill="both", expand=True)
        elif name == "Git":
            from manager.ui.git_panel import GitPanel
            GitPanel(self.content, self).pack(fill="both", expand=True)

    def open_page_text(self, issue_id: str):
        for child in self.content.winfo_children():
            child.destroy()
        from manager.ui.page_text_view import PageTextView
        PageTextView(self.content, self, issue_id=issue_id).pack(fill="both", expand=True)

    def run_bg(self, fn: Callable, on_done: Callable):
        def worker():
            try:
                self._results.put((on_done, fn(), None))
            except Exception as exc:  # noqa: BLE001
                self._results.put((on_done, None, exc))
        threading.Thread(target=worker, daemon=True).start()

    def post(self, on_done: Callable, value):
        """Schedule a UI callback from a worker thread (e.g. progress)."""
        self._results.put((on_done, value, None))

    def _poll_results(self):
        try:
            while True:
                on_done, value, err = self._results.get_nowait()
                on_done(value, err)
        except queue.Empty:
            pass
        self.after(100, self._poll_results)
