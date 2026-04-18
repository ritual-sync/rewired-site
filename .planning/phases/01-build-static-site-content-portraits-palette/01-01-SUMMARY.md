---
phase: 01-build-static-site-content-portraits-palette
plan: 01
subsystem: scaffold
tags: [hugo, theme, palette, portraits, typography, foundation]
dependency_graph:
  requires: []
  provides:
    - "Buildable Hugo project at /Users/falkensmage/RitualSync/rewired-site/"
    - "Vendored arcaeon theme at themes/arcaeon/ (read-only)"
    - "ARCÆON warm-core palette tokens available as CSS custom properties on :root"
    - "Both host portraits at /images/portraits/{matt,jaye-anne}.jpg, 1024x1024 1:1"
    - "Typography pairing (Cinzel + Space Grotesk) inherited from theme"
    - "Rewired-specific semantic aliases + D-12 responsive/touch-target rules in assets/css/rewired-overrides.css"
  affects:
    - "Plan 01-02 (Wave 2) — builds homepage content partials on this foundation"
tech_stack:
  added:
    - "Hugo v0.160.1+extended+withdeploy"
    - "arcaeon theme (vendored via direct copy, 20 files)"
  patterns:
    - "Theme vendor-by-copy (D-01 deviation: source repo is not standalone)"
    - "Project-root assets/ shadow theme assets/ via Hugo layout lookup"
    - "Static-asset portrait pattern (swap-ready, zero-code replacement)"
key_files:
  created:
    - "hugo.toml"
    - ".gitignore"
    - "content/_index.md"
    - "assets/css/rewired-overrides.css"
    - "static/images/portraits/matt.jpg"
    - "static/images/portraits/jaye-anne.jpg"
    - "themes/arcaeon/ (entire tree, 20 files, vendored read-only)"
  modified: []
decisions:
  - "D-01 deviation: vendor theme via `cp -R` instead of Hugo module / git submodule (source lacks .git / .gitmodules)"
  - "D-04: INHERIT Cinzel + Space Grotesk from theme (no Fraunces/Inter override)"
  - "Plan 02 owns baseof.html override that wires rewired-overrides.css (Option A path)"
metrics:
  duration: "~30 minutes"
  tasks_completed: 3
  files_created: 26  # 6 project files + 20 theme files
  files_modified: 0
  commits: 3
completed_date: "2026-04-18"
---

# Phase 1 Plan 01: Scaffold Hugo + Vendor Arcaeon + Install Portraits + Palette Foundation — Summary

Hugo project scaffolded at `/Users/falkensmage/RitualSync/rewired-site/` with arcaeon theme vendored read-only, both host portraits installed at canonical swap-ready paths, and the Rewired CSS override file wired with warm-core palette aliases and D-12 responsive guardrails. Baseline `hugo --minify` exits 0. Plan 02 can now build homepage content partials on this foundation.

## What Was Built

