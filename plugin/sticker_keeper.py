import os
import sys

# Add local lib folder to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from flowlauncher import FlowLauncher

# PySide6 for alpha-aware clipboard
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage

# Initialize a single QApplication instance
app = QApplication([])


class StickerKeeper(FlowLauncher):
    def __init__(self):
        self.sticker_dir = os.path.expanduser("~/stickers")
        os.makedirs(self.sticker_dir, exist_ok=True)
        super().__init__()

    def query(self, query):
        results = []

        if not query.strip():
            return [{
                "Title": "No query",
                "SubTitle": "Type something to search your stickers",
                "IcoPath": "icon.png"
            }]

        for file in os.listdir(self.sticker_dir):
            if query.lower() in file.lower():
                file_path = os.path.join(self.sticker_dir, file)
                results.append({
                    "Title": file,
                    "SubTitle": "Click to copy sticker to clipboard (preserves transparency)",
                    "IcoPath": file_path,
                    "JsonRPCAction": {
                        "method": "copy_to_clipboard",
                        "parameters": [file_path],
                        "dontHideAfterAction": False
                    }
                })
        return results

    def copy_to_clipboard(self, filepath):
        """Copy PNG sticker to clipboard with alpha channel preserved"""
        if os.path.exists(filepath):
            image = QImage(filepath)
            if not image.isNull():
                clipboard = app.clipboard()
                clipboard.setImage(image)
                return True
        return False
