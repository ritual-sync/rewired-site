// Fetch per-episode Apple Podcasts + Spotify deep links and write
// data/platform-episode-links.json, which generate-episode-pages.py reads
// alongside data/youtube-episode-ids.json.
//
// Apple: public iTunes Lookup API, no auth. Joined to assets/episodes.xml
// by the Substack GUID (substack:post:<id>) — Apple's episodeGuid field
// carries that same value verbatim, so this join is exact, not fuzzy.
//
// Spotify: Web API (api.spotify.com/v1/shows/{id}/episodes), needs the
// spotify:matt credential (already used for playback elsewhere in Psyche —
// reading public show/episode data works on a plain user token, no extra
// scope). Joined by exact episode title (verified 1:1 identical to the
// Substack feed's <title>, not fuzzy-matched).
//
// Usage: npx tsx scripts/fetch-platform-links.mts

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const FEED_PATH = path.join(REPO_ROOT, "assets", "episodes.xml");
const OUT_PATH = path.join(REPO_ROOT, "data", "platform-episode-links.json");

const PSYCHE_REPO = `${process.env.HOME}/RitualSync/psyche`;
const CRED = `${PSYCHE_REPO}/mcp/psyche-credentials`;

const APPLE_PODCAST_ID = "1896945601";
const SPOTIFY_SHOW_ID = "033CfL5f9scqVjOibTK0f5";

type FeedItem = { slug: string; title: string; guid: string };

function parseFeed(): FeedItem[] {
  const xml = fs.readFileSync(FEED_PATH, "utf-8");
  const items: FeedItem[] = [];
  for (const m of xml.matchAll(/<item>(.*?)<\/item>/gs)) {
    const block = m[1];
    const title = block.match(/<title><!\[CDATA\[(.*?)\]\]><\/title>/s)?.[1]
      ?? block.match(/<title>(.*?)<\/title>/s)?.[1] ?? "";
    const link = block.match(/<link>(.*?)<\/link>/)?.[1] ?? "";
    const guid = block.match(/<guid[^>]*>(.*?)<\/guid>/)?.[1] ?? "";
    if (!link) continue;
    const slug = link.replace(/\/$/, "").split("/").pop() ?? "";
    items.push({ slug, title, guid });
  }
  return items;
}

async function fetchApple(): Promise<Map<string, string>> {
  const res = await fetch(`https://itunes.apple.com/lookup?id=${APPLE_PODCAST_ID}&entity=podcastEpisode&limit=200`);
  if (!res.ok) throw new Error(`Apple lookup failed HTTP ${res.status}`);
  const body = await res.json();
  const byGuid = new Map<string, string>();
  for (const r of body.results ?? []) {
    if (r.kind === "podcast-episode" && r.episodeGuid && r.trackViewUrl) {
      byGuid.set(r.episodeGuid, r.trackViewUrl);
    }
  }
  return byGuid;
}

async function fetchSpotify(): Promise<Map<string, string>> {
  const { getServiceConfig } = await import(`${CRED}/src/lib/service-config.ts`);
  const { getValidCredential } = await import(`${CRED}/src/lib/credential-store.ts`);
  const cfg = await getServiceConfig("spotify");
  const r = await getValidCredential("spotify", "matt", cfg);
  if (r.status !== "healthy" && r.status !== "refreshable") {
    throw new Error(`spotify credential ${r.status}: ${r.message ?? ""}`);
  }
  const token = r.token?.access_token ?? r.token?.accessToken;
  if (!token) throw new Error("no access_token on spotify credential");

  const byTitle = new Map<string, string>();
  let url: string | null = `https://api.spotify.com/v1/shows/${SPOTIFY_SHOW_ID}/episodes?limit=50`;
  while (url) {
    const res: Response = await fetch(url, { headers: { authorization: `Bearer ${token}` } });
    if (!res.ok) throw new Error(`Spotify episodes fetch failed HTTP ${res.status}`);
    const body: any = await res.json();
    for (const ep of body.items ?? []) {
      byTitle.set(ep.name, `https://open.spotify.com/episode/${ep.id}`);
    }
    url = body.next;
  }
  return byTitle;
}

async function main() {
  const feedItems = parseFeed();
  if (feedItems.length === 0) {
    console.error("ERROR: no items parsed from assets/episodes.xml");
    process.exit(1);
  }

  const [appleByGuid, spotifyByTitle] = await Promise.all([fetchApple(), fetchSpotify()]);

  const out: Record<string, { appleURL?: string; spotifyURL?: string }> = {};
  for (const item of feedItems) {
    const appleURL = appleByGuid.get(item.guid);
    const spotifyURL = spotifyByTitle.get(item.title);
    out[item.slug] = {
      ...(appleURL ? { appleURL } : {}),
      ...(spotifyURL ? { spotifyURL } : {}),
    };
    console.log(`${item.slug}`);
    console.log(`  apple  : ${appleURL ?? "NOT FOUND"}`);
    console.log(`  spotify: ${spotifyURL ?? "NOT FOUND"}`);
  }

  fs.mkdirSync(path.dirname(OUT_PATH), { recursive: true });
  fs.writeFileSync(OUT_PATH, JSON.stringify(out, null, 2) + "\n", "utf-8");
  console.log(`\nwrote ${path.relative(REPO_ROOT, OUT_PATH)}`);
}

main().catch((err) => {
  console.error(err instanceof Error ? err.message : err);
  process.exit(1);
});
