# The Web Search API Landscape

> A long-form comparison of You.com, Exa, Parallel, Tavily, and Keenable — the five web search APIs for developers and AI agents. Updated and verified November 11, 2026. Canonical page: https://websearch.dev/

**Disclosure.** The author builds search APIs for a living and is employed by one of the five companies covered here. Every factual claim links to a public source, every price carries an as-of date, and each vendor — employer included — gets an explicit Weaknesses list. Errors or staleness? See the changelog & corrections policy (section 13).

Machine-readable mirrors: https://websearch.dev/llms.txt · https://websearch.dev/llms-full.txt · https://websearch.dev/index.md

## Contents

1. The TL;DR table
2. How this was evaluated
3. You.com — the all-in-one retrieval stack
4. Exa — the neural search engine for AI
5. Parallel — the deep-research workshop
6. Tavily — the web access layer
7. Keenable — the keyless upstart
8. Winners by use case
9. The agent-readiness scorecard
10. Honorable mentions
11. FAQ
12. Sources
13. Changelog & corrections

---

## 01 · The TL;DR table

Prices per 1,000 units in USD, verified against the vendors' own documentation on November 11, 2026. Pricing in this category moves fast — a dated snapshot, not gospel.

| Vendor | Search /1k | Free tier | Deep research | MCP | Keyless | Best at |
|---|---|---|---|---|---|---|
| You.com | $5 (≤100 results) | Free credits; keyless free MCP profile | $12–1,200 /1k | ✓ | Partial | All-in-one retrieval stack |
| Exa | $4–12 (10 results) | $10 credits/mo, no card | $0.012–1.00 /run | ✓ | ✗ | Semantic & code search |
| Parallel | $1–5 (10 results) | Self-serve; see console | $5–2,400 /1k runs | ✓ | ✗ | Deep research & enrichment |
| Tavily | ≈$4–8 effective | 1,000 credits/mo | 4–250 credits/req | ✓ | ✗ | Crawling & site ingestion |
| Keenable | $4 flat (≤50 results) | Keyless + 100k req/mo free | — (SELECT instead) | ✓ | ✓ | Zero-friction & autonomous agents |

"Keyless" means a working API call with no account and no API key. You.com's free MCP profile (`?profile=free`) is keyless for search; its REST APIs take a key. Effective Tavily pricing converts credits at plan rates ($0.005–0.008/credit; basic search = 1 credit). Deep-research figures are the vendors' effort-tiered ranges.

---

## 02 · How this was evaluated

On November 11, 2026 we read each vendor's public documentation end to end — pricing pages, API references, quickstarts, and, where they exist, their llms.txt files — plus company announcements and public funding records. Every external claim carries a reference to the numbered sources (section 12); every source was retrieved the same day.

Six criteria, in the order working engineers usually weight them:

1. **Retrieval product** — index ownership, search modes, result counts, content extraction.
2. **Price** — normalized per 1,000 requests, including the fine print (per-result add-ons, credit multipliers).
3. **Developer experience** — SDKs, docs quality, error behavior, time-to-first-call.
4. **Agent-readiness** — MCP servers, keyless access, machine payments, machine-readable docs.
5. **Company trajectory** — funding, ownership, and what that implies for roadmap stability.
6. **Fit by use case** — because "best" without a workload is marketing.

**What this edition is not.** We did not run an independent retrieval benchmark — no controlled query set, no latency harness, no relevance judging. Where we discuss quality, we rely on documented behavior and the vendors' published case studies, and we say so. Parallel, to its credit, publishes a rigorous guide to evaluating search APIs fairly [8]; if you are shortlisting, run your own eval on *your* queries before signing anything.

---

## 03 · Vendor № 1 — You.com — the all-in-one retrieval stack

*Last verified 2026-11-11.*

The broadest product surface of the five: one API key covers raw search, page contents, a cited-answer endpoint, multi-step research, a finance vertical, and an inference router that grounds open-weight models in live web results.

**Fact sheet**

- Search price: `$5 / 1k calls`, up to 100 results per call [1]
- Free tier: free credits, no card; keyless search via MCP `?profile=free` [2]
- Contents/extraction: `$1 / 1k pages`; full-page add-on on search `$1 / 1k live pages` [1]
- Deep research: `$12–1,200 / 1k` by effort (`lite`→`frontier`) [1]
- Answer API: `$5 / 1k`, p50 2.67s, cited markdown [1]
- Agent surface: MCP server + plugins for Claude Code, Cursor, Codex, Zed, Gemini CLI & more [2]
- Founded: 2020 — Richard Socher & Bryan McCann [15]
- Funding: ≈$95M+ reported, incl. Series B led by Georgian [17]

