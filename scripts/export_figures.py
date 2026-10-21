"""Export the survey's figures as high-resolution PNG for the repository.

Reads the vector PDFs in paper/figures and writes 2x PNGs to assets/figures.
The pages are flat colour with mostly solid fills, so they are quantised to a
256-colour palette after rendering: the result is visually identical to the
RGB render and roughly half the size, which matters for a repository that
loads these images on its landing page.

Run after changing a figure:

    python scripts/export_figures.py
"""

from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "paper" / "figures"
DST = ROOT / "assets" / "figures"

FIGS = {
    "agent_loop.pdf": "sense_think_act.png",
    "corpora_scale.pdf": "corpora_scale.png",
    "levels.pdf": "levels.png",
    "bci_applications.pdf": "applications.png",
}


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
        image = image.quantize(colors=256, method=Image.MEDIANCUT,
                               dither=Image.FLOYDSTEINBERG)
        image.save(out, "PNG", optimize=True)
        print("%-24s -> %-22s %dx%d  %.0f KB"
              % (src_name, dst_name, image.width, image.height,
                 out.stat().st_size / 1024))


if __name__ == "__main__":
    main()
