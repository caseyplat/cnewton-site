#!/usr/bin/env python3
"""Validate metadata and indexing files for the static cnewton.org site."""

from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
SITE_ORIGIN = "https://cnewton.org"
SOCIAL_IMAGE = f"{SITE_ORIGIN}/social-card.jpg"

INDEXABLE_PAGES = {
    "index.html": {
        "canonical": f"{SITE_ORIGIN}/",
        "schema_types": {"WebSite", "Person"},
    },
    "about/index.html": {
        "canonical": f"{SITE_ORIGIN}/about/",
        "schema_types": {"ProfilePage", "Person"},
    },
    "work/index.html": {
        "canonical": f"{SITE_ORIGIN}/work/",
        "schema_types": {"CollectionPage"},
    },
}

REQUIRED_OG = {
    "og:type",
    "og:url",
    "og:site_name",
    "og:locale",
    "og:title",
    "og:description",
    "og:image",
    "og:image:width",
    "og:image:height",
    "og:image:type",
    "og:image:alt",
}

REQUIRED_TWITTER = {
    "twitter:card",
    "twitter:title",
    "twitter:description",
    "twitter:image",
    "twitter:image:alt",
}


class HeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.in_title = False
        self.in_json_ld = False
        self.json_ld_parts: list[str] = []
        self.json_ld_blocks: list[str] = []
        self.metas: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = {name.lower(): value or "" for name, value in attrs}
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            self.metas.append(values)
        elif tag == "link":
            self.links.append(values)
        elif tag == "script" and values.get("type") == "application/ld+json":
            self.in_json_ld = True
            self.json_ld_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        elif tag == "script" and self.in_json_ld:
            self.in_json_ld = False
            self.json_ld_blocks.append("".join(self.json_ld_parts).strip())
            self.json_ld_parts = []

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.in_json_ld:
            self.json_ld_parts.append(data)

    @property
    def title(self) -> str:
        return "".join(self.title_parts).strip()


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def values_for_meta(
    parser: HeadParser, attribute: str, value: str
) -> list[str]:
    return [
        meta.get("content", "")
        for meta in parser.metas
        if meta.get(attribute) == value
    ]


def links_for_rel(parser: HeadParser, rel: str) -> list[dict[str, str]]:
    return [
        link
        for link in parser.links
        if rel in link.get("rel", "").lower().split()
    ]


def collect_schema_types(value: object) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        schema_type = value.get("@type")
        if isinstance(schema_type, str):
            found.add(schema_type)
        elif isinstance(schema_type, list):
            found.update(item for item in schema_type if isinstance(item, str))
        for child in value.values():
            found.update(collect_schema_types(child))
    elif isinstance(value, list):
        for child in value:
            found.update(collect_schema_types(child))
    return found


def valid_absolute_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def parse_page(relative_path: str, errors: list[str]) -> HeadParser:
    path = ROOT / relative_path
    parser = HeadParser()
    try:
        parser.feed(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"{relative_path}: file is missing", errors)
    return parser


