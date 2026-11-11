# RESEARCH.md — working notes behind the comparison

All data captured **2026-11-11** by fetching the live sources below. This is the
fact base for `index.html`; update this file first when re-verifying, then the page.

## You.com
Sources: https://you.com/docs/choose-the-right-api (+ `.md`), https://you.com/docs/llms.txt, https://en.wikipedia.org/wiki/You.com
- Web Search API $5/1k calls, up to 100 results/call; snippets default; highlights/full-page via `extraction`; full-page add-on $1/1k live pages
- Contents API $1/1k pages · Answer API $5/1k, p50 2.67s · Research API $12/1k (lite) → $1,200/1k (frontier) · Finance Research $110/1k (deep), $500/1k (exhaustive)
- Inference Router: OpenAI-/Anthropic-compatible, open-weight models, server-side web grounding, per-model price, no platform fee
- MCP: `api.you.com/mcp`; keyless `?profile=free` exposes `you-search` + `you-discover`; docs MCP `you.com/docs/_mcp/server`; OpenAPI at you.com/docs/openapi.json; env `YDC_API_KEY`
- Plugins/skills for Claude Code, Cursor, Codex, Windsurf, Gemini CLI, VS Code, JetBrains, Zed, Pi, OpenCode, Copilot CLI, Grok Build, Kimi Code, Jan, Factory Droid, DeepSeek Harness
- Founded 2020, Richard Socher + Bryan McCann (Wikipedia). Funding: ~$95M+ reported incl. $50M Series B led by Georgian (2024) — NOT verified from primary source this session; cited as "reported" via Crunchbase

## Exa
Sources: https://exa.ai/pricing, https://docs.exa.ai/llms.txt, https://exa.ai/blog/announcing-series-b
- Search: Lite $4 / Auto $7 / Deep $12 per 1k (10 results incl.); +$1/1k extra results; AI summaries $1/1k pages; Contents $1/1k pages per content type; Monitors $2/1k; Answer $5/1k
- Agent: effort minimal $0.012 → x-high $1.00 per run; ACU $0.10; email enrich $0.02, phone $0.07; ultra = usage-based
- Free: $10 credits/mo + $10 onboarding, no card; 10 search QPS (25 PAYG); 50 agent concurrency
- Enterprise: SOC 2 Type II, ZDR ($12k annual commitment), HIPAA, SSO/SCIM, custom QPS, custom indexes, up to 1,000 results/search
- Latency: 450ms–1s configurable (per pricing page)
- Cursor case study quoted on pricing page ("Cursor uses Exa to get the latest docs")
- Exa Connect providers self-serve: Jinko, Affiliate.com, Particle, Fiber.ai, Baselayer, Similarweb; on request: ZoomInfo, Crunchbase, Harmonic, DefinitiveHealthcare
- Founded 2021 as Metaphor — Will Bryk & Jeff Wang (YC). $85M Series B led by Benchmark, ~$700M valuation reported (Exa blog title + coverage)

## Parallel
Sources: https://docs.parallel.ai/getting-started/pricing (.md), https://docs.parallel.ai/llms.txt
- Search $1/1k (turbo, fast) or $5/1k (basic, advanced), 10 results incl., +$1/1k beyond; 200ms–3s
- Extract $1/1k URLs · Image/Place search $1–5/1k · Decisions $1/1k (100 questions/req) · Entity Search $5/1k (100 results)
- Task API processors/1k runs: lite $5, base $10, core $25, core2x $50, pro $100, ultra $300, ultra2x $600, ultra4x $1200, ultra8x $2400; only successful runs billed; 10s–2hr
- Responses API $10/$50/$250 per 1k by reasoning effort · Monitor $3–10/1k checks · FindAll $0.25/run + $0.03/match
- v1beta → v1 GA breaking changes (search_queries required, advanced_settings nesting); migration guides from Exa, Tavily, Brave, Perplexity, SERP APIs
- Publishes "How to Eval Parallel Search" incl. common pitfalls (objective vs search_queries)
- Founded 2023 by Parag Agrawal (ex-Twitter CEO). $30M seed (2024) + $100M Series A (late 2025, ~$740M valuation) — reported, cited via Crunchbase

## Tavily
Sources: https://docs.tavily.com/documentation/api-credits (.md), https://docs.tavily.com/llms.txt, https://nebius.com/newsroom/..., https://www.tavily.com/blog/tavily-is-joining-nebius
- Credits: free 1,000/mo (no card) · PAYG $0.008/credit · plans $30/4k → $100/15k → $220/38k → $500/100k ($0.0075→$0.005)
- Search: basic 1 credit, advanced 2 · Extract: 5 URLs = 1 credit (basic) / 2 credits (advanced) · Map: 10 pages = 1 credit (2 with instructions) · Crawl = map + extract · Research: mini 4–110, pro 15–250 credits/req
- Failed extractions/maps never charged
- CLI: `pip install tavily-cli`, `tvly login` · MCP server · docs MCP at docs.tavily.com/mcp · agent skills; x402 machine-payments doc exists
- **Nebius (NASDAQ: NBIS) announced agreement to acquire Tavily, Feb 10, 2026** (Nebius newsroom); Tavily docs llms.txt: "Tavily is part of the Nebius product portfolio"
- Founded 2023; ~$25M raised pre-acquisition (reported: $5M seed + $20M Series A led by Insight Partners, 2025) — cited via Crunchbase

## Keenable
Sources: https://docs.keenable.ai/llms.txt, https://docs.keenable.ai/pricing (.md)
- Keyless (no account): search + fetch free; 1,000 req/hr + 10 rps per IP; raw HTTP via `/v1/search/public`, `/v1/fetch/public` with `X-Keenable-Title` header
- API key (free): 100,000 req/mo free, then $4/1k (1 credit per call: search.pro, search.realtime, fetch, fetch.live); ≤50 results per search billed same as 1
- x402 pay-per-request: $0.01 search/fetch, $0.10 SELECT, USDC on Base; ZeroClick prepaid credits from $0.50; 50 rps per wallet
- Dedicated capacity $1/1k at ≥100 rps (cloud or on-prem); per-org pricing between $1–4/1k
- SDKs TS (`npm i keenable`), Python, Go — keyless by default; `to_context()` citation blocks; device login `keenable login`; MCP server; docs-as-MCP; status.keenable.ai
- Search operators: `"exact"`, `site:a.com OR site:b.com`, `-site:`, `-"phrase"`; modes pro/realtime; fetch returns markdown, `live=true` live-from-source (HTTP only, SDKs pending)
- Data policy: keyless/default-policy queries and fetched URLs are logged and stored — docs explicitly warn against sending secrets (docs.keenable.ai/data-privacy)
- Time Machine endpoints experimental (own SKUs)
- Independent; no public funding announcements found (about page is JS-rendered; no data captured)

## Not verified this session (handle with care on update)
- You.com / Parallel / Tavily funding specifics → cited as "reported" + Crunchbase links
- Keenable index size, company background → nothing published; page says "no public funding announcements as of this writing"
- No hands-on benchmarks were run; the page discloses this in the methodology section
