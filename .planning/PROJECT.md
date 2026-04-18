# Rewired Site

## What This Is

A single-page MVP website for **Rewired** — the podcast by Matt Stine and Jaye Anne Beringer exploring what happens when people leave rigid belief systems and start finding something alive. The site exists to establish the show's presence, capture interest via email signup, and hand visitors a visual and tonal signal of what the show is before the first episodes drop.

## Core Value

A visitor lands, immediately gets the lens of the show, sees the two hosts, and drops their email so they don't miss the launch.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Single-page site with Hero, Lens, Hosts, Coming Soon / email capture sections
- [ ] Dual illustrated host portraits in hero (Feral Architecture medium, ARCÆON palette family)
- [ ] RitualSync warm-core palette subset (Fusion Gold, Ignition Orange, Plasma Pink) on Void Purple base with Ion Glow cyan accent for ARCÆON triad discipline
- [ ] Email capture wired to Systeme.io (Matt's CRM)
- [ ] Responsive — mobile-first, readable on phones, desktop enhances
- [ ] Deployed to a Rewired subdomain with HTTPS
- [ ] OG metadata so link previews render correctly when hosts share

### Out of Scope

- Episode list / audio player — no episodes yet, and the launch is stockpile-based (bank 6, release 3). Revisit after first recordings exist.
- RSS / podcast feed integration — belongs to the podcast host (Transistor / Buzzsprout / wherever), not the marketing site.
- CMS, blog, or dynamic content surfaces — MVP is static; adding CMS is a post-launch decision, not a pre-launch one.
- Multi-page navigation — forces information architecture work that premature for a pre-launch site.
- Analytics beyond signup count — ship first, measure later. Don't block launch on tracking fidelity.
- Newsletter automation flows inside Systeme.io — form capture is v1; welcome sequence is a separate exercise.

## Context

**Show concept:** The through-line is a lens, not a subject — people moving from rigid belief systems into something alive. Six episodes are ranked and scheduled; recording starts Sunday 2026-04-19 with "We Left the Church. The Church Didn't Leave Us." Format is Card pull → Riff → Unresolved close. Target launch: June 2026.

**Brand positioning:** Rewired lives inside the broader RitualSync / TarotPulse universe but has its own identity. Visual language pulls from the ARCÆON palette system (same family as Feral Architecture, Psyche, Digital Intuition). Rewired's subset leans toward the Radiant Core / warm register (gold / orange / pink) as distinct from Feral Architecture's cool subset (cyan / magenta).

**Assets already produced (2026-04-18):**
- Matt's Feral-Architecture-style illustrated portrait — locked at `~/Documents/Business-Brand/Feral-Architecture/portraits/2026-04-13-author-headshot/final/author-headshot.jpg`
- Jaye Anne's Feral-Architecture-style illustrated portrait — tentative v3 lock at `~/Documents/Business-Brand/Feral-Architecture/portraits/2026-04-18-jaye-anne-headshot/final/jaye-anne-headshot.jpg` (Jaye Anne still to confirm via GH Pages review at https://mstine.github.io/rewired-portrait-review/)
- Episode skeletons (six, ranked) — stored in the Google Doc and in the `podcast-with-jaye-anne` thread

**Prior-art reuse candidates:**
- The `arcaeon` Hugo theme used for `~/RitualSync/falkensmage-website` — already encodes ARCÆON palette tokens and may shortcut the build. Check feasibility in Phase 1. If it works, use it; if it forces unfit decisions, go static Astro/HTML instead.
- Systeme.io form embed pattern — already in production for RitualSync brand flows.

**Audience:** Exvangelicals, deconstruction-curious, witchcraft / Jungian / symbolic practitioners, the TarotPulse audience, and Matt's / Jaye Anne's existing networks. The site must feel adult, literary, slightly irreverent — not cute, not corporate.

## Constraints

- **Timeline**: Soft target of June 2026 launch. Site needs to be live well before first episode drops so pre-launch email capture has time to work — aim for late April or early May live date, not launch day.
- **Budget**: Cash infusion conversation with Jaye Anne is still open per the `podcast-with-jaye-anne` thread. Prefer free / cheap hosting (Cloudflare Pages, Netlify, GitHub Pages) over paid CDNs. No new paid SaaS beyond Systeme.io (already in production).
- **Tech stack**: Static site only. No server-side rendering, no database, no auth. Generator TBD in Phase 1 — Hugo (with reuse of `arcaeon` theme) is the leading candidate, Astro is the fallback if Hugo doesn't fit.
- **Design system**: ARCÆON palette family is non-negotiable — no colors from outside the pool. RitualSync warm subset is the primary emphasis for this site. Feral Architecture visual grammar (illustrated plate medium, chiaroscuro lighting) is honored in the portraits only; the surrounding site is RitualSync-warm and softer.
- **Portrait fidelity**: Jaye Anne's v3 is tentative — the build must accommodate a drop-in asset swap if she picks a different variant.
- **Voice**: Matt's public voice per `~/.psyche/identity/voice.md` — direct, structured, resonant, lightly irreverent, non-corporate. Jaye Anne's lens is embodied-practice / Energy Alchemy — respect it. No AI-generic copy.
- **Deployment**: HTTPS required. Custom subdomain (exact domain TBD — `rewired.show`, `rewiredpodcast.com`, or a subdomain on an existing RitualSync-owned domain).

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Single-page MVP concept (Option A — warm-hearth) over split-screen (Option B) or card-pull motif (Option C) | Structure in service of aliveness — minimum viable site that ships, earns the right to grow. Splitting and motif-committing were premature specificity for a pre-launch audience the show hasn't met yet. | — Pending |
| Portraits in Feral Architecture illustrated medium, matched lighting signature | Establishes a visual brand system shared across Matt's properties (Feral Arch, Psyche, Rewired), keeps portrait treatment inside the ARCÆON family, allows dual-host hero to read as "co-hosts of the same show." | — Pending |
| Site palette leans RitualSync warm core, not Feral Arch cool | Rewired is its own identity inside the RitualSync universe, not a Feral Architecture sub-brand. Warm palette signals warmth, conversation, hearth — the right tonal register for deconstruction / integration content. | — Pending |
| Email capture via Systeme.io, no separate ESP | Matt's CRM is already in production; adding another ESP would fragment the audience list and create reconciliation work later. | — Pending |
| Coarse granularity, YOLO mode, research skipped | Scope is small and well-understood; known stack constraints; execution velocity matters more than research depth at this size. | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-18 after initialization*
