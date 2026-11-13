# TPRD — websearch.dev, long term

**Status:** proposal · **Date:** 2026-11-13 · **Supersedes:** the strategy sections of `PRD.md` (v1 page stays as the seed content)

---

## 1. Thesis

websearch.dev should stop being an article and become the **system of record for the web search API category**: an open, machine-readable registry of every provider, the evidence about how they perform, and the tools that turn that evidence into a decision.

The closest analogies are models.dev (registry), a poll aggregator (evidence), and caniuse (decision). Nobody holds that position for search APIs today, and an exact-match `.dev` domain is the right place to hold it.

The article is the wrong long-term product for one reason: it has no moat. Any agent can regenerate a docs-derived comparison of five vendors in minutes, and the prices in it go stale within weeks. Data that is continuously verified, measured, and consumed by other tools cannot be regenerated on demand.

---

## 2. Assessment of the current approach

### What is right and should be kept

- **Agents as first-class readers.** `llms.txt`, markdown mirrors, JSON-LD, and zero-JS HTML are the correct bet.
- **Dated, sourced claims and a weaknesses list for every vendor.**
- **Per-use-case verdicts instead of one ranking.** Every public benchmark found in this review reaches the same conclusion: no provider leads everywhere.
- **The typeset, tracker-free design.** It reads as a reference, which is what it should become.

### What is wrong

| # | Problem | Evidence |
|---|---|---|
| 1 | **The page calls itself independent while the author works for a covered vendor.** | `llms.txt` line 3 opens with "Independent"; the `index.html` footer says "an independent, long-form comparison". `PRD.md` §3 required naming You.com plainly; §8 reversed that. |
| 2 | **The framing favours the employer in ways a skeptical reader will notice.** | You.com is listed first, and wins "Production RAG" on price and breadth alone, with no quality evidence. |
| 3 | **The vendor set omits providers that lead public benchmarks.** | Perplexity's Search API is absent from the five and appears only as "Sonar" in honourable mentions. Brave is excluded for a reason unrelated to its merits. |
| 4 | **No quality evidence at all, in a market now full of it.** | `PRD.md` §8 cut benchmarks. At least nine public benchmarks exist (§3). |
| 5 | **Verdicts conflict with that public evidence.** | Several third-party boards place You.com mid-table or lower (§3), while the page awards it one win and two runner-up spots. |
| 6 | **Hand maintenance will not scale.** | Three hand-synced copies of 5,800 words; the drift check in `PRD.md` §6 was never built; verification is quarterly in a market that reprices faster. |
| 7 | **Nothing is live yet.** | `websearch.dev` resolves to registrar parking and HTTPS does not answer (checked 2026-11-13). |

Problem 7 is good news: problems 1–5 can be fixed before anyone has seen the page.

Problem 1 is the most serious. An agent or journalist who connects the anonymous "independent" page to a You.com employee will discount everything on it, and the discovery will be the story. `PRD.md` already says this in §3. The original instinct was correct.

---

## 3. Market landscape (2026-11-13)

Figures below come from search-result excerpts of each source retrieved today. They have not been audited or reproduced, and each board's configuration choices differ.

### Benchmarks are abundant and they disagree

| Board | Operator | Sells a tested API? | Leader reported |
|---|---|---|---|
| Artificial Analysis Search Index | Artificial Analysis | No | Keenable (83); You.com 74 |
| Openbenchmarks, web search | Openbenchmarks Labs | Not stated | Exa, Perplexity, or Parallel by task; You.com 12th–13th of 14 on search-only coding |
| NEEDLE | Keenable | Yes | Keenable 77%; You.com 63% |
| cloro web-search-api-benchmark | cloro | Yes | Parallel, Exa, cloro tied on SimpleQA |
| AIMultiple agentic search | AIMultiple | No | Parallel Advanced 87.0% |
| Parallel benchmarks | Parallel | Yes | Parallel and Perplexity tied on BrowseComp |
| exa-labs/benchmarks | Exa | Yes | Exa |
| perplexityai/search_evals | Perplexity | Yes | Perplexity |
| Rawlinson bake-off | Individual | No | Perplexity fast for balance |

