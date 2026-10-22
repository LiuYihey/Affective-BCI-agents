"""Check the pages follow the layout conventions GitHub actually renders.

Two things GitHub does that hand-written Markdown usually gets wrong:

* An ``h2`` already carries a bottom border, so a ``---`` immediately before
  one draws a second rule and the section reads as two separators.
* Markdown inside a raw HTML table cell is rendered, but the cell's own
  content is not padded, so a table that has been given no ``valign`` puts
  a short cell's text at the top of a tall row.

Neither breaks the page, but both are what makes a rendered README look
accidental rather than designed. These checks keep the fix in place.

Run in CI:

    python scripts/check_layout.py
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Pages that are written by hand and therefore subject to the conventions.
HAND_WRITTEN = [
    "README.md",
    "CONTRIBUTING.md",
    "resources/README.md",
    "playbooks/README.md",
    "playbooks/evaluation-protocol.md",
    "playbooks/closed-loop-design.md",
    "playbooks/maturity-ladder.md",
]

# Generated pages are checked too: CI cannot rebuild them, but it can
# confirm that the committed output still follows the conventions.
GENERATED = [
    "resources/corpora.md",
    "resources/papers.md",
    "resources/by-area/README.md",
]

# A thematic break directly followed by a heading, with only blank lines
# between them.
RULE_THEN_HEADING = re.compile(
    r"^---\s*$\n(?:\s*$\n)+^(#{1,6})\s", re.M)

# A table cell that carries an image but no vertical alignment.
CELL_WITHOUT_VALIGN = re.compile(
    r"<td(?![^>]*\bvalign=)[^>]*>\s*$\n\s*<img", re.M)


def main() -> int:
    problems = []
    pages = HAND_WRITTEN + GENERATED

    for name in pages:
        path = ROOT / name
        if not path.exists():
            problems.append("missing page: %s" % name)
            continue
        text = path.read_text(encoding="utf-8")

        for match in RULE_THEN_HEADING.finditer(text):
            line = text[:match.start()].count("\n") + 1
            problems.append("%s:%d has a rule before a heading; the heading "
                            "already draws one" % (name, line))

        for match in CELL_WITHOUT_VALIGN.finditer(text):
            line = text[:match.start()].count("\n") + 1
            problems.append("%s:%d has a table cell with an image but no "
                            "valign" % (name, line))

    for problem in problems:
        print("LAYOUT %s" % problem)
    print("\nchecked %d pages | layout problems: %d"
          % (len(pages), len(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
