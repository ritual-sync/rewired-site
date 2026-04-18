---
phase: 01-build-static-site-content-portraits-palette
plan: 02
subsystem: homepage-composition
tags: [hugo, layout, hero, lens, hosts, coming-soon, responsive, portraits, palette]
dependency_graph:
  requires:
    - "Plan 01-01 scaffolding (Hugo project, vendored arcaeon theme, portraits at static/images/portraits/, rewired-overrides.css with palette aliases)"
  provides:
    - "Project-level layouts/_default/baseof.html shadowing theme baseof (loads main.css + rewired-overrides.css via resources pipeline)"
    - "Project-level layouts/index.html composing four section partials in order"
    - "Four section partials: hero, lens, hosts, coming-soon — all wired to content/_index.md frontmatter"
    - "content/_index.md frontmatter carrying all Rewired copy (v0 drafts from CONTEXT.md D-07..D-10)"
    - "Extended rewired-overrides.css with responsive breakpoints (768/1024/1440), hero name (D-05), portrait stack/row (D-06), Ion Glow focus ring (D-11)"
    - "Buildable homepage that renders Hero -> Lens -> Hosts -> Coming Soon in the correct DOM order"
  affects:
    - "Phase 2 Plan 01 (email capture) — will replace .rewired-coming-soon__email-placeholder div with the Systeme.io form"
    - "Phase 2 Plan 02 (deployment) — will add OG metadata, favicon, deploy config to baseof.html"
tech_stack:
  added: []
  patterns:
    - "Hugo project-root layouts/ shadowing theme layouts/"
    - "Frontmatter-driven copy (all strings in content/_index.md; templates read via $.Params.*)"
    - ".bio | safeHTML to pass through inline <a> tags in host bios"
    - "clamp()-based fluid typography (no hard breakpoint font-size switches)"
    - "Mobile-first CSS with three min-width breakpoints (768, 1024, 1440)"
    - "Static-asset portraits via {{ \"path\" | relURL }} — no Hugo image pipeline for Phase 1 (simpler, source plates already at final resolution)"
key_files:
  created:
    - "layouts/_default/baseof.html"
    - "layouts/index.html"
    - "layouts/partials/sections/hero.html"
    - "layouts/partials/sections/lens.html"
    - "layouts/partials/sections/hosts.html"
    - "layouts/partials/sections/coming-soon.html"
  modified:
    - "content/_index.md"
    - "assets/css/rewired-overrides.css"
decisions:
  - "Stub partials created up-front in Task 1 commit because Hugo hard-errors (not warns) on missing partial references; stubs replaced with full content in Tasks 2/3"
  - "Static-asset relURL chosen over resources.Get|Fill|Process 'webp' for portraits — source plates are already 1024x1024 final, the extra pipeline adds build complexity for marginal byte savings (clarity over intensity)"
  - "Host bios use safeHTML to pass through inline <a> tags; source is controlled content (Matt's own copy) so injection risk is nil"
  - "Ion Glow accent used in exactly 2 locations (global :focus-visible + email-placeholder :focus-within); both serve the same focus-indication affordance, counting as 'one accent location' per D-11"
metrics:
  duration: "~4 minutes"
  tasks_completed: 3
  files_created: 6
  files_modified: 2
  commits: 3
completed_date: "2026-04-18"
---

# Phase 1 Plan 02: Rewired Homepage — Hero, Lens, Hosts, Coming Soon — Summary

Rewired homepage composed from four section partials wired to frontmatter copy, rendering Hero (show name + dual portraits + one-line lens) -> Lens (CONT-01 paragraph) -> Hosts (Matt + Jaye Anne bios with Feral Architecture and Tarot Pulse links) -> Coming Soon (Phase 2 email-placeholder with Ion Glow focus ring primed). Build exits 0; DOM order verified; all 5 canonical copy strings present; zero non-palette hex values in rewired-overrides.css; theme directory untouched.

## What Was Built

