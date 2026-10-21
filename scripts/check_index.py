"""Check that the committed resource index is internally consistent.

The index is generated from the survey's private source, so CI cannot rebuild
it: the source is not in the repository. What CI can check is that the
committed output still agrees with itself, which catches the common failure
modes -- a hand-edited page, a cluster that lost a member, a count that no
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
COUNT = re.compile(r"\*\*(\d+) references\*\* list here; (\d+) are filed primarily")


def main() -> int:
    problems = []
    data = json.loads((RES / "papers.json").read_text(encoding="utf-8"))
    papers = data["papers"]
    clusters = data["clusters"]

    def fail(msg: str) -> None:
        problems.append(msg)

    if not papers:
        fail("papers.json contains no papers")

    # Every reference needs a way to be opened, and a reason to be opened.
    for p in papers:
        if not (p["doi"] or p["arxiv"] or p["url"]):
            fail("no link: %s (%s)" % (p["key"], p["title"]))
        if not p.get("note"):
            fail("no note: %s (%s)" % (p["key"], p["title"]))
        if p["primary_cluster"] not in clusters:
            fail("unknown cluster %r: %s" % (p["primary_cluster"], p["key"]))
        for c in p["clusters"]:
            if c not in clusters:
                fail("unknown cluster %r in clusters: %s" % (c, p["key"]))
        if not p["clusters"]:
            fail("no cluster: %s (%s)" % (p["key"], p["title"]))

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

    # One page per question, whose stated counts match its own table.
    for key, info in clusters.items():
        page = RES / "by-question" / ("%s.md" % key)
        if not page.exists():
            fail("missing page: resources/by-question/%s.md" % key)
            continue
        text = page.read_text(encoding="utf-8")
        m = COUNT.search(text)
        if not m:
            fail("no count line: %s" % page.name)
            continue
        stated_total, stated_primary = int(m.group(1)), int(m.group(2))
        rows = ROW.findall(text)
        members = [p for p in papers if key in p["clusters"]]
        primary = [p for p in papers if p["primary_cluster"] == key]
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
        if info["question"] not in text.splitlines()[0]:
            fail("%s heading does not match the question: %s"
                 % (page.name, info["question"]))

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

    print("papers: %d | clusters: %d | corpora: %d"
          % (len(papers), len(clusters), len(corpora)))
    print("problems: %d" % len(problems))
    for p in problems:
        print("  ", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