Two things follow. Running a tenth benchmark adds little. Reconciling the nine adds a lot, because a developer today has to read all of them and guess which to trust. Five of the nine are run by a vendor, and each of those vendors leads or ties for the lead on its own headline result.

### Gateways are abundant and undifferentiated

Mux, OpenWebSearch, GroundRoute, two products named SearchRouter, Lava, Octoryn Search Gateway, and OpenRouter's web search tool all offer one schema, fallbacks, and one bill across the same providers. Each invents its own schema and maintains its own provider price table.

### What is missing

1. A neutral, structured, current record of what each provider offers and charges.
2. A reconciliation of the benchmarks, with operator conflicts made visible.
3. Continuous operational data: latency, uptime, and freshness over time, rather than one-off runs.
4. A shared schema that gateways and SDKs can adopt instead of inventing.
5. A way to test providers on your own queries without building a harness.

websearch.dev should supply these five things. It should not build a hosted gateway or another headline benchmark.

---

## 4. Strategy

**Position:** the reference layer that benchmarks, gateways, agents, and buyers all read from. Gateways and benchmark operators become consumers and contributors, which a competing gateway could never achieve.

**Why not a hosted gateway.** The field has eight entrants, it needs capital and reseller agreements, and it puts a You.com employee in the request path of You.com's competitors. That conflict cannot be disclosed away.

**Why not another benchmark.** See §3. A meta-analysis is cheaper, harder to dismiss as biased, and more useful.

**The compounding loop:**

1. The registry gets cited because it is current and structured.
2. Tools (gateways, SDKs, agents) consume it, so vendors have a reason to submit corrections.
3. Corrections and probes make it more current, which earns more citations.
4. The open SDK and eval runner produce opt-in results on real workloads, which no public benchmark has.

---

## 5. Governance (prerequisite to everything else)

The asset is trust, so these come before any feature.

1. **Name the author and employer** on the page, in `llms.txt`, and in JSON-LD (`author` as a `Person` with `affiliation`).
2. **Remove the word "independent"** as a self-description until a governance structure justifies it.
3. **Everything open:** data under CC BY 4.0, code under MIT, all in this repository. Every figure traces to a source URL, a retrieval date, and a commit.
4. **Vendor-neutral ordering:** alphabetical by default, or sorted by a metric the reader chooses.
5. **Recusal rule:** editorial verdicts involving You.com are either derived mechanically from published evidence or reviewed by a named outside maintainer.
6. **Right of reply:** any vendor can open a pull request or issue against its own record; accepted and rejected corrections are both public.
7. **No paid placement, ever.** Stated in the repository and on the site.

---

## 6. Product

Four surfaces, built in this order. Each is useful alone.

### 6.1 Registry — what exists and what it costs

One YAML record per provider, validated against a JSON Schema.

- **Scope:** about 25 providers at launch. Search APIs (Brave, Exa, Keenable, Linkup, Parallel, Perplexity, Tavily, You.com and others), SERP resellers, extract and crawl tools, model-native search tools, and gateways as their own class.
- **Fields:** endpoints and modes, price per unit with all multipliers, free tier, rate limits, result limits, index ownership, latency claims, compliance posture, data-retention policy, MCP and SDK surface, keyless access, machine payments, ownership and funding.
- **Every field carries** `value`, `source_url`, `retrieved_at`, and `verified_by` (`bot`, `maintainer`, or `vendor`).
- **Outputs generated from the records:** the HTML pages, markdown mirrors, `llms.txt`, a JSON API, per-provider pages, and pairwise "A vs B" pages.
- **Cost calculator:** enter a workload (queries per month, results per query, pages fetched) and get normalized monthly cost per provider. Static, computed at build time for common workloads and client-side for custom ones as optional enhancement.
- **Change feed:** every price or capability change becomes a dated entry, published as Atom and JSON. This is the one thing people will subscribe to.

### 6.2 Evidence — how they perform

**Meta-benchmark.** Ingest every public board into a common table: operator, whether the operator sells a tested product, task type, date, provider configuration, score, rank.

- Show each provider's rank across boards, split by task type.
- Show the **house effect**: how each vendor ranks on its own board against its rank elsewhere.
- Link every row to the original. Publish scores as cited facts, not copied datasets; check each board's terms before ingesting.

