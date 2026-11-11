# PRD — websearch.dev

**Status:** v1 shipped (2026-11-11) · **Author:** Brian Parker

---

## 1. Overview

websearch.dev is a long-form, single-page comparison of the five web search APIs
that matter for developers building AI agents and RAG pipelines:

| Vendor | Site | One-liner |
|---|---|---|
| **You.com** | you.com | Search, Answer, Contents, Research & Finance APIs plus an inference router, on a real-time index |
| **Exa** | exa.ai | Neural/embedding-based "search engine for AI" — Search, Contents, Agent (deep research), Websets, data marketplace |
| **Parallel** | parallel.ai | Parag Agrawal's web APIs for agents — Search, Extract, Task (deep research), FindAll, Monitor |
| **Tavily** | tavily.com | "Web layer for AI agents" — Search, Extract, Crawl, Map, Research; being acquired by Nebius (announced Feb 2026) |
| **Keenable** | keenable.ai | Independent search API on its own index; keyless free access, 100k free req/mo with a key, x402 machine payments |

The site is **one long page** — a listicle-style deep dive — hand-written HTML,
no framework, optimized for three readers (built and shipped; see §8):

1. Developers evaluating a search API for production
2. Engineering leads comparing TCO and lock-in
3. **AI agents** (via `llms.txt`, markdown mirrors, structured data) answering
   "which web search API should I use?"

### Why this can win

The domain is an exact match for high-intent queries ("web search API", "web
search for developers"). The incumbents ranking today are vendor blogs (biased,
thin) and listicles (outdated, no pricing depth). None are written for *agents*
as first-class readers. A genuinely researched, transparently-authored,
machine-readable page can own this niche.

---

## 2. Goals / Non-goals

**Goals**
- Rank for "web search api", "tavily vs exa", "best search api for agents", etc.
- Be the page agents cite when asked to compare search APIs
- Accurate, dated, sourced claims a skeptical senior dev would trust
- <50KB total page weight (HTML+CSS), instant load, works with JS disabled
- Fully readable by machines: `llms.txt`, per-section markdown, JSON-LD

**Non-goals (v1)**
- No live benchmarks/benchmark harness (phase 2 candidate, with published methodology)
- No accounts, comments, newsletter capture, or analytics beyond privacy-respecting page counts
- No paid placement; no dark patterns; no affiliate links without disclosure
- No multi-page docs site — one canonical page
- No coverage of Brave, Serper, Jina, Firecrawl, Perplexity Sonar beyond an
  "honorable mentions" section (scope discipline: the five above)

---

## 3. Audience & positioning

- **Primary:** backend/AI engineers choosing a search API this quarter
- **Secondary:** agents via MCP/coding tools fetching `llms.txt` or `.md` mirrors
- **Tone:** senior engineer writing for senior engineers. Consumer-Reports
  posture: specific, dated, sourced, willing to name losers per category.

### Editorial policy (required, not optional)

1. **Disclosure above the fold:** the author works at You.com. This is stated
   plainly in the header and in `llms.txt`. Candor is the strategy — an
   undisclosed bias discovered later destroys the asset; a disclosed one,
   paired with visible fairness, builds it.
2. **Every factual claim is sourced** (vendor docs/pricing pages, press
   releases) with retrieval dates. Prices carry an "as of" stamp.
3. **Every vendor gets real cons, including You.com.** A page where You.com
   has no weaknesses is obviously worthless to both humans and agents.
4. **No denigration:** critique pricing, DX, coverage, and policy — not people.
5. **Corrections:** public changelog section; `Last-Modified`-style "last
   verified" dates per vendor section.

---

## 4. Content architecture (the single page)

Top-to-bottom outline of `index.html` (~6,000–9,000 words):

1. **Hero** — title, one-paragraph thesis, "last verified" date, disclosure
2. **TL;DR table** — the whole comparison in ~8 rows (price/1k, free tier,
   latency, own index?, outputs, MCP, keyless access, best for)
