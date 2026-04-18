# Roadmap: Rewired Site

**Created:** 2026-04-18
**Target launch:** Live before first episode drops (aim late April / early May 2026)
**Phases:** 3 — Phases 1 & 2 are the Tight MVP (pre-launch); Phase 3 is the Listener Experience layer, triggered when first episodes exist.

---

## Phase 1: Build — Static site, content, portraits, palette

**Goal:** Visitor lands on a working static page with the show identity, lens, hosts, and portraits rendered correctly on mobile and desktop. No email capture yet. Not deployed yet.

**Requirements:** SITE-01, SITE-02, SITE-03, SITE-04, HERO-01, HERO-02, HERO-03, HERO-04, CONT-01, CONT-02, CONT-03

**UI hint:** yes

**Success criteria:**
1. Running the site locally shows the full one-page layout with all four sections in order: Hero → Lens → Hosts → Coming Soon placeholder.
2. Both host portraits render in the hero, pair visually as co-hosts of the same show, and can be swapped via a single-asset replacement with no template edits.
3. Palette matches the RitualSync warm-core subset on Void Purple base, with one Ion Glow cyan accent somewhere in the page — nothing from outside the ARCÆON family.
4. Mobile layout (≤ 480px width) is readable, portraits stack cleanly, no horizontal scroll.
5. The copy for HERO-02 (one-line lens) and CONT-01 ("The Lens" paragraph) is drafted in Matt's voice and reads as adult / literary, not AI-generic.

**Exit:** a static build output can be opened locally and the core value ("lens + hosts + launch signal") lands in under 5 seconds of attention.

**Plans:** 2 plans

Plans:
- [x] 01-01-PLAN.md — Scaffold Hugo project, vendor arcaeon theme, install portraits, establish palette and typography foundation (completed 2026-04-18)
- [x] 01-02-PLAN.md — Build Rewired homepage with Hero, Lens, Hosts, and Coming Soon sections wired to frontmatter copy with responsive CSS (completed 2026-04-18)

---

## Phase 2: Ship — Subscribe capture, deploy, shareable link

**Goal:** Site is publicly live at rewired.show with working email capture wired to the Rewired Substack publication (subscribers land there) and correct link previews when shared. Visitor can drop their email and become a Substack subscriber.

**Requirements:** CAPT-01, CAPT-02, CAPT-03, CAPT-04, DEPL-01, DEPL-02, DEPL-03, DEPL-04, DEPL-05

**Success criteria:**
1. A test email submitted from production appears as a subscriber on the Rewired Substack publication (not on any other Substack Matt owns).
2. Successful submission shows Substack's confirmation state inside the iframe without reloading or redirecting the host page.
3. The live URL returns HTTPS, loads in under 2 seconds on cellular, and renders correctly on iOS Safari, Chrome Android, Firefox desktop.
4. Sharing the URL in iMessage, Slack, and a Twitter/Threads-equivalent compose box produces a correct Open Graph preview with show name, tagline, and at least one host portrait.
5. Pushing to `main` triggers an automatic deploy; no manual steps in the deploy path.

**Exit:** a shareable URL that Matt can paste into a DM to Jaye Anne and to his existing network without cringe, and the first subscribers start landing on the Rewired Substack.

**Plans:** 2 plans

Plans:
- [x] 02-01-PLAN.md — Apply code-side Phase 2 changes: production baseURL, OG/Twitter/canonical meta, favicon set, v1 OG image, CNAME, Substack subscribe iframe wired into coming-soon partial (completed 2026-04-18)
- [x] 02-02-PLAN.md — Ship it live: GitHub Actions deploy workflow, create ritual-sync/rewired-site repo + push, DNS records at registrar, enforce HTTPS, end-to-end smoke test across subscribe flow + link preview on 3 surfaces (completed 2026-04-18)

---

## Phase 3: Listener Experience — episode surface pulled from Substack RSS (post-launch)

**Goal:** rewired.show carries a full listener/viewer experience for the show: episode list, per-episode pages with embedded audio players, show notes in the Card → Riff → Unresolved structure, latest-episode callout on the landing page. Substack remains the operational backbone (audio hosting, RSS feed, subscribers); Hugo renders the branded listener surface.

**Trigger:** first episodes exist on the Rewired Substack (≥ 1 published episode). Not before.

**Requirements (new, not yet in REQUIREMENTS.md):** EPS-01 episode list surface, EPS-02 per-episode permalink pages, EPS-03 RSS pull at build time, EPS-04 embedded audio player on episode pages, EPS-05 latest-episode callout on landing. To be scoped in a `/gsd-discuss-phase 3` pass once the first episodes are recorded — defining these now is premature.

**Explicitly out of Phase 3** (deferred further):
- Search / filter across episodes — post-launch discovery layer
- Transcript generation / display — separate workflow
- Comment surfaces on rewired.show — Substack handles comments in its own UI; duplicating on rewired.show is scope creep
- Paid / gated content — Substack handles this if/when introduced; rewired.show mirrors the public feed only

**Out of scope for this roadmap (deferred further):**
- Analytics beyond Substack's built-in subscriber count
- Welcome-email drip sequence on Substack

**Plans:** TBD (scoped in future discuss-phase).

---

## Coverage check

All 20 v1 requirements are mapped across Phases 1 & 2. Phase 3 adds EPS-01..05 to the requirements set and those are defined lazily (at `/gsd-discuss-phase 3` time), not now.

## Milestone exit

When Phase 2 succeeds, the site is MVP-live and the subscribe funnel works. Phase 3 opens when episode content exists. Post-launch decisions (search, analytics deeper than subscriber count, welcome sequence, comment mirroring) move into a new milestone driven by observed signal — subscriber growth, feedback from early listeners, and whether the cadence of episode recording actually holds.
