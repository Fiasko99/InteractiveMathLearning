import os
import sys
from pathlib import Path


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = str(Path(__file__).parent.parent)

    base_path = os.path.join(base_path, "assets", "images")
    return os.path.join(base_path, relative_path)


ROOT_PATH = resource_path

URL_PATH = lambda path: "http://localhost:5000/" + path
