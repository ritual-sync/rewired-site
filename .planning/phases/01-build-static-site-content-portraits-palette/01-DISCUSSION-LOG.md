# Phase 1: Build — Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-18
**Phase:** 01-build-static-site-content-portraits-palette
**Mode:** `--auto` (recommended defaults selected non-interactively per user's YOLO config)
**Areas discussed:** Static site generator, Portrait integration, Typography, Hero composition, Content copy, Palette application, Responsive & A11y

---

## Static Site Generator

| Option | Description | Selected |
|--------|-------------|----------|
| Hugo + arcaeon theme reuse | Consume existing arcaeon theme as Hugo module; shortest path | ✓ |
| Astro greenfield | Modern, MDX-capable; fresh CSS; no theme to wrangle | |
| Plain HTML + CSS | Zero build complexity; every styling decision bespoke | |

**Selected:** Hugo + arcaeon theme reuse.
**Notes:** Theme already encodes ARCÆON palette and typography. Fallback to Astro documented if theme forces unfit layout decisions.

---

## Portrait Integration

| Option | Description | Selected |
|--------|-------------|----------|
| Copy into `static/images/portraits/` at project init | Files live in the project; swap by overwriting single file | ✓ |
| External absolute-path reference | Points at `~/Documents/.../final/...jpg` directly | |
| Git LFS / asset repo | Track large images separately; deploy target pulls them | |

**Selected:** Copy into `static/images/portraits/`.
**Notes:** Jaye Anne's v3 swap = single-file replacement. No content edit required when she confirms.

---

## Typography

| Option | Description | Selected |
|--------|-------------|----------|
| Fraunces display + Inter body | Literary serif header, clean sans body | ✓ |
| Full serif stack | Heavier literary register, may feel heavy on mobile | |
| Full sans stack | Cleaner / more modern, less distinctive | |

**Selected:** Fraunces display + Inter body (or arcaeon theme's existing choices if already matched).
**Notes:** Inherit from theme first; override only if the theme's choices fight the adult/literary register.

---

## Hero Composition

**Q1: Show name placement.**
| Option | Selected |
|--------|----------|
| Show name above portraits, centered | ✓ |
| Show name below portraits | |
| Show name overlaid on portraits | |

**Q2: Portrait layout.**
| Option | Selected |
|--------|----------|
| Side-by-side desktop, stacked mobile | ✓ |
| Always stacked | |
| Asymmetric overlap | |

**Q3: Lens line placement.**
| Option | Selected |
|--------|----------|
| Directly below portraits | ✓ |
| Next to show name | |

**Selected layout:** Show name (top, Fusion Gold, display weight) → portraits side-by-side (desktop) / stacked (mobile) → one-line lens (Solar White, display-scale body weight).

---

## Content Copy

**Q1: One-line lens.**
- "We left the systems. We're finding what's alive." ✓ (recommended)
- "For the deconstructed and the feral."
- "Leaving what was. Finding what's alive."

**Q2: Host bio tone.**
- Short, warm, slightly irreverent, bylines linked ✓
- Formal professional bio |
- Longer personal-essay style |

**Q3: Coming Soon copy.**
- "First episodes drop June 2026. Leave your email so you don't miss it." ✓
- "Coming soon." (too terse)
- "Join the waiting list!" (reads like a SaaS, wrong register)

**Selected:** lens as recommended; short warm bio treatment; plain Coming Soon copy. Executor treats copy as v0 drafts; Matt final-calls before shipping Phase 1.

---

## Palette Application

Palette-role rules decided without alternative tables — values baked into D-11:
- Void Purple: page bg
- Fusion Gold: show name, h2
- Ignition Orange: CTAs, key phrase accents
- Plasma Pink: link hover, subtle accents
- Ion Glow cyan: one accent (email input focus ring) — preserves ARCÆON triad discipline
- Solar White: body text
- Deep Indigo: subtle dividers
- Electric Violet: atmospheric depth only

**Rule:** nothing from outside the ARCÆON pool. Ever.

---

## Responsive & A11y

**Q: Mobile-first breakpoints.**
| Option | Selected |
|--------|----------|
| base ≤ 480 / 768 / 1024 / 1440 | ✓ |
| mobile-first single breakpoint | |

**Q: Motion policy.**
| Option | Selected |
|--------|----------|
| No auto-motion; only on user interaction | ✓ |
| Subtle on-load animation | |
| None / static | |

**Selected:** standard mobile-first breakpoint ladder; no auto-motion; WCAG AA contrast; ≥ 44×44px touch targets.

---

## Claude's Discretion

Executor decides:
- Hugo section taxonomy (single-page `_index.md` vs partials-heavy decomposition)
- CSS custom property naming
- Font loading strategy
- Whether to include a minimal favicon stub in Phase 1 (non-blocking; full favicon set is Phase 2 / DEPL-04)

## Deferred Ideas

See CONTEXT.md `<deferred>` section. Episode list, RSS, CMS, analytics, welcome sequence, full favicon set, tarot "card of the episode" surfacing — all deferred out of Phase 1.
