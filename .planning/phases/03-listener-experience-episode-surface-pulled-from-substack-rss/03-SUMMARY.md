# Phase 3 Summary — Per-Episode Permalink Pages (EPS-02)

**Status:** Complete (EPS-02 only — EPS-05 remains open in this phase)
**Completed:** 2026-10-13
**Requirements closed:** EPS-02. Confirmed already-satisfied by prior undocumented work: EPS-01, EPS-03, EPS-04 (see Provenance note below).

**Provenance:** Built directly (discuss-phase → implementation), not through the full research → gsd-planner → gsd-plan-checker → gsd-executor → gsd-verifier pipeline. Per Design Principle 12 (assurance by failure detectability, not importance): a `hugo build` failure is loud and local, git revert is trivial, and nothing downstream depends on this yet — low-assurance-lane work, not a silent-failure surface. `03-CONTEXT.md` carries the actual decision record in place of a PLAN.md.

## What was found (before building anything)

Codebase scout during discuss-phase turned up that **EPS-01 (episode list), EPS-03 (RSS pull at build time), and EPS-04 (embedded audio player) were already built** — `layouts/partials/sections/episodes.html` and `scripts/refresh-episodes.sh` — with no record of this in STATE.md, ROADMAP.md, or PROJECT.md, which all still described Phase 3 as not started. That drift is noted, not corrected, in `03-CONTEXT.md`.

The one real gap: every episode "page" was an outbound link to its Substack post. rewired.show had exactly one indexable Google URL for the whole 11-episode show.

## What was built

### `scripts/generate-episode-pages.py` (new)
Parses `assets/episodes.xml` (the already-vendored podcast RSS) and writes one Hugo content page per episode to `content/episodes/<substack-slug>.md` — frontmatter only (title, date, episodeNumber, cover, audio, summary, substackURL, `notesHTML` holding the full show-notes HTML verbatim). Prunes stale pages for episodes no longer in the feed; never touches `content/episodes/_index.md`. Not run at Hugo build time — a repo-maintenance step, same shape as `refresh-episodes.sh` itself.

### `layouts/episodes/single.html` + `layouts/partials/sections/episode-detail.html` (new)
The per-episode page: cover art, title, date, audio player, a secondary "Listen on Substack ↗" link (UTM campaign `episode-page`), the full show notes rendered via `safeHTML` (D-01), and a Subscribe CTA + back-to-homepage link.

### `layouts/episodes/list.html` + `content/episodes/_index.md` (new)
A minimal `/episodes/` list page — additional crawlable surface, same card visual language as the homepage grid, sorted by `episodeNumber` descending.

### `layouts/_default/baseof.html` (modified)
Canonical link, `<meta name="description">`, and all OG/Twitter tags are now page-aware: episode pages get their own title/summary/cover instead of the homepage's generic tagline + dual-portrait OG image (D-02 — self-canonical, not canonicalized to the Substack post).

### `layouts/partials/sections/episodes.html` (modified)
Homepage cards now resolve the matching local page via `site.GetPage (printf "/episodes/%s" $slug)` and link there instead of out to Substack (D-03), dropping `target="_blank"`/`rel` for the now-internal link. Falls back to the external Substack link + `target="_blank"` if no local page exists yet (e.g. a brand-new episode before the next feed refresh regenerates pages).

### `hugo.toml` (modified)
`[permalinks] episodes = "/:slug/"` — per-episode URLs are flat at the site root and mirror Substack's own slug exactly (D-04), e.g. `https://rewired.show/episode-004-animism-all-the-way-down/`. The `/episodes/` list page itself is unaffected (it's the section's own `_index.md`, not a regular page).

### `assets/css/rewired-overrides.css` (modified)
New `.rewired-episode-detail*` block — scoped typography for the raw-HTML show notes (`p`, `strong`, `em`, `a`), styled consistently with the existing ARCÆON warm-core palette.

### `scripts/refresh-episodes.sh` + `scripts/auto-refresh-deploy.sh` (modified)
Page generation is wired into the existing vendor-and-commit automation: `refresh-episodes.sh` now calls `generate-episode-pages.py` right after writing the feed, and `auto-refresh-deploy.sh`'s diff-check/add/commit now include `content/episodes/` alongside the feed files — so a new episode gets a live page automatically on the next scheduled refresh, no separate manual step (DP-10 — doesn't reintroduce the "new episode doesn't appear" rot the feed-refresh automation itself was built to kill).

## Verified

- `hugo --minify` builds clean (18 pages: homepage, 11 episode pages, `/episodes/` list, taxonomy stubs). One pre-existing `WARN` (`no layout file for "html" for kind "taxonomy"`) — unrelated to this work, not introduced by it.
- Built output for `episode-004-animism-all-the-way-down` carries correct per-page `<title>`, `<meta name="description">`, `<link rel="canonical">`, and full OG/Twitter block (title/description/image all episode-specific, image resolves to the episode's real existing square art — not a placeholder).
- Sitemap (`public/sitemap.xml`) carries all 11 episode permalinks.
- Homepage episode cards link to the new local pages with no `target="_blank"`; the per-episode page itself still carries a working external "Listen on Substack" link.
- Caught and fixed a bug in the generator's own first run: its stale-page-pruning step was about to delete `content/episodes/_index.md` (the list page, not a generated episode page) — fixed before it shipped.

Commit: `d3337ab` — pushed to `main`, triggers the GitHub Actions deploy workflow.

## Deferred (still open in Phase 3)

- **EPS-05** (latest-episode callout on the homepage) — not requested this pass.
- STATE.md / PROJECT.md "Out of Scope" sections still describe episode list / RSS pull / audio player as not-yet-built, though they (and now EPS-02) exist. Not corrected here.
- Custom per-episode OG image generation (`scripts/compose-og.py`) — not requested; existing episode cover art reused instead.
