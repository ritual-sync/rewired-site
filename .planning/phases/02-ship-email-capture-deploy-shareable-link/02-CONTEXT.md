# Phase 2: Ship — Email capture, deploy, shareable link - Context

**Gathered:** 2026-04-18
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase takes Phase 1's locally-built static site and puts it on the public internet at `rewired.show` with working email capture wired to Systeme.io, automatic HTTPS, and correct link previews when the URL is shared. When Phase 2 closes, Matt can send the URL to Jaye Anne in iMessage and the first email signups start landing in a Rewired-specific Systeme.io list.

**In scope:** Systeme.io form integration into the existing Coming Soon placeholder, GitHub Pages deployment pipeline, rewired.show DNS + CNAME wiring, HTTPS enforcement, Open Graph / Twitter Card metadata, favicon set, push-to-main auto-deploy.

**Explicitly out of this phase** (v2 / deferred):
- Episode list / audio player (no episodes yet)
- RSS integration (podcast host handles this)
- Analytics beyond signup count (ship-first; CAPT-02 signup count via Systeme.io is enough for MVP signal)
- Welcome-email sequence inside Systeme.io (list capture is v1; drip is a separate exercise)
- OG image dedicated design pass (use Matt's locked portrait or a simple composition in Phase 2; bespoke OG art is post-launch)

</domain>

<decisions>
## Implementation Decisions

### Load-bearing (locked by Matt)

- **D-01:** **Domain: `rewired.show`.** Matt purchased this domain today. It is ready for DNS configuration — no alternate domain candidates. Apex (`rewired.show`) is canonical; `www.rewired.show` redirects to apex.
- **D-02:** **Hosting: GitHub Pages** — push-to-main auto-deploy, free, HTTPS via Let's Encrypt (GitHub's native integration). Repo is `mstine/rewired-site` or equivalent (to be confirmed during execution — Matt may prefer a specific repo name).
- **D-03:** **Email capture backend: Systeme.io** — Matt's CRM, already in production across other RitualSync brand flows. No second ESP; no newsletter-service fragmentation.

### Systeme.io Integration (D-04, D-05)

- **D-04:** **Systeme.io form embedded via their HTML embed snippet, dropped into the existing `rewired-coming-soon__email-placeholder` div Phase 1 pre-built in `layouts/partials/sections/coming-soon.html`.** Matt generates the form inside Systeme.io (new list: "Rewired — Pre-launch"), copies the embed code, and either (a) pastes the embed directly into the Hugo partial, or (b) hooks it in via a site-config parameter in `hugo.toml` so copy lives in config not template. Executor's call based on whether the embed snippet is stable or has per-form identifiers that change.
- **D-05:** **New dedicated Systeme.io list: "Rewired — Pre-launch"** (or similar naming). Captured emails go here, NOT into any existing RitualSync / TarotPulse / Falken's Labyrinth list — this satisfies CAPT-02 explicitly. Matt creates the list in Systeme.io during execution; executor documents the list name and list ID in SUMMARY.md.

### DNS & HTTPS (D-06, D-07)

