"""Tests for scripts/check.py.

Each test copies the real site into a temporary directory, makes the kind of
edit that happens when one copy is updated and another is forgotten, and
asserts that the right check catches it. Run with:

    python3 -m unittest discover -s tests -v
"""

import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check  # noqa: E402

SITE_FILES = [
    "index.html", "index.md", "llms-full.txt", "llms.txt", "styles.css",
    "sitemap.xml", "robots.txt", "humans.txt", "RESEARCH.md",
]


class SiteCase(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp(prefix="websearchdev-"))
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)
        for name in SITE_FILES:
            shutil.copy(ROOT / name, self.dir / name)
        shutil.copytree(ROOT / "assets", self.dir / "assets")

    def edit(self, name, old, new, count=1):
        path = self.dir / name
        text = path.read_text(encoding="utf-8")
        self.assertGreaterEqual(text.count(old), 1, f"{old!r} not found in {name}")
        path.write_text(text.replace(old, new, count), encoding="utf-8")

    def edit_mirrors(self, old, new, count=1):
        for name in ("index.md", "llms-full.txt"):
            self.edit(name, old, new, count)

    def results(self, **kwargs):
        return check.run(self.dir, **kwargs)

    def failing(self, **kwargs):
        return {name for name, problems in self.results(**kwargs).items() if problems}

    def problems(self, name):
        return "\n".join(self.results()[name])