**Hugo project root** (`/Users/falkensmage/RitualSync/rewired-site/`):
- `hugo.toml` — `theme = "arcaeon"`, `baseURL = "/"`, `title = "Rewired"`, `[params.colors]` with the Radiant Core warm-core subset per D-11 (voidPurple, deepIndigo, fusionGold, ignitionOrange, plasmaPink, ionGlow, solarWhite, electricViolet only — no Neon Magenta, Electric Blue, or Midnight Blue since Rewired's palette is warm-core, not cool-core)
- `.gitignore` — excludes `/public/`, `/resources/_gen/`, `.hugo_build.lock`, `hugo_stats.json`, `.DS_Store`, editor dirs
- `content/_index.md` — stub with `title: "Rewired"` frontmatter (body deferred to Plan 02)

**Vendored theme** (`themes/arcaeon/`, 20 files):
- `layouts/_default/baseof.html` — base HTML shell with font preloads, OG/Twitter meta (still falkensmage-specific — Plan 02 overrides at project-root)
- `layouts/index.html` — homepage layout that references partials (will be overridden by Plan 02)
- `layouts/partials/sections/*.html` — hero, currently, identity-cta, social, footer (falkensmage-specific — Plan 02 won't reference most; Rewired's own partials supersede them)
- `layouts/partials/icons/*.html` — social icon SVGs (reusable for Plan 02 if needed)
- `assets/css/main.css` — ARCÆON palette tokens defined at `:root` (--arcaeon-void-purple, --arcaeon-fusion-gold, etc.) plus semantic aliases (--color-bg, --color-text, --color-cta-start)
- `assets/images/magus-hero.jpg` — harmless baggage; Rewired's index layout (Plan 02) won't reference it so it won't appear in the build output
- `static/fonts/cinzel-latin-wght-normal.woff2` + `space-grotesk-latin-wght-normal.woff2` — display serif + body sans, preloaded via baseof.html

**Portraits** (both 1024x1024, 1:1 square):
- `static/images/portraits/matt.jpg` — 685,003 bytes, copied from `~/Documents/Business-Brand/Feral-Architecture/portraits/2026-04-13-author-headshot/final/author-headshot.jpg`
- `static/images/portraits/jaye-anne.jpg` — 777,711 bytes, copied from `~/Documents/Business-Brand/Feral-Architecture/portraits/2026-04-18-jaye-anne-headshot/final/jaye-anne-headshot.jpg`

**Rewired CSS overrides** (`assets/css/rewired-overrides.css`):
- `:root` aliases pinned to warm-core per D-11: `--rewired-bg` (Void Purple), `--rewired-heading` (Fusion Gold), `--rewired-cta` (Ignition Orange), `--rewired-link-hover` (Plasma Pink), `--rewired-accent-cyan` (Ion Glow — reserved for Plan 02's focus ring per ARCÆON triad discipline), `--rewired-text` (Solar White), `--rewired-bg-alt` (Deep Indigo), `--rewired-divider`
- D-12: `html, body { overflow-x: hidden; }` — no horizontal scroll at any width
- D-12: `.rewired-cta { min-height: 44px; min-width: 44px; }` — touch-target compliance
- Responsive padding helper: `.rewired-section { padding: clamp(2rem, 6vw, 6rem) clamp(1rem, 4vw, 3rem); }`

## Typography Decision

**`TYPOGRAPHY_DECISION=inherit`** — retain Cinzel (display serif) + Space Grotesk (body sans) from the vendored theme.

Rationale: D-04 explicitly permits inheritance ("if it already ships Fraunces/Inter or a close equivalent, inherit"). Cinzel is a Roman-inscription literary serif (adult, not cute); Space Grotesk is a clean neo-grotesque geometric sans. The pairing already reads as literary/adult on falkensmage.com, which passed the same brand filter Rewired is held to. Choosing Fraunces/Inter would add a second font-loading pipeline (two more `@font-face` declarations, two more preload paths, two more network weights) for a marginal aesthetic difference. No override was made. Both fonts are already preloaded by the theme's `baseof.html` with matching `@font-face` paths.

## Verification Results

| Check | Result |
|-------|--------|
| `hugo --minify --destination /tmp/rewired-baseline-build` exits 0 | PASS |
| `/tmp/rewired-baseline-build/index.html` exists | PASS |
| `/tmp/rewired-baseline-build/images/portraits/matt.jpg` exists | PASS |
| `/tmp/rewired-baseline-build/images/portraits/jaye-anne.jpg` exists | PASS |
| `--arcaeon-void-purple: #1a0f2e` defined at `:root` in theme main.css | PASS (4 occurrences in main.css) |
| `var(--arcaeon-void-purple)` referenced in rewired-overrides.css | PASS |
| `var(--arcaeon-fusion-gold)` referenced in rewired-overrides.css | PASS |
| `var(--arcaeon-ion-glow)` referenced in rewired-overrides.css | PASS |
| `min-height: 44px` present for touch-target compliance | PASS |
| Files modified under `themes/arcaeon/` after vendor copy | 0 (theme read-only preserved) |
| Both portraits 1:1 square (1024x1024) | PASS |
| Both portrait files > 10 KB | PASS (685 KB + 778 KB) |

Note on the baseline build at this stage: the rendered index.html inherits from the theme's falkensmage-specific `layouts/index.html`, so the output looks like a partial falkensmage homepage (hero references Matt's Magus image, partials reference falkensmage params that aren't in Rewired's hugo.toml). This is EXPECTED per the plan — Plan 02 creates a project-root `layouts/index.html` that shadows the theme's version and builds Rewired's actual Hero/Lens/Hosts/ComingSoon composition.

Hugo did emit one WARN during build: `WARN found no layout file for "html" for kind "taxonomy"`. This is a standard Hugo warning when taxonomies aren't defined — it's harmless and not specific to this plan's work. Plan 02 may choose to silence it by disabling unused taxonomies in hugo.toml, or leave it (it's informational only).

