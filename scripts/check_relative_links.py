"""Check that every relative path in the Markdown points at a real file.

Covers both Markdown links and the src attributes of images, because the
README places its figures with raw HTML. A path that resolves on the author's
machine but not on GitHub is a broken image in the rendered page.

Run after moving files, and in CI:

    python scripts/check_relative_links.py
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# [text](target) and <img src="target">
PATTERNS = [
    re.compile(r"\[[^\]]*\]\(([^)\s]+)"),
    re.compile(r"<img[^>]+src=\"([^\"]+)\""),
]

SKIP_DIRS = {".git", "paper", "node_modules", "__pycache__"}


def main() -> int:
    broken = []
    total = 0
    for md in sorted(ROOT.rglob("*.md")):
        if SKIP_DIRS & set(md.parts):
            continue
        text = md.read_text(encoding="utf-8")
        for pattern in PATTERNS:
            for match in pattern.finditer(text):
                target = match.group(1).strip()
                if target.startswith(("http://", "https://", "#", "mailto:", "data:")):
                    continue
                target = target.split("#")[0].split("?")[0]
                if not target:
                    continue
                total += 1
                if not (md.parent / target).resolve().exists():
                    broken.append("%s -> %s" % (md.relative_to(ROOT).as_posix(), target))

    print("relative links checked: %d | broken: %d" % (total, len(broken)))
    for item in broken:
        print("  BROKEN:", item)
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
