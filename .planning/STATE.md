# STATE: Rewired Site

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-04-18)

**Core value:** A visitor lands, immediately gets the lens of the show, sees the two hosts, and drops their email so they don't miss the launch.
**Current focus:** Phase 2 complete — site live at https://rewired.show/. MVP shipped. Next: Phase 3 (Listener Experience) once first episodes exist.

## Current Phase

**Phase 2: Ship — Email capture, deploy, shareable link** — complete (both plans shipped)

- [x] Plan 02-01 — code changes (baseURL, OG meta, favicon, OG image, CNAME, Substack embed)
- [x] Plan 02-02 — deploy (GitHub Actions, repo, DNS, HTTPS, smoke test)

All Phase 2 requirements closed: CAPT-01..04, DEPL-01..05. Live URL: https://rewired.show/.

## Recent Activity

- 2026-04-18 — Project initialized. PROJECT.md, REQUIREMENTS.md, ROADMAP.md, config.json written. Tight MVP scope, 2 phases, coarse granularity, YOLO mode, research skipped.
- 2026-04-18 — Concept locked (Option A — warm-hearth MVP). Palette: RitualSync warm subset on Void Purple base. Portraits: Feral Architecture medium, dual hero placement.
- 2026-04-18 — Jaye Anne portrait v3 tentatively locked at `~/Documents/Business-Brand/Feral-Architecture/portraits/2026-04-18-jaye-anne-headshot/final/jaye-anne-headshot.jpg`. GH Pages review live at https://mstine.github.io/rewired-portrait-review/ — Jaye Anne's final pick pending.
- 2026-04-18 — Plan 01-01 executed. Hugo project scaffolded at /Users/falkensmage/RitualSync/rewired-site/. Arcaeon theme vendored read-only. Both portraits installed at `static/images/portraits/`. `rewired-overrides.css` wired with warm-core palette aliases + D-12 responsive/touch-target guardrails. Baseline `hugo --minify` exits 0.
- 2026-04-18 — Plan 01-02 executed. Project-level `layouts/_default/baseof.html` + `layouts/index.html` shadow the theme. Four section partials (hero / lens / hosts / coming-soon) wired to `content/_index.md` frontmatter. Extended rewired-overrides.css with hero/lens/hosts/coming-soon rules, three responsive breakpoints (768/1024/1440), global :focus-visible Ion Glow ring. Built HTML renders all four sections in correct DOM order; all 5 canonical copy strings present; zero hex leaks in overrides CSS; theme directory untouched. Requirements ticked: SITE-03, HERO-01, HERO-02, CONT-01, CONT-02, CONT-03. Commits: 0038f9e, c700cdb, 08ed567. See `.planning/phases/01-build-static-site-content-portraits-palette/01-02-SUMMARY.md`.
- 2026-04-18 — Plan 02-01 executed. Production baseURL (`https://rewired.show/`), OG + Twitter + canonical meta in baseof.html, ARCÆON favicon set (svg + native ICO + 180×180 apple-touch), v1 dual-portrait OG image (1200×630 JPEG, 34.7 KB), CNAME, Substack iframe wired into coming-soon.html. Publication: **rewiredshow.substack.com** (bare `rewired` was taken). Jaye Anne invited but not yet confirmed as collaborator. Commits: 97daa80, ba25586, 65f3fe0, 3ba294c, 5950c45. See `02-01-SUMMARY.md`.
- 2026-04-18 — Plan 02-02 executed. Repo created at **ritual-sync/rewired-site** (public). GitHub Actions workflow (Hugo 0.160.1 via peaceiris/actions-hugo@v3, native Pages chain). DNS: 4 apex A records + www CNAME → `ritual-sync.github.io`. Let's Encrypt cert issued; Enforce HTTPS on via UI. Site live at **https://rewired.show/**, www 301s to apex, http 301s to https. Smoke tests: subscribe success (new-tab flow — host page stays on apex), subscribe failure, Substack subscriber landing, OG previews on iMessage + Slack + Threads/X all ✓. Commit: 88e1e75. See `02-02-SUMMARY.md`.

## Assets & References

- **Matt's portrait:** `~/Documents/Business-Brand/Feral-Architecture/portraits/2026-04-13-author-headshot/final/author-headshot.jpg`
- **Jaye Anne's portrait (v3 tentative):** `~/Documents/Business-Brand/Feral-Architecture/portraits/2026-04-18-jaye-anne-headshot/final/jaye-anne-headshot.jpg`
- **Portrait review (public):** https://mstine.github.io/rewired-portrait-review/
- **Palette canonical reference:** `~/.psyche/swipe-files/podcasting-creative/2026-04-16-12-33-18-arc-on-color-palette-full.md`
- **Feral Architecture aesthetic contract:** `~/Documents/Business-Brand/Feral-Architecture/covers/TEMPLATE.md`
- **Prior-art Hugo theme candidate:** `arcaeon` theme used at `~/RitualSync/falkensmage-website`
- **Linked Psyche thread:** `podcast-with-jaye-anne`

## Open Threads

- Jaye Anne's final portrait pick. If she picks v1 or v2, swap the single asset in `images/` — no code change required.
- Jaye Anne's Substack collaborator invite — accept pending.
- Cross-device coverage: Matt smoke-tested iOS Safari + Firefox desktop; Chrome Android unverified (organic coverage once URL is shared).
- Substack embed UX (new-tab multi-screen, not inline). Functional pass, but a custom form POSTing directly to Substack is a Phase 3 candidate if the new-tab friction costs signups.
- Node.js 20 deprecation on deploy workflow actions — bump before 2026-06-02.
- Cash infusion conversation entangled via `podcast-with-jaye-anne` thread.
