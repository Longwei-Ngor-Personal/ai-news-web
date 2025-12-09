from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Article
from ..schemas import ArticleOut

router = APIRouter(prefix="/articles", tags=["Articles"])


def _parse_keywords(raw: Optional[str]) -> list[str]:
    if not raw:
        return []
    return [s.strip().lower() for s in raw.split(",") if s.strip()]


def _is_ai_relevant(
    article: Article,
    include_keywords: list[str],
    exclude_keywords: list[str],
    strict: bool,
) -> bool:
    """
    Same idea as your original JS isAIRelevant:
      - build a haystack from title + summary + source
      - require at least 1 include keyword (or 2 in strict mode) if include list is non-empty
      - reject if any exclude keyword appears
    """
    hay = f"{article.title or ''} {article.summary or ''} {article.source or ''}".lower()

    inc_matches = sum(1 for k in include_keywords if k in hay)
    if include_keywords:
        if strict and inc_matches < 2:
            return False
        if not strict and inc_matches < 1:
            return False

    if exclude_keywords and any(k in hay for k in exclude_keywords):
        return False

    return True


def _apply_per_source_cap(articles: list[Article], cap: int) -> list[Article]:
    """
    Similar to your JS applyPerSourceCap: keep at most 'cap' items per source.
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
        description="Comma-separated keywords that must appear in title/summary/source",
    ),
    exclude: Optional[str] = Query(
        None,
        description="Comma-separated keywords that MUST NOT appear",
    ),
    strict: bool = Query(
        False,
        description="If true, require at least 2 include-keyword matches instead of 1",
    ),
    per_source_cap: Optional[int] = Query(
        None,
        ge=1,
        le=50,
        description="Max items per source (after keyword/time filtering)",
    ),
    db: Session = Depends(get_db),
):
    """
    Return latest articles, with optional time, keyword, and per-source filters.
    """

    # Base query: newest first
    query = db.query(Article)

    # Time window based on *published_at*, not fetch time
    if hours is not None:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        query = query.filter(Article.published_at >= cutoff)

    query = query.order_by(Article.published_at.desc())

    # Pull more than 'limit' so we have room to filter down
    raw_items = query.limit(limit * 5).all()

    inc_list = _parse_keywords(include)
    exc_list = _parse_keywords(exclude)

    # Keyword filtering
    filtered = [
        art
        for art in raw_items
        if _is_ai_relevant(art, include_keywords=inc_list, exclude_keywords=exc_list, strict=strict)
    ]

    # Per-source cap (after keyword + time filtering)
    if per_source_cap:
        filtered = _apply_per_source_cap(filtered, per_source_cap)

    # The query was already sorted newest first; slice to requested limit
    return filtered[:limit]
