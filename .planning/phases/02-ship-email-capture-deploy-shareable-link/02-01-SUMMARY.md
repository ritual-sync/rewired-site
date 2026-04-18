# Plan 02-01 Summary

**Status:** Complete
**Completed:** 2026-04-18
**Requirements closed:** CAPT-01, CAPT-02, DEPL-02 (anchor), DEPL-03, DEPL-04

## What was built

### Task 1 — Production baseURL, OG/Twitter/canonical meta, CNAME

- `hugo.toml` — `baseURL = "/"` → `baseURL = "https://rewired.show/"`.
- `layouts/_default/baseof.html` — added a canonical `<link>` and a full Open Graph + Twitter Card meta block (`og:type`, `og:site_name`, `og:title`, `og:description`, `og:url`, `og:image` + width/height/alt, `twitter:card=summary_large_image`, `twitter:title`, `twitter:description`, `twitter:image` + alt). Tagline and title keyed to `site.Title` + `site.Params.tagline` so the content stays single-sourced.
- `CNAME` at repo root with single line `rewired.show`. Plan 02-02 moves this into `static/CNAME` so Hugo copies it through the deploy artifact.

Commit: `97daa80`.

### Task 2 — ARCÆON favicon set

- `static/favicon.svg` — Fusion Gold `R` glyph (Cinzel/serif fallback) on Void Purple rounded-square. Palette: two hex values only — `#1a0f2e` + `#ffb347` — matches D-11 discipline.
- `static/favicon.ico` — 32×32 native MS Windows icon resource (3931 bytes).
- `static/apple-touch-icon.png` — 180×180 PNG RGBA (3931 bytes).
- `layouts/_default/baseof.html` — 3× favicon `<link>` tags (svg, ico, apple-touch-icon) + `<meta name="theme-color" content="#1a0f2e">` for iOS home-screen / Chrome mobile URL-bar tinting.

Commit: `ba25586`.

### Task 3 — v1 Open Graph image

- `static/images/og/rewired-og.jpg` — 1200×630 JPEG, 34,757 bytes (well under the 200 KB soft budget).
- Dual-portrait composition on Void Purple: Matt (360×360, left third) + Jaye Anne (360×360, right third) + "Rewired" wordmark in Fusion Gold + tagline in Solar White. Generated via SVG → `rsvg-convert` → `sips -s format jpeg`.
- Palette discipline attested at the SVG-source level: three hex values (`#1a0f2e`, `#ffb347`, `#fff4e6`). Portrait natural tones are from the ARCÆON-system originals.

Commit: `65f3fe0`.

### Task 5 — Substack iframe wired into Coming Soon

- `layouts/partials/sections/coming-soon.html` — Phase 1 placeholder div contents replaced with Matt's Substack iframe, pasted verbatim.
- Wrapper class `.rewired-coming-soon__email-placeholder` preserved (Phase 1 layout rules still load-bearing).
- `aria-label` updated from `"Email signup (coming soon)"` to `"Subscribe to Rewired on Substack"`.
- Inline `style="opacity: 1;"` on the wrapper overrides the Phase 1 70% placeholder dim.

Commit: `3ba294c`.

## Substack trail (CAPT-02 audit record)

- **Publication URL:** `rewiredshow.substack.com` — the bare `rewired.substack.com` was taken, so the publication landed at `rewiredshow`.
- **Iframe src:** `https://rewiredshow.substack.com/embed`
- **Iframe dimensions:** 480×320, no height/width override applied. If the form feels cramped on mobile in Plan 02-02 smoke tests, revisit in Phase 3.
- **Tier:** free only (paid is a post-launch decision).
- **Collaborators:** Jaye Anne **invited but not yet confirmed** on Substack. Track as a post-Phase-2 follow-up — once she confirms, she gets editor/admin on the publication without code changes here.

## Deviations from plan

1. **sips ICO format token.** Plan said `sips -s format microsoft_icon`. That token fails on this macOS (`Can't write format: microsoft_icon`). Correct token is `ico`. Produces a real MS Windows icon resource — better than the plan's anticipated PNG-as-ICO fallback.
2. **Task 4 was a human checkpoint**, not a code task — executed via Matt creating the publication and pasting the embed back. No commit for Task 4.
3. **CNAME stays at repo root** for now (Plan 02-02 Task 1 moves it into `static/` as part of the deploy workflow setup). Per the plan's verification note, this is intentional — Plan 02-02 handles CNAME propagation into the deploy artifact.
4. **Publication URL:** `rewiredshow.substack.com`, not `rewired.substack.com` as assumed in the plan and CONTEXT.md references. All future doc references should use `rewiredshow.substack.com`. The 02-CONTEXT.md D-05 still says `rewired.substack.com` — worth a retroactive correction, but not load-bearing for Plan 02-02.

## Hugo build state (Plan 02-01 end-to-end verification)

```
rm -rf public && hugo --minify
Total in 59 ms
```

All nine acceptance greps pass on `public/index.html` + `public/`:

- `index.html`, `favicon.ico`, `favicon.svg`, `apple-touch-icon.png`, `images/og/rewired-og.jpg` all present in `public/`
- `https://rewired.show/images/og/rewired-og.jpg` present in `index.html`
- favicon `rel` tags, `rel=canonical`, and `substack` all present in `index.html`

## Plan 02-02 handoff notes

What Plan 02-02 needs to wire:

- **CNAME move:** `git mv CNAME static/CNAME` (or plain `mv`, then re-add) so Hugo copies it through into `public/CNAME` on every build. Don't rely on the workflow to manually `cp` it.
- **GitHub Actions workflow** `.github/workflows/deploy.yml`. Pin Hugo to **0.160.1** (local: `hugo v0.160.1+extended+withdeploy darwin/arm64`). Use `peaceiris/actions-hugo@v3` + native `actions/configure-pages` + `actions/upload-pages-artifact` + `actions/deploy-pages` chain.
- **Repo name:** confirm with Matt — default `mstine/rewired-site` per Matt's naming pattern (`psyche-infographic`, `rewired-portrait-review`, `falkensmage-website`).
- **DNS records:** human action, Matt's registrar. 4× A records on apex + CNAME `www` → `mstine.github.io`.
- **HTTPS toggle:** human action in repo settings after cert issues.
- **Smoke tests:** subscribe success + failure (CAPT-03, CAPT-04), link previews on 3 surfaces (DEPL-03), cross-device (DEPL-02).

## Commits

| Task | SHA | Subject |
|------|-----|---------|
| 1 | `97daa80` | feat(02-01): production baseURL + OG/Twitter/canonical meta + CNAME |
| 2 | `ba25586` | feat(02-01): ARCÆON favicon set (svg + ico + apple-touch-icon) |
| 3 | `65f3fe0` | feat(02-01): v1 dual-portrait Open Graph image |
| 5 | `3ba294c` | feat(02-01): wire Substack subscribe iframe into Coming Soon |
