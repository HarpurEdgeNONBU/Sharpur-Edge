import importlib


def test_page_text_view_module_imports():
    mod = importlib.import_module("manager.ui.page_text_view")
    assert hasattr(mod, "PageTextView")
