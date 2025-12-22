from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparser

from .url_utils import canonicalize_url
from typing import Dict, Any, List, Optional

def debug_html_source(source: Dict) -> Dict[str, Any]:
    """
    Debug scraper for a single HTML source.
    Returns structured diagnostics: HTTP status, page length, extracted links count,
    sample URLs, and which filters removed items.
    """
    listing_url = source["url"]

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close",
    }

    timeout = float(source.get("timeout", 15))

    r = requests.get(listing_url, headers=headers, timeout=timeout, allow_redirects=True)
    html = r.text or ""

    result: Dict[str, Any] = {
        "name": source.get("name"),
        "url": listing_url,
        "http_status": r.status_code,
        "final_url": r.url,
        "html_bytes": len(html.encode("utf-8")) if html else 0,
        "found_nodes": 0,
        "raw_links": 0,
        "kept_links": 0,
        "dropped_empty": 0,
        "dropped_fragment": 0,
        "dropped_domain": 0,
        "dropped_include": 0,
        "dropped_exclude": 0,
        "samples_raw": [],
        "samples_kept": [],
    }

    # Catch anti-bot / challenge pages quickly
    lowered = html.lower()
    if r.status_code in (403, 429) or "cf-mitigated" in lowered or "cloudflare" in lowered:
        result["note"] = "Blocked / challenged (Cloudflare or rate limit). HTML may not contain real content."
        # still return samples for inspection
        result["samples_raw"] = [html[:300]]
        return result

    soup = BeautifulSoup(html, "lxml")

    item_selector = source.get("item_selector") or "a"
    link_attr = source.get("link_attr") or "href"

    nodes = soup.select(item_selector)
    result["found_nodes"] = len(nodes)

    include_patterns = source.get("include_url_regex") or []
    exclude_patterns = source.get("exclude_url_regex") or []

    include_res = [re.compile(p) for p in include_patterns] if include_patterns else []
    exclude_res = [re.compile(p) for p in exclude_patterns] if exclude_patterns else []

    listing_host = urlparse(listing_url).netloc.lower()

    raw: List[str] = []
    kept: List[str] = []

    def matches_any(url: str, regs: List[re.Pattern]) -> bool:
        return any(rx.search(url) for rx in regs)

    for node in nodes:
        # If selector is not <a>, try find an <a> inside
        link_node = node
        if getattr(node, "name", None) != "a":
            a = node.select_one("a")
            if not a:
                continue
            link_node = a

        href = (link_node.get(link_attr) or "").strip()
        if not href:
            result["dropped_empty"] += 1
            continue
        if href.startswith("#"):
            result["dropped_fragment"] += 1
            continue

        abs_url = urljoin(listing_url, href)

        raw.append(abs_url)

        link_host = urlparse(abs_url).netloc.lower()
        if listing_host and link_host and listing_host != link_host:
            result["dropped_domain"] += 1
            continue

        if include_res and not matches_any(abs_url, include_res):
            result["dropped_include"] += 1
            continue

        if exclude_res and matches_any(abs_url, exclude_res):
            result["dropped_exclude"] += 1
            continue

        kept.append(abs_url)

    result["raw_links"] = len(raw)
    result["kept_links"] = len(kept)
    result["samples_raw"] = raw[:10]
    result["samples_kept"] = kept[:10]
    return result


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

def _compiled(patterns):
    return [re.compile(p, re.IGNORECASE) for p in (patterns or [])]

def _matches_any(url: str, regs) -> bool:
    return any(r.search(url) for r in regs)

def _in_layout_noise(node) -> bool:
    # skip links inside header/nav/footer
    try:
        return node.find_parent(["nav", "header", "footer"]) is not None
    except Exception:
        return False

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
    include_regs = _compiled(source.get("include_url_regex"))
    exclude_regs = _compiled(source.get("exclude_url_regex"))

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
        
                # Skip nav/header/footer anchors quickly
        if _in_layout_noise(link_node):
            continue

        # Domain sanity: require same host as listing URL (prevents social/share links)
        try:
            host_listing = urlparse(listing_url).netloc.lower()
            host_link = urlparse(abs_url).netloc.lower()
            if host_listing and host_link and host_listing != host_link:
                continue
        except Exception:
            pass

        # Apply per-source include/exclude URL regex rules
        if include_regs and not _matches_any(abs_url, include_regs):
            continue
        if exclude_regs and _matches_any(abs_url, exclude_regs):
            continue

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
