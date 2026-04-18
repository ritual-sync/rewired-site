# Phase 2: Ship — Discussion Log

> **Audit trail only.** Decisions captured in CONTEXT.md.

**Date:** 2026-04-18
**Phase:** 02-ship-email-capture-deploy-shareable-link
**Mode:** `--auto` with pre-locked D-01..D-03 from Matt's inline AskUserQuestion answers
**Areas discussed:** Domain, Hosting, Email backend, Systeme.io integration method, DNS pattern, HTTPS enforcement, OG metadata, Favicon, Deploy pipeline

---

## Domain (pre-locked)

Matt's inline answer: "I just bought rewired.show".
Locked as D-01. No alternatives considered in this run.

## Hosting (pre-locked)

Matt's inline answer: GitHub Pages.
Locked as D-02. Cloudflare Pages and Netlify were offered as options and rejected in favor of GH Pages' simplicity.

## Email backend (pre-locked from Phase 1)

Systeme.io per PROJECT.md. Locked as D-03. No alternative ESPs entertained.

## Systeme.io integration method

| Option | Description | Selected |
|--------|-------------|----------|
| Direct embed in coming-soon partial | Paste Systeme.io embed snippet into existing `.rewired-coming-soon__email-placeholder` div | ✓ |
| Proxy via custom form → Systeme.io API | Custom HTML form → Cloudflare Worker (or similar) → Systeme.io API | |
| Form-action direct POST | `<form action="systeme-endpoint">` | |

**Selected:** direct embed. Least fragile, matches Matt's existing Systeme.io patterns.

## Systeme.io list targeting

| Option | Selected |
|--------|----------|
| New dedicated "Rewired — Pre-launch" list | ✓ |
| Add to existing RitualSync list with a tag | |

**Selected:** new dedicated list. Satisfies CAPT-02 directly.

## DNS pattern

| Option | Selected |
|--------|----------|
| Apex canonical + www redirect | ✓ |
| www canonical + apex redirect | |
| Apex only, no www | |

**Selected:** apex canonical + www redirect. Standard GH Pages pattern.

## HTTPS

GitHub Pages auto-issues Let's Encrypt cert via "Enforce HTTPS" toggle. No alternative considered.

## OG metadata

| Option | Selected |
|--------|----------|
| Minimal OG using Matt's portrait as v1 image (with optional quick composed dual-portrait if trivial) | ✓ |
| Full bespoke OG image design pass | (deferred to post-launch) |
| No OG metadata for MVP | |

**Selected:** minimal OG now, bespoke later if warranted.

## Favicon

| Option | Selected |
|--------|----------|
| 32×32 .ico + 180×180 apple-touch, single glyph "R" or geometric mark, Fusion Gold on Void Purple | ✓ |
| Full favicon set (16/32/48/64/96/180/192/256/512) | |
| Skip favicon, default browser treatment | |

**Selected:** minimal favicon pair. Full set is post-launch.

## Deploy pipeline

| Option | Selected |
|--------|----------|
| GitHub Actions workflow → Hugo build → actions/deploy-pages | ✓ |
| GitHub's native Hugo-on-Pages (configure-pages) | (executor fallback if deploy-pages action proves brittle) |
| Manual build + push gh-pages branch | |

**Selected:** GH Actions + actions/deploy-pages. Executor can pivot to native if the action has issues.

## Claude's Discretion

- Exact repo name (`rewired-site`, `rewired`, `rewired.show`)
- Whether to produce composed dual-portrait OG image during Phase 2 or defer
- Pinning specific action versions
- Whether to add a separate CI build-check workflow

## Deferred Ideas

See CONTEXT.md `<deferred>` section. Bespoke OG art, analytics, welcome drip, 404 copy, robots.txt — all deferred out of Phase 2.
