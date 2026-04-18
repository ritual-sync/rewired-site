# Phase 2 Addendum — Post-plan Polish

**Recorded:** 2026-04-18
**Covers:** work done outside the formal Plan 02-01 / Plan 02-02 flow, after both plans' SUMMARY.md files marked the phase complete.

## Why this exists

Plans 02-01 and 02-02 closed all of Phase 2's originally-scoped requirements (CAPT-01..04, DEPL-01..05) and the site went live at https://rewired.show/. After that, an extended session iterated on polish that materially improved the ship-ready state but wasn't captured in the original plans. This addendum records what changed, why, and where to find it — so a future session (or a future reader) doesn't have to reconstruct it from git archaeology.

Nothing here reopens or contradicts Plan 02-01 / Plan 02-02's SUMMARY.md records — both remain accurate for their scope. This is strictly delta.

---

## Changes

### 1. Branded subscribe button replacing the Substack iframe

**Commit:** `1062feb`
**Files:** `layouts/partials/sections/coming-soon.html`, `assets/css/rewired-overrides.css`

Plan 02-01 Task 5 wired Substack's iframe embed directly into the Coming Soon partial. Smoke-testing (Plan 02-02 Task 5) revealed Substack's embed pops a new tab into their multi-screen subscribe flow rather than confirming inline — so the iframe's role was effectively "a styled link to Substack." Since iframe contents are cross-origin and cannot be repainted from rewired.show, any palette-clash with the site is structural.

**Fix:** replaced the iframe with a Rewired-branded `<a>` button targeting `https://rewiredshow.substack.com/subscribe`. Same flow, full palette control. Ignition Orange bg (D-11 `--rewired-cta`), Void Purple text (AAA contrast), Fusion Gold on hover (palette-legal warm-to-warmer shift), box-shadow lift, small external-link glyph. Touch-target via existing `.rewired-cta` class; keyboard-focus ring via the global `:focus-visible` rule.

**Pairs with:** Jaye Anne also set the Substack publication theme to match the ARCÆON palette, so the destination page after the click is visually continuous with the site.

### 2. Rewired logo generation (3 rounds, Gemini + Feral Architecture template)

**External workspace:** `~/Documents/Business-Brand/Rewired/logos/v1/`
**Public review site:** https://ritual-sync.github.io/rewired-logo-review/
**Review repo:** `ritual-sync/rewired-logo-review`

Adapted the Feral Architecture cover generation template (`~/Documents/Business-Brand/Feral-Architecture/covers/TEMPLATE.md`) to produce square 1024×1024 brand marks for Rewired. Key adaptations:

- Palette pivot: F3's cyan/magenta → Rewired's warm-core subset (Void Purple + Fusion Gold + Ignition Orange + Solar White per D-11)
- Format: 1024×1024 square instead of 1200×628 landscape
- Subject: sigil/mark as foreground (not scene with human figure)
- No wordmark in the image (reserved for the Cinzel wordmark elsewhere on the page)

**Three concepts explored in Round 1** (3 variants each, 9 total images):
- A — Rewiring Sigil: rigid circuit trace severed, re-routed into organic root
- B — Broken Circle Healing: gold ring mid-rejoin with forge-weld ember
- C — R-as-Sigil: Cinzel-adjacent R with flame in the bowl and root below the stem

**Round 1 feedback** (Matt + Jaye Anne reviewing together): A rejected (poor favicon scaling, didn't land); B concept strong but execution weak (break too subtle, ember too small, handmade read as sloppy, center dot out of place, concept didn't land); C v3 letterform strong, v1 flame preferred over v3's.

**Round 2:** fresh-executed B (3 variants with tighter prompt — bigger break, substantial forge-weld, line-weight variation, empty center, "engraved authority"); composite C (v3 letterform × v1 flame via multi-reference compositing).

**Round 3:** three-way composite B (r2v3 base × r2v1 flame × r1v2 criss-cross knot joinery).

**Winners locked:**
- `~/Documents/Business-Brand/Rewired/logos/v1/final/rewired-mark.jpg` — the R (primary brand mark)
- `~/Documents/Business-Brand/Rewired/logos/v1/final/rewired-sigil.jpg` — the ring (secondary / closing sigil)

Site uses 512×512 resized JPEGs at `static/images/logos/`.

### 3. Logos placed on the site

**Commit:** `aa232fc`
**Files:** `layouts/partials/sections/hero.html`, new `layouts/partials/sections/closing-sigil.html`, `layouts/index.html`, `assets/css/rewired-overrides.css`, new `static/images/logos/rewired-mark.jpg` + `rewired-sigil.jpg`

- **R mark** sits above the "Rewired" Cinzel wordmark in the hero, clamped 120–200px, centered. Publication-heraldry lockup: mark → wordmark → portraits → tagline.
- **Ring sigil** added to a new closing section below Coming Soon. Smaller (clamped 100–160px) — page punctuation, not a headline. Section bg is Void Purple so the JPEG's baked-in Void Purple background mats flush. Continues the alternating section-bg pattern (void → depth → void → depth → void).
- Both JPEGs were resized from 1024×1024 to 512×512 at q85 (~50KB each) before shipping.

