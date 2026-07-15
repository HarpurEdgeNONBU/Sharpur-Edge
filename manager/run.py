"""Entry point: python manager/run.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manager.ui.app import App


def main():
    App().mainloop()


if __name__ == "__main__":
    main()
