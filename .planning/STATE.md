# STATE: Rewired Site

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-04-18)

**Core value:** A visitor lands, immediately gets the lens of the show, sees the two hosts, and drops their email so they don't miss the launch.
**Current focus:** Phase 2 in flight — email capture + deploy to rewired.show

## Current Phase

**Phase 2: Ship — Email capture, deploy, shareable link** — executing (2 plans, 8 tasks, 4 human checkpoints)

- [ ] Plan 02-01 — code changes (baseURL, OG meta, favicon, OG image, CNAME, Substack embed)
- [ ] Plan 02-02 — deploy (GitHub Actions, repo, DNS, HTTPS, smoke test)

Phase 1 verified by Matt 2026-04-18 (verification not captured in docs at the time).

## Recent Activity

- 2026-04-18 — Project initialized. PROJECT.md, REQUIREMENTS.md, ROADMAP.md, config.json written. Tight MVP scope, 2 phases, coarse granularity, YOLO mode, research skipped.
- 2026-04-18 — Concept locked (Option A — warm-hearth MVP). Palette: RitualSync warm subset on Void Purple base. Portraits: Feral Architecture medium, dual hero placement.
- 2026-04-18 — Jaye Anne portrait v3 tentatively locked at `~/Documents/Business-Brand/Feral-Architecture/portraits/2026-04-18-jaye-anne-headshot/final/jaye-anne-headshot.jpg`. GH Pages review live at https://mstine.github.io/rewired-portrait-review/ — Jaye Anne's final pick pending.
- 2026-04-18 — Plan 01-01 executed. Hugo project scaffolded at /Users/falkensmage/RitualSync/rewired-site/. Arcaeon theme vendored read-only. Both portraits installed at `static/images/portraits/`. `rewired-overrides.css` wired with warm-core palette aliases + D-12 responsive/touch-target guardrails. Baseline `hugo --minify` exits 0.
- 2026-04-18 — Plan 01-02 executed. Project-level `layouts/_default/baseof.html` + `layouts/index.html` shadow the theme. Four section partials (hero / lens / hosts / coming-soon) wired to `content/_index.md` frontmatter. Extended rewired-overrides.css with hero/lens/hosts/coming-soon rules, three responsive breakpoints (768/1024/1440), global :focus-visible Ion Glow ring. Built HTML renders all four sections in correct DOM order; all 5 canonical copy strings present; zero hex leaks in overrides CSS; theme directory untouched. Requirements ticked: SITE-03, HERO-01, HERO-02, CONT-01, CONT-02, CONT-03. Commits: 0038f9e, c700cdb, 08ed567. See `.planning/phases/01-build-static-site-content-portraits-palette/01-02-SUMMARY.md`.

## Assets & References

- **Matt's portrait:** `~/Documents/Business-Brand/Feral-Architecture/portraits/2026-04-13-author-headshot/final/author-headshot.jpg`
- **Jaye Anne's portrait (v3 tentative):** `~/Documents/Business-Brand/Feral-Architecture/portraits/2026-04-18-jaye-anne-headshot/final/jaye-anne-headshot.jpg`
- **Portrait review (public):** https://mstine.github.io/rewired-portrait-review/
- **Palette canonical reference:** `~/.psyche/swipe-files/podcasting-creative/2026-04-16-12-33-18-arc-on-color-palette-full.md`
- **Feral Architecture aesthetic contract:** `~/Documents/Business-Brand/Feral-Architecture/covers/TEMPLATE.md`
- **Prior-art Hugo theme candidate:** `arcaeon` theme used at `~/RitualSync/falkensmage-website`
- **Linked Psyche thread:** `podcast-with-jaye-anne`

## Open Threads

- Domain / subdomain choice — not yet picked. Options: `rewired.show`, `rewiredpodcast.com`, subdomain on RitualSync-owned domain. Phase 2 decides.
- Jaye Anne's final portrait pick. If she picks v1 or v2, swap the single asset in `images/` — no code change required.
- Cash infusion conversation entangled via `podcast-with-jaye-anne` thread — may affect deploy timing but not MVP scope.
