"""Wiki maintenance tool: validate, lint, and report on wiki articles.

Usage (from costimize-v2/):
    python -m tools.wiki_compiler check          # Validate all articles
    python -m tools.wiki_compiler stats          # Token counts, keyword coverage
    python -m tools.wiki_compiler test "MSG"     # Test topic routing for a message
"""

import sys
from pathlib import Path

# Add parent to path so we can import api.wiki_loader
sys.path.insert(0, str(Path(__file__).parent.parent))

WIKI_DIR = Path(__file__).parent.parent / "docs" / "wiki"
RESEARCH_DIR = Path(__file__).parent.parent / "docs" / "research"
REQUIRED_FIELDS = {"slug", "title", "keywords", "sources"}


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Simple frontmatter parser (mirrors wiki_loader)."""
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
        if "," in value:
            meta[key] = [v.strip() for v in value.split(",") if v.strip()]
        else:
            meta[key] = value
    return meta, parts[2].strip()


def cmd_check():
    """Validate all wiki articles."""
    errors = []
    warnings = []
    count = 0

    for path in sorted(WIKI_DIR.glob("*.md")):
        if path.name == "index.md":
            continue
        count += 1
        text = path.read_text(encoding="utf-8")
        meta, body = _parse_frontmatter(text)

        # Check required fields
        missing = REQUIRED_FIELDS - set(meta.keys())
        if missing:
            errors.append(f"{path.name}: missing frontmatter fields: {missing}")

        # Check slug matches filename
        slug = meta.get("slug", "")
        if slug and slug != path.stem:
            errors.append(f"{path.name}: slug '{slug}' doesn't match filename '{path.stem}'")

        # Check word count
        words = len(body.split())
        if words < 300:
            warnings.append(f"{path.name}: only {words} words (target: 500-2000)")
        elif words > 2500:
            warnings.append(f"{path.name}: {words} words (target: 500-2000, may be too long)")

        # Check source references exist
        sources = meta.get("sources", [])
        if isinstance(sources, str):
            sources = [sources]
        for src in sources:
            src_path = RESEARCH_DIR / src
            if not src_path.exists():
                warnings.append(f"{path.name}: source '{src}' not found in research/")

        # Check keywords count
        keywords = meta.get("keywords", [])
        if isinstance(keywords, str):
            keywords = [keywords]
        if len(keywords) < 5:
            warnings.append(f"{path.name}: only {len(keywords)} keywords (target: 5-15)")

    # Print results
    print(f"\n  Wiki Check: {count} articles\n")

    if errors:
        print(f"  ERRORS ({len(errors)}):")
        for e in errors:
            print(f"    x {e}")
    else:
        print("  ERRORS: none")

    if warnings:
        print(f"\n  WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"    ! {w}")
    else:
        print("\n  WARNINGS: none")

    print()
    return len(errors) == 0


def cmd_stats():
    """Print table of all articles with stats."""
    print(f"\n  {'Slug':<35} {'Title':<40} {'Words':>6} {'Tokens':>7} {'Keywords':>8}")
    print("  " + "-" * 100)

    total_words = 0
    total_tokens = 0

    for path in sorted(WIKI_DIR.glob("*.md")):
        if path.name == "index.md":
            continue
        text = path.read_text(encoding="utf-8")
        meta, body = _parse_frontmatter(text)

        raw_slug = meta.get("slug", path.stem)
        slug = raw_slug if isinstance(raw_slug, str) else str(raw_slug)
        raw_title = meta.get("title", path.stem)
        if isinstance(raw_title, list):
            raw_title = ", ".join(raw_title)
        title = raw_title[:38]
        words = len(body.split())
        tokens = len(body) // 4
        keywords = meta.get("keywords", [])
        if isinstance(keywords, str):
            keywords = [keywords]
        kw_count = len(keywords)

        total_words += words
        total_tokens += tokens

        print(f"  {slug:<35} {title:<40} {words:>6} {tokens:>7} {kw_count:>8}")

    print("  " + "-" * 100)
    print(f"  {'TOTAL':<35} {'':<40} {total_words:>6} {total_tokens:>7}")
    print()


def cmd_test(message: str):
    """Test topic routing for a message."""
    from api.wiki_loader import route_topics, get_wiki_context, load_wiki

    articles = load_wiki()
    slugs = route_topics(message)

    print(f"\n  Message: \"{message}\"")
    print(f"  Matched: {len(slugs)} article(s)\n")

    if not slugs:
        print("  (no matches)")
    else:
        for slug in slugs:
            article = articles.get(slug)
            if article:
                print(f"    -> {slug}: {article.title} (~{article.token_estimate} tokens)")

    # Show full context size
    ctx = get_wiki_context(message)
    if ctx:
        print(f"\n  Total context: {len(ctx)} chars, ~{len(ctx)//4} tokens")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m tools.wiki_compiler [check|stats|test MSG]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "check":
        ok = cmd_check()
        sys.exit(0 if ok else 1)
    elif cmd == "stats":
        cmd_stats()
    elif cmd == "test":
        if len(sys.argv) < 3:
            print("Usage: python -m tools.wiki_compiler test \"your message here\"")
            sys.exit(1)
        cmd_test(" ".join(sys.argv[2:]))
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
