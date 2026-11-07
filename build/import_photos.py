#!/usr/bin/env python3
"""Import new job photos into the site image set.

Usage:
    python3 build/import_photos.py [--in DIR] [--out DIR]

Reads originals from  ../photos-in  (default), writes WebP derivatives at 480/800/1280/1920
into ../build/images, and updates ../photos-manifest.json.

Naming:  <project>-<suburb>-01.jpg  ->  <project>-<suburb>-01-{480,800,1280,1920}.webp
Files already processed (same name + same source mtime) are skipped.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow is required:  python3 -m pip install --user pillow")

ROOT = Path(__file__).resolve().parent.parent
WIDTHS = (1920, 1280, 800, 480)
EXTRA = 30          # append a little width when upscaling so 1920 stays sharp
QUALITY = 82
ACCEPTED = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp", ".tif", ".tiff"}


def slug(name: str) -> str:
    stem = Path(name).stem.lower()
    stem = re.sub(r"[^a-z0-9]+", "-", stem).strip("-")
    return stem or "photo"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", default=str(ROOT / "photos-in"))
    ap.add_argument("--out", dest="out", default=str(ROOT / "build" / "images"))
    args = ap.parse_args()

    src, out = Path(args.src), Path(args.out)
    src.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)

    files = sorted(f for f in src.iterdir() if f.suffix.lower() in ACCEPTED)
    if not files:
        print(f"No photos in {src}. Drop originals there and re-run.")
        return 1

    manifest_path = ROOT / "photos-manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}

    made = skipped = 0
    for f in files:
        key = slug(f.name)
        stamp = int(f.stat().st_mtime)
        if manifest.get(key, {}).get("source_mtime") == stamp:
            skipped += 1
            continue
        try:
            im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
        except Exception as e:                      # noqa: BLE001
            print(f"  ! {f.name}: cannot open ({e})")
            continue

        written = []
        for w in WIDTHS:
            if im.width < w:
                canvas = im.copy()
                canvas.thumbnail((w, round(im.height * w / im.width)), Image.LANCZOS)
                target = canvas
            else:
                target = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            p = out / f"{key}-{w}.webp"
            target.save(p, "WEBP", quality=QUALITY, method=6)
            written.append(p.name)

        manifest[key] = {
            "source": f.name,
            "source_mtime": stamp,
            "source_pixels": f"{im.width}x{im.height}",
            "derivatives": written,
        }
        made += 1
        flag = "  (upscaled)" if im.width < 1280 else ""
        print(f"  + {key}: {im.width}x{im.height} -> {len(written)} files{flag}")

    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True))
    print(f"\n{made} imported, {skipped} already current. Derivatives in {out}")
    if made:
        print("Next: add the new keys to GALLERY in build/build.py, then run:  cd build && python3 build2.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
