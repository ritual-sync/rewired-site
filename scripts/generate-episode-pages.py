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

Show notes (the <description> HTML) come out of Substack as a flat run of
sibling <p> tags — including hand-typed "* " bullets and bare one-line
section headers ("In this episode", "Lines that landed", "Referenced",
"What we left unresolved", "Chapters") rather than real <ul>/<h2> markup.
`transform_notes_html()` below turns that into actual lists and headings,
and turns "Chapters" timestamp lines into links that jump to that moment
on the episode's YouTube video (data/youtube-episode-ids.json), when one
exists for the episode. The result is stored as a raw-HTML frontmatter
param (`notesHTML`) and rendered with `safeHTML` in
layouts/episodes/single.html, rather than passed through Hugo's
Markdown/Goldmark pipeline — it's HTML, not Markdown, and this avoids
touching the project's default (safe, no raw-HTML-passthrough) Goldmark
config.

Usage: python3 scripts/generate-episode-pages.py [--dry-run]
"""
from __future__ import annotations

import json
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
YOUTUBE_IDS_PATH = REPO_ROOT / "data" / "youtube-episode-ids.json"
PLATFORM_LINKS_PATH = REPO_ROOT / "data" / "platform-episode-links.json"
COVERS_DIR = REPO_ROOT / "assets" / "images" / "episodes"

ITUNES_NS = "http://www.itunes.com/dtds/podcast-1.0.dtd"
NS = {"itunes": ITUNES_NS}

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")
PARAGRAPH_RE = re.compile(r"<p[^>]*>(.*?)</p>", re.S)
CHAPTER_RE = re.compile(r"^(\d{1,3}(?::\d{2}){1,2})\s+—\s+(.+)$")

# The fixed, small vocabulary of bare-paragraph section headers Substack's
# show-note template uses. Matched on exact plain-text content — anything
# outside this set stays a normal paragraph, never misfires into a heading.
NOTE_HEADERS = {
    "In this episode",
    "Lines that landed",
    "Referenced",
    "What we left unresolved",
    "Chapters",
}

# Trailing Substack-specific boilerplate ("This is a public episode...")
# that sits outside any <p> tag after the last real paragraph — dropped
# entirely since rewired.show already has its own "Listen on Substack" link.
TRAILING_BOILERPLATE_RE = re.compile(r"This is a public episode\..*$", re.S)


def load_youtube_ids() -> dict[str, str]:
    if not YOUTUBE_IDS_PATH.exists():
        return {}
    data = json.loads(YOUTUBE_IDS_PATH.read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if not k.startswith("_")}


def load_platform_links() -> dict[str, dict[str, str]]:
    # scripts/fetch-platform-links.mts writes this — Apple Podcasts (public
    # lookup API) + Spotify (Web API) per-episode deep links, keyed by slug.
    if not PLATFORM_LINKS_PATH.exists():
        return {}
    return json.loads(PLATFORM_LINKS_PATH.read_text(encoding="utf-8"))


def parse_timestamp(ts: str) -> int:
    parts = [int(p) for p in ts.split(":")]
    seconds = 0
    for p in parts:
        seconds = seconds * 60 + p
    return seconds


def transform_notes_html(html: str, youtube_id: str | None) -> str:
    html = TRAILING_BOILERPLATE_RE.sub("", html)
    paragraphs = PARAGRAPH_RE.findall(html)

    out: list[str] = []
    in_chapters = False
    i = 0
    while i < len(paragraphs):
        raw = paragraphs[i].strip()
        plain = unescape(TAG_RE.sub("", raw)).strip()

        # Drop the show-level "Listen: Spotify · Apple Podcasts" paragraph —
        # superseded by the real per-episode platform links rendered above
        # the notes (episode-detail.html), which point at this exact
        # episode, not just the show.
        if plain.startswith("Listen:"):
            i += 1
            continue

        if plain in NOTE_HEADERS:
            out.append(f"<h2>{plain}</h2>")
            in_chapters = plain == "Chapters"
            i += 1
            continue

        if raw.startswith("* "):
            items = []
            while i < len(paragraphs) and paragraphs[i].strip().startswith("* "):
                items.append(paragraphs[i].strip()[2:].strip())
                i += 1
            out.append("<ul>" + "".join(f"<li>{it}</li>" for it in items) + "</ul>")
            continue

        if in_chapters:
            items = []
            while i < len(paragraphs):
                m = CHAPTER_RE.match(paragraphs[i].strip())
                if not m:
                    break
                ts, label = m.group(1), m.group(2)
                if youtube_id:
                    seconds = parse_timestamp(ts)
                    link = f"https://youtu.be/{youtube_id}?t={seconds}"
                    items.append(f'<li><a href="{link}" target="_blank" rel="noopener noreferrer">{ts}</a> — {label}</li>')
                else:
                    items.append(f"<li>{ts} — {label}</li>")
                i += 1
            in_chapters = False
            if items:
                out.append("<ol>" + "".join(items) + "</ol>")
                continue

        out.append(f"<p>{raw}</p>")
        i += 1

    return "".join(out)


def plainify(html: str, limit: int = 180) -> str:
    text = unescape(TAG_RE.sub(" ", html or ""))
    text = WS_RE.sub(" ", text).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",;:.-—")


def short_title(title: str) -> str:
    # "Episode N: Hook — Keyword A, Keyword B & Keyword C" -> "Episode N: Hook".
    # Mirrors the search_engine_title / title split already applied on the
    # Substack side (publishing-pipeline/scripts/substack/update-search-engine-titles.mts)
    # — derived here, not hand-maintained, so it can never drift from the title.
    return title.split(" — ", 1)[0].strip()


def iso8601_duration(seconds: int | None) -> str | None:
    if not seconds:
        return None
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    parts = "PT"
    if h:
        parts += f"{h}H"
    if m:
        parts += f"{m}M"
    if s or not (h or m):
        parts += f"{s}S"
    return parts


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


def parse_item(item: ET.Element, youtube_ids: dict[str, str], platform_links: dict[str, dict[str, str]]) -> dict | None:
    title = (item.findtext("title") or "").strip()
    link = (item.findtext("link") or "").strip()
    if not link:
        return None
    slug = slug_from_link(link)
    youtube_id = youtube_ids.get(slug)
    links = platform_links.get(slug, {})

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

    duration_seconds = int(itunes_duration) if (itunes_duration or "").isdigit() else None

    return {
        "title": title,
        "shortTitle": short_title(title),
        "slug": slug,
        "substackURL": link,
        "youtubeId": youtube_id,
        "youtubeURL": f"https://youtu.be/{youtube_id}" if youtube_id else None,
        "appleURL": links.get("appleURL"),
        "spotifyURL": links.get("spotifyURL"),
        "episodeNumber": episode_number(title, itunes_episode),
        "episodeType": itunes_episode_type or "full",
        "date": dt.isoformat(),
        "cover": cover,
        # Local, Hugo-resizable asset (scripts/fetch-episode-covers.py) —
        # templates prefer this and fall back to the remote `cover` URL
        # (full-res, un-resized) only when it hasn't been fetched yet.
        "coverLocal": f"images/episodes/{slug}.jpg" if (COVERS_DIR / f"{slug}.jpg").exists() else None,
        "audio": audio_url,
        "audioType": audio_type,
        "durationSeconds": duration_seconds,
        "durationISO": iso8601_duration(duration_seconds),
        "explicit": (itunes_explicit or "").strip().lower() == "yes",
        "summary": plainify(description, 155),
        "notesHTML": transform_notes_html(description, youtube_id),
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

    youtube_ids = load_youtube_ids()
    platform_links = load_platform_links()

    written: list[Path] = []
    skipped = 0
    for item in items:
        ep = parse_item(item, youtube_ids, platform_links)
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
