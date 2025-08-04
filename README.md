# ComfyUI-custom-pickers

ComfyUI custom nodes that pull default values from JSON files, e.g. for image formats.
The image format picker offers expandable standard formats for images, which can be selected via a dropdown menu. 
https://github.com/millerlight/ComfyUI-custom-pickers

---

## 🔧 Features

- Selectable **image formats and sizes** from `image_formats.json`
- Detects **real image size** from an input image (width & height)
- Toggle between:
  - **Chosen dimensions** (e.g., `16:9`, `bigger`)
  - **Original image size**
- Easily extendable via `image_formats.json`

---

## 📦 Installation

Copy this folder to your `ComfyUI/custom_nodes/` directory:

```
ComfyUI/
└── custom_nodes/
    └── ComfyUI-image-formats/
        ├── image_format_node.py
        ├── __init__.py
        └── image_formats.json
```

Upon startup, `image_formats.json` is automatically made available to the frontend.

---

## 📥 Example `image_formats.json`

```json
{
  "image-formats": [
    {
      "16:9": [
        {
          "small": [512, 288],
          "medium": [1024, 576],
          "big": [1200, 675],
          "bigger": [1600, 900]
        }
      ]
    }
  ]
}
```

---

## 🧠 Node Outputs

- `image`: the passthrough image
- `width`, `height`: Final selected width/height, depending on toggle (picker vs original image)

---

## 🔁 Node Manager Integration

### Example `comfyui.json` snippet for PR:

```json
{
  "name": "ComfyUI-custom-pickers",
  "author": "millerlight",
  "description": "Selectable image formats and original image size detection for ComfyUI.",
  "version": "1.0.0",
  "link": "https://github.com/millerlight/ComfyUI-custom-pickers",
  "tags": ["image", "resolution", "format", "size"],
  "modules": ["image_format_node.py"]
}
```

---

## 📜 License

MIT License – free for personal and commercial use.