from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(r"C:\Users\dodo\Documents\Codex\ACG_AI_picture")
RAW_DIR = ROOT / "data" / "raw" / "senren_banka_asatake_yoshino"
OUT_DIR = ROOT / "outputs" / "triage" / "senren_banka_asatake_yoshino"
OUT_DIR.mkdir(parents=True, exist_ok=True)

paths = sorted(
    [p for p in RAW_DIR.iterdir() if p.is_file() and p.suffix.lower() in {".webp", ".jpg", ".jpeg", ".png"}],
    key=lambda p: (p.name.lower(), p.stat().st_size),
)

if not paths:
    raise SystemExit("No images found in raw dir.")

sample_size = min(120, len(paths))
if len(paths) <= sample_size:
    sample = paths
else:
    # Evenly sample across the full collection so the contact sheet is representative.
    sample = []
    step = len(paths) / sample_size
    for i in range(sample_size):
        idx = min(len(paths) - 1, int(i * step))
        sample.append(paths[idx])

thumb_w = 192
thumb_h = 192
label_h = 26
cols = 6
rows = math.ceil(len(sample) / cols)
sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "#202020")
draw = ImageDraw.Draw(sheet)

for i, path in enumerate(sample):
    try:
        with Image.open(path) as img:
            img = img.convert("RGB")
            img.thumbnail((thumb_w, thumb_h))
            x = (i % cols) * thumb_w
            y = (i // cols) * (thumb_h + label_h)
            bg = Image.new("RGB", (thumb_w, thumb_h), "#111111")
            ox = (thumb_w - img.width) // 2
            oy = (thumb_h - img.height) // 2
            bg.paste(img, (ox, oy))
            sheet.paste(bg, (x, y))
            draw.rectangle([x, y, x + thumb_w - 1, y + thumb_h + label_h - 1], outline="#444444", width=1)
            draw.text((x + 4, y + thumb_h + 3), f"{i+1:03d} {path.name[:18]}", fill="#f0f0f0")
    except Exception as exc:
        x = (i % cols) * thumb_w
        y = (i // cols) * (thumb_h + label_h)
        draw.rectangle([x, y, x + thumb_w - 1, y + thumb_h + label_h - 1], fill="#550000", outline="#aa0000", width=1)
        draw.text((x + 4, y + 4), f"ERR {path.name}", fill="#ffffff")
        draw.text((x + 4, y + 30), str(exc), fill="#ffffff")

out = OUT_DIR / "raw_contact_sheet.png"
sheet.save(out)
print(out)
print(f"count={len(paths)} sample={len(sample)} rows={rows} cols={cols}")