def validate_indexable_page(
    relative_path: str,
    expected: dict[str, object],
    errors: list[str],
) -> tuple[str, str]:
    parser = parse_page(relative_path, errors)
    label = relative_path

    if not parser.title:
        fail(f"{label}: missing title", errors)

    descriptions = values_for_meta(parser, "name", "description")
    if len(descriptions) != 1 or not descriptions[0]:
        fail(f"{label}: expected one non-empty meta description", errors)

    canonicals = links_for_rel(parser, "canonical")
    expected_canonical = str(expected["canonical"])
    if len(canonicals) != 1:
        fail(f"{label}: expected exactly one canonical link", errors)
    elif canonicals[0].get("href") != expected_canonical:
        fail(
            f"{label}: canonical must be {expected_canonical}",
            errors,
        )
    if expected_canonical != f"{SITE_ORIGIN}/" and not expected_canonical.endswith("/"):
        fail(f"{label}: canonical violates the trailing-slash policy", errors)

    robots_values = values_for_meta(parser, "name", "robots")
    if any("noindex" in value.lower() for value in robots_values):
        fail(f"{label}: indexable page contains noindex", errors)

    og_values = {
        name: values_for_meta(parser, "property", name)
        for name in REQUIRED_OG
    }
    for name, values in og_values.items():
        if len(values) != 1 or not values[0]:
            fail(f"{label}: expected one non-empty {name}", errors)
    if og_values["og:url"] and og_values["og:url"][0] != expected_canonical:
        fail(f"{label}: og:url disagrees with canonical", errors)
    if og_values["og:image"] and og_values["og:image"][0] != SOCIAL_IMAGE:
        fail(f"{label}: og:image must use the approved social card", errors)
    if og_values["og:image:width"] and og_values["og:image:width"][0] != "1200":
        fail(f"{label}: og:image:width must be 1200", errors)
    if og_values["og:image:height"] and og_values["og:image:height"][0] != "630":
        fail(f"{label}: og:image:height must be 630", errors)

    twitter_values = {
        name: values_for_meta(parser, "name", name)
        for name in REQUIRED_TWITTER
    }
    for name, values in twitter_values.items():
        if len(values) != 1 or not values[0]:
            fail(f"{label}: expected one non-empty {name}", errors)
    if twitter_values["twitter:card"] and twitter_values["twitter:card"][0] != "summary_large_image":
        fail(f"{label}: twitter:card must be summary_large_image", errors)
    if twitter_values["twitter:image"] and twitter_values["twitter:image"][0] != SOCIAL_IMAGE:
        fail(f"{label}: twitter:image must use the approved social card", errors)

    feeds = links_for_rel(parser, "alternate")
    feed_types = {link.get("type"): link.get("href") for link in feeds}
    expected_feeds = {
        "application/rss+xml": "https://blog.cnewton.org/feed.xml",
        "application/feed+json": "https://blog.cnewton.org/feed.json",
    }
    for feed_type, href in expected_feeds.items():
        if feed_types.get(feed_type) != href:
            fail(f"{label}: missing {feed_type} autodiscovery", errors)

    if len(parser.json_ld_blocks) != 1:
        fail(f"{label}: expected exactly one JSON-LD block", errors)
    else:
        try:
            structured_data = json.loads(parser.json_ld_blocks[0])
        except json.JSONDecodeError as error:
            fail(f"{label}: malformed JSON-LD ({error})", errors)
        else:
            present_types = collect_schema_types(structured_data)
            missing_types = set(expected["schema_types"]) - present_types
            if missing_types:
                fail(
                    f"{label}: JSON-LD missing {', '.join(sorted(missing_types))}",
                    errors,
                )

    for value in [expected_canonical, *(v[0] for v in og_values.values() if v)]:
        if value.startswith("http") and not valid_absolute_url(value):
            fail(f"{label}: malformed absolute URL {value}", errors)

    return parser.title, descriptions[0] if descriptions else ""


def validate_404(errors: list[str]) -> None:
    parser = parse_page("404.html", errors)
    if parser.title != "Page Not Found — Casey Newton":
        fail("404.html: missing or inaccurate title", errors)
    robots_values = values_for_meta(parser, "name", "robots")
    if len(robots_values) != 1 or "noindex" not in robots_values[0].lower():
        fail("404.html: must contain one noindex robots directive", errors)
    if links_for_rel(parser, "canonical"):
        fail("404.html: non-indexable error page must not have a canonical", errors)


def validate_sitemap(errors: list[str]) -> None:
    sitemap_path = ROOT / "sitemap.xml"
    try:
        tree = ElementTree.parse(sitemap_path)
    except (FileNotFoundError, ElementTree.ParseError) as error:
        fail(f"sitemap.xml: invalid or missing ({error})", errors)
        return
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locations = [
        element.text or ""
        for element in tree.findall(".//s:loc", namespace)
    ]
    expected_locations = [
        str(page["canonical"]) for page in INDEXABLE_PAGES.values()
    ]
    if locations != expected_locations:
        fail(
            "sitemap.xml: URLs must exactly match canonical indexable pages in display order",
            errors,
        )
    for location in locations:
        if not valid_absolute_url(location):
            fail(f"sitemap.xml: malformed URL {location}", errors)
        if "/blog" in location or location.endswith("/404.html"):
            fail(f"sitemap.xml: redirected or non-indexable URL {location}", errors)


def validate_robots(errors: list[str]) -> None:
    path = ROOT / "robots.txt"
    try:
        contents = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail("robots.txt: file is missing", errors)
        return
    if "User-agent: *" not in contents or "Allow: /" not in contents:
        fail("robots.txt: site must remain crawlable", errors)
    if f"Sitemap: {SITE_ORIGIN}/sitemap.xml" not in contents:
        fail("robots.txt: sitemap declaration is missing", errors)


def main() -> int:
    errors: list[str] = []
    titles: list[str] = []
    descriptions: list[str] = []

    for relative_path, expected in INDEXABLE_PAGES.items():
        title, description = validate_indexable_page(
            relative_path, expected, errors
        )
        titles.append(title)
        descriptions.append(description)

    if len(set(titles)) != len(titles):
        fail("Indexable pages must have unique titles", errors)
    if len(set(descriptions)) != len(descriptions):
        fail("Indexable pages must have unique descriptions", errors)

    validate_404(errors)
    validate_sitemap(errors)
    validate_robots(errors)

    social_image = ROOT / "social-card.jpg"
    if not social_image.exists():
        fail("social-card.jpg: approved social image is missing", errors)

    if errors:
        print("Metadata validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Metadata is valid for 3 indexable pages, the 404 page, "
        "sitemap.xml, robots.txt, and both blog feeds."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
