# Phase 2: Ship — Email capture, deploy, shareable link - Context

**Gathered:** 2026-04-18
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase takes Phase 1's locally-built static site and puts it on the public internet at `rewired.show` with working email capture wired to **Substack** (the Rewired publication — also the future home for episode audio + RSS), automatic HTTPS, and correct link previews when the URL is shared. When Phase 2 closes, Matt can send the URL to Jaye Anne in iMessage and the first email signups start landing as subscribers to the Rewired Substack.

**In scope:** Substack subscribe-form embed into the existing Coming Soon placeholder, GitHub Pages deployment pipeline, rewired.show DNS + CNAME wiring, HTTPS enforcement, Open Graph / Twitter Card metadata, favicon set, push-to-main auto-deploy.

**Explicitly out of this phase** (belongs to the new Phase 3 — Listener Experience — or deferred):
- Episode list surface / per-episode pages / embedded audio player on rewired.show — **Phase 3** (pulls Substack RSS into Hugo build once episodes exist)
- Bespoke OG image design pass (v1 uses Matt's portrait or a simple composition; bespoke art is post-launch)
- Analytics beyond Substack's built-in subscriber count (ship-first; signup count suffices for MVP signal)
- Welcome-email sequence on Substack (subscribe is v1; drip is a separate exercise once episodes and content start flowing)

</domain>

<decisions>
## Implementation Decisions

### Load-bearing (locked by Matt)

- **D-01:** **Domain: `rewired.show`.** Matt purchased this domain today. It is ready for DNS configuration — no alternate domain candidates. Apex (`rewired.show`) is canonical; `www.rewired.show` redirects to apex.
- **D-02:** **Hosting: GitHub Pages** — push-to-main auto-deploy, free, HTTPS via Let's Encrypt (GitHub's native integration). Repo is `mstine/rewired-site` or equivalent (to be confirmed during execution — Matt may prefer a specific repo name).
- **D-03:** **Email + publishing + audio backend: Substack.** Matt knows the platform (Feral Architecture, prior podcasts). Substack hosts the subscriber list, publishes posts → email newsletter, hosts podcast audio natively, and generates an RSS feed that syndicates to Apple Podcasts / Spotify. Replaces the earlier Systeme.io default — Matt is actively exiting Systeme.io (see `brand-website-own-the-stack` thread). Rewired gets its own Substack publication so subscribers are clean and portable. No deepening of any platform Matt is leaving.

### Substack Integration (D-04, D-05)

- **D-04:** **Substack's official embedded subscribe form (iframe variant) dropped into the existing `rewired-coming-soon__email-placeholder` div Phase 1 pre-built in `layouts/partials/sections/coming-soon.html`.** Matt creates the Rewired Substack publication during execution, copies the embed URL from the publication's Dashboard → Settings → Subscribe widget (or equivalent), and pastes the embed into the Hugo partial. The iframe comes with Substack's default styling — minor palette clash with the Void Purple section is accepted as a Phase 2 tradeoff; CSS overrides for the iframe wrapper can tune the surrounding container but cannot restyle the iframe contents (cross-origin). A future enhancement is a custom form that POSTs to Substack's subscribe endpoint for full brand control; out of Phase 2 scope.
- **D-05:** **Substack publication name: "Rewired"** (URL: `rewired.substack.com`). Subscribers on this publication are exclusive to Rewired — no mixing with Feral Architecture or any other Substack publication. This satisfies CAPT-02 (dedicated Rewired list). Matt creates the publication during execution; executor documents the publication URL and subscribe-embed shape in SUMMARY.md.

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
- `.planning/phases/01-build-static-site-content-portraits-palette/01-02-SUMMARY.md` — Phase 1 handoff: `rewired-coming-soon__email-placeholder` div already exists in `layouts/partials/sections/coming-soon.html` with a `:focus-within` Ion Glow cyan ring primed for the subscribe form input. `layouts/_default/baseof.html` intentionally ships without OG/Twitter/canonical/favicon meta so Phase 2 owns SEO + deployment.

### Substack
- No canonical doc on disk — Matt's Substack account is the source of truth. Executor (via Matt checkpoint) creates the "Rewired" publication at `rewired.substack.com`, copies the embedded subscribe form, pastes into the Hugo partial. Document the publication URL and subscribe-embed shape in SUMMARY.md.
- Related context: `brand-website-own-the-stack` thread — Matt is exiting Systeme.io + Coach Vantage + Kartra. Substack does NOT become the sovereign stack later; it stays the publishing + subscribe layer for Rewired specifically, while Own-the-Stack proceeds separately for Matt's broader brand.