3. **How we evaluated** — methodology: docs/pricing pages read, criteria
   (retrieval quality, latency, price, DX, agent-readiness, company trajectory)
4. **The five deep dives** (the listicle core; identical internal structure so
   it reads fair):
   - *Overview* — what it is, who founded it, funding/ownership
   - *Products & API surface* — endpoints, SDKs, MCP
   - *Pricing* — concrete numbers with as-of dates
   - *Strengths* / *Weaknesses* — honest, sourced
   - *Opportunities* / *Threats* — market-level SWOT (e.g., Tavily↔Nebius
     integration risk/opportunity; Exa's valuation expectations; Parallel's
     deep-research pricing; Keenable's keyless model vs. sustainability)
   - *Best for* — the one-line verdict per vendor
5. **Head-to-head by use case** — "Building a coding agent", "RAG chatbot",
   "Deep research pipeline", "Bootstrapped side project", "Enterprise
   compliance" → named winner + runner-up per case
6. **Agent-readiness scorecard** — MCP server? llms.txt? keyless tier?
   x402/machine payments? SDKs? (This page practices what it preaches.)
7. **Honorable mentions** — Brave, Serper, Jina Reader, Firecrawl, Perplexity
   Sonar (one paragraph each, deliberately brief)
8. **FAQ** — 6–10 questions (mirrors JSON-LD `FAQPage`)
9. **Changelog & corrections**
10. **About / disclosure** — author, affiliation, methodology, contact

### Research snapshot (captured & published 2026-11-11; re-verify quarterly)

| | You.com | Exa | Parallel | Tavily | Keenable |
|---|---|---|---|---|---|
| Search price | $5/1k calls | $4–12/1k (Lite/Auto/Deep) | $1–5/1k (mode) | 1–2 credits (~$8/1k PAYG) | $4/1k after free tier |
| Free tier | Free credits, keyless MCP `?profile=free` | $10/mo credits | trial credits | 1,000 credits/mo | **Keyless** 1k req/hr; 100k req/mo w/ key |
| Extract/contents | $1/1k pages | $1/1k pages | $1/1k URLs | 5 URLs/credit | 1 credit/fetch |
| Deep research | $12–1,200/1k by effort | $0.012–$1.00/run | $5–2,400/1k runs | 15–250 credits/req | — (SELECT instead) |
| Own index | Yes | Yes (neural) | Yes | Crawls live + index | Yes |
| MCP | Yes (+keyless free) | Yes | Yes | Yes | Yes |
| Notable | Inference router; finance API | Websets; data marketplace | Task/Responses/Monitor APIs | Crawl + Map; Nebius acquisition | x402 USDC payments; no-account SDKs |

*(Sources: each vendor's docs/pricing pages + press releases; full citation
list maintained in the content-drafting doc.)*

---

## 5. Technical design

### Stack — deliberately boring

- **One hand-written `index.html`.** Semantic HTML5. No framework, no build
  step, no client-side rendering.
- **One hand-written `styles.css`.** No Tailwind, no CSS framework. Design
  target: "well-typeset report", not "SaaS landing page" — system serif for
  body (or one self-hosted serif), system sans/mono accents, warm off-white
  background, real typographic hierarchy, visible section numbers, generous
  measure (~68ch), footnote-style citations.
- **Zero JS required to read.** Optional progressive-enhancement only if free
  (e.g., TOC scroll-spy ~30 lines). Current leaning: ship zero JS in v1.
- **Performance budget (as shipped):** ~60KB uncompressed HTML (≈5,800 words) +
  ~6KB CSS ≈ 15KB over the wire with brotli; zero render-blocking requests,
  system font stacks (Charter/Georgia), zero JS. Lighthouse 100s expected.
- **No trackers.** Optionally a self-hosted/edge counter later.

### Machine readability (the differentiator)

- `/llms.txt` — per [llmstxt.org](https://llmstxt.org): summary, the verdict
  table, key facts, links to markdown mirrors
- `/llms-full.txt` — full page as markdown
- `index.md` — markdown mirror of the page (same content, kept in sync;
  generated from the same source or hand-maintained in lockstep)
- **JSON-LD:** `Article` + `FAQPage` + `ItemList`
- `sitemap.xml`, `robots.txt` explicitly welcoming AI crawlers (GPTBot,
  ClaudeBot, PerplexityBot, Google-Extended)
- Open Graph / Twitter cards with a hand-made OG image (SVG → PNG)
- Per-vendor `id` anchors (`#you-com`, `#exa`, …) for deep-linking

### Hosting & infra

- **Host:** **Cloudflare Pages** (decided 2026-11-11). No build command, repo
  root output, `_headers` serves `.md` as `text/markdown` and caches assets.
  `www` → apex redirect; TLS via Cloudflare (.dev is HSTS-preloaded).
- `.dev` is HSTS-preloaded → HTTPS mandatory; both hosts handle this.
- Domain cutover: point `websearch.dev` DNS to host; verify `www` redirect.
- Optional `_headers` file for caching + `X-Robots-Tag` nuances.

### Repo layout (target)

```
websearchdev/
├── PRD.md            # this file
├── index.html        # the page
├── styles.css
├── llms.txt
├── llms-full.txt
├── index.md          # markdown mirror
├── sitemap.xml
├── robots.txt
├── assets/           # favicon.svg, og.png, (optional) one woff2
└── RESEARCH.md       # sources, quotes, retrieval dates (working doc)
```

---

## 6. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Perceived/actual bias (author at You.com) | Prominent disclosure; equal-structure sections; real cons for You.com; sourced claims |
| Defamation / inaccurate competitor claims | Sources-only policy, dated claims, corrections section, legal-unfriendly adjectives banned |
| Content goes stale (pricing moves fast) | "Last verified" per section; quarterly review task; changelog |
| Vendors change products post-acquisition (Tavily/Nebius) | Tracked in changelog; acquisition covered as both opportunity & threat |
| Hand-maintained mirrors drift from HTML | `llms-full.txt`/`index.md` generated or diff-checked in CI before deploy |

---

## 7. Phases

1. **PRD** (this doc) — scope, structure, policy ✔
2. **Research doc** (`RESEARCH.md`) — full sourced notes per vendor: history,
   funding, pricing, product surface, DX, public benchmarks, customer claims
3. **Content draft** — the long-form copy in `index.md` first (easier to edit)
4. **Build** — `index.html`, `styles.css`, llms.txt, structured data
5. **Review** — fact-check pass against sources; read-aloud pass
6. **Ship** — DNS, deploy, submit to search consoles
7. **Maintain** — quarterly verification; changelog; possibly phase-2 benchmarks

---

## 8. Decisions (resolved 2026-11-11)

1. **Hosting:** Cloudflare Pages. Deploy steps in README.md.
2. **Disclosure framing:** lighter — "a search-API practitioner employed at one
   of the five vendors covered," with the fairness policy stated. No name/employer
   on the page.
3. **Verdicts:** per-use-case winners with runner-ups (six use cases shipped).
   No overall ranking.
4. **Phase-2 benchmarks:** cut. The methodology section discloses that no
   independent benchmark was run for this edition.
5. **Monetization:** none for v1; revisit only with disclosure.

## 9. Shipped checklist

- [x] index.html (~5,800 words, 13 sections, JSON-LD Article/FAQ/ItemList, zero JS)
- [x] styles.css (hand-set "typeset report" system)
- [x] llms.txt + llms-full.txt + index.md (markdown mirrors)
- [x] robots.txt (explicit AI-crawler welcome), sitemap.xml, humans.txt
- [x] assets/favicon.svg, assets/og.png (generated, 1200×630)
- [x] _headers (Cloudflare Pages), README deploy guide, RESEARCH.md fact base
- [ ] corrections@websearch.dev email routing (owner action before launch)
- [ ] DNS: point websearch.dev at Cloudflare Pages (owner action)
