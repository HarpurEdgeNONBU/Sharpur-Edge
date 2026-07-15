"""Regression guard for the translucent-window bug.

CustomTkinter's automatic DPI-scaling loop briefly sets the window alpha to
0.15 while it re-measures scaling, then restores it to 1. If a scaling callback
raises in between (e.g. a stale callback for a widget destroyed during a
dashboard refresh or a just-closed modal), the restore is skipped and the main
window stays translucent. We disable that loop at import time; this test ensures
the switch stays flipped.
"""
from customtkinter.windows.widgets.scaling.scaling_tracker import ScalingTracker


def test_app_import_disables_dpi_alpha_loop():
    import manager.ui.app  # noqa: F401 -- importing must disable the DPI loop
    assert ScalingTracker.deactivate_automatic_dpi_awareness is True
