# Phase 3: Listener Experience — episode surface pulled from Substack RSS - Context

**Gathered:** 2026-10-13
**Status:** Ready for planning

<domain>
## Phase Boundary

This pass delivers **EPS-02: per-episode permalink pages** on rewired.show — one real, indexable Hugo page per Rewired episode, built at `hugo` build time from the already-vendored `assets/episodes.xml` feed.

**Already satisfied by existing code (found during codebase scout, not previously reflected in STATE.md/ROADMAP.md):**
- **EPS-01** (episode list surface) — `layouts/partials/sections/episodes.html` already renders a homepage grid of all episodes parsed from `assets/episodes.xml`, cover art, date, summary, embedded native `<audio>` player.
- **EPS-03** (RSS pull at build time) — `scripts/refresh-episodes.sh` already vendors the podcast RSS into `assets/episodes.xml` (Substack 403s GitHub Actions IPs on live fetch, so this is vendor-and-commit, not live fetch).
- **EPS-04** (embedded audio player) — the homepage grid already embeds a native `<audio>` element per episode from the feed's `<enclosure>`.

**Not in this pass (deferred, not requested):**
- **EPS-05** (latest-episode callout on the landing page) — not asked for; the homepage grid already surfaces all episodes, newest-first.

**Why this is the real SEO lever:** rewired.show currently has exactly one indexable URL (the homepage) for the whole show — every episode "page" is actually an outbound link to its Substack post. Per-episode local pages turn 17 episodes into 17 indexable, shareable URLs with their own title/description/OG image.

</domain>

<decisions>
## Implementation Decisions

User deferred all three gray areas to Claude's judgment ("None — you decide").

### Content depth (SEO vs. duplication)
- **D-01:** Full show notes (chapters, "lines that landed," referenced material — already present in the feed's `<description>`) render on the per-episode page, not a thin teaser. — **Reversibility:** reversible — purely a template-rendering choice, no data model implication.
- **D-02:** Each per-episode page sets its own `canonical` URL to itself (not to the Substack post). Duplicate content across two domains is not disqualifying for either URL individually, and the whole point of this phase is giving Google a rewired.show-branded entity to rank per episode. — **Reversibility:** reversible.

### Homepage linking (internal vs. external)
- **D-03:** Homepage episode cards (`episodes.html`) switch from linking out to the Substack post to linking to the new local per-episode page. The local page keeps a secondary "Listen on Substack ↗" external link/button (preserves the subscribe/comment funnel Substack provides). — **Reversibility:** reversible — a template change, not a data change.

### URL / slug scheme
- **D-04:** Per-episode URLs mirror Substack's own slug exactly, e.g. `/episode-004-animism-all-the-way-down/`. Rationale: trivial to generate (slug already present in the feed's `<link>`), predictable, and keeps any future cross-linking between Substack and rewired.show 1:1. — **Reversibility:** costly — changing the slug scheme later breaks any inbound links/backlinks accumulated against the old URLs; would need redirects.

### Claude's Discretion
- Exact Hugo mechanism for generating one page per feed item without hand-authored content files: resolved as a technical implementation detail (build-time generation keyed off `assets/episodes.xml`, consistent with the existing vendor-and-commit pattern), not a user-facing gray area.
- OG/meta tags (title, description, image) per episode page: derived from feed title / truncated description / the episode's own `<itunes:image>` (parallel to what `episodes.html` already extracts) — reusing the existing field-extraction patterns from `episodes.html` rather than re-deriving them.
- STATE.md currently says "Phase 2 complete... Next: Phase 3 once first episodes exist" with no mention of the already-built homepage episode grid — that work happened outside the formal GSD phase tracking at some point. Not corrected as part of this discussion; the planner/executor should just build on what's there. Worth a STATE.md cleanup pass separately if it bothers future-Matt.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Roadmap / requirements
- `.planning/ROADMAP.md` Phase 3 section — goal, requirements EPS-01..05, explicit out-of-scope list (search/filter, transcripts, comments, paid/gated content)
- `.planning/REQUIREMENTS.md` v2 Requirements → Episodes — note this is a shorter/staler list (EPS-01..03 only) than ROADMAP.md's EPS-01..05; ROADMAP.md is authoritative for this phase
- `.planning/PROJECT.md` — "Out of Scope" table still lists "Episode list / audio player" and "RSS / podcast feed integration" as out of scope; both are now built. Stale, not corrected here — planner should treat ROADMAP.md Phase 3 as current truth over PROJECT.md's original MVP framing.

