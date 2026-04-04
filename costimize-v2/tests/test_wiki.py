"""Tests for the wiki knowledge base system (Karpathy-style LLM KB)."""

import pytest
from pathlib import Path

# Ensure wiki_loader can find the wiki directory
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.wiki_loader import (
    load_wiki,
    reload_wiki,
    route_topics,
    get_wiki_context,
    _parse_frontmatter,
    _estimate_tokens,
    MAX_ARTICLES_PER_QUERY,
    MAX_WIKI_TOKENS,
    WIKI_DIR,
)

REQUIRED_FIELDS = {"slug", "title", "keywords", "sources"}


@pytest.fixture(autouse=True)
def fresh_wiki():
    """Reload wiki before each test to ensure clean state."""
    reload_wiki()
    yield


class TestFrontmatterParsing:
    def test_parse_valid_frontmatter(self):
        text = """---
slug: test-article
title: Test Article
keywords: foo, bar, baz
sources: A.md, B.md
---

# Content here"""
        meta, body = _parse_frontmatter(text)
        assert meta["slug"] == "test-article"
        assert meta["title"] == "Test Article"
        assert meta["keywords"] == ["foo", "bar", "baz"]
        assert meta["sources"] == ["A.md", "B.md"]
        assert body.startswith("# Content")

    def test_parse_no_frontmatter(self):
        text = "# Just content\nNo frontmatter here."
        meta, body = _parse_frontmatter(text)
        assert meta == {}
        assert body == text

    def test_estimate_tokens(self):
        text = "a" * 400
        assert _estimate_tokens(text) == 100


class TestWikiLoading:
    def test_articles_load_without_errors(self):
        articles = load_wiki()
        assert len(articles) >= 15, f"Expected 15+ articles, got {len(articles)}"

    def test_all_articles_have_required_fields(self):
        articles = load_wiki()
        for slug, article in articles.items():
            assert article.slug, f"{slug}: missing slug"
            assert article.title, f"{slug}: missing title"
            assert len(article.keywords) >= 1, f"{slug}: no keywords"
            assert article.content, f"{slug}: no content"
            assert article.token_estimate > 0, f"{slug}: zero tokens"

    def test_slug_matches_filename(self):
        """Every article's slug should match its filename."""
        articles = load_wiki()
        for path in WIKI_DIR.glob("*.md"):
            if path.name == "index.md":
                continue
            stem = path.stem
            if stem in articles:
                assert articles[stem].slug == stem, (
                    f"Slug mismatch: file={stem}, slug={articles[stem].slug}"
                )

    def test_idempotent_loading(self):
        """Loading twice returns the same articles."""
        a1 = load_wiki()
        a2 = load_wiki()
        assert len(a1) == len(a2)
        assert set(a1.keys()) == set(a2.keys())


class TestTopicRouting:
    def test_machining_query_routes_to_relevant_articles(self):
        slugs = route_topics("What cutting speed should I use for EN8 turning?")
        assert len(slugs) > 0
        # Should match materials or machining articles
        relevant = {"materials-and-machinability", "turning-milling-machining",
                     "physics-engine", "should-cost-estimation"}
        assert any(s in relevant for s in slugs), f"Got {slugs}, expected overlap with {relevant}"

    def test_surface_treatment_query(self):
        slugs = route_topics("How much does zinc plating cost per square decimetre?")
        assert "surface-treatments" in slugs

    def test_regional_cost_query(self):
        slugs = route_topics("What are manufacturing costs in Bangalore vs Pune?")
        assert len(slugs) > 0
        relevant = {"indian-regional-costs", "indian-manufacturing-landscape"}
        assert any(s in relevant for s in slugs)

    def test_no_match_returns_empty(self):
        slugs = route_topics("xyzzy foobar nonsense gibberish")
        assert slugs == []

    def test_max_articles_respected(self):
        # Use a very broad query that could match many articles
        slugs = route_topics("manufacturing cost estimation material process India")
        assert len(slugs) <= MAX_ARTICLES_PER_QUERY

    def test_competitor_query(self):
        slugs = route_topics("How does aPriori compare to CADDi?")
        assert "competitors" in slugs


class TestWikiContext:
    def test_context_format_has_delimiters(self):
        ctx = get_wiki_context("What is should-cost estimation?")
        if ctx:
            assert ctx.startswith("=== KNOWLEDGE BASE ===")
            assert ctx.endswith("=== END KNOWLEDGE BASE ===")

    def test_empty_for_no_match(self):
        ctx = get_wiki_context("xyzzy foobar nonsense")
        assert ctx == ""

    def test_token_budget_respected(self):
        # Broad query to trigger multiple articles
        ctx = get_wiki_context("manufacturing cost material process turning sheet metal surface")
        if ctx:
            token_est = len(ctx) // 4
            # Allow some slack over MAX_WIKI_TOKENS since we estimate roughly
            assert token_est < MAX_WIKI_TOKENS * 1.5, (
                f"Context too large: ~{token_est} tokens vs {MAX_WIKI_TOKENS} budget"
            )
