"""Check that every link in the resource index still resolves.

A DOI is validated by content negotiation against the DOI registry rather than
by following the redirect to the publisher, because publishers block automated
requests and their certificates often fail verification. A 403 from a
publisher therefore means the link is fine, not broken.

Run after rebuilding the index, and in CI:

    python scripts/check_links.py
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIMEOUT = 25
UA = "Affective-BCI-agents link check (https://github.com/LiuYihey/Affective-BCI-agents)"

# Statuses that mean the link works but the server refused the automated
# request. The link is alive; the check cannot confirm it further.
ACCEPTED = {401, 403, 405, 429}

# A connection-level failure (DNS blip, reset socket, TLS hiccup) says nothing
# about whether the target exists, so it is always retried before giving up.
NETWORK_ERROR = 0

# github.com/<owner>/<repo> and its tree/blob variants.
GITHUB_REPO = re.compile(
    r"^https?://github\.com/([\w.\-]+)/([\w.\-]+?)(?:\.git)?(?:/(?:tree|blob)/.*)?/?$")

# The API reports a missing repository as a clean 404 and says whether the
# caller is being rate limited, which a plain page fetch cannot.
GITHUB_API = "https://api.github.com/repos/%s/%s"


def _get(url: str, headers: dict) -> tuple[int, str]:
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            r.read(1024)
            return r.status, ""
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return NETWORK_ERROR, type(e).__name__


def _fetch(url: str, headers: dict, attempts: int) -> tuple[int, str]:
    """GET with backoff. Only connection-level failures are retried."""
    status, err = NETWORK_ERROR, ""
    for attempt in range(attempts):
        status, err = _get(url, headers)
        if status != NETWORK_ERROR:
            return status, err
        if attempt < attempts - 1:
            time.sleep(4 * (attempt + 1))
    return status, err


def _registry(doi: str) -> tuple[str, str]:
    """Validate a DOI against the registry that actually holds it."""
    # Crossref indexes the publisher literature; arXiv mints its DOIs through
    # DataCite, so a Crossref miss is not evidence the DOI is gone.
    for api, label in (("https://api.crossref.org/works/", "crossref"),
                       ("https://api.datacite.org/dois/", "datacite")):
        status, err = _fetch(api + doi, {"User-Agent": UA}, 2)
        if status == 200:
            return ("ok", label)
        if status in ACCEPTED:
            return ("blocked", str(status))
    return ("dead", err or "not in registry")


def _github(url: str) -> tuple[str, str]:
    """Check a repository through the API, which distinguishes 404 from 429."""
    m = GITHUB_REPO.match(url)
    if not m:
        status, err = _fetch(url, {"User-Agent": UA}, 3)
        if status == 200:
            return ("ok", "")
        if status in ACCEPTED:
            return ("blocked", str(status))
        return ("dead", err or str(status))

    owner, repo = m.group(1), m.group(2)
    headers = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    status, err = _fetch(GITHUB_API % (owner, repo), headers, 4)
    if status == 200:
        return ("ok", "api")
    if status == 404:
        return ("dead", "404")
    if status in ACCEPTED:
        return ("blocked", str(status))
    return ("dead", err or str(status))


def resolve(url: str) -> tuple[str, str]:
    """Return (verdict, detail). Verdict is ok, blocked or dead."""
    if "doi.org/" in url:
        doi = url.split("doi.org/", 1)[1]
        status, _ = _fetch("https://doi.org/" + doi,
                           {"Accept": "application/vnd.citationstyles.csl+json",
                            "User-Agent": UA}, 3)
        if status == 200:
            return ("ok", "doi")
        if status in ACCEPTED:
            return ("blocked", str(status))
        # Redirect target unreachable: fall back to the registry API.
        return _registry(doi)

    if "github.com/" in url:
        return _github(url)

    status, err = _fetch(url, {"User-Agent": UA}, 3)
    if status == 200:
        return ("ok", "")
    if status in ACCEPTED:
        return ("blocked", str(status))
    return ("dead", err or str(status))


def main() -> int:
    data = json.loads((ROOT / "resources" / "papers.json").read_text(encoding="utf-8"))
    papers = data["papers"]

    dead = []
    blocked = []
    checked = 0
    for p in papers:
        for url in [p["doi"], p["arxiv"], p["url"], p["code"]]:
            if not url:
                continue
            checked += 1
            verdict, detail = resolve(url)
            if verdict == "dead":
                dead.append((p["key"], url, detail))
                print("DEAD   %-26s %-6s %s" % (p["key"], detail, url))
            elif verdict == "blocked":
                blocked.append((p["key"], url, detail))

    print("\nchecked %d links across %d papers" % (checked, len(papers)))
    print("confirmed dead: %d | alive but not machine-checkable: %d"
          % (len(dead), len(blocked)))
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