**Probes.** A scheduled job sends a small fixed query set to every provider from several regions and records latency percentiles, error rate, and result freshness.

- This is operational telemetry and is labelled that way. It makes no relevance claims.
- Estimated cost: 25 configurations × 10 queries × 4 runs a day is about 30,000 queries a month, roughly $150 a month at a typical $5 per 1,000. Hourly runs would be about $900. Both are estimates from list prices.
- Output: a public status and latency history per provider. Vendors publish their own status pages; nobody publishes a neutral cross-provider one.

### 6.3 Decide — an answer an agent can use

- **Advisor endpoint and MCP tool:** `recommend({workload, constraints})` returns ranked candidates with the evidence rows and dates behind each. The logic is deterministic rules over the registry and evidence tables, so every recommendation can be audited. No language model sits in the path.
- **Other MCP tools:** `get_provider`, `compare`, `estimate_cost`, `list_changes`.
- The editorial verdicts in the current page become the output of these rules plus a short written rationale.

### 6.4 Run — test it on your own queries

- **Open specification:** one request and response schema for search, fetch, and research, published as OpenAPI with a conformance test suite. Offered to gateway and SDK authors to adopt.
- **Open SDK and CLI** (TypeScript and Python): adapters for each provider, bring your own keys, runs entirely on the user's machine. No hosted proxy, no markup, no traffic through websearch.dev.
- **Eval runner:** `websearch eval --queries mine.jsonl --providers a,b,c` runs the user's queries against chosen providers and writes a report on relevance (judge model of the user's choice), latency, and cost.
- **Opt-in result sharing:** users may submit aggregate results. This becomes the only evidence source built on real workloads.

---

## 7. Technical design

### Principles carried over

Static-first, zero JavaScript required to read, no trackers, small pages. The "no build step" rule is dropped: one generator replaces three hand-synced copies.

### Repository layout

```
websearchdev/
├── data/
│   ├── providers/*.yaml        # one record per provider
│   ├── benchmarks/*.yaml       # one record per public board, with rows
│   ├── probes/                 # daily rollups committed by the probe job
│   └── schema/*.json           # JSON Schemas
├── spec/                       # OpenAPI for the common schema, conformance tests
├── site/                       # templates and styles.css
├── build/                      # generator: data → HTML, md, llms.txt, JSON
├── workers/
│   ├── api/                    # advisor endpoint and MCP server
│   ├── probe/                  # scheduled latency and uptime probes
│   └── watch/                  # source change detection
├── packages/
│   ├── sdk-ts/  sdk-py/        # adapters and CLI
│   └── eval/                   # eval runner
└── dist/                       # generated output (not committed)
```

### Pipelines

| Pipeline | Trigger | Behaviour |
|---|---|---|
| Build | Push to `main` | Validate data against schemas, generate all outputs, fail on broken source links or missing dates |
| Watch | Daily | Fetch each record's source URLs, diff against the last snapshot, extract proposed field changes with a model, open a pull request for human review. Never merges on its own. |
| Probe | Every 6 hours | Run the canary set, write raw results to object storage, commit daily rollups |
| Benchmark ingest | Weekly and on demand | Check tracked boards for updates, open a pull request with new rows |
| Staleness | Daily | Any field older than 30 days is flagged on the page and in the API |

### Hosting

Stay on Cloudflare: Pages for the static site, Workers for the API and MCP server, Cron Triggers for jobs, R2 for raw probe results, D1 for probe history queries. Provider API keys for probes live in Worker secrets.

### Public interfaces

| Path | Content |
|---|---|
| `/` | Overview, generated from data |
| `/providers/{id}` and `.md` | One provider |
| `/compare/{a}-vs-{b}` and `.md` | Pairwise comparison |
| `/benchmarks` | Meta-benchmark and house effects |
| `/status` | Probe history |
| `/changes`, `/changes.atom` | Change feed |
| `/api/v1/providers.json`, `/api/v1/providers/{id}.json` | Registry |
| `/api/v1/evidence.json`, `/api/v1/changes.json` | Evidence and changes |
| `/api/v1/recommend` | Advisor |
| `/mcp` | MCP server, keyless and read-only |
| `/llms.txt`, `/llms-full.txt` | Generated |