**Project-level base layout** (`layouts/_default/baseof.html`):
Shadows the theme's baseof for Rewired. Preserves theme font preloads (Cinzel + Space Grotesk .woff2) intact per the key_wave1_context note. Loads theme `css/main.css` through Hugo's `resources.Get | css.Build | minify | fingerprint` pipeline with `externals` to match @font-face paths. Loads `css/rewired-overrides.css` through `resources.Get | minify | fingerprint` (no css.Build since overrides has no @import). Drops the theme's falkensmage-specific OG metadata and Twitter Card meta — Phase 2 will add Rewired-specific SEO.

**Homepage template** (`layouts/index.html`):
Defines the `main` block with a `.rewired-main` flex container calling four partials in DOM order: hero -> lens -> hosts -> coming-soon. Entirely replaces the theme's index.html which referenced falkensmage partials (currently, identity-cta, social, footer) — Rewired's homepage is its own composition.

**Hero section** (`layouts/partials/sections/hero.html`):
Renders H1 "Rewired" in Fusion Gold via `.rewired-hero__name` (clamp 3rem–6rem, 700 weight), two `<img>` tags with `width="800" height="800"` to prevent CLS, `loading="eager"` and `decoding="async"`, descriptive alt text pulled from `hosts.matt.portraitAlt` / `hosts.jayeAnne.portraitAlt` frontmatter. The one-line lens renders below the portrait pair in Solar White at clamp 1.125rem–1.625rem.

Portrait paths use `{{ "images/portraits/matt.jpg" | relURL }}` — direct static reference, no Hugo image pipeline. Rationale: source plates are already 1:1 at 1024x1024 with appropriate file sizes (685 KB + 778 KB). Adding `Fill | Process "webp"` would cost build time for marginal byte savings at Phase 1 scale. If either file later exceeds 500 KB of visible weight on slow connections, the resources pipeline is a drop-in swap.

**Lens section** (`layouts/partials/sections/lens.html`):
Renders H2 "The Lens" + the CONT-01 paragraph on `section-depth` (Deep Indigo) background for visual variation from the Void Purple hero. `.rewired-lens__heading` uses Cinzel at clamp 1.75rem–2.5rem; `.rewired-lens__body` uses Space Grotesk at clamp 1rem–1.1875rem.

**Hosts section** (`layouts/partials/sections/hosts.html`):
Renders H2 "Hosts" + a 2-up grid with an `<article class="rewired-host ...">` for each host. Grid is `1fr` on mobile (stacked), `1fr 1fr` at `(min-width: 768px)`. Bios pass through `safeHTML` so the inline `<a href="https://feralarchitecture.com">` and `<a href="https://tarotpulse.com">` tags render as links. Link hover color transitions from Solar White to Plasma Pink (`--rewired-link-hover`) via 120ms ease.

**Coming Soon section** (`layouts/partials/sections/coming-soon.html`):
Renders H2 "Coming Soon" + the CONT-03 line + a placeholder `<div class="rewired-coming-soon__email-placeholder">` carrying "Email signup wired in Phase 2." copy, dashed border, 0.7 opacity. The `:focus-within` Ion Glow outline is pre-wired so when Phase 2's Systeme.io `<input>` drops in, the focus ring already lights up cyan.

**Extended `assets/css/rewired-overrides.css`** (+ ~200 lines):
- `.rewired-main` flex container
- `.rewired-section` with `clamp(3rem, 8vw, 7rem)` vertical padding and `clamp(1rem, 5vw, 4rem)` horizontal
- Hero rules: centered flex column, name (Fusion Gold display), portraits (column on mobile, row at ≥768px), lens (centered 40ch max)
- Lens rules: 52rem max-width, centered
- Hosts rules: 64rem max-width, grid template columns responsive
- Coming Soon rules: 48rem max-width, centered; placeholder div + focus-within Ion Glow outline
- Three responsive breakpoints: 768, 1024, 1440
- Global `:focus-visible` Ion Glow ring (the single ARCÆON triad-discipline accent per D-11)
- `@media (prefers-reduced-motion: reduce)` clamping all animations/transitions to 0.01ms

