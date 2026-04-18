# Phase 1: Build — Static site, content, portraits, palette - Context

**Gathered:** 2026-04-18
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase delivers a locally-runnable static build of the Rewired MVP site: all four one-page sections (Hero → Lens → Hosts → Coming Soon placeholder), dual illustrated host portraits rendered correctly on desktop and mobile, and the RitualSync warm-core palette applied throughout.

**In scope:** static site generator setup, theme/layout work, hero composition, copy for lens + host bios + coming soon placeholder, portrait asset integration with swap-in capability, responsive CSS, typography system.

**Explicitly out of this phase** (belongs to Phase 2): email form wiring, deployment, OG metadata, favicon generation, domain configuration.

</domain>

<decisions>
## Implementation Decisions

### Static Site Generator (D-01)

- **D-01:** **Hugo with a new project directory, consuming the existing `arcaeon` theme as a Hugo module (or git submodule) from the `falkensmage-website` source.** Rationale: the arcaeon theme already encodes the ARCÆON palette, typography, and component grammar — reusing it is the shortest path to a consistent brand surface. We get a working theme in minutes instead of days. If during execution the theme forces unfit layout decisions for a two-host landing page, the fallback is plain Astro with hand-written CSS — do NOT fork the theme mid-phase; document the blocker and escalate.

### Portrait Integration (D-02)

- **D-02:** **Copy the two portrait files into `static/images/portraits/` at project initialization, not referenced by absolute external path.** Paths in layouts use `{{ "images/portraits/matt.jpg" | relURL }}` (or equivalent). Jaye Anne's v3 file is copied now; if she picks a different variant, we overwrite that single file — zero code change, zero content edit.
- **D-03:** Both portraits render in the hero at the same aspect ratio (1:1 square, matching the source plates) with matched sizes. CSS enforces a max-width so the hero never explodes on ultra-wide screens.

### Typography (D-04)

- **D-04:** **Serif display font for headings (Fraunces or equivalent literary serif from Google Fonts) paired with a clean geometric sans for body (Inter).** The arcaeon theme's existing typography is the starting point — if it already ships Fraunces/Inter or a close equivalent, inherit. Otherwise override in the Rewired site's custom CSS. Rationale: literary / adult, not cute or corporate, matches the voice of the show.

### Hero Composition (D-05, D-06, D-07)

- **D-05:** **Show name "Rewired" above the portrait pair, in Fusion Gold, display-weight, large (clamp 48–96px responsive).** Single-word show name gets single-line treatment. No subtitle or tagline in the show-name line itself — the one-line lens lives directly below the portraits.
- **D-06:** **Portraits side-by-side on desktop (≥ 768px), stacked vertically on mobile.** Matt's portrait on the left, Jaye Anne's on the right at desktop. Stack order on mobile: Matt above Jaye Anne (preserves left-to-right reading rhythm).
- **D-07:** **One-line lens below the portrait pair**, centered, in Solar White at display-scale body weight. Default lens copy: **"We left the systems. We're finding what's alive."** (final-call opportunity during execution if Matt wants to iterate.)

### Content Copy (D-08, D-09, D-10)

- **D-08:** **"The Lens" section — one short paragraph, max 80 words, in Matt's voice.** Draft for execution:
  > "Rewired is a conversation between two people who left the systems they were raised in and kept going. Evangelical deconstruction, embodied practice, tarot, Jungian work, the slow repatterning of a nervous system that was never wrong — just aimed somewhere false. It's not a recovery story. It's what happens after you stop trying to get back to who you were and start finding out what you actually are."
  — Execution agent should treat this as a v0 draft. Matt can redline before shipping.
