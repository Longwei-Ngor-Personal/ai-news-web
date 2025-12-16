from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparser

from .url_utils import canonicalize_url


DEFAULT_HEADERS = {
    # Browser-ish UA helps with basic bot filtering
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


@dataclass
class HtmlItem:
    title: str
    url: str
    published_at: datetime
    summary: Optional[str] = None


def _safe_parse_datetime(raw: Optional[str]) -> datetime:
    """
    Parse various datetime formats. If missing/unparseable, fallback to now (UTC).
    """
    if not raw:
        return datetime.now(timezone.utc)

    try:
        dt = dateparser.parse(raw)
        if not dt:
            return datetime.now(timezone.utc)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return datetime.now(timezone.utc)


def fetch_html_source(source: Dict) -> List[Dict]:
    """
    Fetch and parse an HTML listing page into a list of normalized article dicts
    matching your Article constructor expectations.
    """
    name = source["name"]
    listing_url = source["url"]
    category = source.get("category")

    item_selector = source.get("item_selector") or "article"
    title_selector = source.get("title_selector")
    link_attr = source.get("link_attr") or "href"
    date_selector = source.get("date_selector")
    date_attr = source.get("date_attr")
    summary_selector = source.get("summary_selector")
    max_items = int(source.get("max_items") or 30)

    res = requests.get(
        listing_url,
        headers=DEFAULT_HEADERS,
        timeout=20,
        allow_redirects=True,
    )
    # Raise for 4xx/5xx so caller can log failure cleanly
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")

    # Find candidates
    nodes = soup.select(item_selector)
    items: List[Dict] = []
    seen: Set[str] = set()

    def node_text(n) -> str:
        return " ".join((n.get_text(" ", strip=True) or "").split())

    for n in nodes:
        # Determine link node
        link_node = n
        if n.name != "a":
            # try to find first anchor inside
            a = n.find("a")
            if a:
                link_node = a

        href = (link_node.get(link_attr) or "").strip()
        if not href:
            continue

        abs_url = urljoin(listing_url, href)
        abs_url = canonicalize_url(abs_url)

        # Skip obvious non-article links quickly
        if not abs_url.startswith("http"):
            continue

        if abs_url in seen:
            continue
        seen.add(abs_url)

        # Title
        title = ""
        if title_selector:
            tnode = n.select_one(title_selector)
            if tnode:
                title = node_text(tnode)
        if not title:
            # fallback: anchor text
            title = node_text(link_node)

        if not title or len(title) < 8:
            # too weak, likely nav
            continue

        # Date
        published_at = datetime.now(timezone.utc)
        if date_selector:
            dnode = n.select_one(date_selector) or soup.select_one(date_selector)
            if dnode:
                if date_attr:
                    published_at = _safe_parse_datetime(dnode.get(date_attr))
                else:
                    published_at = _safe_parse_datetime(node_text(dnode))

        # Summary/excerpt (optional)
        summary = None
        if summary_selector:
            snode = n.select_one(summary_selector)
            if snode:
                summary = node_text(snode)[:500]

        items.append(
            {
                "title": title,
                "url": abs_url,
                "source": name,
                "published_at": published_at,
                "summary": summary,
                "category": category,
            }
        )

        if len(items) >= max_items:
            break

    return items
