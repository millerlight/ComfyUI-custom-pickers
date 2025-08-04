# Image Format Picker (ComfyUI) – liest image_formats.json aus demselben Ordner
# Outputs: width (INT), height (INT)
# Defaults: format="4:3", size="medium"
# Reihenfolge von Formaten und Größen folgt der JSON-Definition (nicht alphabetisch)

import os, json

print("[ImageFormatPicker] loading:", __file__)
_THIS_DIR = os.path.dirname(__file__)
_JSON_PATH = os.path.join(_THIS_DIR, "image_formats.json")

def _load_config():
    cfg = {}
    order_formats = []
    order_sizes = []
    try:
        with open(_JSON_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
        top = raw.get("image-formats", [])
        if top and isinstance(top, list) and isinstance(top[0], dict):
            fmts = top[0]
            for ratio, arr in fmts.items():
                order_formats.append(str(ratio))
                sizes = {}
                if isinstance(arr, list) and arr and isinstance(arr[0], dict):
                    for size, wh in arr[0].items():
                        if isinstance(wh, list) and len(wh) == 2:
                            w, h = int(wh[0]), int(wh[1])
                            sizes[str(size)] = (w, h)
                            if str(size) not in order_sizes:
                                order_sizes.append(str(size))
                if sizes:
                    cfg[str(ratio)] = sizes
    except Exception as e:
        print(f"[ImageFormatPicker] WARN: cannot read { _JSON_PATH }: {e}")
    if not cfg:
        cfg = {"4:3": {"medium": (1024, 768)}}
        order_formats = ["4:3"]
        order_sizes = ["medium"]
    return cfg, order_formats, order_sizes

_CFG, _FORMAT_ORDER, _SIZE_ORDER = _load_config()

# Formate & Größen in JSON-Reihenfolge
_FORMATS = _FORMAT_ORDER if _FORMAT_ORDER else list(_CFG.keys())
_SIZES = _SIZE_ORDER if _SIZE_ORDER else (sorted(next(iter(_CFG.values())).keys()) if _CFG else ["medium"])

# Explizite Defaults: bevorzugt "4:3" und "medium" wenn vorhanden
_DEFAULT_FORMAT = "4:3" if "4:3" in _FORMATS else (_FORMATS[0] if _FORMATS else "4:3")
_DEFAULT_SIZE = "medium" if "medium" in _SIZES else (_SIZES[0] if _SIZES else "medium")

def _resolve(fmt, size):
    fmt = str(fmt)
    size = str(size)
    if fmt not in _CFG:
        fmt = _DEFAULT_FORMAT
    size_map = _CFG.get(fmt, {})
    if size not in size_map:
        size = _DEFAULT_SIZE
    w, h = size_map.get(size, (1024, 768))
    return int(w), int(h)

class ImageFormatPicker:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "format": (_FORMATS or ["4:3"], {"default": _DEFAULT_FORMAT}),
                "size": (_SIZES or ["medium"], {"default": _DEFAULT_SIZE}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "pick"
    CATEGORY = "Utils/Resolution"

    def pick(self, format, size):
        w, h = _resolve(format, size)
        return (w, h)

NODE_CLASS_MAPPINGS = {
    "ImageFormatPicker": ImageFormatPicker,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageFormatPicker": "Image Format Picker",
}
