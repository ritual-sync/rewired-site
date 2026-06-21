# Follow-up: make the episode feed fetch live again (custom-domain route)

## Current state (2026-06-21)

The Episodes section reads a **vendored** copy of the Substack podcast feed at
`assets/episodes.xml`, parsed at build time. We do NOT fetch it live, because:

- Substack returns **403 Forbidden** to GitHub Actions' datacenter IP ranges on
  *every* `*.substack.com` feed endpoint — both the main publication feed
  (`rewiredshow.substack.com/feed`) and the podcast distribution feed
  (`api.substack.com/feed/podcast/8721195.rss`), regardless of user-agent.
- So `resources.GetRemote` can never succeed from CI. Every build silently fell
  back to "Coming Soon" even with episodes published.

Refresh today is manual: run `scripts/refresh-episodes.sh` from a non-blocked IP
(a laptop), commit, push.

## The insight that points to a real fix

The sister site **falkensmage.com** fetches `feralarchitecture.com/feed` live at
build time on the *same* GitHub Actions runners — and it works (zero
`RSS fetch failed` warnings in CI; the "Currently" card shows live posts).

The only difference is the **domain**:

| Feed host | Type | Blocks GH runner? |
|---|---|---|
| `rewiredshow.substack.com/feed` | bare `*.substack.com` subdomain | **Yes (403)** |
| `api.substack.com/feed/podcast/...` | Substack API subdomain | **Yes (403)** |
| `feralarchitecture.com/feed` | **custom domain** on Substack | **No (200)** |

Substack runs aggressive Cloudflare datacenter-IP blocking on its own
`*.substack.com` edge, but **custom domains route through a different edge config
that does not blanket-block datacenter IPs.**

## The fix (when there's appetite)

Give the **Rewired Substack publication a custom domain** for its feed —
something like `posts.rewired.show` or `feed.rewired.show` pointed at the
publication (Substack Settings → custom domain; note `rewired.show` itself is
already this Hugo site, so use a subdomain).

Then revert `layouts/partials/sections/episodes.html` to live fetch:

```go-html-template
{{ $feedURL := "https://posts.rewired.show/feed" }}   {{/* custom domain — not 403'd */}}
{{ with try (resources.GetRemote $feedURL) }}
  {{ with .Err }}{{ warnf "feed fetch failed: %s" . }}
  {{ else with .Value }}{{ $data := .Value | transform.Unmarshal }} ... {{ end }}
{{ end }}
```

and the scheduled rebuild becomes meaningful again: new episodes appear on the
next build with no manual `refresh-episodes.sh` step. Drop the vendored
`assets/episodes.xml` and `scripts/refresh-episodes.sh` at that point.

### Tradeoff vs. the laptop-cron alternative
The other way to automate refresh is a launchd job on a personal machine that
re-fetches + commits `assets/episodes.xml` on a schedule. That keeps the vendored
file but adds a machine dependency and a moving part. The custom-domain route is
cleaner: it removes the vendored file entirely and restores the site's original
"rebuild = fresh" design. Prefer the custom domain if/when you set one up.
