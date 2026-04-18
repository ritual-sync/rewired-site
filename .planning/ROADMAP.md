# Roadmap: Rewired Site

**Created:** 2026-04-18
**Target launch:** Live before first episode drops (aim late April / early May 2026)
**Phases:** 2 (Tight MVP)

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

---

## Phase 2: Ship — Email capture, deploy, shareable link

**Goal:** Site is publicly live at a Rewired subdomain with working email capture to Systeme.io and correct link previews when shared. Visitor can drop their email and get a confirmation.

**Requirements:** CAPT-01, CAPT-02, CAPT-03, CAPT-04, DEPL-01, DEPL-02, DEPL-03, DEPL-04, DEPL-05

**Success criteria:**
1. A test email submitted from production lands in a Rewired-specific Systeme.io list (not mixed with other RitualSync lists).
2. Successful submission shows an inline confirmation state without a page reload or redirect away.
3. The live URL returns HTTPS, loads in under 2 seconds on cellular, and renders correctly on iOS Safari, Chrome Android, Firefox desktop.
4. Sharing the URL in iMessage, Slack, and a Twitter/Threads-equivalent compose box produces a correct Open Graph preview with show name, tagline, and at least one host portrait.
5. Pushing to `main` triggers an automatic deploy; no manual steps in the deploy path.

**Exit:** a shareable URL that Matt can paste into a DM to Jaye Anne and to his existing network without cringe, and the first email signups start landing in Systeme.io.

---

## Coverage check

All 20 v1 requirements are mapped across the 2 phases. No v1 gaps.

## Milestone exit

When Phase 2 succeeds, the site is MVP-live. Post-launch decisions (episode surfaces, analytics, welcome sequence) move from v2 into a new milestone driven by observed signal — signup rate, feedback from early subscribers, and whether episodes are actually getting recorded on cadence.