class CleanSite(SiteCase):
    def test_the_committed_site_passes_every_check(self):
        self.assertEqual(self.failing(), set())

    def test_cli_exit_codes(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(check.main(["--root", str(self.dir)]), 0)
            self.edit("index.md", "$5 / 1k calls", "$6 / 1k calls")
            self.assertEqual(check.main(["--root", str(self.dir)]), 1)
        self.assertIn("All 10 checks passed.", out.getvalue())
        self.assertIn("FAIL  facts", out.getvalue())

    def test_json_output(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            check.main(["--root", str(self.dir), "--json", "--only", "mirror"])
        self.assertEqual(json.loads(out.getvalue()), {"ok": True, "checks": {"mirror": []}})

    def test_only_runs_the_named_checks(self):
        self.assertEqual(set(self.results(only=["facts", "dates"])), {"facts", "dates"})


class Mirrors(SiteCase):
    def test_markdown_edited_without_llms_full(self):
        self.edit("index.md", "the keyless upstart", "the keyless newcomer")
        self.assertIn("mirror", self.failing())

    def test_price_changed_in_html_only(self):
        self.edit("index.html", "<code>$5 / 1k calls</code>", "<code>$6 / 1k calls</code>")
        self.assertEqual(self.failing(), {"facts"})
        message = self.problems("facts")
        self.assertIn("#you-com", message)
        self.assertIn("in index.html but not index.md: $6", message)

    def test_price_changed_in_markdown_only(self):
        self.edit_mirrors("`$5 / 1k calls`", "`$7.50 / 1k calls`")
        self.assertEqual(self.failing(), {"facts"})
        self.assertIn("in index.md but not index.html: $7.50", self.problems("facts"))

    def test_thousands_separators_and_date_formats_do_not_matter(self):
        self.edit_mirrors("`$12–1,200 / 1k`", "`$12–1200 / 1k`")
        self.edit_mirrors("*Last verified 2026-11-11.*", "*Last verified November 11, 2026.*")
        self.assertEqual(self.failing(), set())

    def test_citation_dropped_from_markdown(self):
        self.edit_mirrors("up to 100 results per call [1]", "up to 100 results per call")
        self.assertNotIn("facts", self.failing())  # [1] is still cited elsewhere in the section
        self.edit_mirrors("is a strong runner-up with cheaper top-end runs ($1.00 x-high) [3]",
                          "is a strong runner-up with cheaper top-end runs ($1.00 x-high) [4]")
        self.assertIn("cited in index.md but not index.html: [4]", self.problems("facts"))

    def test_section_renamed_in_one_copy(self):
        self.edit_mirrors("## 08 · Winners by use case", "## 08 · Verdicts by workload")
        self.assertIn("sections", self.failing())

    def test_section_added_to_markdown_only(self):
        self.edit_mirrors("## 13 · Changelog & corrections",
                          "## 13 · Benchmarks\n\nNone yet.\n\n---\n\n## 14 · Changelog & corrections")
        self.assertIn("index.html has 13 sections, index.md has 14", self.problems("sections"))

    def test_source_url_changed_in_one_copy(self):
        self.edit("index.html", 'href="https://exa.ai/pricing">Exa — Pricing',
                  'href="https://exa.ai/pricing/api">Exa — Pricing')
        self.assertIn("sources", self.failing())


class LlmsTxt(SiteCase):
    def test_stale_price_in_llms_txt(self):
        self.edit("llms.txt", "monitors $2/1k", "monitors $15/1k")
        self.assertEqual(self.failing(), {"llms"})
        self.assertIn("not found in index.html or RESEARCH.md: $15", self.problems("llms"))

    def test_figure_from_the_fact_base_is_allowed(self):
        # $110 (You.com finance research) is in RESEARCH.md but not on the page.
        self.assertIn("$110", (self.dir / "llms.txt").read_text(encoding="utf-8"))
        self.assertNotIn("$110", (self.dir / "index.html").read_text(encoding="utf-8"))
        self.assertEqual(self.results(only=["llms"])["llms"], [])
        (self.dir / "RESEARCH.md").unlink()
        self.assertIn("$110", self.problems("llms"))

    def test_broken_local_link_in_llms_txt(self):
        self.edit("llms.txt", "https://websearch.dev/index.md", "https://websearch.dev/page.md")
        self.assertIn("page.md, which is not a file", self.problems("llms"))

    def test_broken_anchor_in_llms_txt(self):
        self.edit("llms.txt", "https://websearch.dev/#changelog", "https://websearch.dev/#updates")
        self.assertIn("#updates", self.problems("llms"))


class StructuredData(SiteCase):
    def test_faq_question_missing_from_json_ld(self):
        self.edit("index.html", "<summary>Is this page biased?</summary>",
                  "<summary>Is this page biased?</summary></details><details><summary>Is it free?</summary>")
        self.assertIn("visible FAQ has 8", self.problems("structured"))

    def test_json_ld_answer_with_a_number_the_page_does_not_state(self):
        self.edit("index.html", "Exa grants $10 in credits monthly", "Exa grants $25 in credits monthly")
        self.assertIn("$25", self.problems("structured"))

    def test_invalid_json_ld(self):
        self.edit("index.html", '"@context": "https://schema.org",', '"@context": "https://schema.org"')
        self.assertIn("does not parse", self.problems("structured"))

    def test_vendor_anchor_renamed(self):
        self.edit("index.html", '<section id="you-com"', '<section id="youcom"')
        failing = self.failing()
        self.assertIn("structured", failing)
        self.assertIn("links", failing)  # the table of contents still points at #you-com


class Dates(SiteCase):
    def test_date_modified_bumped_without_sitemap_or_changelog(self):
        self.edit("index.html", '"dateModified": "2026-11-11"', '"dateModified": "2026-12-01"')
        message = self.problems("dates")
        self.assertIn("sitemap.xml lastmod is 2026-11-11", message)
        self.assertIn("newest changelog row is 2026-11-11", message)

    def test_vendor_reverified_without_bumping_date_modified(self):
        self.edit("index.html", "Vendor № 2 — Last verified 2026-11-11", "Vendor № 2 — Last verified 2026-12-01")
        self.assertIn("after dateModified 2026-11-11", self.problems("dates"))

    def test_full_update_passes(self):
        self.edit("index.html", '"dateModified": "2026-11-11"', '"dateModified": "2026-12-01"')
        self.edit("sitemap.xml", "<lastmod>2026-11-11</lastmod>", "<lastmod>2026-12-01</lastmod>")
        self.edit("index.html", "Vendor № 2 — Last verified 2026-11-11", "Vendor № 2 — Last verified 2026-12-01")
        self.edit_mirrors("*Last verified 2026-11-11.*\n\nThe retrieval purist.",
                          "*Last verified 2026-12-01.*\n\nThe retrieval purist.")
        row = "Exa section verified again; no price changes."
        self.edit("index.html", "    <tbody>\n      <tr><td class=\"num\">2026-11-11</td>",
                  f"    <tbody>\n      <tr><td class=\"num\">2026-12-01</td><td>{row}</td></tr>\n"
                  "      <tr><td class=\"num\">2026-11-11</td>")
        self.edit_mirrors("| 2026-11-11 | Initial publication.",
                          f"| 2026-12-01 | {row} |\n| 2026-11-11 | Initial publication.")
        self.assertEqual(self.failing(), set())

    def test_vendor_section_without_a_verified_stamp(self):
        self.edit("index.html", "Vendor № 5 — Last verified 2026-11-11", "Vendor № 5")
        self.assertIn("#keenable has no 'Last verified' date", self.problems("dates"))


class Links(SiteCase):
    def test_broken_anchor(self):
        self.edit("index.html", 'href="#use-cases"', 'href="#usecases"')
        self.assertIn("#usecases", self.problems("links"))

    def test_missing_asset(self):
        (self.dir / "assets" / "favicon.svg").unlink()
        self.assertIn("/assets/favicon.svg", self.problems("links"))

    def test_duplicate_id(self):
        self.edit("index.html", '<section id="exa"', '<section id="tldr"')
        self.assertIn("id 'tldr' is used more than once", self.problems("links"))

    def test_sitemap_entry_without_a_file(self):
        self.edit("sitemap.xml", "</urlset>",
                  "<url><loc>https://websearch.dev/benchmarks.md</loc></url></urlset>")
        self.assertIn("benchmarks.md", self.problems("links"))


class PagePromises(SiteCase):
    def test_script_tag(self):
        self.edit("index.html", "</body>", "<script>console.log(1)</script></body>")
        self.assertEqual(self.failing(), {"nojs"})

    def test_external_script_and_inline_handler(self):
        self.edit("index.html", "</body>",
                  '<script src="https://cdn.example.com/a.js"></script><p onclick="x()">hi</p></body>')
        message = self.problems("nojs")
        self.assertIn("from another host", message)
        self.assertIn("inline handler onclick", message)

    def test_web_font_import_in_css(self):
        self.edit("styles.css", "", "@import url('https://fonts.googleapis.com/css2?family=Inter');\n")
        self.assertIn("nojs", self.failing())

    def test_json_ld_is_not_counted_as_javascript(self):
        self.assertEqual(self.results(only=["nojs"])["nojs"], [])

    def test_page_weight_budget(self):
        self.assertIn("budget", self.failing(raw_budget=10_000))
        self.assertIn("budget", self.failing(gzip_budget=5_000))
        self.assertNotIn("budget", self.failing())


class FactExtraction(unittest.TestCase):
    def test_numbers_units_and_dates(self):
        self.assertEqual(
            check.facts_in("Search is $1,200 / 1k, p50 2.67s, 450ms, 100k req/mo, ~$700M, on November 11, 2026."),
            {"$1200", "1k", "2.67s", "450ms", "100k", "$700M", "date 2026-11-11"},
        )

    def test_single_digits_and_section_references_are_ignored(self):
        self.assertEqual(check.facts_in("The five vendors, rows 1 to 5, see section 12."), set())

    def test_single_digit_prices_are_kept(self):
        self.assertEqual(check.facts_in("$5 per 1,000 calls"), {"$5", "1000"})

    def test_the_second_figure_in_a_money_range_is_money(self):
        self.assertEqual(check.facts_in("$12–1,200 /1k and $0.005-0.008/credit, 4–250 credits"),
                         {"$12", "$1200", "1k", "$0.005", "$0.008", "250"})


if __name__ == "__main__":
    unittest.main()