**Homepage content** (`content/_index.md`):
Frontmatter carries all Rewired copy verbatim from CONTEXT.md D-07..D-10 drafts. Body stays empty — all string edits happen in frontmatter; templates never touch copy.

## Verification Results

| Check | Result |
|-------|--------|
| `hugo --minify --destination /tmp/rewired-final-build` exits 0 | PASS |
| `/tmp/rewired-final-build/index.html` exists (3,495 bytes) | PASS |
| DOM order: H1 Rewired (902) -> H2 The Lens (1654) -> H2 Hosts (2242) -> H2 Coming Soon (3163) | PASS |
| Copy: "We left the systems. We're finding what's alive." | FOUND |
| Copy: "It's not a recovery story." | FOUND |
| Copy: "Lives in the seam between grep and The Morrigan." | FOUND |
| Copy: "Rooted in curanderismo-derived embodied practice." | FOUND |
| Copy: "First episodes drop June 2026." | FOUND |
| Palette audit: `grep -Eo "#[0-9a-fA-F]{3,8}" assets/css/rewired-overrides.css` | 0 hex values (all via var(--arcaeon-*)) |
| Built CSS bundle palette audit: only 11 canonical ARCÆON hex values (Void Purple, Deep Indigo, Midnight Blue, Electric Violet, Neon Magenta, Plasma Pink, Electric Blue, Ion Glow, Solar White, Fusion Gold, Ignition Orange) | PASS (zero non-palette leaks) |
| Responsive: `flex-direction: column` (mobile default) present | PASS |
| Responsive: `flex-direction: row` inside `@media (min-width: 768px)` | PASS |
| Responsive: `overflow-x: hidden` (D-12 horizontal scroll guard) | PASS |
| Three explicit media query breakpoints (768, 1024, 1440) | PASS |
| Ion Glow `var(--rewired-accent-cyan)` references | 2 (both focus-indication affordances — global :focus-visible + email-placeholder :focus-within; counts as one UI role per D-11) |
| Theme directory (`themes/arcaeon/`) modifications after vendor copy | 0 (read-only preserved) |
| HERO-04 swap-ready: replacing `static/images/portraits/jaye-anne.jpg` and rebuilding would produce a site with the swapped portrait and zero code changes | PASS (confirmed by path: hero.html references the static path unchanged) |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocker] Hugo hard-errors on missing partials; plan expected warnings**
- **Found during:** Task 1 verification build
- **Issue:** The plan stated: *"Expect Hugo to emit warnings like `partial "sections/hero.html" not found` — that is EXPECTED and the build should still produce an index.html skeleton."* In reality Hugo treats missing partials referenced by `{{ partial "..." . }}` as fatal errors. Task 1's verify step requires the build to exit 0, but it exits 1 with `error calling partial: partial "sections/lens.html" not found`.
- **Fix:** Created minimal stub partials at `layouts/partials/sections/{hero,lens,hosts,coming-soon}.html` each containing a Hugo comment placeholder. Tasks 2 and 3 overwrite the stubs with the real partials. Net result: Task 1's commit includes stubs; Tasks 2/3 replace them. No behavioral deviation from the plan's intent — the file set and commit boundaries are the same.
- **Files affected:** All four `layouts/partials/sections/*.html` created as stubs in Task 1 commit
- **Commit:** `0038f9e`

**2. [Informational — not a fix] Plan's verify grep strings use quoted attribute values; Hugo minify strips quotes**
- **Found during:** Task 2 verification
- **Issue:** The plan's `<verify>` regex for Task 2 includes `'<h1 class="rewired-hero__name">Rewired</h1>'` and `'src="/images/portraits/matt.jpg"'`. Hugo's `--minify` strips quotes from attributes when HTML5 allows it, so the built output reads `<h1 class=rewired-hero__name>Rewired</h1>` and `src=/images/portraits/matt.jpg`. The content is correct but the quoted patterns don't match.
- **Fix:** None required — content is rendered correctly. Used quote-agnostic grep patterns for verification (`'class=rewired-hero__name>Rewired'`, `'src=/images/portraits/matt.jpg'`) which confirmed content integrity. Recorded here for plan authors' future reference.
- **Files affected:** None
- **Commit:** N/A

