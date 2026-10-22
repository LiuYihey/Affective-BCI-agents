"""Export the survey's figures as high-resolution PNG for the repository.

Reads the vector PDFs in paper/figures and writes 2x PNGs to assets/figures.
The pages are flat colour with mostly solid fills, so they are quantised to a
256-colour palette after rendering: the result is visually identical to the
RGB render and roughly half the size, which matters for a repository that
loads these images on its landing page.

The PDF pages carry whitespace around the artwork, which becomes dead space
once the figure is placed in a README at full column width. Each export is
therefore trimmed to its content, with a small even margin left around it, so
the figure fills the space it is given.

Run after changing a figure:

    python scripts/export_figures.py
"""

from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "paper" / "figures"
DST = ROOT / "assets" / "figures"

FIGS = {
    "agent_loop.pdf": "sense_think_act.png",
    "corpora_scale.pdf": "corpora_scale.png",
    "levels.pdf": "levels.png",
    "bci_applications.pdf": "applications.png",
}

# White margin left around the trimmed artwork, in pixels at 200 dpi.
MARGIN = 12
# Content darker than this counts as part of the artwork.
THRESHOLD = 8


def trim(image: Image.Image) -> Image.Image:
    """Cut the white margin off a rendered page, keeping an even margin."""
    white = Image.new("RGB", image.size, (255, 255, 255))
    diff = ImageChops.difference(image, white).convert("L")
    mask = diff.point(lambda v: 255 if v > THRESHOLD else 0)
    bbox = mask.getbbox()
    if bbox is None:
        return image
    left, top, right, bottom = bbox
    left = max(0, left - MARGIN)
    top = max(0, top - MARGIN)
    right = min(image.width, right + MARGIN)
    bottom = min(image.height, bottom + MARGIN)
    return image.crop((left, top, right, bottom))


def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)
    for src_name, dst_name in FIGS.items():
        src = SRC / src_name
        if not src.exists():
            print("skip (missing):", src_name)
            continue
        doc = fitz.open(src)
        page = doc[0]
        pix = page.get_pixmap(dpi=200, alpha=False)
        out = DST / dst_name
        pix.save(out)
        doc.close()

        image = Image.open(out).convert("RGB")
        image = trim(image)
        image = image.quantize(colors=256, method=Image.MEDIANCUT,
                               dither=Image.FLOYDSTEINBERG)
        image.save(out, "PNG", optimize=True)
        print("%-24s -> %-22s %dx%d  %.0f KB"
              % (src_name, dst_name, image.width, image.height,
                 out.stat().st_size / 1024))


if __name__ == "__main__":
    main()
