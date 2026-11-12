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
| `PRD.md` | Product requirements doc |
| `RESEARCH.md` | Sourced fact base behind the page (update this first) |
| `scripts/check.py` | Consistency check: fails when the copies of the page disagree (see below) |
| `tests/` | Tests for the checker |

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
5. Run `python3 scripts/check.py` (see below) and fix anything it reports.
6. Push — Cloudflare Pages redeploys on push to main.

## Check before you push

The page ships four times (`index.html`, `index.md`, `llms-full.txt`, and the
summary in `llms.txt`), and all four are edited by hand. `scripts/check.py`
fails when they stop agreeing. It needs Python 3.9+ and nothing else.

```sh
python3 scripts/check.py                  # all checks
python3 scripts/check.py --only facts     # one or more, comma-separated
python3 scripts/check.py --json           # machine-readable
python3 -m unittest discover -s tests     # tests for the checker itself
```

| Check | Fails when |
|---|---|
| `mirror` | `index.md` and `llms-full.txt` are not byte-identical |
| `sections` | `index.html` and `index.md` do not have the same sections in the same order |
| `facts` | A section states a price, number, date, or citation in one copy but not the other. Prose can differ; the figures cannot. `1,200` equals `1200` and `November 11, 2026` equals `2026-11-11` |
| `llms` | `llms.txt` quotes a figure found neither on the page nor in `RESEARCH.md`, or links to a file or anchor that does not exist |
| `structured` | JSON-LD does not parse, the `FAQPage` has a different number of questions than the visible FAQ, an answer states a figure the page does not, or the `ItemList` does not match the vendor sections |
| `dates` | JSON-LD `dateModified`, `sitemap.xml` `lastmod`, and the newest changelog row disagree, a "last verified" stamp is newer than `dateModified`, or a vendor section has no stamp |
| `links` | An internal anchor, local file, or sitemap entry does not resolve, an `id` is duplicated, or a numbered source is never cited |
| `sources` | The numbered source list differs between `index.html` and `index.md` |
| `nojs` | The page gains a `<script>` (JSON-LD excepted), an inline event handler, or a request to another host |
| `budget` | `index.html` + `styles.css` exceed 80,000 bytes raw or 24,000 gzipped (`--raw-budget`, `--gzip-budget`) |

Output names the file and line, for example:

```
FAIL  facts: Each section states the same numbers, dates and citations in both copies
        section 03 (#you-com, index.html:234, index.md:60): in index.html but not index.md: $6
```

To run the same command in GitHub Actions on every push and pull request,
copy the ready-made workflow into place (one time):

```sh
mkdir -p .github/workflows && cp docs/workflows/check.yml .github/workflows/check.yml
```

Cloudflare Pages deploys on push to main whether or not that run passes, so to
stop a bad push before it leaves your machine, install the check as a git hook:

```sh
printf '#!/bin/sh\nexec python3 scripts/check.py\n' > .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

Corrections inbox (referenced on the page): corrections@websearch.dev — set this
up (e.g., Cloudflare Email Routing → forward to your real inbox) before launch.
