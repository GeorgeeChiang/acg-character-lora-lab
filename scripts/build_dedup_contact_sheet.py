from __future__ import annotations

import csv
import math
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(r"C:\Users\dodo\Documents\Codex\ACG_AI_picture")
RAW_DIR = ROOT / "data" / "raw" / "senren_banka_asatake_yoshino"
OUT_DIR = ROOT / "outputs" / "triage" / "senren_banka_asatake_yoshino"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def ahash(path: Path) -> str:
    with Image.open(path) as img:
        img = img.convert("L").resize((8, 8), Image.Resampling.LANCZOS)
        pixels = list(img.getdata())
        avg = sum(pixels) / len(pixels)
        bits = "".join("1" if p >= avg else "0" for p in pixels)
        return hex(int(bits, 2))[2:].rjust(16, "0")


paths = [p for p in RAW_DIR.iterdir() if p.is_file() and p.suffix.lower() in {".webp", ".jpg", ".jpeg", ".png"}]
groups: dict[str, list[Path]] = {}
for path in paths:
    groups.setdefault(ahash(path), []).append(path)

representatives: list[tuple[str, Path, int]] = []
for h, items in groups.items():
    rep = sorted(items, key=lambda p: (-p.stat().st_size, p.name.lower()))[0]
    representatives.append((h, rep, len(items)))

representatives.sort(key=lambda x: (-x[2], x[1].name.lower()))

csv_path = OUT_DIR / "dedup_representatives.csv"
with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["hash", "representative", "group_size"])
    for h, rep, size in representatives:
        writer.writerow([h, rep.name, size])

thumb_w = 192
thumb_h = 192
label_h = 36
cols = 5
rows = math.ceil(len(representatives) / cols)
sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "#202020")
draw = ImageDraw.Draw(sheet)

for i, (h, path, size) in enumerate(representatives):
    x = (i % cols) * thumb_w
    y = (i // cols) * (thumb_h + label_h)
    try:
        with Image.open(path) as img:
            img = img.convert("RGB")
            img.thumbnail((thumb_w, thumb_h))
            bg = Image.new("RGB", (thumb_w, thumb_h), "#111111")
            ox = (thumb_w - img.width) // 2
            oy = (thumb_h - img.height) // 2
            bg.paste(img, (ox, oy))
            sheet.paste(bg, (x, y))
            draw.rectangle([x, y, x + thumb_w - 1, y + thumb_h + label_h - 1], outline="#444444", width=1)
            draw.text((x + 4, y + thumb_h + 3), f"{i+1:03d} x{size} {path.name[:16]}", fill="#f0f0f0")
            draw.text((x + 4, y + thumb_h + 18), h[:16], fill="#b0b0b0")
    except Exception as exc:
        draw.rectangle([x, y, x + thumb_w - 1, y + thumb_h + label_h - 1], fill="#550000", outline="#aa0000", width=1)
        draw.text((x + 4, y + 4), f"ERR {path.name}", fill="#ffffff")
        draw.text((x + 4, y + 30), str(exc), fill="#ffffff")

out = OUT_DIR / "dedup_representatives.png"
sheet.save(out)
print(out)
print(csv_path)
print(f"groups={len(groups)} reps={len(representatives)}")
