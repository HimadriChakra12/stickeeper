# plugin/main.py
import os
import base64
import pyperclip

class StickerKeeper:
    def __init__(self, plugin_context):
        """
        plugin_context: FlowLauncher passes context info, if needed
        """
        self.plugin_context = plugin_context
        # Default stickers folder inside plugin dir
        self.stickers_dir = os.path.join(os.path.dirname(__file__), "..", "stickers")
        if not os.path.exists(self.stickers_dir):
            os.makedirs(self.stickers_dir)

        # Supported image extensions
        self.supported_exts = {".png", ".jpg", ".jpeg", ".gif"}

    def query(self, query_text):
        """
        Returns a list of dicts for FlowLauncher to display
        """
        results = []
        query_lower = query_text.lower()
        for fname in os.listdir(self.stickers_dir):
            if os.path.splitext(fname)[1].lower() in self.supported_exts:
                if query_lower in fname.lower():
                    full_path = os.path.join(self.stickers_dir, fname)
                    results.append({
                        "Title": fname,
                        "SubTitle": "Click to copy image path to clipboard",
                        "IcoPath": full_path,
                        "JsonRPCAction": {
                            "method": "copy_image",
                            "parameters": [full_path],
                            "dontHideAfterAction": False
                        }
                    })
        return results

    def copy_image(self, image_path):
        """
        Copies the image path or image data to clipboard
        """
        try:
            with open(image_path, "rb") as f:
                img_bytes = f.read()
            # Convert to base64 string if you want the image itself
            img_b64 = base64.b64encode(img_bytes).decode("utf-8")
            pyperclip.copy(img_b64)
            return {"Result": f"Copied {os.path.basename(image_path)} to clipboard"}
        except Exception as e:
            return {"Result": f"Failed to copy: {str(e)}"}

