#!/usr/bin/env python3
"""Vendor each episode's tarot card photo (and its caption) for the episode pages.

Every Rewired episode opens on a card, and the Substack post carries a photo of
it — but the podcast RSS feed (assets/episodes.xml) strips all images from
<description>, so the card never reached rewired.show. The photo lives only in
the post body, which Substack's public post API returns as body_html:

    GET https://rewiredshow.substack.com/api/v1/posts/<slug>  ->  body_html

The card is the post's captioned <figure> (publishing-pipeline's
add_card_image.py splices it in right after the opening paragraph). We take the
figure whose caption starts with "Card", else the first figure — ep1-3 predate
captions and have exactly one, uncaptioned.

The image is fetched through the figure's own substackcdn URL with
`Accept: image/jpeg`, NOT from the S3 original: since ep4 the originals are
HEIC (phone photos), which Hugo's image pipeline can't decode. The CDN URL is
signed, so its params can't be rewritten — the Accept header is what makes it
transcode to a 1456px-wide, orientation-corrected JPEG.

Writes:
  assets/images/cards/<slug>.jpg   Hugo-resizable at build time, like covers
  data/episode-cards.json          {slug: {"caption": ...}}

Same shape as fetch-episode-covers.py: reads slugs from the feed, skips a slug
whose image already exists unless --force. A caption already present in
data/episode-cards.json is NEVER overwritten — ep1-3's captions are
hand-entered there from the episode records, because their Substack figures
have none. Same residential-IP constraint as the feed: run from refresh-episodes.sh.

Usage: python3 scripts/fetch-episode-cards.py [--force]
"""
from __future__ import annotations

import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from html import unescape
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FEED_PATH = REPO_ROOT / "assets" / "episodes.xml"
OUT_DIR = REPO_ROOT / "assets" / "images" / "cards"
CAPTIONS_PATH = REPO_ROOT / "data" / "episode-cards.json"

POST_API = "https://rewiredshow.substack.com/api/v1/posts/{slug}"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"

FIGURE_RE = re.compile(r"<figure.*?</figure>", re.S)
IMG_SRC_RE = re.compile(r'<img[^>]+src="([^"]+)"')
CAPTION_RE = re.compile(r"<figcaption[^>]*>(.*?)</figcaption>", re.S)
TAG_RE = re.compile(r"<[^>]+>")


def slug_from_link(link: str) -> str:
    return link.rstrip("/").rsplit("/", 1)[-1]


def get(url: str, accept: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def card_figure(body_html: str) -> tuple[str, str | None] | None:
    """(image src, caption or None) for the card figure, or None if the post has none."""
    figures = []
    for fig in FIGURE_RE.findall(body_html):
        src = IMG_SRC_RE.search(fig)
        if not src:
            continue
        cap = CAPTION_RE.search(fig)
        caption = re.sub(r"\s+", " ", unescape(TAG_RE.sub("", cap.group(1)))).strip() if cap else None
        figures.append((unescape(src.group(1)), caption or None))
    for f in figures:
        if f[1] and f[1].lower().startswith("card"):
            return f
    return figures[0] if figures else None


def main() -> int:
    force = "--force" in sys.argv

    if not FEED_PATH.exists():
        print(f"ERROR: {FEED_PATH} not found — run scripts/refresh-episodes.sh first", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    captions: dict = json.loads(CAPTIONS_PATH.read_text(encoding="utf-8")) if CAPTIONS_PATH.exists() else {}

    fetched = skipped = failed = 0
    for item in ET.parse(FEED_PATH).getroot().findall(".//item"):
        link = (item.findtext("link") or "").strip()
        if not link:
            continue
        slug = slug_from_link(link)
        out_path = OUT_DIR / f"{slug}.jpg"
        if out_path.exists() and not force:
            skipped += 1
            continue

        try:
            post = json.loads(get(POST_API.format(slug=slug), "application/json"))
            fig = card_figure(post.get("body_html") or "")
            if not fig:
                print(f"{slug}: no figure in post body, skipping")
                continue
            src, caption = fig
            data = get(src, "image/jpeg")
            if not data.startswith(b"\xff\xd8"):
                raise ValueError(f"CDN did not return a JPEG ({data[:12]!r})")
            out_path.write_bytes(data)
            entry = captions.setdefault(slug, {})
            if caption and not entry.get("caption"):
                entry["caption"] = caption
            print(f"{slug}: fetched {len(data):,} bytes -> {out_path.relative_to(REPO_ROOT)}"
                  f"  caption: {entry.get('caption') or '(none)'}")
            fetched += 1
        except Exception as e:
            print(f"{slug}: FAILED — {e}", file=sys.stderr)
            failed += 1

    CAPTIONS_PATH.write_text(json.dumps(dict(sorted(captions.items())), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n{fetched} fetched, {skipped} already present, {failed} failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
