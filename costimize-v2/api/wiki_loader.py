"""Wiki knowledge base: load, index, and route articles for CAG injection.

Karpathy-style LLM Knowledge Base — compiled markdown articles loaded at
startup, topic-routed by keyword matching, injected into chat context.
No vector DB, no RAG, no new dependencies.
"""

import logging
import re
from pathlib import Path
from dataclasses import dataclass, field

logger = logging.getLogger("costimize")

WIKI_DIR = Path(__file__).parent.parent / "docs" / "wiki"
MAX_ARTICLES_PER_QUERY = 3
MAX_WIKI_TOKENS = 8000  # budget cap per chat turn


@dataclass
class WikiArticle:
    slug: str
    title: str
    keywords: list[str]
    sources: list[str]
    content: str
    token_estimate: int = 0


# Module-level cache
_articles: dict[str, WikiArticle] = {}
_loaded: bool = False


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML-ish frontmatter from --- delimited block.

    Returns (metadata_dict, body_text). No PyYAML dependency.
    """
    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    meta = {}
    for line in parts[1].strip().splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        # Parse comma-separated lists
        if "," in value:
            meta[key] = [v.strip() for v in value.split(",") if v.strip()]
        else:
            meta[key] = value

    body = parts[2].strip()
    return meta, body


def _estimate_tokens(text: str) -> int:
    """Rough token count: ~4 chars per token."""
    return len(text) // 4


def load_wiki() -> dict[str, WikiArticle]:
    """Load all .md files from wiki/ dir, parse frontmatter, cache."""
    global _articles, _loaded

    if _loaded:
        return _articles

    if not WIKI_DIR.exists():
        logger.warning("Wiki directory not found: %s", WIKI_DIR)
        _loaded = True
        return _articles

    for path in sorted(WIKI_DIR.glob("*.md")):
        if path.name == "index.md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
            meta, body = _parse_frontmatter(text)

            slug = meta.get("slug", path.stem)
            keywords = meta.get("keywords", [])
            if isinstance(keywords, str):
                keywords = [k.strip() for k in keywords.split(",")]
            sources = meta.get("sources", [])
            if isinstance(sources, str):
                sources = [s.strip() for s in sources.split(",")]

            article = WikiArticle(
                slug=slug,
                title=meta.get("title", path.stem.replace("-", " ").title()),
                keywords=keywords,
                sources=sources,
                content=body,
                token_estimate=_estimate_tokens(body),
            )
            _articles[slug] = article

        except Exception as e:
            logger.warning("Failed to load wiki article %s: %s", path.name, e)

    _loaded = True
    logger.info("Wiki loaded: %d articles, ~%d tokens total",
                len(_articles),
                sum(a.token_estimate for a in _articles.values()))
    return _articles


def route_topics(user_message: str) -> list[str]:
    """Given a user message, return up to MAX_ARTICLES_PER_QUERY article slugs.

    Scoring: exact word match = 2 points, substring match = 1 point.
    Returns slugs sorted by score descending, only those with score > 0.
    """
    articles = load_wiki()
    if not articles:
        return []

    msg_lower = user_message.lower()
    msg_words = set(re.findall(r"\w+", msg_lower))

    scores: list[tuple[str, int]] = []

    for slug, article in articles.items():
        score = 0
        for kw in article.keywords:
            kw_lower = kw.lower()
            kw_words = set(re.findall(r"\w+", kw_lower))

            # Exact word match (keyword is a single word found in message words)
            if kw_words and kw_words.issubset(msg_words):
                score += 2
            # Substring match (keyword appears anywhere in message)
            elif kw_lower in msg_lower:
                score += 1

        if score > 0:
            scores.append((slug, score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return [slug for slug, _ in scores[:MAX_ARTICLES_PER_QUERY]]


def get_wiki_context(user_message: str) -> str:
    """Main entry point for chat.py.

    Routes message -> selects articles -> formats as context block.
    Returns empty string if no relevant articles found.
    """
    slugs = route_topics(user_message)
    if not slugs:
        return ""

    articles = load_wiki()
    sections = []
    total_tokens = 0

    for slug in slugs:
        article = articles.get(slug)
        if not article:
            continue

        # Token budget check
        if total_tokens + article.token_estimate > MAX_WIKI_TOKENS:
            # Truncate content to fit budget
            remaining = MAX_WIKI_TOKENS - total_tokens
            if remaining < 200:
                break
            chars = remaining * 4
            content = article.content[:chars] + "\n...(truncated)"
        else:
            content = article.content

        total_tokens += article.token_estimate
        sections.append(f"## {article.title}\n\n{content}")

    if not sections:
        return ""

    return (
        "=== KNOWLEDGE BASE ===\n"
        + "\n\n".join(sections)
        + "\n=== END KNOWLEDGE BASE ==="
    )


def reload_wiki():
    """Force reload wiki articles (for development/testing)."""
    global _articles, _loaded
    _articles = {}
    _loaded = False
    return load_wiki()