### Overview

You.com is the elder of this cohort. Founded in 2020 by Richard Socher — formerly Salesforce's chief scientist and one of the most-cited researchers in NLP — and Bryan McCann, it began life as a consumer search engine before pivoting, earlier than most, to selling search as infrastructure [15]. That pivot shows in the catalog: rather than one search endpoint, You.com sells a small retrieval department. The Web Search API returns ranked web and news results at a flat $5 per 1,000 calls with up to 100 results per call — the most results per request of anyone here. The Contents API turns known URLs into markdown at $1 per 1,000 pages. The Answer API does one retrieval pass and returns a cited markdown answer at a published p50 of 2.67 seconds. Above that sit the Research API — multi-step, effort-tiered from `lite` ($12/1k) to `frontier` ($1,200/1k) — and a Finance Research API over a finance-tuned index. The Inference Router wraps it all: OpenAI- and Anthropic-compatible endpoints for leading open-weight models with server-side web grounding, priced per model with no platform fee [1].

### Products & developer experience

The developer experience is built around meeting agents where they live. There is a hosted MCP server (`api.you.com/mcp`), a separate read-only MCP for searching the documentation itself, and — unusually — a **keyless free tier**: appending `?profile=free` to the MCP URL exposes working search with no signup at all [2]. Official plugins exist for Claude Code, Cursor, Codex, Gemini CLI, Zed, Windsurf, VS Code, JetBrains, and a long tail of other harnesses [2]. Every docs page is available as markdown and there is a public OpenAPI spec. Time-to-first-call is the shortest of the five if you start from an agent; from raw REST it is a normal API-key flow with free credits and no card required.

### Strengths

- **Breadth in one bill.** Search, contents, answers, deep research, finance, and grounded inference share one key and one invoice. Replacing two or three vendors with one is real money and real operational simplicity.
- **Simple, flat search pricing.** $5/1k with up to 100 results per call undercuts per-result models once you consume more than ~10 results per query. [1]
- **Keyless on-ramp for agents.** The free MCP profile lets an agent search before any human creates an account — a genuine differentiator for autonomous tooling. [2]
- **Published latency.** The Answer API's p50 2.67s is the kind of specificity buyers want and vendors rarely print. [1]
- **Enterprise runway.** The oldest company here, with the longest track record of supplying search into third-party products.

### Weaknesses

- **Breadth over depth.** No single endpoint is the category's sharpest: Exa's code retrieval and Parallel's research ladder are each more specialized than their You.com counterparts.
- **Top-end research is expensive.** `frontier` effort at $1.20 per call adds up fast in agent loops that default to maximum effort. [1]
- **Add-on pricing for full pages.** Snippets come with search, but full-page extraction during search is a separate $1/1k live-page charge to keep in your cost model. [1]
- **Keyless covers MCP only.** The no-account path is real but narrow — the REST APIs still require signup, where Keenable is keyless end to end.
- **Brand residue.** The consumer-search years still muddy positioning; some buyers file You.com under "search engine" rather than "retrieval infrastructure."

### Opportunities

- Consolidation: teams that started on three point solutions may collapse onto one retrieval-plus-inference vendor — exactly the bundle You.com sells.
- The Inference Router rides open-weight model adoption; grounding is table stakes for production open models, and "no platform fee" is a sharp wedge.
- Vertical research (finance today) is a repeatable playbook — legal, life sciences, and procurement are natural sequels.

### Threats

- Foundation-model vendors bundle web search into their APIs (OpenAI, Anthropic, Google all do), squeezing standalone retrieval for casual use cases.
- Keyless free tiers from Keenable and others reset price expectations toward zero at the low end.
- Focused competitors out-position on single workloads ("search for coding agents," "deep research API") even where the bundled product is comparable.

**Best for:** teams that want one vendor for search, extraction, answers, and research — and agents that need to search before anyone has created an account.

---

## 04 · Vendor № 2 — Exa — the neural search engine for AI

*Last verified 2026-11-11.*

The retrieval purist. Exa built its own neural (embedding-based) search engine from scratch, optimized for the queries machines write rather than the queries humans type — and it shows in a customer list led by coding tools.

**Fact sheet**

