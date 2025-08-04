import os
import json
import torch

print("[ImageFormatPicker] loading:", __file__)
_THIS_DIR = os.path.dirname(__file__)
_JSON_PATH = os.path.join(_THIS_DIR, "image_formats.json")

DEBUG = True

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

_FORMATS = _FORMAT_ORDER if _FORMAT_ORDER else list(_CFG.keys())
_SIZES = _SIZE_ORDER if _SIZE_ORDER else (
    sorted(next(iter(_CFG.values())).keys()) if _CFG else ["medium"]
)

_DEFAULT_FORMAT = "4:3" if "4:3" in _FORMAT_ORDER else (_FORMAT_ORDER[0] if _FORMAT_ORDER else "4:3")
_DEFAULT_SIZE = "medium" if "medium" in _SIZE_ORDER else (_SIZE_ORDER[0] if _SIZE_ORDER else "medium")

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
                "format": (_FORMAT_ORDER or ["4:3"], {"default": _DEFAULT_FORMAT}),
                "size": (_SIZE_ORDER or ["medium"], {"default": _DEFAULT_SIZE}),
                "image": ("IMAGE",),
                "use_pick": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = (
        "INT",
        "INT",
    )
    RETURN_NAMES = (
        "width",
        "height",
    )
    FUNCTION = "pick"
    CATEGORY = "Utils/Resolution"

    def pick(self, format, size, image, use_pick):
        pick_width, pick_height = _resolve(format, size)
        img_w = 0
        img_h = 0

        try:
            if DEBUG:
                print(f"\n[ImageFormatPicker] Received image type: {type(image)}")

            if isinstance(image, dict):
                if "samples" in image:
                    samples = image["samples"]
                    if isinstance(samples, list) and len(samples) > 0:
                        t = samples[0]
                        if isinstance(t, torch.Tensor):
                            if t.dim() == 3:
                                img_h = int(t.shape[1])
                                img_w = int(t.shape[2])
                                if DEBUG:
                                    print(f"[ImageFormatPicker] Got from samples[0] (3D): {t.shape}")
                            elif t.dim() == 4:
                                if t.shape[1] in [1, 3]:
                                    img_h = int(t.shape[2])
                                    img_w = int(t.shape[3])
                                    if DEBUG:
                                        print(f"[ImageFormatPicker] Got from samples[0] (4D CHW): {t.shape}")
                                elif t.shape[3] in [1, 3]:
                                    img_h = int(t.shape[1])
                                    img_w = int(t.shape[2])
                                    if DEBUG:
                                        print(f"[ImageFormatPicker] Got from samples[0] (4D HWC): {t.shape}")

                elif "image" in image:
                    pil = image["image"]
                    if hasattr(pil, "size"):
                        img_w, img_h = pil.size
                        if DEBUG:
                            print(f"[ImageFormatPicker] Got from PIL image.size: {pil.size}")

            elif isinstance(image, torch.Tensor):
                if image.dim() == 3:
                    img_h = int(image.shape[1])
                    img_w = int(image.shape[2])
                    if DEBUG:
                        print(f"[ImageFormatPicker] Got from direct tensor (3D): {image.shape}")
                elif image.dim() == 4:
                    if image.shape[1] in [1, 3]:
                        img_h = int(image.shape[2])
                        img_w = int(image.shape[3])
                        if DEBUG:
                            print(f"[ImageFormatPicker] Got from direct tensor (4D CHW): {image.shape}")
                    elif image.shape[3] in [1, 3]:
                        img_h = int(image.shape[1])
                        img_w = int(image.shape[2])
                        if DEBUG:
                            print(f"[ImageFormatPicker] Got from direct tensor (4D HWC): {image.shape}")

        except Exception as e:
            print(f"[ImageFormatPicker] WARN: image size extraction failed: {e}")

        final_w = pick_width if use_pick else img_w
        final_h = pick_height if use_pick else img_h

        if DEBUG:
            print(f"[ImageFormatPicker] → Out: pick=({pick_width},{pick_height})  img=({img_w},{img_h})  → final=({final_w},{final_h})")

        return (
            final_w,
            final_h,
        )

NODE_CLASS_MAPPINGS = {
    "ImageFormatPicker": ImageFormatPicker,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageFormatPicker": "Image Format Picker",
}
