# ComfyUI-image-formats: Web-Assets bereitstellen + Nodes re-exportieren

import os, shutil

# --- Web-Assets (JSON für das Frontend verfügbar machen) ---
WEB_DIRECTORY = "./web"

_here = os.path.dirname(__file__)
_src_json = os.path.join(_here, "image_formats.json")
_web_dir  = os.path.join(_here, "web")
_dst_json = os.path.join(_web_dir, "image_formats.json")

try:
    os.makedirs(_web_dir, exist_ok=True)
    if os.path.isfile(_src_json):
        if (not os.path.isfile(_dst_json)) or (os.path.getmtime(_src_json) > os.path.getmtime(_dst_json)):
            shutil.copy2(_src_json, _dst_json)
            print("[ComfyUI-image-formats] exported image_formats.json to web/")
except Exception as e:
    print("[ComfyUI-image-formats] WARN:", e)

# --- Nodes aus dem Modul re-exportieren ---
from .image_format_node import (
    NODE_CLASS_MAPPINGS as _NCM,
    NODE_DISPLAY_NAME_MAPPINGS as _NDM,
)

NODE_CLASS_MAPPINGS = dict(_NCM)
NODE_DISPLAY_NAME_MAPPINGS = dict(_NDM)