- **D-09:** **Host bios — 2-3 sentences each, Matt's voice for Matt's bio; collaboratively-drafted for Jaye Anne's (she gets editorial approval).** Draft stubs to refine during execution:
  > **Matt Stine.** Enterprise systems architect by day, witch and Jungian co-conspirator by everything else. Writes at [Feral Architecture](https://feralarchitecture.com). Lives in the seam between grep and The Morrigan.
  > **Jaye Anne Beringer.** Energy Alchemy practitioner, RitualSync co-founder, and the reason most of the hard questions get asked in the first place. Rooted in curanderismo-derived embodied practice. Writes [Tarot Pulse](https://tarotpulse.com).
- **D-10:** **Coming Soon framing — no fake urgency, clear signal.** Draft:
  > "First episodes drop June 2026. Leave your email so you don't miss it."

### Palette Application (D-11)

- **D-11:** Palette rules for this site specifically:
  - **Void Purple `#1a0f2e`** — page background, card backgrounds where needed
  - **Fusion Gold `#ffb347`** — show name, section headings (h2)
  - **Ignition Orange `#ff7a18`** — CTA button background, key phrase accents (1-2 per page max)
  - **Plasma Pink `#ff5fd2`** — link hover states, subtle decorative accents
  - **Ion Glow cyan `#5be7ff`** — ONE accent location (recommended: email input focus ring) for ARCÆON triad discipline
  - **Solar White `#fff4e6`** — primary body text
  - **Deep Indigo `#0a0f3c`** — subtle section dividers, secondary card backgrounds
  - **Electric Violet `#7a2cff`** — atmospheric depth only, no foreground use
  - **Nothing from outside the ARCÆON palette. Ever.**

### Responsive & A11y (D-12)

- **D-12:** Mobile-first breakpoints: base (≤ 480px), tablet (≥ 768px), desktop (≥ 1024px), wide (≥ 1440px). No horizontal scroll at any width. Touch targets ≥ 44×44px. Color contrast meets WCAG AA for body text; headline treatments may exceed AA but must read cleanly at all sizes. No motion on load unless a user-triggered interaction.

### Claude's Discretion

- Exact Hugo section taxonomy (single-page `_index.md` vs partials-heavy): executor picks based on theme structure.
- Specific CSS custom property naming conventions: follow the arcaeon theme's conventions if consumable; otherwise use `--color-*` BEM-adjacent naming.
- Exact font loading strategy (preload, swap, fallback stack): executor picks based on Hugo/theme integration.
- Whether to include a minimal favicon stub in Phase 1 (non-blocking): executor's call — a placeholder 32×32 in Fusion Gold is acceptable, full favicon set is Phase 2 (DEPL-04).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Context
- `.planning/PROJECT.md` — Rewired Site project context, core value, key decisions
- `.planning/REQUIREMENTS.md` — 20 v1 requirements (SITE-01..04, HERO-01..04, CONT-01..03 are in this phase)
- `.planning/ROADMAP.md` — Phase 1 goal and success criteria

### Palette & Brand
- `~/.psyche/swipe-files/podcasting-creative/2026-04-16-12-33-18-arc-on-color-palette-full.md` — Full ARCÆON palette hex values and usage tiers (Radiant Core is Rewired's primary register)
- `~/.psyche/swipe-files/podcasting-creative/2026-04-16-12-32-43-arc-on-color-palette-canonical.md` — Feral Architecture subset reference for contrast with Rewired's warm subset
- `~/Documents/Business-Brand/Feral-Architecture/covers/TEMPLATE.md` — Feral Architecture aesthetic contract (context only — Rewired's site is RitualSync-warm, not Feral-cool)

### Voice
- `~/.psyche/identity/voice.md` — Matt's public writing voice (direct, structured, resonant, lightly irreverent, non-corporate)
- `~/.psyche/identity/voice-samples.md` — Calibration excerpts (rhythm, fourth-wall breaks, casual profanity as texture)

### Reusable Assets (prior art)
- `~/RitualSync/falkensmage-website/` — existing Hugo project consuming the `arcaeon` theme
- `~/RitualSync/falkensmage-website/themes/arcaeon/` — the theme itself (layouts/, assets/css/, static/)
- `~/RitualSync/falkensmage-website/hugo.toml` — reference configuration for Hugo + arcaeon theme wiring

### Portraits
- `~/Documents/Business-Brand/Feral-Architecture/portraits/2026-04-13-author-headshot/final/author-headshot.jpg` — Matt's locked portrait
- `~/Documents/Business-Brand/Feral-Architecture/portraits/2026-04-18-jaye-anne-headshot/final/jaye-anne-headshot.jpg` — Jaye Anne's tentative v3 lock (swap-ready)
- https://mstine.github.io/rewired-portrait-review/ — public review page where Jaye Anne picks a variant

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- **`arcaeon` Hugo theme** (`~/RitualSync/falkensmage-website/themes/arcaeon/`) — already encodes ARCÆON palette tokens and brand typography. Strong reuse candidate; consume as Hugo theme module or git submodule.
- **falkensmage-website hugo.toml** — reference for site-config wiring against the arcaeon theme.

### Established Patterns

- Matt has shipped at least one Hugo+arcaeon site (falkensmage.com); the pattern is proven.
- Psyche-infographic was deployed to GitHub Pages — similar static deploy target is available if Phase 2 lands there.

### Integration Points

- This is a fresh project — no existing code in the `rewired-site` repo to integrate with. Integration is outward: pulling the arcaeon theme in, and (in Phase 2) connecting to Systeme.io.

</code_context>

<specifics>
## Specific Ideas

- **Visual model reference:** portraits in Feral Architecture medium (illustrated dark graphic novel plate) set into a RitualSync-warm page — a deliberate contrast between portrait register (cool cyan/magenta chiaroscuro on Void Purple) and page register (warm gold/orange/pink on Void Purple). Same family, different slices. Phase 1 must hold that contrast cleanly, not collapse it.
- **Tonal anchor:** the site should feel like a warm evening room with two thoughtful people in it — not a startup landing page, not a cult altar. If executor feels pulled toward either extreme, pull back.
- **Copy calibration:** lines like "We left the systems. We're finding what's alive." and "leave your email so you don't miss it" are deliberately plain. Resist upgrades to literary/clever — the surrounding treatment carries the weight.

</specifics>

<deferred>
## Deferred Ideas

- **Episode list / audio player** — no episodes yet; belongs to a post-launch phase once recordings exist.
- **RSS / podcast feed** — lives on the podcast host (Transistor / Buzzsprout), not the marketing site.
- **CMS / dynamic content** — static MVP by design.
- **Analytics / tracking pixels** — ship-first, measure-later.
- **Welcome email sequence inside Systeme.io** — form capture is v1; drip is a separate exercise.
- **Full favicon set and app icons** — Phase 2 (DEPL-04).
- **Tarot card "of the episode" surfacing** — symbolic riff worth noting; potential for a post-launch phase that surfaces the card pull of the most recent episode.

</deferred>

---

*Phase: 01-build-static-site-content-portraits-palette*
*Context gathered: 2026-04-18*