### 4. Favicon + OG image swapped to the R mark

**Commits:** `93dfc7b` (favicon), `35735e9` (OG v2 via Pillow)
**Files:** `static/favicon.png` (new), `static/favicon.ico` (regenerated), `static/apple-touch-icon.png` (regenerated), `static/favicon.svg` (deleted — was a placeholder), `static/images/og/rewired-og.jpg` (regenerated), `layouts/_default/baseof.html` (link tags updated)

Plan 02-01 Task 2 shipped placeholder favicon assets — a hand-drawn SVG R glyph + derived PNG/ICO. Once the real R mark existed:

- `static/favicon.svg` removed (not representative of the new brand)
- New `static/favicon.png` (32×32, 2.3KB) derived from `rewired-mark.jpg`
- `static/favicon.ico` (32×32, 3.3KB) regenerated from the same
- `static/apple-touch-icon.png` (180×180, 45KB) regenerated from the same
- `baseof.html` link tags: PNG now first (modern browsers prefer), ICO as legacy fallback, apple-touch as before

**OG image** also got a proper composition pass — see Change 8 for the pipeline details.

### 5. Rounded corners on logo marks

**Commit:** `1570adf`
**Files:** `assets/css/rewired-overrides.css`

Matt: *"round the corners on the logos like on the portraits."* Added `border-radius: 12px` to `.rewired-hero__mark` and `.rewired-closing__sigil` to match `.rewired-hero__portrait`'s existing 12px radius. Consistent rounded-corner language across all rasters on the page.

### 6. Portraits side-by-side at all widths

**Commit:** `aed3f3c`
**Files:** `assets/css/rewired-overrides.css`

**Supersedes D-06 partially.** The original phase context locked "portraits side-by-side desktop (>=768px) / stacked mobile (Matt above Jaye Anne)." Matt reversed this after seeing the site live: *"reflow the portraits on mobile so they're still side-by-side."*

**Rationale:** the two-host identity reads more clearly when the pair stays paired at every width. The stacked mobile layout made the show feel like two separate people on a small screen.

**Implementation:** `flex-direction: row` at base (was `column`). `.rewired-hero__portrait` switched from `width: 100%; max-width: 420px` to `flex: 1 1 0; min-width: 0; max-width: 380px` — flex children share the container equally, capped per-portrait. Gap tightened on mobile (`clamp(0.75rem, 2.5vw, 2rem)`). The 768px media query still bumps hosts__grid to two columns; the portrait rules there are now redundant and removed.

### 7. Host bios iterated to v3

**Commit:** `4cf2ab4`
**Files:** `content/_index.md`

Both hosts' bios rewritten. The originals had two issues:

1. **Matt's bio performed a dichotomy** ("enterprise systems architect by day, witch and Jungian co-conspirator by everything else") that the show's thesis explicitly rejects. Integration-forward version leads with "In the world where grep and The Morrigan are equally real" (Feral Architecture template language) and lists four identities flat: chaos witch, archetypal tarotist, Jungian depth coach, enterprise systems architect.

2. **Jaye Anne's bio was rewritten from her own site copy at embodiedalchemyhealing.com** to land her authentic voice. Preserves her distinctive relational hook ("the reason most of the hard questions get asked in the first place"). Adds "tarotist" per the show's pairing spec.

**Both bios now include:**
- RitualSync co-founder hook reciprocating each other ("with Jaye Anne" / "with Matt")
- TarotPulse attribution linking to the correct URL — **`mytarotpulse.com`**, not `tarotpulse.com` as Phase 1 had incorrectly. This was a live URL bug on the deployed site for several hours.

**Still pending:** Jaye Anne is writing her own bio draft and will send it. The v3 above is a strong holding pattern; swap to her own words when they arrive.

### 8. OG image composition pipeline — Pillow + fontTools (supersedes rsvg-convert)

**Commit:** `35735e9`
**Files:** new `scripts/compose-og.py`, regenerated `static/images/og/rewired-og.jpg`

Plan 02-01 Task 3 used `rsvg-convert` to rasterize a hand-composed SVG into the OG JPEG. Turned out to be subtly broken in two ways that weren't caught by smoke tests:

1. **`rsvg-convert ≥ 2.60` silently blocks external `file://` references** from `<image xlink:href="file://...">` elements. The Plan 02-01 OG image was therefore text-only against a Void Purple canvas — the portraits and mark never rendered. Matt flagged it mid-session as "kinda bland."

2. **`rsvg-convert` uses system fonts via fontconfig.** Cinzel and Space Grotesk only ship as woff2 web fonts in the arcaeon theme. So the wordmark was rendering in Georgia/serif (the CSS fallback), not matching the site's typography. Matt flagged it as "typeface doesn't match the website."

**New pipeline:** `scripts/compose-og.py` — Pillow composites the image directly from JPGs (no URL security layer), and fontTools converts the theme's woff2 files to TTF at runtime so Pillow can render with the exact site typefaces.