- Search price: `$4 / $7 / $12 per 1k` (Lite / Auto / Deep), 10 results included [3]
- Free tier: $10 credits/mo + $10 onboarding, no card; 10 QPS [3]
- Contents: `$1 / 1k pages` per content type; summaries `$1 / 1k` [3]
- Agent (research): `$0.012–$1.00 / run` by effort; usage-based ultra [3]
- Latency: configurable, 450ms–1s [3]
- Enterprise: SOC 2 Type II, ZDR, HIPAA, SSO/SCIM, custom indexes [3]
- Founded: 2021 (as Metaphor) — Will Bryk & Jeff Wang
- Funding: $85M Series B led by Benchmark; reported ~$700M valuation [5]

### Overview

Exa started in 2021 as Metaphor, a YC-backed bet that Google-style keyword retrieval was the wrong primitive for language models. The thesis: humans type "best CRM 2026"; agents need "the paragraph in the docs that explains idempotent payout creation." That needs embeddings, not inverted indexes, so Exa built a neural search engine over its own crawl. The market agreed — an $85M Series B led by Benchmark, at a reported valuation around $700M, makes it the best-funded pure-play on this list [5].

The product line has grown well past search. The Search API offers three latency/quality tiers — Lite ($4/1k), Auto ($7/1k), and Deep ($12/1k) — each including 10 results, with extra results at $1/1k and AI page summaries at $1/1k pages [3]. Contents fetches clean page text at $1/1k pages. The Agent API runs asynchronous deep research with structured outputs and citations, priced by effort from $0.012 (minimal) to $1.00 (x-high) per run, plus compute units. Around that sit Monitors ($2/1k, scheduled searches with webhooks), an Answer endpoint ($5/1k), Websets for list-building, Exa Snapshot for pinning results to a point in time, and Exa Connect — a marketplace that pipes third-party premium data (Similarweb, Baselayer, Fiber.ai; ZoomInfo and Crunchbase on request) through the same integration [3][4]. Specialized sub-indexes cover code and docs, companies and people, academic research, legal records, financials, and news [4].

### Strengths

- **Semantic recall is the real deal.** For fuzzy, conceptual, "find-me-things-like-this" queries — company lookalikes, paper discovery, doc paragraphs — neural retrieval finds what keyword search misses.
- **The coding-agent darling.** A dedicated code/docs index, sub-second Lite search, and a public case study with Cursor make it the default answer in IDE tooling circles. [3]
- **Enterprise paperwork done.** SOC 2 Type II, zero data retention, HIPAA, SSO/SCIM, custom QPS, custom indexes, up to 1,000 results per search on enterprise plans. [3]
- **Genuinely useful free tier.** $10 in credits every month (not just once) with no card, at 10 QPS — enough to run a hobby agent indefinitely. [3]
- **Data-marketplace optionality.** Exa Connect turns one integration into many data sources; nobody else here does that. [4]

### Weaknesses

- **Costs compound by result count.** The headline prices include only 10 results; hungry agent loops that want 50–100 results per query pay per extra result, where You.com's $5 includes 100. [3]
- **Neural search can be opaque.** Embedding retrieval sometimes returns conceptually-adjacent-but-wrong pages, and exact-match queries (part numbers, error strings) can behave less predictably than on keyword engines.
- **Agent pricing is spiky.** Usage-based compute on deep-research runs is hard to budget; fixed effort tiers help but top out at $1/run. [3]
- **No crawl/map product.** For whole-site ingestion you bring your own crawler — Tavily's home turf.
- **$700M expectations.** A rich valuation invites aggressive monetization; watch pricing drift across renewals.

### Opportunities

- Coding agents are still early: every IDE, CLI, and code-review bot needs fresh docs retrieval, and Exa owns the mindshare.
- Websets-style structured list building extends retrieval into GTM, recruiting, and research budgets far beyond engineering.
- Exa Connect could become the distribution layer for niche data providers — a take-rate business on top of search.

### Threats

