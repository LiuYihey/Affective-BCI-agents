"""Render a Markdown page the way GitHub does, into a local HTML preview.

GitHub's own renderer is not available offline, so this approximates it: the
Markdown is converted with tables, fenced code, and raw HTML enabled, then
wrapped in a stylesheet close to GitHub's light theme. The point is to see
whether the layout holds -- figure widths, table columns, the shape of the
"Start here" grid -- before pushing.

Not part of the repository's checks; a local drafting aid. It needs one
package that the checks do not:

    pip install markdown
    python scripts/preview_readme.py                  # README.md
    python scripts/preview_readme.py resources/by-area/evaluation.md
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent

CSS = """
body { margin: 0; background: #f6f8fa; font-family: -apple-system, "Segoe UI",
       Helvetica, Arial, sans-serif; color: #1f2328; }
.page { max-width: 1012px; margin: 0 auto; padding: 32px 40px 80px; }
.markdown-body { font-size: 16px; line-height: 1.5; word-wrap: break-word; }
.markdown-body h1, .markdown-body h2 { border-bottom: 1px solid #d1d9e0;
    padding-bottom: .3em; margin-top: 24px; }
.markdown-body h1 { font-size: 2em; } .markdown-body h2 { font-size: 1.5em; }
.markdown-body table { border-collapse: collapse; margin: 16px 0; display: block;
    width: max-content; max-width: 100%; overflow: auto; }
.markdown-body table th, .markdown-body table td { border: 1px solid #d1d9e0;
    padding: 6px 13px; }
.markdown-body table th { background: #f6f8fa; font-weight: 600; }
.markdown-body table tr:nth-child(2n) { background: #f6f8fa; }
.markdown-body img { max-width: 100%; box-sizing: content-box;
    background: #fff; }
.markdown-body hr { height: .25em; background: #d1d9e0; border: 0; margin: 24px 0; }
.markdown-body blockquote { border-left: .25em solid #d1d9e0; color: #59636e;
    padding: 0 1em; margin: 0 0 16px 0; }
.markdown-body code { background: #eff1f3; padding: .2em .4em;
    border-radius: 6px; font-size: 85%; }
.markdown-body pre { background: #f6f8fa; padding: 16px; border-radius: 6px;
    overflow: auto; }
.markdown-body pre code { background: none; padding: 0; }
.markdown-body a { color: #0969da; text-decoration: none; }
.markdown-body p[align="center"] { margin: 8px 0 16px; }
.markdown-body p[align="center"] sub { color: #59636e; font-size: 12px;
    line-height: 1.4; }
"""


CENTRED_BLOCK = re.compile(
    r'<div align="center">(?P<body>.*?)</div>', re.S)
CELL = re.compile(r'(<td[^>]*>)(?P<body>.*?)(</td>)', re.S)
IMG_SRC = re.compile(r'(<img[^>]*\ssrc=")([^"]+)(")')


def render_block(match: re.Match) -> str:
    """Render the Markdown inside a centred block, as GitHub does."""
    inner = markdown.markdown(match.group("body"),
                              extensions=["tables", "fenced_code"],
                              output_format="html5")
    return '<div align="center">%s</div>' % inner


def render_cell(match: re.Match) -> str:
    """Render the Markdown inside a table cell, as GitHub does."""
    inner = markdown.markdown(match.group("body"),
                              extensions=["tables", "fenced_code"],
                              output_format="html5")
    return "%s%s%s" % (match.group(1), inner, match.group(3))


def build(source: str) -> str:
    path = (ROOT / source).resolve()
    text = path.read_text(encoding="utf-8")
    # GitHub parses Markdown inside raw HTML blocks and inside table cells;
    # the library does not, so those are rendered separately and put back.
    text = CENTRED_BLOCK.sub(render_block, text)
    text = CELL.sub(render_cell, text)
    body = markdown.markdown(
        text, extensions=["tables", "fenced_code"], output_format="html5")
    # The preview always lives at the repository root, so a page's own
    # relative image paths have to be rewritten to point at the same files.
    prefix = os.path.relpath(path.parent, ROOT).replace(os.sep, "/")
    if prefix == ".":
        prefix = ""
    else:
        prefix += "/"

    def fix_src(match: re.Match) -> str:
        src = match.group(2)
        if src.startswith(("http://", "https://", "/")):
            return match.group(0)
        return "%s%s%s" % (match.group(1), prefix + src, match.group(3))

    body = IMG_SRC.sub(fix_src, body)
    return ("<!doctype html><html><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            "<title>Affective BCI Agents</title><style>%s</style></head>"
            "<body><div class='page'><article class='markdown-body'>%s"
            "</article></div></body></html>" % (CSS, body))


def main() -> None:
    source = sys.argv[1] if len(sys.argv) > 1 else "README.md"
    name = Path(source).stem
    out = ROOT / ("_preview.html" if source == "README.md"
                  else "_preview_%s.html" % name)
    out.write_text(build(source), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
