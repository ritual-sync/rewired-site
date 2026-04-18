# Requirements: Rewired Site

**Defined:** 2026-04-18
**Core Value:** A visitor lands, immediately gets the lens of the show, sees the two hosts, and drops their email so they don't miss the launch.

## v1 Requirements

### Site Infrastructure

- [ ] **SITE-01**: Project scaffolded with a static site generator (Hugo preferred if `arcaeon` theme can be reused; Astro is the fallback)
- [ ] **SITE-02**: ARCÆON palette tokens available as CSS variables (Void Purple, Fusion Gold, Ignition Orange, Plasma Pink, Ion Glow cyan, and supporting depth colors)
- [ ] **SITE-03**: Responsive layout — mobile-first, readable on phones, desktop adds breathing room
- [ ] **SITE-04**: Typography system picked (one display, one body) that reads as adult / literary, not cute or corporate

### Hero Section

- [ ] **HERO-01**: Show name ("Rewired") displayed as primary headline with distinctive typographic treatment
- [ ] **HERO-02**: One-line show lens (e.g., "We left the systems. We're finding what's alive.") — exact copy to be drafted in Phase 1
- [ ] **HERO-03**: Dual illustrated host portraits (Matt + Jaye Anne) placed as a pair that reads as co-hosts of the same show
- [ ] **HERO-04**: Portrait asset references are swappable — replacing Jaye Anne's v3 with a different variant is a single-asset swap, not a code rewrite

### Content Sections

- [ ] **CONT-01**: "The Lens" — one short paragraph articulating the show's through-line (deconstruction → something alive)
- [ ] **CONT-02**: "Hosts" — short bios for Matt and Jaye Anne, each 2-3 sentences, true to voice
- [ ] **CONT-03**: "Coming Soon" callout framing the June 2026 launch without creating a false-urgency feel

### Email Capture

- [ ] **CAPT-01**: Systeme.io form embedded or proxied into the page (whichever integration method is least fragile)
- [ ] **CAPT-02**: Captured emails land in a Systeme.io list specifically for Rewired (not mixed with other RitualSync lists)
- [ ] **CAPT-03**: Successful submission shows a clear confirmation state without leaving the page
- [ ] **CAPT-04**: Submission failures show a recoverable error state (no silent failures)

### Deployment

- [ ] **DEPL-01**: Site deployed to free / low-cost static host (Cloudflare Pages, Netlify, or GitHub Pages)
- [ ] **DEPL-02**: Custom subdomain configured with HTTPS (exact domain TBD in Phase 1)
- [ ] **DEPL-03**: Open Graph and Twitter Card metadata render correctly when the URL is shared on major platforms
- [ ] **DEPL-04**: Favicon produced in the ARCÆON palette and installed
- [ ] **DEPL-05**: Deploy pipeline is automatic — push to main → live within minutes, no manual steps

## v2 Requirements

Deferred — will be considered after first episodes exist or after an observed MVP signal.

### Episodes

- **EPS-01**: Episode list surface with show notes and embedded player
- **EPS-02**: Per-episode permalink pages
- **EPS-03**: Podcast feed (RSS) link in nav / footer

### Discovery

- **DISC-01**: Basic analytics (Plausible or similar) to track signup rate
- **DISC-02**: Social share buttons on the page (or link-sharing improvements)

## Out of Scope

| Feature | Reason |
|---------|--------|
| Episode audio player | No episodes yet; launch is stockpile-based |
| RSS feed generation on site | Podcast host handles this, not the marketing site |
| CMS / blog | Static MVP; dynamic content is a post-launch decision |
| Multi-page navigation | Premature IA work for a pre-launch site |
| Analytics beyond signup count | Ship first, measure later; don't block on tracking fidelity |
| Newsletter automation / welcome sequence | Form capture is v1; drip sequences are a separate exercise |
| OAuth / user accounts | No user state exists; no reason to add one |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| SITE-01 | Phase 1 | Pending |
| SITE-02 | Phase 1 | Pending |
| SITE-03 | Phase 1 | Pending |
| SITE-04 | Phase 1 | Pending |
| HERO-01 | Phase 1 | Pending |
| HERO-02 | Phase 1 | Pending |
| HERO-03 | Phase 1 | Pending |
| HERO-04 | Phase 1 | Pending |
| CONT-01 | Phase 1 | Pending |
| CONT-02 | Phase 1 | Pending |
| CONT-03 | Phase 1 | Pending |
| CAPT-01 | Phase 2 | Pending |
| CAPT-02 | Phase 2 | Pending |
| CAPT-03 | Phase 2 | Pending |
| CAPT-04 | Phase 2 | Pending |
| DEPL-01 | Phase 2 | Pending |
| DEPL-02 | Phase 2 | Pending |
| DEPL-03 | Phase 2 | Pending |
| DEPL-04 | Phase 2 | Pending |
| DEPL-05 | Phase 2 | Pending |

**Coverage:**
- v1 requirements: 20 total
- Mapped to phases: 20
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-18*
*Last updated: 2026-04-18 after initialization*
