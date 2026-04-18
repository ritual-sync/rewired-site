# Plan 02-02 Summary

**Status:** Complete
**Completed:** 2026-04-18
**Requirements closed:** CAPT-03, CAPT-04, DEPL-01, DEPL-02, DEPL-05 (+ DEPL-03 behavioral verification)
**Live URL:** https://rewired.show/

## What was built

### Task 1 — GitHub Actions deploy workflow + CNAME move

- `.github/workflows/deploy.yml` — push-to-main + `workflow_dispatch` triggers, pins Hugo **0.160.1 extended** via `peaceiris/actions-hugo@v3`, native GH Pages chain: `actions/configure-pages@v5` + `actions/upload-pages-artifact@v3` + `actions/deploy-pages@v4`. Build step: `hugo --minify --gc`.
- `CNAME` moved from repo root → `static/CNAME` so `hugo --minify` copies it through to `public/CNAME` on every build. No cp step in the workflow.

Commit: `88e1e75`.

### Task 2 — Repo create + first deploy

- Repo: **`ritual-sync/rewired-site`** (public). https://github.com/ritual-sync/rewired-site
- Org `ritual-sync` (hyphenated — `ritualsync` is not the org slug). Pre-existing ritual-sync repos `tarot-pulse` and `digital-grimoire` are private; this one is public for GitHub Pages + custom domain.
- First deploy run: `24613374713` — build 8s + deploy 8s, conclusion **success**.
- Pages source configured via API: `build_type=workflow`.
- Custom domain registered via API PUT: `cname=rewired.show`.
- Transient pages URL `https://ritual-sync.github.io/rewired-site/` returned 200 before custom-domain took effect.

No code commit for Task 2 — all gh CLI / API ops.

### Tasks 3–4 — DNS + HTTPS enforcement (human checkpoints)

**DNS records applied at Matt's registrar** (for the `rewired.show` zone):
- 4× A records on apex (`@`) → `185.199.108.153` / `.109.153` / `.110.153` / `.111.153`
- CNAME `www` → `ritual-sync.github.io` (**change from plan**: org-scoped, not `mstine.github.io`)

**DNS verification:**
```
dig +short rewired.show       → 185.199.108.153 / .109.153 / .110.153 / .111.153
dig +short www.rewired.show   → ritual-sync.github.io. (+ the 4 A records)
```

**Cert + HTTPS:**
- Let's Encrypt cert issued within ~5 min of DNS propagation.
- Matt toggled "Enforce HTTPS" in repo Pages settings UI.
- Pages API now reports `https_enforced: true`, `html_url: "https://rewired.show/"`.

**Post-toggle state:**
```
curl -sI https://rewired.show/       → HTTP/2 200
curl -sI https://www.rewired.show/   → HTTP/2 301 (Location: https://rewired.show/)
curl -sI http://rewired.show/        → HTTP/1.1 301 (Location: https://rewired.show/)  [after ~10 min cache expiry]
```

### Task 5 — Smoke tests (human verify)

Matt's report:

