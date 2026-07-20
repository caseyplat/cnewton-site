#!/usr/bin/env python3
"""Render and validate the static Selected Work list from its JSON source."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "selected-work.json"
PAGE_PATH = ROOT / "work" / "index.html"
START_MARKER = "        <!-- BEGIN GENERATED SELECTED WORK ITEMS -->"
END_MARKER = "        <!-- END GENERATED SELECTED WORK ITEMS -->"
REQUIRED_FIELDS = ("title", "publication", "date", "url", "category", "description")


def load_and_validate() -> list[dict[str, str]]:
    entries = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    if not isinstance(entries, list) or not entries:
        raise ValueError("Selected work data must be a non-empty list.")

    seen_urls: set[str] = set()
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            raise ValueError(f"Entry {index} must be an object.")

        missing = [field for field in REQUIRED_FIELDS if not entry.get(field)]
        if missing:
            raise ValueError(f"Entry {index} is missing: {', '.join(missing)}.")

        try:
            datetime.strptime(entry["date"], "%Y-%m-%d")
        except ValueError as error:
            raise ValueError(
                f"Entry {index} has an invalid ISO date: {entry['date']}."
            ) from error

        parsed_url = urlparse(entry["url"])
        if parsed_url.scheme != "https" or not parsed_url.netloc:
            raise ValueError(f"Entry {index} must use a valid HTTPS URL.")
        if entry["url"] in seen_urls:
            raise ValueError(f"Entry {index} duplicates URL: {entry['url']}.")
        seen_urls.add(entry["url"])

    return entries


def display_date(iso_date: str) -> str:
    date = datetime.strptime(iso_date, "%Y-%m-%d")
    return f"{date.strftime('%B')} {date.day}, {date.year}"


def render_items(entries: list[dict[str, str]]) -> str:
    rendered: list[str] = []
    for entry in entries:
        title = html.escape(entry["title"])
        publication = html.escape(entry["publication"])
        iso_date = html.escape(entry["date"], quote=True)
        url = html.escape(entry["url"], quote=True)
        category = html.escape(entry["category"])
        description = html.escape(entry["description"])
        accessible_label = html.escape(
            f"{entry['title']} — {entry['publication']} (opens in a new tab)",
            quote=True,
        )
        credit = entry.get("credit")
        credit_html = (
            f'\n                        <span class="work-credit">{html.escape(credit)}</span>'
            if credit
            else ""
        )

        rendered.append(
            f"""            <li class="work-item">
                <article>
                    <div class="work-meta">
                        <span class="work-category">{category}</span>
                        <span aria-hidden="true">·</span>
                        <span>{publication}</span>
                        <span aria-hidden="true">·</span>
                        <time datetime="{iso_date}">{display_date(entry["date"])}</time>{credit_html}
                    </div>
                    <h2><a href="{url}" target="_blank" rel="noopener" aria-label="{accessible_label}">{title}</a></h2>
                    <p>{description}</p>
                </article>
            </li>"""
        )

    return "\n".join(rendered)


def replace_generated_section(page: str, rendered_items: str) -> str:
    pattern = re.compile(
        rf"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}",
        re.DOTALL,
    )
    replacement = f"{START_MARKER}\n{rendered_items}\n{END_MARKER}"
    updated, count = pattern.subn(replacement, page)
    if count != 1:
        raise ValueError("Expected exactly one generated Selected Work section.")
    return updated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate data and confirm the generated HTML is current.",
    )
    args = parser.parse_args()

    try:
        entries = load_and_validate()
        page = PAGE_PATH.read_text(encoding="utf-8")
        expected = replace_generated_section(page, render_items(entries))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Selected Work validation failed: {error}", file=sys.stderr)
        return 1

    if args.check:
        if expected != page:
            print(
                "Selected Work HTML is out of date. "
                "Run scripts/render_selected_work.py.",
                file=sys.stderr,
            )
            return 1
        print(f"Selected Work is valid and current ({len(entries)} entries).")
        return 0

    PAGE_PATH.write_text(expected, encoding="utf-8")
    print(f"Rendered {len(entries)} Selected Work entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