- Keyword-native rivals are adding vector retrieval; "neural" stops being a moat if hybrid becomes standard.
- Free tiers elsewhere (Keenable's 100k requests/month) undercut the hobbyist mindshare that feeds bottom-up adoption.
- Deep-research economics: if model vendors absorb research workloads into their own APIs, per-run agent pricing compresses.

**Best for:** coding agents and semantic discovery — and enterprises whose procurement checklist includes SOC 2, ZDR, and HIPAA on day one.

---

## 05 · Vendor № 3 — Parallel — the deep-research workshop

*Last verified 2026-11-11.*

Founded by former Twitter CEO Parag Agrawal, Parallel sells the widest API surface of the five — and its center of gravity is not search at all, but multi-step web research as a programmable, per-task-priced product.

**Fact sheet**

- Search price: `$1 / 1k` (turbo, fast) · `$5 / 1k` (basic, advanced); 10 results included [6]
- Extract: `$1 / 1k URLs` [6]
- Task API (research): `$5–2,400 / 1k runs`, 9 processors; failed runs unbilled [6]
- Other APIs: Responses, FindAll, Monitor, Decisions, Image / Place / Entity Search [6][7]
- Latency: search 200ms–3s; Tasks 10s–2hr [6]
- Agent surface: MCP server; migration guides from Exa/Tavily/Brave/Perplexity [7]
- Founded: 2023 — Parag Agrawal
- Funding: $30M seed + reported $100M Series A (late 2025, ~$740M valuation) [16]

### Overview

Parallel launched in 2023 with an unusual founder for this space: Parag Agrawal ran Twitter as CEO through 2022, and before that spent a decade as its CTO. The company raised a $30M seed in early 2024 and a reported $100M Series A in late 2025 at a valuation around $740M [16] — and it has spent that money building not one API but eight: Search, Extract, Task (deep research), Responses, FindAll, Monitor, Decisions, plus Image, Place, and Entity search [6].

The Search API itself is aggressively priced at the low end: $1 per 1,000 requests in `turbo`/`fast` modes (10 results included), $5 per 1,000 in the higher-quality `basic`/`advanced` modes, extra results at $1/1k [6]. Extract converts URLs to LLM-ready markdown at $1/1k URLs. But the flagship is the Task API: nine processor tiers from `lite` ($5/1k runs, 10–60s) to `ultra8x` ($2,400/1k runs, up to two hours), billed per completed run — failed runs are explicitly not billed — with citations, reasoning traces, and confidence levels attached [6]. If Exa sells search and You.com sells a retrieval stack, Parallel sells analyst-hours by the thousand.

### Products & developer experience

The docs are unusually candid about their own sharp edges. Parallel publishes a guide to evaluating its Search API — including the common pitfalls that make *it* look bad in naive benchmarks [8] (sending the raw question as both objective and query is the classic mistake). It also ships migration guides from Exa, Tavily, Brave, Perplexity, and SERP APIs [7], which tells you exactly who it thinks it is replacing. One caution: the Search and Extract APIs went through a beta-to-GA transition with breaking request-body changes (`/v1beta` → `/v1`), so pin your integration and read the migration guide before upgrading [7].

### Strengths

- **The deepest research ladder.** Nine priced tiers with latency bands let you dial cost against difficulty per task — the most granular deep-research offering anywhere. [6]
- **Cheapest entry search.** $1/1k at the turbo tier is the lowest sticker price among the five for standard queries. [6]
- **Only-pay-for-success policies.** Failed Task runs and failed extracts don't bill — the pricing model trusts you back. [6]
- **Beyond web pages.** Entity, image, and place search plus FindAll list-building cover enrichment workflows the others route around. [6]
- **Eval culture.** Publishing a "how to eval us fairly" guide signals confidence and respect for buyers' methodology. [8]

### Weaknesses

- **Request-schema complexity.** The objective/search_queries split is powerful but easy to get wrong — their own docs warn about it — and the v1beta→v1 breaking change cost early adopters a migration. [7][8]
- **Two-tier search quality pricing.** The $1 tier exists partly to make the $5 tier the real recommendation; budget for the mode you actually need.
- **Youngest brand, biggest expectations.** A ~$740M valuation on a 2023 company means enterprise buyers should test staying power, not just accuracy.
- **No keyless or recurring free on-ramp documented.** Evaluation requires signup, where rivals offer keyless calls or monthly free credits.
- **Surface sprawl.** Eight APIs is a lot of roadmap to keep coherent; watch for uneven investment across products.

### Opportunities

- Deep research is the budget line enterprises understand ("analyst work, but API-shaped"), and Parallel has the clearest packaging for it.
- Monitoring and FindAll open recurring-revenue workflows — compliance watchlists, competitive intelligence, database enrichment.
- If agents shift from "search and read" to "research and decide," the center of the market moves toward Parallel's home turf.

### Threats

- Model labs ship their own deep-research products (OpenAI, Gemini, Perplexity), which could cap what an independent research API can charge.
- Complexity tax: simpler rivals win the default integration while Parallel is still being evaluated.
- Search as a loss leader: the $1 tier invites price-war dynamics with Keenable's free tier and Exa's credits.

**Best for:** deep-research and enrichment pipelines — teams that think in tasks and reports, not queries and snippets.

---

## 06 · Vendor № 4 — Tavily — the web access layer

*Last verified 2026-11-11.*

The developer-experience darling and the only one of the five with real crawl and site-map products. Now part of Nebius — which makes it both the safest pair of hands here and the biggest strategic question mark.

**Fact sheet**

- Search price: 1 credit (basic) / 2 credits (advanced) per request [9]
- Credit price: `$0.008` PAYG · `$0.005–0.0075` on plans [9]
- Free tier: 1,000 credits/mo, no card [9]
- Extract / Map / Crawl: extract 5 URLs/credit · map 10 pages/credit · crawl = map + extract [9]
- Research: 4–110 credits (`mini`) · 15–250 credits (`pro`) per request [9]
- Agent surface: MCP, CLI (`tavily-cli`), agent skills, docs-as-MCP [10]
- Founded: 2023; reported ~$25M raised pre-acquisition [18]
- Ownership: acquired by Nebius (announced Feb 2026) [11][12]

### Overview

Tavily named its category early — "the web layer for AI agents" — and executed on a single idea: return clean, LLM-ready web content instead of raw HTML, with billing that never surprises. The product line is compact: Search, Extract, Map, Crawl, and Research [10]. The pricing model is one currency: API credits. Basic search costs 1 credit, advanced costs 2; five extractions cost 1 credit; ten mapped pages cost 1; crawling is just map + extract priced as the sum; research runs 4–250 credits depending on model and depth. Failed extractions and failed maps are never charged [9]. At pay-as-you-go rates ($0.008/credit) a basic search works out to $8 per 1,000; on the $500 Growth plan ($0.005/credit) it falls to $4 [9].

The big 2026 story is corporate: in February, Nebius — the NASDAQ-listed AI cloud company — announced an agreement to acquire Tavily, folding agentic search into its Token Factory stack [11]. Tavily's own docs now describe it as part of the Nebius product portfolio [10]. For buyers this cuts both ways, and we score both directions below.

### Strengths

- **The only crawler in the room.** Map (site-structure discovery) and Crawl (bulk page ingestion) are products none of the other four ship; for feeding a RAG pipeline from whole sites, Tavily is the shortest path. [9]
- **Fastest integration.** Two commands — `pip install tavily-cli`, `tvly login` — and you are searching from a terminal; SDKs, MCP, and agent skills round it out. [10]
- **Failure-is-free billing.** You never pay for a failed extraction or map — small thing, big trust. [9]
- **Predictable credit math.** One currency across five products makes capacity planning trivial compared to multi-SKU rivals.
- **Public-company backing.** Nebius ownership brings GPU supply, enterprise channel, and balance-sheet credibility no startup here can match. [11]

### Weaknesses

- **Smallest recurring free tier.** 1,000 credits/month is roughly 1,000 basic searches — an order of magnitude below Keenable's 100k requests, and tighter than Exa's monthly credit drip for real workloads. [9]
- **Effective prices are mid-pack, not cheap.** $8/1k PAYG basic search (and $16/1k advanced) only becomes competitive at plan volume; casual users pay the most. [9]
- **Research costs are bounded but variable.** A 4–110 or 15–250 credit range per request is harder to budget than a flat per-call price. [9]
- **Acquisition integration risk.** Roadmap, pricing, and brand are Nebius decisions now; the "independent web layer" story is over by definition. [11]
- **Few hard numbers published.** Compared to Exa's 450ms tiers or You.com's p50 figure, Tavily publishes less on latency and index architecture to plan around.

### Opportunities

- Nebius distribution: every GPU-cloud customer is now a warm lead for the web layer — an enterprise channel none of the independents can buy. [11]
- Bundled agentic stack: search + inference + compute in one procurement motion is genuinely simpler for large buyers.
- Crawl-led lock-in: teams that ingest their corpus through Tavily tend to keep querying through it too.

### Threats

- Post-acquisition focus drift is the classic failure mode — especially if Nebius prioritizes bundle revenue over the standalone API.
- Agent-ecosystem wariness: some buyers will avoid a search layer owned by a cloud provider for the same reason they avoid single-cloud lock-in.
- Independents (Keenable, Exa) now own the "neutral Switzerland" positioning Tavily vacated.

**Best for:** ingestion-heavy RAG (crawl a site, keep it fresh) and teams that value a two-command quickstart — with eyes open about the Nebius roadmap.

---

## 07 · Vendor № 5 — Keenable — the keyless upstart

*Last verified 2026-11-11.*

The newest and strangest of the five: an independent index, no funding announcements, and a radical distribution bet — search that works with no account, no key, and (if you are a machine) payment in USDC per request.

**Fact sheet**

- Search price: `$4 / 1k requests` flat, up to 50 results; 1 credit per call [14]
- Keyless tier: free, no account: 1,000 req/hr + 10 rps per IP [13][14]
- Free tier (with key): **100,000 requests/mo free**, then prepaid credits [14]
- Machine payments: x402 `$0.01`/request in USDC on Base; ZeroClick prepaid from $0.50 [14]
- Fetch: 1 credit; markdown out; `live=true` bypasses the index [13]
- Also: SELECT structured queries; Time Machine (experimental); TS/Python/Go SDKs; MCP [13]
- Modes: `pro` (deeper) & `realtime` (fastest), both 1 credit [13]
- Company: independent; no public funding announcements as of this writing

### Overview

Keenable is what you get if you design a search API for the agent economy instead of for human developers who later add agents. Its documentation leads with an llms.txt file of agent instructions: install the SDK — TypeScript, Python, or Go — and it works *keyless by default*, rate-limited per IP (1,000 requests/hour, 10/second) instead of by account [13]. Add a free API key and the limits change shape: 100,000 requests per month free, then prepaid credits at $4 per 1,000 requests — search or fetch, one credit per call whether you ask for 1 result or 50 [14]. Dedicated capacity runs $1 per 1,000 at 100+ requests per second. And for agents that will never have a human in the loop, there is x402 — HTTP-native payment per request in USDC on Base — plus prepaid micro-credits through ZeroClick starting at fifty cents [14].

The API itself is refreshingly small: `/v1/search` with real operators (quotes, `site:`, `OR`, negation) in `pro` or `realtime` mode, and `/v1/fetch`, which returns any page as markdown — from Keenable's own index, or live from the source with `live=true` [13]. SELECT adds structured queries over web data for free accounts; experimental Time Machine endpoints hint at historical snapshots. Results ship with a `to_context()` helper that formats numbered, citable blocks for a model [13].

### Strengths

- **Friction zero.** `npm install keenable` and you are searching — no signup, no key, no card. For hackathons, CI jobs, and truly autonomous agents, nothing else here comes close. [13]
- **The most generous free tier by far.** 100,000 requests/month with a free key is 100× Tavily's allowance and, in request terms, dwarfs Exa's credit drip. [14]
- **Agent-native payments.** x402 USDC per-request billing is the only credible machine-to-machine payment story here — agents can pay for their own search. [14]
- **Flat, honest pricing.** $4/1k regardless of result count (up to 50) or mode; failed calls unbilled; a published error taxonomy with causes and fixes. [13][14]
- **Practices what it preaches.** Docs ship as an llms.txt, an MCP server, and per-page markdown; there is a public status page and a plain-language data-privacy doc. [13]

### Weaknesses

- **Unproven index depth.** Running your own crawl is brutally expensive; freshness and long-tail coverage against Exa's and You.com's mature indexes is the open question buyers must test with their own queries.
- **Thin product line.** Search, fetch, SELECT. No answer endpoint, no deep research, no crawl/map, no monitors — you will pair it with something else for advanced workloads.
- **Enterprise unknowns.** No published SOC 2 / ZDR / HIPAA posture, no SSO story; custom pricing is "per organization" on request. [14]
- **Query logging by default.** On keyless and default-policy traffic, Keenable stores queries and fetched URLs — fine for public data, a real consideration for anything sensitive. [13]
- **SDK/HTTP feature lag.** The `live=true` fetch flag is HTTP-only so far — small, but a reminder of how young the platform is. [13]

### Opportunities

- The x402/machine-payment niche is Keenable's to lose; if agent-to-agent commerce materializes, being first matters.
- Bottom-up adoption: keyless SDKs spread through templates, examples, and agent skills faster than any sales team.
- Price disruption: $1/1k dedicated capacity at scale undercuts everyone if quality holds. [14]

### Threats

- Free-tier economics: 100k free requests per month per organization is a lot of crawl compute to give away without announced funding behind it.
- Incumbents copy keyless: You.com already ships a keyless MCP profile; if Exa or Parallel follow, Keenable's wedge narrows to price.
- Trust gap: enterprises will hesitate to route production traffic through a vendor with no published compliance posture, however elegant the SDK.

**Best for:** prototypes, side projects, CI jobs, and autonomous agents that need search before — or without — a human signing up for anything.

---

## 08 · Winners by use case

There is no honest overall ranking — there are workloads. Who we'd pick today for the six we see most:

1. **Building a coding agent or IDE tool → Exa** (runner-up: You.com). Exa's code/docs index, 450ms-class Lite tier, and the Cursor case study make it the purpose-built choice [3]; You.com is the runner-up for its keyless free MCP profile and plugins covering nearly every agent harness [2].
2. **Production RAG & Q&A chatbots → You.com** (runner-up: Tavily). One flat $5/1k for up to 100 results, a $1/1k contents endpoint, and a cited Answer API at a published p50 2.67s is the most complete RAG toolkit on one bill [1]; Tavily's one-currency model is the simplest to budget at smaller scale [9].
3. **Deep-research & enrichment pipelines → Parallel** (runner-up: Exa). Nine Task processors from $5 to $2,400 per 1k runs, failed runs unbilled, structured outputs with citations [6]; Exa's Agent API is a strong runner-up with cheaper top-end runs ($1.00 x-high) [3].
4. **Side projects, prototypes & account-free agents → Keenable** (runner-up: Exa). Keyless SDKs and 100k free requests a month mean your prototype may never cost anything [14]; Exa's recurring $10 monthly credits are the best runner-up for hobby scale [3].
5. **Site crawling & bulk ingestion → Tavily** (runner-up: Parallel). Tavily is the only one shipping Map and Crawl products, with failed pages unbilled [9]; for URL lists you already have, Parallel's Extract at $1/1k URLs is a clean alternative [6].
6. **Enterprise procurement & compliance → Exa** (runner-up: You.com). Exa publishes the full checklist — SOC 2 Type II, zero data retention, HIPAA, SSO/SCIM, custom indexes and QPS [3]; You.com offers enterprise plans and the longest operating history.

---

## 09 · The agent-readiness scorecard

In 2026, a growing share of "developers" evaluating these APIs are themselves agents. How the five score on machine-first criteria (verified 2026-11-11):

| | You.com | Exa | Parallel | Tavily | Keenable |
|---|---|---|---|---|---|
| MCP server | ✓ + docs MCP | ✓ | ✓ | ✓ + docs MCP | ✓ + docs MCP |
| Keyless first call | ✓ (MCP free profile) | ✗ | ✗ | ✗ | **✓ (all APIs)** |
| llms.txt docs | ✓ | ✓ | ✓ | ✓ | ✓ |
| Machine payments | ✗ | ✗ | ✗ | ✓ (x402 docs) | **✓ (x402 live)** |
| Agent skills / plugins | **✓ (broadest)** | ✓ | — | ✓ | ✓ (AI SDK tool) |
| Recurring free tier | ✓ credits | **✓ $10/mo** | — | ✓ 1k credits/mo | **✓ 100k req/mo** |

Sources: each vendor's docs/llms.txt. Tavily documents x402 machine payments; Keenable runs them in production with per-request USDC pricing. [10][14]

---

## 10 · Honorable mentions

Five slots meant hard cuts. These are worth knowing, briefly:

- **Brave Search API** — an independent index with a generous free tier and LLM-grounding endpoints; the credible sixth man, excluded only because Parallel's docs already treat it as the incumbent they migrate customers from. [7]
- **Serper / SerpAPI / DataForSEO** — Google SERP APIs: cheap, fast, familiar — but they resell Google results rather than operate an AI-native index, with different terms-of-service trade-offs.
- **Jina AI Reader** — `r.jina.ai` remains the quick-and-free way to turn a URL into LLM-ready text; a utility more than a search platform.
- **Firecrawl** — open-source crawling/scraping for LLMs; overlaps Tavily's crawl lane more than the search lane.
- **Perplexity Sonar API** — a cited-answer API riding Perplexity's consumer brand; an Answer-API alternative more than a raw-results one.

---

## 11 · FAQ

**Which web search API is the best overall?**
There isn't one. Exa leads for coding agents and semantic search, You.com for production RAG, Parallel for deep research, Keenable for zero-budget and keyless prototyping, and Tavily for crawling and ingestion. Pick by workload.

**What's the cheapest way to add web search to an agent?**
Keenable: no key at all gets you 1,000 requests/hour per IP, and a free key gets 100,000 requests/month [14]. Also free-ish: You.com's keyless MCP profile [2], Exa's $10 monthly credits [3], and Tavily's 1,000 monthly credits [9].

**Does it matter whether a vendor owns its index?**
Mostly yes. Owning the index (as all five here do to varying degrees) means control over freshness, ranking, and coverage — and no dependency on Google or Bing's API terms. SERP-reselling APIs can be cheaper for simple keyword lookups but inherit upstream risk and offer less control over what an agent actually receives.

**How current is the pricing on this page?**
Every price was verified against the vendors' public documentation on November 11, 2026, and each vendor section carries a "last verified" stamp. This market reprices quarterly — confirm on the vendor's page before committing budget, and check the changelog for updates.

**Is this page biased?**
The author works at one of the five vendors — that's disclosed at the top, and it's why the comparison exists (practitioners read these docs daily). The counterweights: every factual claim is sourced, pricing is dated, every vendor including the author's employer gets an explicit weaknesses list, winners are named per use case rather than overall, and corrections go in the public changelog.

**Can my agent read this page?**
Yes — that's the point. /llms.txt has the summary and verdicts, /llms-full.txt has the full text, and /index.md is the page as Markdown. The HTML is semantic, script-free, and readable by any extractor.

**What about Brave, Serper, Jina, Firecrawl, or Perplexity Sonar?**
See honorable mentions (section 10). They're real options — we scoped this page to the five APIs purpose-built as web search infrastructure for AI developers.

---

## 12 · Sources

All links retrieved November 11, 2026. Funding figures not drawn from a vendor's own announcement are marked "reported" in the text and sourced to public records.

1. You.com Docs — Choose the Right API (products, latency, pricing table): https://you.com/docs/choose-the-right-api
2. You.com Docs — llms.txt (MCP server, keyless `?profile=free`, agent-harness plugins): https://you.com/docs/llms.txt
3. Exa — Pricing (endpoint prices, free tier, QPS, enterprise controls, Cursor case study): https://exa.ai/pricing
4. Exa Docs — llms.txt (product surface, data indexes, Exa Connect providers): https://docs.exa.ai/llms.txt
5. Exa Blog — Series B announcement ($85M led by Benchmark; ~$700M valuation as reported): https://exa.ai/blog/announcing-series-b
6. Parallel Docs — Pricing (all API prices, processor tiers, billing policies): https://docs.parallel.ai/getting-started/pricing
7. Parallel Docs — llms.txt (product surface, v1beta→v1 migration, migration guides): https://docs.parallel.ai/llms.txt
8. Parallel Docs — How to Eval Parallel Search (evaluation methodology and pitfalls): https://docs.parallel.ai/search/evaluating-search
9. Tavily Docs — Credits & Pricing (credit model, plan prices, per-endpoint costs): https://docs.tavily.com/documentation/api-credits
10. Tavily Docs — llms.txt (product surface, CLI, MCP, Nebius portfolio note, x402 docs): https://docs.tavily.com/llms.txt
11. Nebius Newsroom — Agreement to acquire Tavily (February 10, 2026): https://nebius.com/newsroom/nebius-announces-agreement-to-acquire-tavily-to-add-agentic-search-to-its-ai-cloud-platform
12. Tavily Blog — Tavily is Joining Nebius: https://www.tavily.com/blog/tavily-is-joining-nebius
13. Keenable Docs — llms.txt (keyless access, SDKs, operators, modes, data policy, MCP): https://docs.keenable.ai/llms.txt
14. Keenable Docs — Pricing (free tiers, $4/1k, x402, dedicated capacity, billing rules): https://docs.keenable.ai/pricing
15. Wikipedia — You.com (founders, founding year): https://en.wikipedia.org/wiki/You.com
16. Crunchbase — Parallel AI (reported seed and Series A figures): https://www.crunchbase.com/organization/parallel-ai
17. Crunchbase — You.com (reported funding history): https://www.crunchbase.com/organization/you-com
18. Crunchbase — Tavily (reported pre-acquisition funding): https://www.crunchbase.com/organization/tavily

---

## 13 · Changelog & corrections

Pricing in this market moves quarterly. Each vendor section carries its own "last verified" date; material changes are logged here. Spot an error? Email corrections@websearch.dev — sourced corrections are applied within 48 hours and noted below.

| Date | Change |
|---|---|
| 2026-11-11 | Initial publication. All five vendor sections verified against public docs same-day. |

---

*websearch.dev — an independent, long-form comparison of web search APIs for developers and the agents reading on their behalf. No cookies, no analytics, no JavaScript. Hand-written HTML & CSS. All trademarks belong to their owners. Prices are dated snapshots of public pages, not offers.*