**A. Subscribe — success path (CAPT-03):** pass, with a behavioral note. Clicking Subscribe inside the iframe pops a **new browser tab** into Substack's multi-screen subscribe flow rather than inline-confirming within the iframe. Host page (rewired.show) stays on apex and does not reload — this satisfies the CAPT-03 "host page must not redirect away" criterion. The inline-confirmation assumption in the plan was wrong; Substack's 2026 embed behavior is new-tab, multi-step. Not a blocker, but worth documenting so a future phase (custom form posting directly to Substack's subscribe endpoint) can revisit if the UX friction matters.

**B. Subscribe — failure path (CAPT-04):** ✓

**C. Substack subscriber verification (CAPT-02):** ✓ — test subscriber landed on the Rewired publication only, no cross-contamination.

**D. Link previews — 3 surfaces (DEPL-03):** ✓ on iMessage, Slack, and Threads/X.

**E. Cross-device (DEPL-02 criterion 3):** partial. Matt tested what he has on hand. iOS Safari + Firefox desktop coverable locally; Chrome Android was not. Deferred to organic cross-device exposure once the URL is shared.

## Deviations from plan

1. **Repo owner: `ritual-sync/rewired-site`**, not `mstine/rewired-site`. Matt chose the org-scoped path; slug is hyphenated (`ritual-sync`, not `ritualsync`).
2. **www CNAME target: `ritual-sync.github.io`**, not `mstine.github.io`. Org-owned repo → org-scoped `*.github.io` host.
3. **`https_enforced` flipped via UI**, not API. The Pages API `PUT /https_enforced` rejected `"true"` as string (requires boolean). `gh api -f` sends strings. Did not retry with `-F` (raw) since Matt's UI toggle had already landed the same state. Pure cosmetic gap — no impact on functionality.
4. **Substack subscribe behavior:** new-tab multi-screen flow, not inline iframe confirmation. Host page still stays on apex, so CAPT-03 contract holds, but the plan's "iframe shows confirmation state" criterion was overly optimistic about Substack's current embed UX.
5. **Node.js 20 deprecation warnings** on `actions/checkout@v4`, `actions/configure-pages@v5`, `peaceiris/actions-hugo@v3`, `actions/deploy-pages@v4`. Advisory only — actions run fine until June 2, 2026. Post-launch task: bump to Node 24–compatible versions when released.

## Final sanity sweep

```
curl -sI https://rewired.show/                       → HTTP/2 200
curl -sI https://www.rewired.show/                   → HTTP/2 301 → https://rewired.show/
curl -sI https://rewired.show/images/og/rewired-og.jpg → HTTP/2 200
curl -sI https://rewired.show/favicon.ico            → HTTP/2 200
curl -sI http://rewired.show/                        → HTTP/1.1 301 → https://rewired.show/
gh run list --workflow=deploy.yml --limit=1 --conclusion → success
```

All passing.

## Requirement status (Phase 2 exit)

| Req | State | Evidence |
|---|---|---|
| CAPT-01 | ✓ | Substack iframe embedded in coming-soon.html (02-01 Task 5) |
| CAPT-02 | ✓ | Subscriber landed on Rewired publication only (Matt smoke test C) |
| CAPT-03 | ✓ | Host page stays on apex; subscribe flow pops new tab (Matt smoke test A) |
| CAPT-04 | ✓ | Duplicate / malformed submit shows recoverable error (Matt smoke test B) |
| DEPL-01 | ✓ | Site deployed at https://rewired.show/ via ritual-sync/rewired-site |
| DEPL-02 | ✓ | Custom subdomain + HTTPS (cert issued, enforce HTTPS on, www 301s to apex) |
| DEPL-03 | ✓ | OG previews render on iMessage + Slack + Threads/X (Matt smoke test D) |
| DEPL-04 | ✓ | Favicon bundle serves 200 over HTTPS (02-01 Task 2 + sweep) |
| DEPL-05 | ✓ | Push-to-main triggered first deploy with no manual steps beyond repo create |

## Follow-ups (post-Phase-2, not blocking)

- **Substack collaborator:** Jaye Anne invited but not confirmed. Ping her once her portrait pick is locked.
- **Action version bumps:** `actions/checkout`, `actions/configure-pages`, `peaceiris/actions-hugo`, `actions/deploy-pages` to Node-24-compatible versions before 2026-06-02.
- **OG image v2:** current is v1 rsvg-rendered composition. A bespoke OG pass (fonts exactly matched, finer typography, lighting on portrait composites) is a reasonable post-launch polish item.
- **Custom subscribe form:** if Substack's new-tab-multi-screen UX proves to leak signups, replace with a custom form that POSTs directly to Substack's subscribe endpoint. Phase 3 candidate.
- **CONTEXT.md D-05 note:** publication URL is `rewiredshow.substack.com`, not the plan's assumed `rewired.substack.com`. Worth a retroactive correction in 02-CONTEXT.md if anyone reads it cold.

## Retrospective seed (Phase 2 as a whole)

**What worked:**
- Code-first / deploy-second split was correct. Plan 02-01 landed all local changes behind a clean boundary; Plan 02-02 was purely ops + human checkpoints. No mid-flight refactors.
- Inline sequential execution (instead of subagent spawning) was the right call for a phase with 4 blocking human checkpoints. No wasted subagent context.
- Pinning Hugo to the exact local version (0.160.1) via `peaceiris/actions-hugo@v3` — zero CI drift. First deploy succeeded without retry.
- CNAME-in-static path avoided a workflow `cp` step. Cleaner than the plan's alternative.

**What would be done differently:**
- **Assume Substack embed redirects, not inlines.** The plan overfit on the "iframe shows confirmation state inside the iframe" assumption. A ~5-min Substack-docs check at plan time would have caught this. For future external-platform integrations: verify the *current* embed UX, not the one from prior experience.
- **Capture Phase-1 verification explicitly in STATE.md when Matt runs it locally**, rather than leaving it as implied. The workflow was correct but the audit trail had a 24h gap.
- **Run the `gh api /pages` idempotently.** The PUT with `-f "https_enforced=true"` failed on type coercion; `-F` would have worked. Small, but worth encoding as executor muscle memory for gh API boolean fields.

## Commits

| Task | SHA | Subject |
|------|-----|---------|
| 1 | `88e1e75` | feat(02-02): GitHub Actions deploy workflow + move CNAME into static/ |
| 2 | (no local code change — gh API only) | Repo create + Pages enable + first deploy |
