#!/usr/bin/env python3
"""Generate a static bookshelf website from Obsidian vault notes."""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

import yaml

from template import HTML_TEMPLATE


WIKILINK_RE = re.compile(r"\[\[(?:[^\]|]*\|)?([^\]]+)\]\]")


def strip_wikilinks(value):
    """Recursively strip [[...]] wikilinks from strings/lists/dicts."""
    if isinstance(value, str):
        return WIKILINK_RE.sub(r"\1", value).strip()
    elif isinstance(value, list):
        return [strip_wikilinks(item) for item in value]
    elif isinstance(value, dict):
        return {k: strip_wikilinks(v) for k, v in value.items()}
    return value


def parse_book_file(filepath: Path) -> dict | None:
    """Parse a single markdown file and return a book dict, or None if not a book."""
    content = filepath.read_text(encoding="utf-8")

    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None

    if not isinstance(frontmatter, dict):
        return None

    # Strip wikilinks from all frontmatter values
    frontmatter = strip_wikilinks(frontmatter)

    # Check if this note belongs to the Books category
    categories = frontmatter.get("categories", [])
    if isinstance(categories, str):
        categories = [categories]
    if not isinstance(categories, list):
        return None

    if "Books" not in categories:
        return None

    # Extract description (body content after frontmatter)
    body = parts[2].strip()

    # Map reading status
    read_val = str(frontmatter.get("read", "")).lower()
    if read_val == "true":
        status = "Read"
    else:
        status = "Want to Read"

    # Parse telegram / reading links
    telegram_raw = frontmatter.get("telegram", [])
    if isinstance(telegram_raw, str):
        telegram = [telegram_raw] if telegram_raw.strip() else []
    elif isinstance(telegram_raw, list):
        telegram = [str(t).strip() for t in telegram_raw if str(t).strip()]
    else:
        telegram = []

    # Build book object
    book = {
        "id": filepath.stem,
        "title": frontmatter.get("title") or filepath.stem,
        "authors": frontmatter.get("author", []) or [],
        "genre": frontmatter.get("genre", []) or [],
        "pages": frontmatter.get("pages"),
        "year": frontmatter.get("year"),
        "scoreGr": frontmatter.get("scoreGr"),
        "rating": frontmatter.get("rating"),
        "cover": frontmatter.get("cover", ""),
        "status": status,
        "telegram": telegram,
        "description": body,
    }

    # Ensure list fields are actually lists
    for list_field in ("authors", "genre"):
        val = book[list_field]
        if isinstance(val, str):
            book[list_field] = [val] if val else []
        elif not isinstance(val, list):
            book[list_field] = []

    # Clean numeric fields
    for num_field in ("pages", "year"):
        try:
            book[num_field] = (
                int(book[num_field]) if book[num_field] is not None else None
            )
        except (ValueError, TypeError):
            book[num_field] = None

    # Ensure scoreGr is float or None
    try:
        book["scoreGr"] = (
            float(book["scoreGr"]) if book["scoreGr"] is not None else None
        )
    except (ValueError, TypeError):
        book["scoreGr"] = None

    # Carry through any extra frontmatter keys not already captured
    known_keys = {
        "title",
        "author",
        "genre",
        "pages",
        "year",
        "scoreGr",
        "rating",
        "cover",
        "read",
        "telegram",
        "categories",
        "tags",
    }
    for k, v in frontmatter.items():
        if k not in known_keys and k not in book:
            book[k] = v

    return book


def generate(vault_path: str, output_path: str, site_title: str = "Bookshelf") -> None:
    """Generate the static site."""
    vault = Path(vault_path)
    books = []

    for md_file in vault.rglob("*.md"):
        book = parse_book_file(md_file)
        if book:
            books.append(book)

    # Default sort by title
    books.sort(key=lambda b: b["title"].lower())

    books_json = json.dumps(books, ensure_ascii=False)
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = (
        HTML_TEMPLATE.replace("{{BOOKS_JSON}}", books_json)
        .replace("{{GENERATED}}", generated)
        .replace("{{SITE_TITLE}}", site_title)
    )

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    print(f"Generated {output} with {len(books)} books")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate bookshelf static site from Obsidian vault"
    )
    parser.add_argument("--vault", required=True, help="Path to Obsidian vault")
    parser.add_argument("--output", required=True, help="Path to output index.html")
    parser.add_argument("--title", default="Bookshelf", help="Site title")
    args = parser.parse_args()
    generate(args.vault, args.output, args.title)


if __name__ == "__main__":
    main()