## Deviations from Plan

### Auto-fixed / Pre-documented

**1. [D-01 pre-documented deviation] Theme vendored via direct copy instead of Hugo module / git submodule**
- **Found during:** Task 1 (plan already anticipated this and documented the deviation path)
- **Issue:** The plan originally proposed consuming the arcaeon theme as a Hugo module OR git submodule. Verified during context gathering that the source theme at `/Users/falkensmage/RitualSync/falkensmage-website/themes/arcaeon/` has no `.git` directory inside it, and the parent `falkensmage-website` repo has no `.gitmodules` file. Both the Hugo module and git submodule paths are therefore structurally unavailable.
- **Fix:** Vendor the theme via `cp -R /Users/falkensmage/RitualSync/falkensmage-website/themes/arcaeon ./themes/arcaeon`. Treat the vendored tree as read-only — all Rewired customization goes in project-root `layouts/`, `assets/`, `static/` which Hugo's lookup order prefers over theme equivalents. If the source theme ever gets its own repo in the future, this can be retrofitted to a proper Hugo module; until then, copy-vendor is the pragmatic path.
- **Files affected:** `themes/arcaeon/` (entire tree, 20 files)
- **Commit:** `b2c48a8`

No other deviations. Plan executed as written.

## Commits (3 atomic + 1 metadata final)

- `b2c48a8` feat(01-01): scaffold Hugo project and vendor arcaeon theme (23 files, +1090 lines — includes all 20 theme files + hugo.toml + .gitignore + content/_index.md)
- `aadb864` feat(01-01): install host portraits as swap-ready static assets (2 binary JPEGs)
- `a44f515` feat(01-01): add rewired-overrides.css with warm-core palette aliases (1 file, +34 lines)
- (forthcoming) docs(01-01): complete scaffold + palette + portraits plan — metadata commit for SUMMARY.md

## File Manifest for Plan 02

Plan 02 can count on these existing:

```
/Users/falkensmage/RitualSync/rewired-site/
├── .gitignore
├── hugo.toml                                    # theme = "arcaeon", warm-core [params.colors]
├── content/
│   └── _index.md                                # stub — Plan 02 fills body
├── assets/
│   └── css/
│       └── rewired-overrides.css                # :root aliases, D-12 rules — Plan 02 extends
├── static/
│   └── images/
│       └── portraits/
│           ├── matt.jpg                         # 1024x1024, 685 KB
│           └── jaye-anne.jpg                    # 1024x1024, 778 KB — swap-ready
└── themes/
    └── arcaeon/                                 # READ-ONLY — do not modify
        ├── assets/css/main.css                  # ARCÆON :root tokens
        ├── layouts/_default/baseof.html         # to be shadowed by project-root baseof in Plan 02
        ├── layouts/index.html                   # to be shadowed by project-root index in Plan 02
        └── static/fonts/*.woff2                 # Cinzel + Space Grotesk (inherited)
```

## Self-Check: PASSED

Confirmed existence of all created files:
- `/Users/falkensmage/RitualSync/rewired-site/hugo.toml` — FOUND
- `/Users/falkensmage/RitualSync/rewired-site/.gitignore` — FOUND
- `/Users/falkensmage/RitualSync/rewired-site/content/_index.md` — FOUND
- `/Users/falkensmage/RitualSync/rewired-site/assets/css/rewired-overrides.css` — FOUND
- `/Users/falkensmage/RitualSync/rewired-site/static/images/portraits/matt.jpg` — FOUND
- `/Users/falkensmage/RitualSync/rewired-site/static/images/portraits/jaye-anne.jpg` — FOUND
- `/Users/falkensmage/RitualSync/rewired-site/themes/arcaeon/layouts/_default/baseof.html` — FOUND
- `/Users/falkensmage/RitualSync/rewired-site/themes/arcaeon/assets/css/main.css` — FOUND
- `/Users/falkensmage/RitualSync/rewired-site/themes/arcaeon/static/fonts/cinzel-latin-wght-normal.woff2` — FOUND

Confirmed all 3 task commits exist in `git log`:
- `b2c48a8` — FOUND
- `aadb864` — FOUND
- `a44f515` — FOUND
