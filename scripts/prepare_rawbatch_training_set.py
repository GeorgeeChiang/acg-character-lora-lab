from __future__ import annotations

import csv
import hashlib
import math
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(r"C:\Users\dodo\Documents\Codex\ACG_AI_picture")
RAW_DIR = ROOT / "data" / "raw" / "senren_banka_asatake_yoshino"
TRAIN_DIR = ROOT / "data" / "train" / "senren_banka_asatake_yoshino"
LOG_DIR = ROOT / "logs"
CONFIG_PATH = ROOT / "configs" / "dataset_senren_banka_asatake_yoshino.toml"
MANIFEST_PATH = LOG_DIR / "rawbatch_training_manifest_senren_banka_asatake_yoshino.csv"

TRAIN_DIR.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ahash(path: Path) -> str:
    with Image.open(path) as img:
        img = img.convert("L").resize((8, 8), Image.Resampling.LANCZOS)
        pixels = list(img.getdata())
        avg = sum(pixels) / len(pixels)
        bits = "".join("1" if p >= avg else "0" for p in pixels)
        return hex(int(bits, 2))[2:].rjust(16, "0")


existing_exact = {sha256(p) for p in TRAIN_DIR.iterdir() if p.is_file() and p.suffix.lower() in {".webp", ".jpg", ".jpeg", ".png"}}

raw_paths = [p for p in RAW_DIR.iterdir() if p.is_file() and p.suffix.lower() in {".webp", ".jpg", ".jpeg", ".png"}]
groups: dict[str, list[Path]] = {}
for path in raw_paths:
    groups.setdefault(ahash(path), []).append(path)

selected: list[tuple[Path, Path, int]] = []
for _, items in groups.items():
    rep = sorted(items, key=lambda p: (-p.stat().st_size, p.name.lower()))[0]
    rep_hash = sha256(rep)
    if rep_hash in existing_exact:
        continue
    selected.append((rep, rep, len(items)))

selected.sort(key=lambda x: (-x[2], x[0].name.lower()))

caption = "sksgirl, 朝武芳乃, white hair, blue eyes, twintails, 1girl"

manifest_rows = []
for idx, (src, _, group_size) in enumerate(selected, start=1):
    stem = f"rawbatch_{idx:03d}_{src.stem}"
    dst_image = TRAIN_DIR / f"{stem}{src.suffix.lower()}"
    dst_caption = TRAIN_DIR / f"{stem}.txt"
    shutil.copy2(src, dst_image)
    dst_caption.write_text(caption + "\n", encoding="utf-8")
    manifest_rows.append(
        {
            "index": idx,
            "source": src.name,
            "output_image": dst_image.name,
            "output_caption": dst_caption.name,
            "group_size": group_size,
            "caption": caption,
        }
    )

with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["index", "source", "output_image", "output_caption", "group_size", "caption"])
    writer.writeheader()
    writer.writerows(manifest_rows)

count_after = len([p for p in TRAIN_DIR.iterdir() if p.is_file() and p.suffix.lower() in {".webp", ".jpg", ".jpeg", ".png"} and not p.name.endswith(".txt")])
repeats = max(1, math.floor(1200 / max(1, count_after)))
if count_after * repeats < 1050:
    repeats += 1

text = CONFIG_PATH.read_text(encoding="utf-8")
new_lines = []
for line in text.splitlines():
    if line.strip().startswith("num_repeats ="):
        new_lines.append(f"  num_repeats = {repeats}")
    else:
        new_lines.append(line)
CONFIG_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

print(f"selected={len(selected)}")
print(f"train_images={count_after}")
print(f"num_repeats={repeats}")
print(MANIFEST_PATH)
