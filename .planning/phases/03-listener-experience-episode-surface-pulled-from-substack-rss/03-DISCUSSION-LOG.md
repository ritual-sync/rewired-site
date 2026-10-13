# Phase 3: Listener Experience — episode surface pulled from Substack RSS - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-10-13
**Phase:** 3-listener-experience-episode-surface-pulled-from-substack-rss
**Areas discussed:** Content depth (SEO vs. duplication), Homepage linking (internal vs. external), URL / slug scheme

---

## Gray areas presented

| Option | Description | Selected |
|--------|-------------|----------|
| Content depth (SEO vs. duplication) | Full show notes on-page (stronger SEO, duplicates Substack post) vs. thin teaser | — |
| Homepage linking (internal vs. external) | Homepage cards link to new local pages vs. keep linking out to Substack | — |
| URL / slug scheme | Mirror Substack's exact slug vs. a site-native scheme | — |
| None — you decide | Defer all three to Claude's implementation judgment | ✓ |

**User's choice:** "None — you decide"
**Notes:** User chose to defer all three areas rather than discuss each individually. Claude resolved them directly in CONTEXT.md (D-01 through D-04).

---

## Claude's Discretion

All three presented gray areas were deferred to Claude:
- Full show notes rendered on-page, self-canonical (D-01, D-02)
- Homepage cards switch to internal links, Substack link kept as secondary action (D-03)
- URL slugs mirror Substack's own slug exactly (D-04)

Additionally, Claude resolved without presenting as a gray area (pure implementation detail, not vision-level):
- Mechanism for generating per-episode pages from `assets/episodes.xml` at build time without hand-authored content files per episode.
- Per-page OG/meta derivation (title/description/image) reusing `episodes.html`'s existing field-extraction logic.

## Deferred Ideas

- EPS-05 (latest-episode homepage callout) — in Phase 3's roadmap scope but not requested this pass.
- STATE.md / PROJECT.md "Out of Scope" sections are stale (still list episode list / RSS / audio player as not-yet-built, though they already exist in the codebase) — noted, not corrected.
- Custom per-episode OG image generation via `scripts/compose-og.py` — not requested; reusing existing episode cover art instead.