### Existing implementation (the real spec for this phase)
- `layouts/partials/sections/episodes.html` — the canonical reference implementation for: parsing `assets/episodes.xml`, episode-number-based sort (title-parsed, handles the octal zero-pad gotcha), per-item field extraction (title, link, enclosure/audio, itunes:image/cover, pubDate, description), UTM-tagged outbound links. New per-episode page generation should reuse this extraction logic rather than reinventing it.
- `scripts/refresh-episodes.sh` — how `assets/episodes.xml` gets refreshed (vendor-and-commit; Substack blocks CI fetch). No changes needed for this phase, but the planner should know new episodes require re-running this script before new pages appear.
- `layouts/_default/baseof.html` — current OG/Twitter/canonical meta is homepage-only (hardcoded `site.Title` / `site.Params.tagline` / one static OG image). Per-episode pages need this made page-aware (`.IsHome` branch or per-page front-matter-driven meta) — this is the direct blocker for per-episode pages actually working as shareable/indexable SEO assets, not just a nice-to-have.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `episodes.html`'s XML-parsing + sort + field-extraction block (lines ~22-60) is directly reusable for generating per-episode pages — same feed, same fields, same octal-zero-pad fix for episode numbers.
- `scripts/compose-og.py` (Pillow + fontTools OG image pipeline, mentioned in STATE.md) — may be relevant if per-episode pages want a generated OG image distinct from the episode's own cover art; not required (episode's own `<itunes:image>` / cover art is a perfectly good og:image), but exists if wanted.

### Established Patterns
- Vendor-and-commit for any Substack-sourced data (never live-fetch at build time — Substack 403s CI).
- ARCÆON palette tokens via `site.Params.colors`, warm-core subset — the per-episode page should look like a sibling of the homepage, not a bolt-on.
- UTM tagging convention (`utm_source=rewired.show&utm_medium=website&utm_campaign=...`) on every outbound link to Substack — the new "Listen on Substack ↗" link on each episode page should follow this same convention (new campaign value, e.g. `episode-page`).

### Integration Points
- New per-episode pages are generated from the same `assets/episodes.xml` resource `episodes.html` already reads — single source of truth, no new data plumbing needed.
- `episodes.html` itself needs a small edit: card link target changes from the Substack `$trackedLink` to the new local page's permalink (D-03).
- `baseof.html` needs per-page meta support (title/description/OG image) to make the new pages actually useful for sharing/indexing — without this, the pages exist but still look like the homepage when shared.

</code_context>

<specifics>
## Specific Ideas

No specific visual/copy requirements raised beyond the three decisions above — user deferred to implementation judgment. Keep the existing homepage grid card visual language (cover image, date, title, summary, audio player) consistent on the per-episode page itself, just with full show notes added below.

</specifics>

<deferred>
## Deferred Ideas

- **EPS-05** (latest-episode callout on the landing page) — in ROADMAP.md's Phase 3 scope but not requested in this pass. Future work, same phase.
- STATE.md / PROJECT.md "Out of Scope" cleanup to reflect that episode list + RSS pull + audio player are already live — noted, not actioned.
- `scripts/compose-og.py`-generated custom OG images per episode (vs. reusing existing cover art) — not requested; existing cover art is sufficient.

### Reviewed Todos (not folded)
None — discussion stayed within phase scope.

</deferred>

---

*Phase: 3-listener-experience-episode-surface-pulled-from-substack-rss*
*Context gathered: 2026-10-13*
