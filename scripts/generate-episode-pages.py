#!/usr/bin/env python3
"""Generate one Hugo content page per Rewired episode from the vendored feed.

Reads assets/episodes.xml (the vendored podcast RSS feed — see
refresh-episodes.sh and layouts/partials/sections/episodes.html for why it's
vendored instead of fetched at build time) and writes one frontmatter-only
.md file per episode into content/episodes/, keyed by the episode's own
Substack slug (CONTEXT.md D-04 — URLs mirror Substack's slug exactly).

This is NOT run at Hugo build time. It's a repo-maintenance step, same shape
as refresh-episodes.sh itself: run it, commit the result, push, Hugo renders
the committed content pages natively (permalinks, sitemap, canonical meta —
all free from Hugo's normal content pipeline, no custom page-generation
plumbing needed in templates).

Show notes (the <description> HTML) are stored as a raw-HTML frontmatter
param (`notesHTML`) and rendered with `safeHTML` in layouts/episodes/single.html,
rather than passed through Hugo's Markdown/Goldmark pipeline — it's already
HTML from Substack, not Markdown, and this avoids touching the project's
default (safe, no raw-HTML-passthrough) Goldmark config.

Usage: python3 scripts/generate-episode-pages.py [--dry-run]
"""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
FEED_PATH = REPO_ROOT / "assets" / "episodes.xml"
OUT_DIR = REPO_ROOT / "content" / "episodes"

ITUNES_NS = "http://www.itunes.com/dtds/podcast-1.0.dtd"
NS = {"itunes": ITUNES_NS}

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def plainify(html: str, limit: int = 180) -> str:
    text = unescape(TAG_RE.sub(" ", html or ""))
    text = WS_RE.sub(" ", text).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",;:.-—")


def episode_number(title: str, itunes_episode: str | None) -> int:
    if itunes_episode:
        try:
            return int(itunes_episode)
        except ValueError:
            pass
    m = re.search(r"[0-9]+", title or "")
    if not m:
        return 0
    return int(m.group(0).lstrip("0") or "0")


def slug_from_link(link: str) -> str:
    # Substack post links are https://rewiredshow.substack.com/p/<slug> —
    # the slug is the thing CONTEXT.md D-04 says to mirror exactly.
    return link.rstrip("/").rsplit("/", 1)[-1]


def parse_item(item: ET.Element) -> dict | None:
    title = (item.findtext("title") or "").strip()
    link = (item.findtext("link") or "").strip()
    if not link:
        return None
    slug = slug_from_link(link)

    description = item.findtext("description") or ""

    enclosure = item.find("enclosure")
    audio_url = enclosure.get("url") if enclosure is not None else None
    audio_type = enclosure.get("type") if enclosure is not None else None

    itunes_image = item.find("itunes:image", NS)
    cover = itunes_image.get("href") if itunes_image is not None else None

    itunes_episode = item.findtext("itunes:episode", namespaces=NS)
    itunes_episode_type = item.findtext("itunes:episodeType", namespaces=NS)
    itunes_duration = item.findtext("itunes:duration", namespaces=NS)
    itunes_explicit = item.findtext("itunes:explicit", namespaces=NS)

    pub_date_raw = item.findtext("pubDate")
    if pub_date_raw:
        try:
            dt = parsedate_to_datetime(pub_date_raw)
        except (TypeError, ValueError):
            dt = datetime.now(timezone.utc)
    else:
        dt = datetime.now(timezone.utc)

    return {
        "title": title,
        "slug": slug,
        "substackURL": link,
        "episodeNumber": episode_number(title, itunes_episode),
        "episodeType": itunes_episode_type or "full",
        "date": dt.isoformat(),
        "cover": cover,
        "audio": audio_url,
        "audioType": audio_type,
        "durationSeconds": int(itunes_duration) if (itunes_duration or "").isdigit() else None,
        "explicit": (itunes_explicit or "").strip().lower() == "yes",
        "summary": plainify(description, 180),
        "notesHTML": description,
    }


def write_page(ep: dict, dry_run: bool) -> Path:
    front = {k: v for k, v in ep.items() if k != "notesHTML"}
    # yaml.safe_dump renders a literal block scalar for strings containing
    # newlines reasonably, but the raw HTML has none here (Substack ships it
    # as one unbroken string) — dump as a plain (possibly very long) scalar.
    front["notesHTML"] = ep["notesHTML"]

    frontmatter = yaml.safe_dump(front, default_flow_style=False, allow_unicode=True, sort_keys=False, width=100000)
    content = f"---\n{frontmatter}---\n"

    out_path = OUT_DIR / f"{ep['slug']}.md"
    if dry_run:
        print(f"[dry-run] would write {out_path.relative_to(REPO_ROOT)} ({len(content)} bytes)")
    else:
        out_path.write_text(content, encoding="utf-8")
        print(f"wrote {out_path.relative_to(REPO_ROOT)}")
    return out_path


def main() -> int:
    dry_run = "--dry-run" in sys.argv

    if not FEED_PATH.exists():
        print(f"ERROR: {FEED_PATH} not found — run scripts/refresh-episodes.sh first", file=sys.stderr)
        return 1

    tree = ET.parse(FEED_PATH)
    items = tree.getroot().findall(".//item")
    if not items:
        print("ERROR: feed has 0 <item> entries — refusing to generate pages", file=sys.stderr)
        return 1

    if not dry_run:
        OUT_DIR.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    skipped = 0
    for item in items:
        ep = parse_item(item)
        if ep is None:
            skipped += 1
            continue
        written.append(write_page(ep, dry_run))

    # Prune stale pages for episodes no longer in the feed (shouldn't happen
    # in practice — Substack doesn't unpublish — but keeps the directory
    # honest rather than silently accumulating orphans).
    if not dry_run:
        current_slugs = {p.stem for p in written}
        for existing in OUT_DIR.glob("*.md"):
            if existing.name == "_index.md":
                continue  # the section's own list page, not a generated episode page
            if existing.stem not in current_slugs:
                print(f"removing stale page for missing episode: {existing.relative_to(REPO_ROOT)}")
                existing.unlink()

    print(f"\n{len(written)} page(s) generated, {skipped} item(s) skipped (no link).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
