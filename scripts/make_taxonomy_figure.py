"""Render the research-area taxonomy figure used by the repository README.

The figure is native to this repository rather than to the survey: it encodes
the classification that resources/by-area/ uses, so that a reader sees the
same nine areas in the same five tiers in the README, in the index pages and
in the flat reference list.

The area definitions are imported from build_resources.py so that there is a
single source of truth, and the reference counts are read from the committed
index. Regenerate the figure whenever the index changes:

    python scripts/make_taxonomy_figure.py
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
from PIL import Image

from build_resources import AREAS, TIER_NOTES, TIERS

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "figures" / "taxonomy.png"

C_BLUE = "#2F6EA5"
C_ORANGE = "#C4622D"
C_BAND = "#F7FAFD"
C_INK = "#1A1A1A"
C_MUTED = "#5A6B7A"
C_LINE = "#C9D6E3"

BAND_X0 = 0.036
BAND_X1 = 0.990
CARD_X0 = 0.252
CARD_X1 = 0.974
CARD_GAP = 0.032

TOP = 0.985
HEIGHTS = [0.181, 0.181, 0.181, 0.181, 0.181]
GAPS = [0.017, 0.017, 0.017, 0.017]

# Vertical rhythm inside a card, in axes units.
TITLE_Y = 0.038
RULE_Y = 0.054
ASPECT_Y = 0.068
ASPECT_STEP = 0.0235
PAD = 0.010


def style() -> None:
    mpl.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Nimbus Roman", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
    })


def counts(papers: list[dict]) -> dict[str, tuple[int, int]]:
    """area -> (references filed here, references filed primarily here)."""
    out = {}
    for key in AREAS:
        total = sum(1 for p in papers if key in p["areas"])
        primary = sum(1 for p in papers if p["primary_area"] == key)
        out[key] = (total, primary)
    return out


def rounded(ax, x0, y0, x1, y1, face, edge, lw=0.9, dashed=False):
    patch = FancyBboxPatch(
        (x0, y0), x1 - x0, y1 - y0,
        boxstyle="round,pad=0,rounding_size=0.008",
        facecolor=face, edgecolor=edge, linewidth=lw,
        linestyle=(0, (3.2, 2.2)) if dashed else "solid",
        zorder=2,
    )
    ax.add_patch(patch)
    return patch


def count_label(total: int, primary: int) -> str:
    if total == primary:
        return "%d refs" % total
    return "%d refs · %d primary" % (total, primary)


def draw_card(ax, x0, y0, x1, y1, title, aspects, label):
    rounded(ax, x0, y0, x1, y1, "white", C_LINE, lw=0.9)
    y1_ = y1
    ax.text(x0 + 0.016, y1_ - TITLE_Y, title, fontsize=11.0, color=C_INK,
            va="center", ha="left", zorder=5)
    ax.text(x1 - 0.016, y1_ - TITLE_Y, label, fontsize=8.2, color=C_ORANGE,
            va="center", ha="right", zorder=5, weight="bold")
    ax.plot([x0 + 0.016, x1 - 0.016], [y1_ - RULE_Y, y1_ - RULE_Y],
            color=C_LINE, lw=0.7, zorder=4)
    y = y1_ - ASPECT_Y
    for aspect in aspects:
        ax.text(x0 + 0.016, y, "· " + aspect, fontsize=8.2, color=C_MUTED,
                va="center", ha="left", style="italic", zorder=5)
        y -= ASPECT_STEP


def main() -> None:
    style()
    papers = json.loads((ROOT / "resources" / "papers.json")
                         .read_text(encoding="utf-8"))["papers"]
    tally = counts(papers)

    fig, ax = plt.subplots(figsize=(9.4, 6.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    tiers = list(TIERS.items())
    y = TOP
    for i, (tier, keys) in enumerate(tiers):
        h = HEIGHTS[i]
        y0 = y - h

        rounded(ax, BAND_X0, y0, BAND_X1, y0 + h, C_BAND, C_LINE, lw=0.8,
                dashed=(tier == "Boundaries"))

        ax.text(BAND_X0 + 0.026, y0 + h - 0.042, tier, fontsize=14.5,
                color=C_BLUE, va="center", ha="left", zorder=5)
        for j, line in enumerate(textwrap.wrap(TIER_NOTES[tier], 30)):
            ax.text(BAND_X0 + 0.026, y0 + h - 0.082 - j * 0.027, line,
                    fontsize=8.2, color=C_MUTED, va="center", ha="left",
                    style="italic", zorder=5)

        if len(keys) == 1:
            key = keys[0]
            draw_card(ax, CARD_X0, y0 + PAD, CARD_X1, y0 + h - PAD,
                      AREAS[key][0], AREAS[key][2],
                      count_label(*tally[key]))
        else:
            w = (CARD_X1 - CARD_X0 - CARD_GAP) / 2
            for j, key in enumerate(keys):
                x0 = CARD_X0 + j * (w + CARD_GAP)
                draw_card(ax, x0, y0 + PAD, x0 + w, y0 + h - PAD,
                          AREAS[key][0], AREAS[key][2],
                          count_label(*tally[key]))

        if i < len(tiers) - 1:
            cy = y0 - GAPS[i] / 2
            ax.add_patch(Polygon([[BAND_X0 + 0.026, cy + 0.008],
                                   [BAND_X0 + 0.038, cy + 0.008],
                                   [BAND_X0 + 0.032, cy - 0.007]],
                                  closed=True, facecolor=C_LINE,
                                  edgecolor="none", zorder=3))

        y = y0 - GAPS[i] if i < len(tiers) - 1 else y0

    fig.subplots_adjust(left=0.004, right=0.996, top=0.996, bottom=0.004)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200, facecolor="white")
    plt.close(fig)

    image = Image.open(OUT).convert("RGB")
    image = image.quantize(colors=256, method=Image.MEDIANCUT,
                           dither=Image.FLOYDSTEINBERG)
    image.save(OUT, "PNG", optimize=True)
    print("%s  %dx%d  %.0f KB"
          % (OUT.name, image.width, image.height, OUT.stat().st_size / 1024))


if __name__ == "__main__":
    main()