### No other deviations

All content, styling decisions, and class names match the plan exactly. Copy matches CONTEXT.md D-07..D-10 v0 drafts verbatim — no in-flight redlines from Matt during execution.

## Phase 2 Handoff Notes

**Email capture wire-in (Phase 2 Plan for CAPT-01..04):**
- Replace the `<div class="rewired-coming-soon__email-placeholder" aria-label="Email signup (coming soon)">Email signup wired in Phase 2.</div>` in `layouts/partials/sections/coming-soon.html` with the Systeme.io embed / form.
- The `:focus-within` rule on `.rewired-coming-soon__email-placeholder` already lights up Ion Glow cyan at 2px outline with 3px offset — the real `<input>` will inherit this automatically once dropped into the same container class.
- Consider whether the Ion Glow ring should move from `:focus-within` on the wrapper to `:focus-visible` directly on the `<input>` — both work; the wrapper approach is more forgiving of Systeme.io's specific DOM.

**Deployment (Phase 2 Plan for DEPL-01..04):**
- `layouts/_default/baseof.html` intentionally omits OG metadata, Twitter Card meta, canonical URL, and favicon links. Phase 2 adds these to this file.
- `hugo.toml` will need `baseURL` updated from `/` to the real domain when DEPL-02 wires DNS.
- The `WARN found no layout file for "html" for kind "taxonomy"` noise can be silenced by setting `disableKinds = ["taxonomy", "term"]` in hugo.toml if Phase 2 wants a clean build log.

**Class hooks available for future styling:**
- `.rewired-hero-section`, `.rewired-lens-section`, `.rewired-hosts-section`, `.rewired-coming-soon-section` — each section has a modifier class if Phase 2 needs per-section hooks
- `.rewired-host--matt`, `.rewired-host--jaye-anne` — per-host styling hooks (currently unused — both hosts render identically)

## Commits (3 atomic + 1 metadata final)

- `0038f9e` feat(01-02): wire project-level baseof, index template, and section CSS (7 files, +267/-2 lines — includes 4 stub partials to satisfy Hugo's hard-error on missing partials)
- `c700cdb` feat(01-02): wire homepage frontmatter and Hero partial with dual portraits (2 files, +45/-1 lines)
- `08ed567` feat(01-02): wire Lens, Hosts, Coming Soon partials from frontmatter copy (3 files, +44/-3 lines)
- (forthcoming) docs(01-02): complete Rewired homepage composition plan — metadata commit for SUMMARY.md + STATE.md + ROADMAP.md

## Self-Check: PASSED

Confirmed existence of all created files:
- `/Users/falkensmage/RitualSync/rewired-site/layouts/_default/baseof.html` — FOUND
- `/Users/falkensmage/RitualSync/rewired-site/layouts/index.html` — FOUND
- `/Users/falkensmage/RitualSync/rewired-site/layouts/partials/sections/hero.html` — FOUND
- `/Users/falkensmage/RitualSync/rewired-site/layouts/partials/sections/lens.html` — FOUND
- `/Users/falkensmage/RitualSync/rewired-site/layouts/partials/sections/hosts.html` — FOUND
- `/Users/falkensmage/RitualSync/rewired-site/layouts/partials/sections/coming-soon.html` — FOUND

Confirmed existence of all modified files:
- `/Users/falkensmage/RitualSync/rewired-site/content/_index.md` — FOUND (frontmatter populated)
- `/Users/falkensmage/RitualSync/rewired-site/assets/css/rewired-overrides.css` — FOUND (extended)

Confirmed all 3 task commits exist in `git log`:
- `0038f9e` — FOUND
- `c700cdb` — FOUND
- `08ed567` — FOUND