### GitHub Pages
- GitHub Pages custom-domain docs: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site (for executor's reference during DNS setup)
- GitHub's 4 A record IPs for apex: 185.199.108.153 / 109 / 110 / 111 (documented in D-06)

### Palette & Brand
- `~/.psyche/swipe-files/podcasting-creative/2026-04-16-12-33-18-arc-on-color-palette-full.md` — ARCÆON palette. Favicon and OG image must stay inside this family.

### Phase 1 Wired Anchors
- `/Users/falkensmage/RitualSync/rewired-site/layouts/partials/sections/coming-soon.html` — contains `.rewired-coming-soon__email-placeholder` (Phase 2 replaces the div content with the Substack subscribe embed)
- `/Users/falkensmage/RitualSync/rewired-site/layouts/_default/baseof.html` — Phase 2 adds OG/Twitter/canonical/favicon meta here
- `/Users/falkensmage/RitualSync/rewired-site/hugo.toml` — site config; Phase 2 may add `[params.substack]` block for the publication URL if template-vs-config split is useful

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets (from Phase 1)
- `layouts/partials/sections/coming-soon.html` with `:focus-within` Ion Glow ring already primed — drop-in target for the Substack subscribe form
- `layouts/_default/baseof.html` with clean `<head>` — ready to accept OG/Twitter/canonical/favicon meta tags
- `hugo.toml` baseURL is a placeholder — update to `https://rewired.show/` during execution

### Established Patterns
- Push-to-main deploy pattern validated by `psyche-infographic` and `rewired-portrait-review` (already running on GitHub Pages — Matt has the pattern locked)
- CNAME file pattern at repo root is standard GH Pages behavior
- Matt has shipped prior podcasts on Substack — the publishing + audio + RSS pattern is known, not new

### Integration Points
- Outward: Substack (subscribe embed, future post-launch Phase 3 RSS pull for episode pages), GitHub (repo + Actions + Pages), Namecheap / Matt's registrar for rewired.show DNS
- Inward: Phase 1's partial + baseof are the only files Phase 2 modifies structurally; everything else is additive (.github/workflows/, CNAME, static/favicon.*, static/images/og/)

</code_context>

<specifics>
## Specific Ideas

- **Test signup flow before announcing the URL publicly.** Matt submits his own email from the live site, verifies it lands as a subscriber on the Rewired Substack publication, checks that success state renders per Substack's embed behavior (CAPT-03) and that a deliberate failure (e.g., empty submit) is handled recoverably (CAPT-04).
- **Link-preview smoke test across 3 surfaces:** iMessage, Slack, one of Matt's public-social surfaces (Threads or X). Paste the URL, watch the OG preview render. If any surface shows a broken preview, iterate.
- **Don't announce the URL publicly in Phase 2.** Phase 2 exit is "shareable to Jaye Anne via DM" — not "tweeted." Public launch is a separate human-judgment moment after Jaye Anne confirms her portrait pick and Matt is happy with the copy.
- **Hybrid architecture note:** rewired.show (Hugo) is the visual/brand front door; rewired.substack.com is the operational backbone (subscribers, publishing, audio, RSS). Phase 3 will pull Substack's RSS back into Hugo so rewired.show carries a full listener experience (episode pages with embedded players, show notes). Phase 2 doesn't need to solve this yet — just make sure the subscribe capture works.

</specifics>

<deferred>
## Deferred Ideas

- **Bespoke OG image design pass** — v1 uses Matt's portrait or a quick composition; bespoke art is post-launch.
- **Analytics beyond Substack's built-in subscriber count** — Plausible or similar lives in a post-MVP phase if signal warrants.
- **Welcome-email drip on Substack** — subscribe is Phase 2 scope; any automation sequence is a separate exercise, scoped once content is flowing.
- **Custom-form-posting-to-Substack-endpoint** — unofficial but widely-used pattern for full brand control over the subscribe UI. Out of Phase 2; iframe embed is MVP.
- **Phase 3 — Listener Experience** — pull Substack RSS into Hugo build, generate per-episode pages on rewired.show with embedded audio players, show notes in Card→Riff→Unresolved structure, episode list, latest-episode callout. Triggered by first episodes existing; not Phase 2 work.
- **404 page with voice** — Hugo's default 404 is fine for MVP; a written 404 with Matt's register is a post-launch nice-to-have.
- **Sitemap.xml + robots.txt** — Hugo generates a sitemap by default if configured; leave default. Robots.txt not blocking for launch.

</deferred>

---

*Phase: 02-ship-email-capture-deploy-shareable-link*
*Context gathered: 2026-04-18*