The JSON API is versioned and static where possible, so it costs almost nothing to serve and can be mirrored.

---

## 8. Phases

Durations are estimates for one maintainer working with coding agents.

| Phase | Scope | Exit criteria |
|---|---|---|
| **0. Credibility** (1–2 weeks) | Governance items 1–4 and 7. Add Perplexity and Brave as full entries. Cite third-party benchmarks beside each verdict and revise verdicts the evidence contradicts. Deploy. | Site live; no self-description as independent; every verdict cites at least one outside source |
| **1. Registry** (about 6 weeks) | Data records, schemas, generator, JSON API, 25 providers, watch job, change feed, cost calculator | All pages generated from data; one price change caught by the bot and merged within 48 hours |
| **2. Evidence** (about 3 months) | Meta-benchmark, house-effect view, probes, status page | Nine boards ingested; 30 days of probe history public |
| **3. Decide and Run** (about 6 months) | Advisor, MCP server, specification, SDKs, eval runner | An agent can go from question to recommendation to a local eval using only websearch.dev tools |
| **4. Standard** (12 months and beyond) | Conformance programme, opt-in workload results, gateway adoption of the spec, annual category report | At least two third-party tools consume the registry or implement the spec |

Phase 0 is not optional and should not be reordered. The rest can flex.

---

## 9. Success measures

Targets are proposals; there is no baseline yet because the site has not launched.

| Measure | Why it matters | 12-month target |
|---|---|---|
| Median age of registry fields | Currency is the product | Under 14 days |
| Time from vendor price change to registry update | Tests the watch pipeline | Under 72 hours |
| Third-party tools consuming the registry or spec | Proves system-of-record status | 5 |
| Corrections submitted by vendors | Vendors only correct sources that matter | All of the largest ten have submitted at least one |
| Citations by AI assistants on category queries | The original goal in `PRD.md` | Tracked monthly on a fixed query list; target set after first measurement |
| SDK weekly downloads | Reach of the Run surface | Target set after launch |

---

## 10. Sustainability

Running costs are small: hosting is near zero and probes are about $150 a month at the proposed cadence.

Acceptable funding, in order of preference:

1. Self-funded or employer-sponsored with the governance charter in §5 published.
2. Grants or sponsorship pooled across several vendors, listed publicly, with no influence on data.
3. Paid services that do not touch the rankings: hosted eval runs, private registries for enterprises, data-feed service levels.

Not acceptable: paid placement, affiliate links, or sponsorship from a single vendor without the charter.

---

## 11. Risks

| Risk | Mitigation |
|---|---|
| Conflict of interest sinks credibility | §5 in full; mechanical verdicts; outside maintainer for recusals |
| Employer objects to a site that reports unflattering data about its product | Resolve ownership before Phase 0 (§12) |
| Vendor terms prohibit publishing probe or benchmark results | Review each provider's terms before probing; fall back to citing third-party data for any that prohibit it |
| Benchmark operators object to ingestion | Cite scores as facts with links; honour removal requests; never copy datasets |
| Watch bot proposes wrong extractions | Human review on every pull request; schema validation; source snapshot attached |
| A funded competitor builds the same registry | Open licence and early adoption by tools are the defence; being first with governance matters more than features |
| Maintainer bandwidth | Automate verification before adding providers; phases 3 and 4 depend on contributors |

---

## 12. Decisions needed from the owner

1. **Who owns this?** A personal project or a You.com-sponsored open project. This needs a check of the employment agreement and conflict-of-interest policy. It changes the disclosure wording, the funding options, and who can serve as outside maintainer.
2. **Named disclosure.** This document recommends reversing `PRD.md` §8 item 2. Everything else assumes that reversal.
3. **Probe budget.** About $150 a month at six-hour cadence, or about $900 hourly.
4. **Outside maintainer.** Who, if anyone, reviews You.com verdicts.
5. **Package names.** Availability of `websearch` on npm and PyPI has not been checked.

---

## 13. Non-goals

- A hosted search gateway or any proxying of user queries.
- A new headline relevance benchmark.
- Operating a search index.
- Accounts, comments, or a newsletter. The change feed covers subscription.
- Covering general SEO or consumer search engines.