**Layout:** trinity row at top (Matt portrait | R mark | Jaye Anne portrait, each 280×280 with 40px gaps, centered). Cinzel "Rewired" wordmark + Space Grotesk tagline stacked below. 84KB output, well under the 400KB hard ceiling.

**Regeneration:** `python3 scripts/compose-og.py` from the repo root. Idempotent. After any OG change, force a re-scrape on social scrapers (Facebook Debugger, Twitter Card Validator, Slack, iMessage) — their caches are aggressive.

---

## Decisions Made (cumulative)

- **D-11 override (partial):** portraits side-by-side at all widths, supersedes "stacked mobile."
- **New — primary brand mark:** R sigil (`rewired-mark.jpg`). Locked winner from Concept C Round 2 composite (v3 letterform × v1 flame).
- **New — secondary brand mark:** broken-circle-healing ring (`rewired-sigil.jpg`). Locked winner from Concept B Round 3 three-way composite.
- **New — subscribe flow:** Rewired-branded button, not Substack iframe. Substack publication theme handles the post-click page.
- **New — OG pipeline:** Pillow + fontTools, never rsvg-convert for images+fonts compositions on this project.
- **Correction — TarotPulse URL:** `mytarotpulse.com`. The `tarotpulse.com` link shipped in Phase 1 was a live bug.
- **Bio voice framing (both hosts):** integration-forward, no by-day/by-night split, seam-line upfront. Canonical titles for Matt: chaos witch, archetypal tarotist, Jungian depth coach, enterprise systems architect. For Jaye Anne: Embodied Alchemy healer, somatic cycle-breaker, tarotist.

---

## Requirements Impact

All Phase 2 requirements remain ✓ closed (CAPT-01..04, DEPL-01..05). The addendum work strengthens the ship-ready state without opening new requirements or invalidating closed ones.

**CAPT-01 (subscribe form embedded):** now served by the Rewired-branded button → same Substack endpoint. Contract honored.
**CAPT-02 (dedicated Rewired publication):** unchanged, confirmed via Plan 02-02 smoke test.
**CAPT-03 (host page stays on apex):** reinforced — the new button uses `target="_blank"`, so rewired.show never redirects.
**DEPL-03 (OG preview quality):** materially improved. Plan 02-01's OG was a latent bug (text-only) that would have shipped stale-looking previews. Now fixed.
**DEPL-04 (favicon installed):** upgraded from placeholder to real brand mark.

---

## Assets Added/Changed

**Added to repo:**
- `static/images/logos/rewired-mark.jpg` (512×512, ~50KB)
- `static/images/logos/rewired-sigil.jpg` (512×512, ~50KB)
- `static/favicon.png` (32×32)
- `layouts/partials/sections/closing-sigil.html` (new partial)
- `scripts/compose-og.py` (OG regeneration tool)

**Regenerated:**
- `static/favicon.ico` (from R mark, was from placeholder)
- `static/apple-touch-icon.png` (from R mark, was from placeholder)
- `static/images/og/rewired-og.jpg` (trinity composition, was text-only)

**Removed from repo:**
- `static/favicon.svg` (placeholder no longer representative)

**External (not in repo):**
- `~/Documents/Business-Brand/Rewired/logos/v1/` — full design workspace
- `~/RitualSync/rewired-logo-review/` — review site source for `ritual-sync/rewired-logo-review` repo

---

## Follow-ups / Open Items (non-blocking)

- **Jaye Anne's own bio draft en route.** Swap to her own words when they arrive. RitualSync/TarotPulse framings should stay intact; her voice block is what changes.
- **Jaye Anne's Substack collaborator invite** still pending acceptance. Once accepted, she can edit the Rewired publication directly.
- **Node.js 20 deprecation** on GitHub Actions — `actions/checkout@v4`, `actions/configure-pages@v5`, `peaceiris/actions-hugo@v3`, `actions/deploy-pages@v4`. Advisory only; must be bumped before 2026-06-02.
- **Phase 3 (Listener Experience) is trigger-gated** by first episodes existing on the Rewired Substack. Not ready to plan.
- **Social-scraper cache** on previously-shared URL instances may show stale v1 OG until force-refreshed via FB Debugger / Twitter Card Validator.

---

## Commits (chronological, post-Phase-2-completion)

| # | SHA | Subject |
|---|-----|---------|
| 1 | `1062feb` | feat(ui): replace Substack iframe with Rewired-branded subscribe button |
| 2 | `aa232fc` | feat(ui): Rewired brand mark (R sigil) in hero + closing sigil (ring) |
| 3 | `93dfc7b` | feat(ui): favicon + OG image swapped to the Rewired R mark |
| 4 | `1570adf` | style(ui): round the logo corners to match portraits (12px) |
| 5 | `aed3f3c` | style(ui): portraits side-by-side at all widths (reflow mobile from stacked) |
| 6 | `4cf2ab4` | content: iterate host bios (v3) |
| 7 | `35735e9` | feat(og): Pillow-composited OG image — trinity layout (portraits + R mark) |

All seven commits are on `main`, pushed to `ritual-sync/rewired-site`, and deployed live to https://rewired.show/.
