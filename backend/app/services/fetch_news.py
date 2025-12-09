# backend/app/services/fetch_news.py

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Dict

import httpx
import feedparser

from .rss_feeds import RSS_FEEDS


def _parse_published(entry) -> datetime:
    """
    Try to parse the published date from a feed entry.
    Fallback to 'now' if we can't.
    """
    # feedparser often provides 'published_parsed' or 'updated_parsed'
    for key in ("published_parsed", "updated_parsed"):
        t = getattr(entry, key, None) or entry.get(key)
        if t:
            # t is a time.struct_time
            return datetime(*t[:6], tzinfo=timezone.utc)

    # Fall back to now
    return datetime.now(timezone.utc)


def _extract_summary(entry) -> str | None:
    """
    Extract a reasonable summary/description for the entry.
    """
    for key in ("summary", "description"):
        val = getattr(entry, key, None) or entry.get(key)
        if val:
            return str(val)
    return None


def fetch_feed(name: str, url: str, category: str | None = None) -> List[Dict]:
    """
    Fetch and parse a single RSS/Atom feed.
    Returns a list of dicts with keys: title, url, source, published_at, summary, category
    """
    print(f"[fetch_feed] Fetching {name} from {url}")
    items: List[Dict] = []

    try:
        resp = httpx.get(url, timeout=15.0)
        resp.raise_for_status()
    except Exception as e:
        print(f"[fetch_feed] ERROR fetching {name} ({url}): {e}")
        return items

    parsed = feedparser.parse(resp.text)

    for entry in parsed.entries:
        title = getattr(entry, "title", None) or entry.get("title") or ""
        link = getattr(entry, "link", None) or entry.get("link") or ""
        if not title or not link:
            continue  # skip broken entries

        published_at = _parse_published(entry)
        summary = _extract_summary(entry)

        items.append(
            {
                "title": title.strip(),
                "url": link.strip(),
                "source": name,
                "published_at": published_at,
                "summary": summary,
                "category": category or "AI",
            }
        )

    print(f"[fetch_feed] {name}: got {len(items)} items")
    return items


def fetch_all_feeds() -> List[Dict]:
    """
    Fetch all feeds defined in RSS_FEEDS and return a merged list of items.
    """
    all_items: List[Dict] = []

    for feed in RSS_FEEDS:
        name = feed["name"]
        url = feed["url"]
        category = feed.get("category")
        items = fetch_feed(name=name, url=url, category=category)
        all_items.extend(items)

    print(f"[fetch_all_feeds] Total items fetched: {len(all_items)}")
    return all_items
