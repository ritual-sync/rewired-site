#!/usr/bin/env python3
"""Vendor each episode's cover art locally so Hugo can resize it at build time.

The itunes:image URLs in assets/episodes.xml are Substack-hosted originals —
3000x3000, ~300KB each — but every placement on rewired.show displays them
at 384-640px. Hotlinking the original means a multi-hundred-KB download for
a quarter- or sixth-resolution slot, directly hurting LCP/page weight.

Substack's CDN does not support on-the-fly resizing for these podcast-feed
image paths (tested: the Cloudinary-style /image/fetch/w_640,.../ wrapper
404s on them) — so there is no free lunch here. This script downloads each
original ONCE into assets/images/episodes/<slug>.jpg (Hugo's asset
pipeline, not static/ — static/ files are copied verbatim with zero
processing; assets/ files can be `resources.Get` + `.Resize`'d at Hugo
build time, entirely locally, no network needed at build time). Same
vendor-and-commit shape as refresh-episodes.sh: run this from a non-blocked
IP, commit the result, Hugo does the rest at build time off the committed
originals.

Reads assets/episodes.xml directly (same source generate-episode-pages.py
reads), NOT content/episodes/*.md — so this can run before or after that
script in refresh-episodes.sh with no ordering dependency. (An earlier
version read the generated .md files, which meant a brand-new episode's
cover wouldn't be vendored until the SECOND refresh run — fixed by going
straight to the feed, the actual source of truth both scripts share.)

Skips a slug whose local file already exists (covers don't change after
publish) unless --force is passed.

Usage: python3 scripts/fetch-episode-covers.py [--force]
"""
from __future__ import annotations

import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FEED_PATH = REPO_ROOT / "assets" / "episodes.xml"
OUT_DIR = REPO_ROOT / "assets" / "images" / "episodes"

ITUNES_NS = "http://www.itunes.com/dtds/podcast-1.0.dtd"
NS = {"itunes": ITUNES_NS}
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"


def slug_from_link(link: str) -> str:
    return link.rstrip("/").rsplit("/", 1)[-1]


def main() -> int:
    force = "--force" in sys.argv

    if not FEED_PATH.exists():
        print(f"ERROR: {FEED_PATH} not found — run scripts/refresh-episodes.sh first", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    tree = ET.parse(FEED_PATH)
    items = tree.getroot().findall(".//item")

    fetched = 0
    skipped = 0
    failed = 0

    for item in items:
        link = (item.findtext("link") or "").strip()
        if not link:
            continue
        slug = slug_from_link(link)

        itunes_image = item.find("itunes:image", NS)
        cover_url = itunes_image.get("href") if itunes_image is not None else None
        if not cover_url:
            print(f"{slug}: no itunes:image, skipping")
            continue

        out_path = OUT_DIR / f"{slug}.jpg"
        if out_path.exists() and not force:
            skipped += 1
            continue

        try:
            req = urllib.request.Request(cover_url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            out_path.write_bytes(data)
            print(f"{slug}: fetched {len(data):,} bytes -> {out_path.relative_to(REPO_ROOT)}")
            fetched += 1
        except Exception as e:
            print(f"{slug}: FAILED — {e}", file=sys.stderr)
            failed += 1

    print(f"\n{fetched} fetched, {skipped} already present, {failed} failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