- **D-06:** **DNS pattern: apex + www.** `rewired.show` serves the canonical content. `www.rewired.show` issues a 301 redirect to the apex (GitHub Pages handles this automatically when both are set up). DNS records:
  - 4× A records on apex pointing to GitHub Pages IPs: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
  - CNAME `www` → `mstine.github.io` (or the user's pages-host, confirm during execution)
  - Repo-root `CNAME` file containing the single line `rewired.show`
- **D-07:** **HTTPS enforced via GitHub Pages "Enforce HTTPS" toggle** — Let's Encrypt cert issuance is automatic after DNS propagates. No manual cert management. If the cert hasn't issued within ~24h, file a Psyche issue per Matt's "file issues from field" rule rather than fighting the platform.

### Open Graph / Twitter Cards (D-08)

- **D-08:** **Minimal OG metadata in `layouts/_default/baseof.html` `<head>`**:
  - `og:title` → "Rewired"
  - `og:description` → the one-line lens from HERO-02 ("We left the systems. We're finding what's alive.")
  - `og:image` → Matt's locked illustrated portrait as the v1 OG image (repurposes existing asset, no new design work). If quick to produce, a composed dual-portrait OG image at `static/images/og/rewired-og.jpg` (1200×630) is better — executor uses existing portraits side-by-side, on Void Purple background, with the show name in Fusion Gold. Bespoke OG art is a post-launch exercise; don't block Phase 2 on it.
  - `og:type` → website, `og:url` → `https://rewired.show/`
  - Twitter card: `summary_large_image`, `twitter:title`, `twitter:description`, `twitter:image` mirror OG values
  - `canonical` link tag pointing to `https://rewired.show/`

### Favicon (D-09)

- **D-09:** **Minimal favicon set generated during execution**, not a design phase:
  - 32×32 `favicon.ico` at repo root
  - 180×180 `apple-touch-icon.png`
  - Single glyph: letterform "R" in Fusion Gold on Void Purple background, or a simple geometric mark (a broken-circle echoing ARCÆON sigil grammar)
  - ARCÆON palette discipline holds — no colors outside the family
  - Generated via ImageMagick, a simple SVG→PNG pipeline, or Matt's preferred tool. Claude's discretion.

### Deploy Pipeline (D-10)

- **D-10:** **GitHub Actions workflow `.github/workflows/deploy.yml`** that runs on push to `main`:
  - Checks out repo (including theme submodule / vendored dir)
  - Installs Hugo (pinned version matching local dev — executor reads `hugo version` and pins it)
  - Runs `hugo --minify` to build into `public/`
  - Deploys to GitHub Pages using the actions/deploy-pages action (or equivalent)
  - Alternative: GitHub's native Hugo-on-Pages path via `actions/configure-pages` + `actions/jekyll-build-pages` (Hugo variant). Executor picks whichever is least brittle. Document the choice in SUMMARY.md.

### Claude's Discretion

- **Exact GitHub repo name** — `rewired-site`, `rewired`, `rewired.show` — executor asks during the `gh repo create` step or uses whichever matches Matt's naming pattern for his other GH repos.
- **Whether to produce a composed dual-portrait OG image in Phase 2 or defer to post-launch** — executor's call based on tooling available. If ImageMagick composition is trivial, do it. If it needs a full round trip through Gemini image gen, defer to a post-launch phase and use Matt's portrait only for v1 OG.
- **Exact GitHub Actions action versions** — pin to major versions (`@v4`, etc.) and document.
- **Whether to add a quick CI build-check workflow** separate from deploy (catches Hugo build errors on PR without deploying) — recommended, but not blocking for MVP. Executor's call.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Context
- `.planning/PROJECT.md` — Rewired Site project context; see Key Decisions table for the D-01 domain/hosting constraints
- `.planning/REQUIREMENTS.md` — Phase 2 reqs: CAPT-01..04, DEPL-01..05
- `.planning/ROADMAP.md` — Phase 2 goal and exit criteria
- `.planning/phases/01-build-static-site-content-portraits-palette/01-CONTEXT.md` — Phase 1 decisions (palette discipline D-11 still applies to favicon + OG image)
- `.planning/phases/01-build-static-site-content-portraits-palette/01-02-SUMMARY.md` — Phase 1 handoff: `rewired-coming-soon__email-placeholder` div already exists in `layouts/partials/sections/coming-soon.html` with a `:focus-within` Ion Glow cyan ring primed for the Systeme.io form input. `layouts/_default/baseof.html` intentionally ships without OG/Twitter/canonical/favicon meta so Phase 2 owns SEO + deployment.

### Systeme.io
- No canonical doc on disk — Matt's Systeme.io account is the source of truth. Executor logs into Systeme.io, creates the "Rewired — Pre-launch" list, generates the form, copies embed code. Document list ID and form ID in SUMMARY.md.

### GitHub Pages
- GitHub Pages custom-domain docs: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site (for executor's reference during DNS setup)
- GitHub's 4 A record IPs for apex: 185.199.108.153 / 109 / 110 / 111 (documented in D-06)

### Palette & Brand
- `~/.psyche/swipe-files/podcasting-creative/2026-04-16-12-33-18-arc-on-color-palette-full.md` — ARCÆON palette. Favicon and OG image must stay inside this family.

### Phase 1 Wired Anchors
- `/Users/falkensmage/RitualSync/rewired-site/layouts/partials/sections/coming-soon.html` — contains `.rewired-coming-soon__email-placeholder` (Phase 2 replaces the div content with the Systeme.io embed)
- `/Users/falkensmage/RitualSync/rewired-site/layouts/_default/baseof.html` — Phase 2 adds OG/Twitter/canonical/favicon meta here
- `/Users/falkensmage/RitualSync/rewired-site/hugo.toml` — site config; Phase 2 may add `[params.systeme_io]` block for embed config if template-vs-config split is useful

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets (from Phase 1)
- `layouts/partials/sections/coming-soon.html` with `:focus-within` Ion Glow ring already primed — drop-in target for Systeme.io form embed
- `layouts/_default/baseof.html` with clean `<head>` — ready to accept OG/Twitter/canonical/favicon meta tags
- `hugo.toml` baseURL is a placeholder — update to `https://rewired.show/` during execution

### Established Patterns
- Push-to-main deploy pattern validated by `psyche-infographic` and `rewired-portrait-review` (already running on GitHub Pages — Matt has the pattern locked)
- CNAME file pattern at repo root is standard GH Pages behavior

### Integration Points
- Outward: Systeme.io (form embed), GitHub (repo + Actions + Pages), Namecheap / Matt's registrar for rewired.show DNS
- Inward: Phase 1's partial + baseof are the only files Phase 2 modifies structurally; everything else is additive (.github/workflows/, CNAME, static/favicon.*, static/images/og/)

</code_context>

<specifics>
## Specific Ideas

- **Test signup flow before announcing the URL publicly.** Matt submits his own email from the live site, verifies it lands in the "Rewired — Pre-launch" Systeme.io list, checks that success state renders without page reload (CAPT-03) and that a deliberate failure (e.g., empty submit) shows a recoverable error (CAPT-04).
- **Link-preview smoke test across 3 surfaces:** iMessage, Slack, one of Matt's public-social surfaces (Threads or X). Paste the URL, watch the OG preview render. If any surface shows a broken preview, iterate.
- **Don't announce the URL publicly in Phase 2.** Phase 2 exit is "shareable to Jaye Anne via DM" — not "tweeted." Public launch is a separate human-judgment moment after Jaye Anne confirms her portrait pick and Matt is happy with the copy.

</specifics>

<deferred>
## Deferred Ideas

- **Bespoke OG image design pass** — v1 uses Matt's portrait or a quick ImageMagick composition; bespoke art is post-launch.
- **Analytics beyond Systeme.io signup count** — Plausible or similar lives in a post-MVP phase if signal warrants.
- **Welcome-email drip inside Systeme.io** — list capture is Phase 2 scope; the automation sequence is a separate exercise.
- **404 page with voice** — Hugo's default 404 is fine for MVP; a written 404 with Matt's register is a post-launch nice-to-have.
- **Sitemap.xml + robots.txt** — Hugo generates a sitemap by default if configured; leave default. Robots.txt not blocking for launch.

</deferred>

---

*Phase: 02-ship-email-capture-deploy-shareable-link*
*Context gathered: 2026-04-18*
