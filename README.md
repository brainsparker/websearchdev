# websearch.dev

A long-form, single-page comparison of web search APIs for developers:
You.com vs Exa vs Parallel vs Tavily vs Keenable.

Hand-written HTML/CSS. No build step, no JavaScript, no trackers.

## Files

| File | Purpose |
|---|---|
| `index.html` | The whole site (one long page) |
| `styles.css` | All styling |
| `llms.txt` | Agent-facing summary + verdicts (llmstxt.org convention) |
| `llms-full.txt` | Full page text as Markdown |
| `index.md` | Markdown mirror of the page (same content as llms-full.txt) |
| `sitemap.xml`, `robots.txt`, `humans.txt` | Crawler & human metadata |
| `_headers` | Cloudflare Pages headers (markdown content types, caching) |
| `assets/` | favicon.svg, og.png |
| `PRD.md` | Product requirements doc (v1 page) |
| `TPRD.md` | Long-term technical PRD (proposal) |
| `RESEARCH.md` | Sourced fact base behind the page (update this first) |

## Local preview

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

## Deploy (Cloudflare Pages)

1. Push this repo to GitHub.
2. Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages** → **Connect to Git** → pick this repo.
3. Build settings: **no build command**; output directory = repo root (`/`).
4. After first deploy: **Custom domains** → add `websearch.dev` (and `www.websearch.dev`,
   redirect www → apex). Cloudflare provisions TLS automatically
   (.dev is HSTS-preloaded — HTTPS is mandatory, which Cloudflare handles).
5. `_headers` is picked up automatically: `.md` serves as `text/markdown`,
   assets get immutable caching.

## Updating content

1. Re-fetch sources listed in `RESEARCH.md`, update notes there.
2. Edit `index.html`; update "last verified" stamps + the changelog table.
3. Mirror substantive changes into `llms-full.txt` / `index.md` (keep them in
   sync — currently identical files) and `llms.txt` if verdicts or prices change.
4. Bump `dateModified` in the JSON-LD and `lastmod` in `sitemap.xml`.
5. Push — Cloudflare Pages redeploys on push to main.

Corrections inbox (referenced on the page): corrections@websearch.dev — set this
up (e.g., Cloudflare Email Routing → forward to your real inbox) before launch.
