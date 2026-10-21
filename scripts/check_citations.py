"""Check that every DOI cited in the repository's prose is in the index.

Guards against a link drifting away from the reference it claims to describe.
Run after editing any page outside resources/:

    python scripts/check_citations.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOI_RE = re.compile(r"https?://doi\.org/([^\s\)\"'>]+)")
ARXIV_RE = re.compile(r"https?://arxiv\.org/abs/([^\s\)\"'>]+)")


def normalise(ref: str) -> str:
    """Reduce a reference to a comparable identifier."""
    ref = ref.strip().rstrip(".,;").lower()
    for prefix in ("https://doi.org/", "http://doi.org/",
                   "https://arxiv.org/abs/", "http://arxiv.org/abs/"):
        if ref.startswith(prefix):
            ref = ref[len(prefix):]
            break
    if ref.startswith("10.48550/arxiv."):
        ref = "arxiv." + ref[len("10.48550/arxiv."):]
    return ref


def main() -> int:
    data = json.loads((ROOT / "resources" / "papers.json").read_text(encoding="utf-8"))
    known_doi = set()
    known_arxiv = set()
    for p in data["papers"]:
        if p["doi"]:
            known_doi.add(normalise(p["doi"]))
        if p["arxiv"]:
            known_arxiv.add(normalise(p["arxiv"]))

    unknown = []
    scanned = 0
    for path in sorted(ROOT.rglob("*.md")):
        rel = path.relative_to(ROOT)
        if rel.parts[0] in ("paper", "resources"):
            continue
        text = path.read_text(encoding="utf-8")
        for m in DOI_RE.finditer(text):
            scanned += 1
            ref = normalise(m.group(1))
            if ref not in known_doi:
                unknown.append((str(rel), m.group(1).rstrip(".,;")))
        for m in ARXIV_RE.finditer(text):
            scanned += 1
            ref = normalise(m.group(1))
            if ref not in known_arxiv:
                unknown.append((str(rel), "arXiv:" + m.group(1).rstrip(".,;")))

    for rel, ref in unknown:
        print("UNKNOWN %-42s %s" % (rel, ref))
    print("\nchecked %d reference links in prose | unknown: %d" % (scanned, len(unknown)))
    return 1 if unknown else 0


if __name__ == "__main__":
    sys.exit(main())
