"""Check that the committed resource index is internally consistent.

The index is generated from the survey's private source, so CI cannot rebuild
it: the source is not in the repository. What CI can check is that the
committed output still agrees with itself, which catches the common failure
modes -- a hand-edited page, an area that lost a member, a count that no
longer matches the table below it, a reference that lost its link or its note.

Run in CI:

    python scripts/check_index.py
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RES = ROOT / "resources"

ROW = re.compile(r"^\| \[(.+?)\]\((.+?)\) \|", re.M)
COUNT = re.compile(r"\*\*(\d+) references\*\* are listed here; (\d+) of them are "
                   r"filed primarily")

# A link to an area's page, as it appears in a hand-written table. The path
# is relative to the page the link sits on: from the repository root it is
# resources/by-area/<key>.md, from inside resources/by-area/ it is <key>.md.
AREA_LINK = re.compile(r"\[([^\]]+)\]\((?:(?:resources/)?by-area/)?([a-z-]+)\.md\)")
# A cell holding nothing but a number.
NUMBER = re.compile(r"^\*\*(\d+)\*\*$|^\s*(\d+)\s*$")

# Hand-written pages whose tables quote reference counts.
COUNTED_PAGES = [ROOT / "README.md", RES / "README.md", RES / "by-area" / "README.md"]

# Pages that state what each area settles, in the index's own wording.
SETTLED_PAGES = [ROOT / "README.md", RES / "by-area" / "README.md"]


def main() -> int:
    problems = []
    data = json.loads((RES / "papers.json").read_text(encoding="utf-8"))
    papers = data["papers"]
    areas = data["areas"]
    tiers = data["tiers"]

    def fail(msg: str) -> None:
        problems.append(msg)

    if not papers:
        fail("papers.json contains no papers")

    # The tiers must partition the areas, with no area left out and none
    # filed twice.
    tiered = [k for keys in tiers.values() for k in keys]
    for key in areas:
        if key not in tiered:
            fail("area %r is in no tier" % key)
    if len(tiered) != len(set(tiered)):
        fail("an area appears in more than one tier")
    for key, info in areas.items():
        if info.get("tier") not in tiers:
            fail("area %r has an unknown tier: %r" % (key, info.get("tier")))

    # Every reference needs a way to be opened, and a reason to be opened.
    for p in papers:
        if not (p["doi"] or p["arxiv"] or p["url"]):
            fail("no link: %s (%s)" % (p["key"], p["title"]))
        if not p.get("note"):
            fail("no note: %s (%s)" % (p["key"], p["title"]))
        if p["primary_area"] not in areas:
            fail("unknown area %r: %s" % (p["primary_area"], p["key"]))
        for a in p["areas"]:
            if a not in areas:
                fail("unknown area %r in areas: %s" % (a, p["key"]))
        if not p["areas"]:
            fail("no area: %s (%s)" % (p["key"], p["title"]))
        if p.get("tier") != areas[p["primary_area"]]["tier"]:
            fail("tier mismatch: %s" % p["key"])

    # The flat list must hold every paper, once.
    flat = (RES / "papers.md").read_text(encoding="utf-8")
    flat_rows = ROW.findall(flat)
    if len(flat_rows) != len(papers):
        fail("papers.md has %d rows, papers.json has %d papers"
             % (len(flat_rows), len(papers)))
    flat_titles = [t for t, _ in flat_rows]
    for p in papers:
        if p["title"] not in flat_titles:
            fail("missing from papers.md: %s" % p["title"])

    # One page per area, whose stated counts match its own table.
    for key, info in areas.items():
        page = RES / "by-area" / ("%s.md" % key)
        if not page.exists():
            fail("missing page: resources/by-area/%s.md" % key)
            continue
        text = page.read_text(encoding="utf-8")
        m = COUNT.search(text)
        if not m:
            fail("no count line: %s" % page.name)
            continue
        stated_total, stated_primary = int(m.group(1)), int(m.group(2))
        rows = ROW.findall(text)
        members = [p for p in papers if key in p["areas"]]
        primary = [p for p in papers if p["primary_area"] == key]
        if stated_total != len(members):
            fail("%s says %d references, index has %d"
                 % (page.name, stated_total, len(members)))
        if stated_primary != len(primary):
            fail("%s says %d filed primarily, index has %d"
                 % (page.name, stated_primary, len(primary)))
        if len(rows) != len(members):
            fail("%s lists %d rows, index has %d members"
                 % (page.name, len(rows), len(members)))
        for p in members:
            if p["title"] not in [t for t, _ in rows]:
                fail("missing from %s: %s" % (page.name, p["title"]))
        if info["title"] not in text.splitlines()[0]:
            fail("%s heading does not match the area: %s"
                 % (page.name, info["title"]))
        if info["tier"] not in text:
            fail("%s does not state its tier: %s" % (page.name, info["tier"]))

    # Every corpus needs a source.
    corpora = data.get("corpora", [])
    if not corpora:
        fail("no corpora in papers.json")
    for c in corpora:
        if not c.get("source_link"):
            fail("corpus without a source link: %s" % c["name"])
    corpora_md = (RES / "corpora.md").read_text(encoding="utf-8")
    for c in corpora:
        if c["name"] not in corpora_md:
            fail("missing from corpora.md: %s" % c["name"])

    # The counts quoted in the hand-written tables must match the index, or
    # the pages will disagree with each other.
    for path in COUNTED_PAGES:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            for i, cell in enumerate(cells):
                link = AREA_LINK.search(cell)
                if not link:
                    continue
                key = link.group(2)
                if key not in areas:
                    fail("%s links an unknown area: %s" % (path.name, key))
                    continue
                quoted = None
                for after in cells[i + 1:]:
                    m = NUMBER.match(after)
                    if m:
                        quoted = int(m.group(1) or m.group(2))
                        break
                if quoted is None:
                    continue
                actual = sum(1 for p in papers if key in p["areas"])
                if quoted != actual:
                    fail("%s says %s has %d references, the index has %d"
                         % (path.name, key, quoted, actual))

    # Where a table states what an area settles, the wording must be the
    # wording the index defines, so that the two never drift apart.
    for path in SETTLED_PAGES:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for key, info in areas.items():
            if info["settles"] not in text:
                fail("%s does not use the index wording for %s"
                     % (path.name, key))

    print("papers: %d | areas: %d | tiers: %d | corpora: %d"
          % (len(papers), len(areas), len(tiers), len(corpora)))
    print("problems: %d" % len(problems))
    for p in problems:
        print("  ", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
