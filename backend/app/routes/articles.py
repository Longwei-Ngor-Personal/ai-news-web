from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Article
from ..schemas import ArticleOut

router = APIRouter(prefix="/articles", tags=["Articles"])


# Things that are almost always junk / promo / SEO spam for our use case
DEFAULT_EXCLUDE_KEYWORDS = [
    "promo code",
    "promocode",
    "coupon",
    "discount code",
    "% off",
    "percent off",
    "sale",
    "deal",
    "flash sale",
    "black friday",
    "cyber monday",
    "voucher",
    "giveaway",
    "sweepstakes",
    "contest",
    "sale ends",
    "buy now",
    "limited time offer",
]


def _parse_keywords(raw: Optional[str]) -> list[str]:
    if not raw:
        return []
    return [s.strip().lower() for s in raw.split(",") if s.strip()]


def _is_relevant(
    article: Article,
    include_keywords: list[str],
    exclude_keywords: list[str],
    strict: bool,
) -> bool:
    """
    Relevance logic:
      - Build a haystack from title + summary + source.
      - If include_keywords is provided:
          * strict=True  -> require >=2 matches
          * strict=False -> require >=1 match
        If include_keywords is empty, we do NOT filter by include at all.
      - Exclude list = DEFAULT_EXCLUDE_KEYWORDS + user-provided.
    """
    hay = f"{article.title or ''} {article.summary or ''} {article.source or ''}".lower()

    # Build effective exclude list
    effective_exc = list(DEFAULT_EXCLUDE_KEYWORDS)
    if exclude_keywords:
        effective_exc.extend(exclude_keywords)
    effective_exc = sorted(set(effective_exc))

    # If user provided include keywords, enforce them; otherwise, pass everything.
    if include_keywords:
        inc_matches = sum(1 for k in include_keywords if k in hay)
        if strict:
            if inc_matches < 2:
                return False
        else:
            if inc_matches < 1:
                return False

    # Apply exclude filter (always)
    if any(k in hay for k in effective_exc):
        return False

    return True


def _apply_per_source_cap(articles: list[Article], cap: int) -> list[Article]:
    """
    Keep at most 'cap' items per source.
    """
    if not cap or cap <= 0:
        return articles

    buckets: dict[str, int] = {}
    out: list[Article] = []

    for art in articles:
        key = art.source or "Unknown"
        count = buckets.get(key, 0)
        if count < cap:
            buckets[key] = count + 1
            out.append(art)

    return out


@router.get("/", response_model=List[ArticleOut])
def list_articles(
    limit: int = Query(100, ge=1, le=500, description="Max number of articles to return"),
    hours: Optional[int] = Query(
        None,
        ge=1,
        le=168,
        description="Lookback window in hours, based on article published time",
    ),
    include: Optional[str] = Query(
        None,
        description="Comma-separated keywords that must appear in title/summary/source (optional).",
    ),
    exclude: Optional[str] = Query(
        None,
        description="Comma-separated extra keywords that MUST NOT appear (added to default exclude list).",
    ),
    strict: bool = Query(
        False,
        description="If true, require at least 2 include-keyword matches instead of 1 (only when include is set).",
    ),
    per_source_cap: Optional[int] = Query(
        None,
        ge=1,
        le=50,
        description="Max items per source (after keyword/time filtering).",
    ),
    db: Session = Depends(get_db),
):
    """
    Return latest articles, with optional time, keyword, and per-source filters.
    """

    # Base query: newest first
    query = db.query(Article)

    # Time window based on *published_at* (what the feed reports)
    if hours is not None:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        query = query.filter(Article.published_at >= cutoff)

    query = query.order_by(Article.published_at.desc())

    # Pull more than 'limit' so we have room to filter down
    raw_items = query.limit(limit * 5).all()

    inc_list = _parse_keywords(include)
    exc_list = _parse_keywords(exclude)

    # Filtering
    filtered = [
        art
        for art in raw_items
        if _is_relevant(art, include_keywords=inc_list, exclude_keywords=exc_list, strict=strict)
    ]

    # Per-source cap (after keyword + time filtering)
    if per_source_cap:
        filtered = _apply_per_source_cap(filtered, per_source_cap)

    # Already sorted newest first; slice to requested limit
    return filtered[:limit]
