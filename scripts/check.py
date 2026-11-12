#!/usr/bin/env python3
"""Consistency check for websearch.dev.

The site is hand-written and ships the same comparison four times: index.html,
index.md, llms-full.txt and the summary in llms.txt. This script fails when
those copies stop agreeing, or when the page breaks one of its own promises
(no JavaScript, small page weight, dated and sourced claims).

Standard library only. Run from anywhere:

    python3 scripts/check.py            # check the repo this script lives in
    python3 scripts/check.py --root .   # check another checkout
    python3 scripts/check.py --only facts,dates

Exit status is 0 when every check passes and 1 otherwise.
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

SITE = "https://websearch.dev"

# Page weight budgets, in bytes. PRD.md records the page as shipped at about
# 66 KB of HTML and CSS, about 15 KB over the wire with brotli. gzip is what the
# standard library offers; it lands above brotli (about 21 KB for the page as
# shipped), so the wire budget is set against the gzip figure.
RAW_BUDGET = 80_000
GZIP_BUDGET = 24_000

MONTHS = {
    name: number
    for number, name in enumerate(
        [
            "january", "february", "march", "april", "may", "june", "july",
            "august", "september", "october", "november", "december",
        ],
        start=1,
    )
}

ISO_DATE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
LONG_DATE = re.compile(
    r"\b(" + "|".join(MONTHS) + r")\s+(\d{1,2}),\s+(\d{4})\b", re.IGNORECASE
)
# A number with its optional currency sign and unit suffix: $1,200  0.008  100k
# 450ms  2.67s  $95M  25%
NUMBER = re.compile(
    r"(?<![\w.])(\$?)(\d[\d,]*(?:\.\d+)?)(ms|[kKMB%s])?(?![\w])"
)
# "$12–1,200" and "$0.005-0.008": the second figure is money too.
MONEY_RANGE = re.compile(r"(\$\d[\d,]*(?:\.\d+)?[kKMB]?\s*[–-]\s*)(?=\d)")
MD_CITATION = re.compile(r"\[(\d{1,3})\]")
MD_SECTION = re.compile(r"^## (\d\d) · (.*)$", re.MULTILINE)
SECTION_REF = re.compile(r"\bsections?\s+\d+(?:\s*(?:and|,|–|-)\s*\d+)*", re.IGNORECASE)
URL = re.compile(r"https?://[^\s<>()\"'`]+")


# --------------------------------------------------------------------------
# Parsing
# --------------------------------------------------------------------------


class Page(HTMLParser):
    """Collects what the checks need from index.html in one pass."""

    VOID = {
        "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "source", "track", "wbr",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: dict[str, int] = {}
        self.duplicate_ids: list[tuple[str, int]] = []
        self.hrefs: list[tuple[str, int]] = []
        self.resources: list[tuple[str, str, int]] = []  # (tag, url, line)
        self.scripts: list[tuple[str, int]] = []  # (type, line)
        self.handlers: list[tuple[str, str, int]] = []  # (tag, attr, line)
        self.jsonld: list[str] = []
        self.sections: list[dict] = []
        self.faq_questions: list[str] = []
        self.all_text: list[str] = []
        self._section: dict | None = None
        self._stack: list[tuple[str, dict]] = []
        self._script_type: str | None = None
        self._script_buf: list[str] = []

    # -- helpers ----------------------------------------------------------
    def _inside(self, predicate) -> bool:
        return any(predicate(tag, attrs) for tag, attrs in self._stack)

    def _line(self) -> int:
        return self.getpos()[0]

    # -- parser callbacks -------------------------------------------------
    def handle_starttag(self, tag, attrs):
        attrs = {k: (v or "") for k, v in attrs}
        line = self._line()

        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.duplicate_ids.append((attrs["id"], line))
            self.ids[attrs["id"]] = line
        for name in attrs:
            if name.startswith("on"):
                self.handlers.append((tag, name, line))

        if tag == "a" and "href" in attrs:
            self.hrefs.append((attrs["href"], line))
        if tag == "link" and "href" in attrs:
            self.resources.append((tag, attrs["href"], line))
        if tag in ("img", "script", "iframe", "source", "video", "audio", "embed") and attrs.get("src"):
            self.resources.append((tag, attrs["src"], line))

        if tag == "script":
            self._script_type = attrs.get("type", "")
            self._script_buf = []
            self.scripts.append((self._script_type, line))

        if tag == "section" and attrs.get("id"):
            self._section = {
                "id": attrs["id"],
                "line": line,
                "title": [],
                "label": [],
                "text": [],
                "citations": set(),
            }
            self.sections.append(self._section)

        if tag == "a" and attrs.get("href", "").startswith("#src-") and self._section:
            self._section["citations"].add(attrs["href"][len("#src-"):])

        if tag == "summary" and self._section and self._section["id"] == "faq":
            self.faq_questions.append("")

        if tag not in self.VOID:
            self._stack.append((tag, attrs))

    def handle_endtag(self, tag):
        if tag == "script":
            if self._script_type == "application/ld+json":
                self.jsonld.append("".join(self._script_buf))
            self._script_type = None
        if tag == "section":
            self._section = None
        for index in range(len(self._stack) - 1, -1, -1):
            if self._stack[index][0] == tag:
                del self._stack[index:]
                break

    def handle_data(self, data):
        if self._script_type is not None:
            self._script_buf.append(data)
            return
        if self._inside(lambda t, a: t == "style"):
            return
        # Footnote markers are compared as citations, not as numbers.
        if self._inside(lambda t, a: t == "a" and a.get("href", "").startswith("#src-")):
            return
        self.all_text.append(data)

        section = self._section
        if section is None:
            return
        in_h2 = self._inside(lambda t, a: t == "h2")
        in_label = self._inside(lambda t, a: t == "span" and a.get("class") == "no")
        if in_h2 and in_label:
            section["label"].append(data)
            return
        if in_h2:
            section["title"].append(data)
            return
        if self._inside(lambda t, a: t == "summary") and section["id"] == "faq" and self.faq_questions:
            self.faq_questions[-1] += data
        section["text"].append(data)


def squash(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def to_iso(year, month, day) -> str:
    return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"


def dates_in(text: str) -> set[str]:
    found = {to_iso(*m.groups()) for m in ISO_DATE.finditer(text)}
    for m in LONG_DATE.finditer(text):
        found.add(to_iso(m.group(3), MONTHS[m.group(1).lower()], m.group(2)))
    return found


def facts_in(text: str) -> set[str]:
    """The checkable facts in a run of prose: dates and significant numbers.

    Bare single digits are skipped. They are almost always list numbering or
    counts written loosely ("the five vendors", "rows 1 to 5"), and the two
    mirrors are free to word those differently.
    """
    facts = {"date " + d for d in dates_in(text)}
    text = ISO_DATE.sub(" ", LONG_DATE.sub(" ", text))
    text = SECTION_REF.sub(" ", text)
    text = MONEY_RANGE.sub(r"\1$", text)
    for sign, digits, unit in NUMBER.findall(text):
        digits = digits.replace(",", "")
        if not sign and not unit and re.fullmatch(r"\d", digits):
            continue
        facts.add(sign + digits + (unit or ""))
    return facts


def md_sections(md: str) -> list[dict]:
    sections = []
    matches = list(MD_SECTION.finditer(md))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(md)
        body = md[match.end():end]
        sections.append(
            {
                "number": match.group(1),
                "title": match.group(2).strip(),
                "line": md.count("\n", 0, match.start()) + 1,
                "body": body,
                "citations": set(MD_CITATION.findall(body)),
            }
        )
    return sections


def md_prose(body: str) -> str:
    body = MD_CITATION.sub(" ", body)
    return re.sub(r"^\s*\d+\.\s", "", body, flags=re.MULTILINE)


def bare_title(title: str) -> str:
    """'Vendor № 1 — You.com — the stack' and 'You.com — the stack' compare equal."""
    title = re.sub(r"^Vendor\s+№\s*\d+\s+—\s+", "", squash(title))
    return title.replace("&amp;", "&").casefold()


# --------------------------------------------------------------------------
# Checks. Each returns a list of problem strings; an empty list is a pass.
# --------------------------------------------------------------------------


class Site:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.html = self.read("index.html")
        self.md = self.read("index.md")
        self.full = self.read("llms-full.txt")
        self.llms = self.read("llms.txt")
        research = root / "RESEARCH.md"
        self.research = research.read_text(encoding="utf-8") if research.is_file() else ""
        self.page = Page()
        self.page.feed(self.html)
        self.page.close()
        self.md_sections = md_sections(self.md)

    def read(self, name: str) -> str:
        path = self.root / name
        if not path.is_file():
            raise FileNotFoundError(f"{name} is missing from {self.root}")
        return path.read_text(encoding="utf-8")

    def graph(self) -> list[dict]:
        nodes: list[dict] = []
        for block in self.page.jsonld:
            data = json.loads(block)
            if isinstance(data, dict) and "@graph" in data:
                nodes.extend(data["@graph"])
            elif isinstance(data, list):
                nodes.extend(data)
            else:
                nodes.append(data)
        return nodes

    def node(self, kind: str) -> dict | None:
        return next((n for n in self.graph() if n.get("@type") == kind), None)


def check_mirror(site: Site) -> list[str]:
    """index.md and llms-full.txt are byte-identical."""
    if site.md == site.full:
        return []
    a, b = site.md.splitlines(), site.full.splitlines()
    for number, (left, right) in enumerate(zip(a, b), start=1):
        if left != right:
            return [f"index.md and llms-full.txt differ, first at line {number}"]
    return [f"index.md has {len(a)} lines, llms-full.txt has {len(b)}"]


def check_sections(site: Site) -> list[str]:
    """index.html and index.md have the same sections, in the same order."""
    problems = []
    html, md = site.page.sections, site.md_sections
    if len(html) != len(md):
        problems.append(f"index.html has {len(html)} sections, index.md has {len(md)}")
    for index, (h, m) in enumerate(zip(html, md), start=1):
        if m["number"] != f"{index:02d}":
            problems.append(f"index.md:{m['line']}: section is numbered {m['number']}, expected {index:02d}")
        label = squash("".join(h["label"]))
        if not label.startswith(f"{index:02d}"):
            problems.append(f"index.html:{h['line']}: #{h['id']} is labelled '{label}', expected {index:02d}")
        if bare_title("".join(h["title"])) != bare_title(m["title"]):
            problems.append(
                f"section {index:02d} title differs: index.html:{h['line']} "
                f"'{squash(''.join(h['title']))}' vs index.md:{m['line']} '{m['title']}'"
            )
    return problems


def check_facts(site: Site) -> list[str]:
    """Each section states the same numbers, dates and citations in both copies."""
    problems = []
    for h, m in zip(site.page.sections, site.md_sections):
        where = f"section {m['number']} (#{h['id']}, index.html:{h['line']}, index.md:{m['line']})"
        # From the heading label ("03 · Vendor № 1 — Last verified 2026-11-11")
        # only the date is a fact; the rest is numbering.
        html_facts = facts_in(" ".join(h["text"]))
        html_facts |= {"date " + d for d in dates_in(" ".join(h["label"]))}
        md_facts = facts_in(md_prose(m["body"]))
        only_html = sorted(html_facts - md_facts)
        only_md = sorted(md_facts - html_facts)
        if only_html:
            problems.append(f"{where}: in index.html but not index.md: {', '.join(only_html)}")
        if only_md:
            problems.append(f"{where}: in index.md but not index.html: {', '.join(only_md)}")
        if h["id"] == "sources":
            continue  # the source list is compared by URL in the sources check
        cite_html = sorted(h["citations"] - m["citations"], key=int)
        cite_md = sorted(m["citations"] - h["citations"], key=int)
        if cite_html:
            problems.append(f"{where}: cited in index.html but not index.md: [{'], ['.join(cite_html)}]")
        if cite_md:
            problems.append(f"{where}: cited in index.md but not index.html: [{'], ['.join(cite_md)}]")
    return problems


def check_llms(site: Site) -> list[str]:
    """Every number and date in llms.txt is backed by the page or RESEARCH.md, and its links resolve."""
    problems = []
    # llms.txt is a summary, so it may quote a figure from the fact base that
    # the page leaves out. A figure found in neither is stale or a typo.
    backing = facts_in(" ".join(site.page.all_text)) | facts_in(URL.sub(" ", site.research))
    for number, line in enumerate(site.llms.splitlines(), start=1):
        missing = sorted(facts_in(URL.sub(" ", line)) - backing)
        if missing:
            problems.append(
                f"llms.txt:{number}: not found in index.html or RESEARCH.md: {', '.join(missing)}"
            )
        for url in URL.findall(line):
            url = url.rstrip(".,;:")
            if url.startswith(SITE):
                problem = resolve_local(site, url[len(SITE):] or "/")
                if problem:
                    problems.append(f"llms.txt:{number}: {url} {problem}")
    return problems


def check_structured(site: Site) -> list[str]:
    """JSON-LD parses and matches the visible page (FAQ, vendor list, dates)."""
    problems = []
    try:
        nodes = site.graph()
    except json.JSONDecodeError as error:
        return [f"index.html: JSON-LD does not parse: {error}"]
    kinds = {n.get("@type") for n in nodes}
    for kind in ("Article", "ItemList", "FAQPage"):
        if kind not in kinds:
            problems.append(f"index.html: JSON-LD has no {kind} node")

    faq = site.node("FAQPage") or {}
    questions = faq.get("mainEntity", [])
    visible = [squash(q) for q in site.page.faq_questions]
    if questions and len(questions) != len(visible):
        problems.append(
            f"JSON-LD FAQPage has {len(questions)} questions, the visible FAQ has {len(visible)}"
        )
    page_facts = facts_in(" ".join(site.page.all_text))
    for question in questions:
        answer = question.get("acceptedAnswer", {}).get("text", "")
        missing = sorted(facts_in(answer) - page_facts)
        if missing:
            problems.append(
                f"JSON-LD FAQ answer to '{question.get('name')}' states facts the page does not: "
                + ", ".join(missing)
            )

    items = (site.node("ItemList") or {}).get("itemListElement", [])
    vendors = [s["id"] for s in site.page.sections if s["id"] not in STRUCTURAL_SECTIONS]
    listed = []
    for item in items:
        url = item.get("url", "")
        anchor = url.split("#", 1)[1] if "#" in url else ""
        listed.append(anchor)
        if anchor not in site.page.ids:
            problems.append(f"JSON-LD ItemList links to {url}, but index.html has no id '{anchor}'")
    if items and listed != vendors:
        problems.append(
            f"JSON-LD ItemList order {listed} does not match the vendor sections {vendors}"
        )
    return problems


STRUCTURAL_SECTIONS = {
    "tldr", "methodology", "use-cases", "agent-scorecard", "honorable-mentions",
    "faq", "sources", "changelog",
}


def check_dates(site: Site) -> list[str]:
    """dateModified, sitemap lastmod and the newest changelog row agree; nothing is dated later."""
    problems = []
    try:
        article = site.node("Article") or {}
    except json.JSONDecodeError:
        return ["index.html: JSON-LD does not parse, so dates cannot be checked"]
    modified = article.get("dateModified")
    published = article.get("datePublished")
    if not modified:
        return ["index.html: JSON-LD Article has no dateModified"]
    if published and published > modified:
        problems.append(f"datePublished {published} is after dateModified {modified}")

    sitemap = site.root / "sitemap.xml"
    if sitemap.is_file():
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        for entry in ET.parse(sitemap).getroot().findall("s:url", ns):
            loc = (entry.findtext("s:loc", "", ns) or "").strip()
            lastmod = (entry.findtext("s:lastmod", "", ns) or "").strip()
            if loc.rstrip("/") == SITE and lastmod != modified:
                problems.append(f"sitemap.xml lastmod is {lastmod}, JSON-LD dateModified is {modified}")
    else:
        problems.append("sitemap.xml is missing")

    for label, sections, text_of in (
        ("index.html", site.page.sections, lambda s: " ".join(s["text"])),
        ("index.md", site.md_sections, lambda s: s["body"]),
    ):
        changelog = sections[-1] if sections else None
        rows = sorted(dates_in(text_of(changelog))) if changelog else []
        if not rows:
            problems.append(f"{label}: the changelog has no dated row")
        elif rows[-1] != modified:
            problems.append(
                f"{label}: newest changelog row is {rows[-1]}, JSON-LD dateModified is {modified}"
            )

    for label, text in (
        ("index.html", " ".join(site.page.all_text) + " " + " ".join(
            " ".join(s["label"]) for s in site.page.sections)),
        ("index.md", site.md),
        ("llms.txt", site.llms),
    ):
        later = sorted(d for d in dates_in(text) if d > modified)
        if later:
            problems.append(
                f"{label} mentions {', '.join(later)}, after dateModified {modified}. "
                "Bump dateModified, sitemap lastmod and the changelog."
            )

    for section in site.page.sections:
        if section["id"] in STRUCTURAL_SECTIONS:
            continue
        if not dates_in(" ".join(section["label"])):
            problems.append(
                f"index.html:{section['line']}: vendor section #{section['id']} has no 'Last verified' date"
            )
    return problems


def resolve_local(site: Site, target: str) -> str | None:
    """Why a site-relative link is broken, or None when it resolves."""
    path, _, fragment = target.partition("#")
    path = path.split("?", 1)[0]
    if path in ("", "/"):
        if fragment and fragment not in site.page.ids:
            return f"points at #{fragment}, which is not an id in index.html"
        return None
    if not (site.root / path.lstrip("/")).is_file():
        return f"points at {path}, which is not a file in the repo"
    return None


def check_links(site: Site) -> list[str]:
    """Anchors, local files, citations and sitemap entries all resolve."""
    problems = []
    for name, line in site.page.duplicate_ids:
        problems.append(f"index.html:{line}: id '{name}' is used more than once")
    targets = [(href, line) for href, line in site.page.hrefs]
    targets += [(url, line) for _, url, line in site.page.resources]
    for href, line in targets:
        if href.startswith(("mailto:", "tel:")):
            continue
        if href.startswith(SITE):
            href = href[len(SITE):] or "/"
        if href.startswith(("http://", "https://", "//")):
            continue
        problem = resolve_local(site, href)
        if problem:
            problems.append(f"index.html:{line}: link {problem}")

    sources = {name[len("src-"):] for name in site.page.ids if name.startswith("src-")}
    cited = set().union(*(s["citations"] for s in site.page.sections)) if site.page.sections else set()
    for number in sorted(sources - cited, key=int):
        problems.append(f"index.html: source {number} is listed but never cited")

    sitemap = site.root / "sitemap.xml"
    if sitemap.is_file():
        for loc in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sitemap.read_text(encoding="utf-8")):
            if not loc.startswith(SITE):
                problems.append(f"sitemap.xml: {loc} is not on {SITE}")
                continue
            problem = resolve_local(site, loc[len(SITE):] or "/")
            if problem:
                problems.append(f"sitemap.xml: {loc} {problem}")
    return problems


def check_sources(site: Site) -> list[str]:
    """The numbered source list is the same, in the same order, in both copies."""
    html_urls = []
    in_sources = False
    for line in site.html.splitlines():
        if '<section id="sources"' in line:
            in_sources = True
        elif in_sources and "</section>" in line:
            break
        elif in_sources:
            match = re.search(r'<li id="src-(\d+)"><a href="([^"]+)"', line)
            if match:
                html_urls.append((match.group(1), match.group(2)))
    md_urls = []
    for section in site.md_sections:
        if bare_title(section["title"]) == "sources":
            for match in re.finditer(r"^(\d+)\.\s.*?(https?://\S+)\s*$", section["body"], re.MULTILINE):
                md_urls.append((match.group(1), match.group(2)))
    problems = []
    if not html_urls:
        problems.append("index.html: no numbered sources found in #sources")
    for index in range(max(len(html_urls), len(md_urls))):
        left = html_urls[index] if index < len(html_urls) else None
        right = md_urls[index] if index < len(md_urls) else None
        if left != right:
            problems.append(
                f"source {index + 1}: index.html has {left[1] if left else 'nothing'}, "
                f"index.md has {right[1] if right else 'nothing'}"
            )
    for position, (number, _) in enumerate(html_urls, start=1):
        if int(number) != position:
            problems.append(f"index.html: source id src-{number} is in position {position}")
    return problems


def check_nojs(site: Site) -> list[str]:
    """No scripts, no inline handlers, no third-party requests."""
    problems = []
    for kind, line in site.page.scripts:
        if kind != "application/ld+json":
            problems.append(f"index.html:{line}: <script> found (only JSON-LD is allowed)")
    for tag, attr, line in site.page.handlers:
        problems.append(f"index.html:{line}: inline handler {attr} on <{tag}>")
    for href, line in site.page.hrefs:
        if href.strip().lower().startswith("javascript:"):
            problems.append(f"index.html:{line}: javascript: link")
    for tag, url, line in site.page.resources:
        external = url.startswith(("http://", "https://", "//")) and not url.startswith(SITE)
        if external:
            problems.append(f"index.html:{line}: <{tag}> loads {url} from another host")
    css = site.root / "styles.css"
    if css.is_file():
        for number, line in enumerate(css.read_text(encoding="utf-8").splitlines(), start=1):
            if re.search(r"@import|url\(\s*['\"]?(?:https?:)?//", line):
                problems.append(f"styles.css:{number}: loads a resource from another host")
    return problems


def check_budget(site: Site, raw_budget: int = RAW_BUDGET, gzip_budget: int = GZIP_BUDGET) -> list[str]:
    """index.html plus styles.css stay inside the page weight budget."""
    payload = site.html.encode("utf-8")
    css = site.root / "styles.css"
    if css.is_file():
        payload += css.read_bytes()
    raw = len(payload)
    packed = len(gzip.compress(payload, compresslevel=9, mtime=0))
    problems = []
    if raw > raw_budget:
        problems.append(f"index.html + styles.css is {raw:,} bytes, budget is {raw_budget:,}")
    if packed > gzip_budget:
        problems.append(f"index.html + styles.css is {packed:,} bytes gzipped, budget is {gzip_budget:,}")
    check_budget.detail = f"{raw:,} bytes raw, {packed:,} gzipped"
    return problems


CHECKS = {
    "mirror": check_mirror,
    "sections": check_sections,
    "facts": check_facts,
    "llms": check_llms,
    "structured": check_structured,
    "dates": check_dates,
    "links": check_links,
    "sources": check_sources,
    "nojs": check_nojs,
    "budget": check_budget,
}


def run(root: Path, only: list[str] | None = None, raw_budget: int = RAW_BUDGET,
        gzip_budget: int = GZIP_BUDGET) -> dict[str, list[str]]:
    site = Site(root)
    results = {}
    for name, check in CHECKS.items():
        if only and name not in only:
            continue
        if name == "budget":
            results[name] = check(site, raw_budget, gzip_budget)
        else:
            results[name] = check(site)
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="repo root to check (default: the repo this script lives in)")
    parser.add_argument("--only", default="",
                        help="comma-separated checks to run: " + ", ".join(CHECKS))
    parser.add_argument("--raw-budget", type=int, default=RAW_BUDGET,
                        help=f"max bytes for index.html + styles.css (default {RAW_BUDGET})")
    parser.add_argument("--gzip-budget", type=int, default=GZIP_BUDGET,
                        help=f"max gzipped bytes for index.html + styles.css (default {GZIP_BUDGET})")
    parser.add_argument("--json", action="store_true", help="print results as JSON")
    args = parser.parse_args(argv)

    only = [name.strip() for name in args.only.split(",") if name.strip()]
    unknown = [name for name in only if name not in CHECKS]
    if unknown:
        parser.error(f"unknown check: {', '.join(unknown)}")

    try:
        results = run(args.root, only or None, args.raw_budget, args.gzip_budget)
    except FileNotFoundError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    failed = sum(1 for problems in results.values() if problems)
    if args.json:
        print(json.dumps({"ok": not failed, "checks": results}, indent=2, ensure_ascii=False))
        return 1 if failed else 0

    for name, problems in results.items():
        summary = (CHECKS[name].__doc__ or "").strip().rstrip(".")
        if problems:
            print(f"FAIL  {name}: {summary}")
            for problem in problems:
                print(f"        {problem}")
        else:
            detail = getattr(CHECKS[name], "detail", "") if name == "budget" else ""
            print(f"ok    {name}: {summary}" + (f" ({detail})" if detail else ""))
    print()
    if failed:
        print(f"{failed} of {len(results)} checks failed.")
        return 1
    print(f"All {len(results)} checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
