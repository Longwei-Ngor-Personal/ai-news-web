from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Article
from ..schemas import ArticleOut

router = APIRouter(prefix="/articles", tags=["Articles"])

# ------------------------
# Default filtering logic
# ------------------------

# If the user does NOT specify include keywords, we'll use these as the default
DEFAULT_INCLUDE_KEYWORDS = [
    "ai",
    "artificial intelligence",
    "machine learning",
    "ml",
    "deep learning",
    "neural network",
    "neural networks",
    "large language model",
    "large language models",
    "llm",
    "llms",
    "chatgpt",
    "gpt-4",
    "gpt4",
    "gpt-5",
    "openai",
    "anthropic",
    "deepmind",
    "google ai",
    "meta ai",
    "generative ai",
    "genai",
    "transformer",
    "foundation model",
    "multimodal",
    "autonomous agent",
    "ai agent",
    "computer vision",
    "reinforcement learning",
]

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


def _is_ai_relevant(
    article: Article,
    include_keywords: list[str],
    exclude_keywords: list[str],
    strict: bool,
) -> bool:
    """
    Relevance logic:
      - Build a haystack from title + summary + source.
      - Always use a baseline AI keyword list (DEFAULT_INCLUDE_KEYWORDS) if user doesn't pass include=.
      - User's include keywords are ADDED on top of the defaults.
      - Exclude list = user's exclude keywords + DEFAULT_EXCLUDE_KEYWORDS.
      - strict = require >=2 matches from the include list; otherwise >=1.
    """
    hay = f"{article.title or ''} {article.summary or ''} {article.source or ''}".lower()

    # Effective include list = defaults + user-provided
    effective_inc = list(DEFAULT_INCLUDE_KEYWORDS)
    if include_keywords:
        effective_inc.extend(include_keywords)
    # dedupe
    effective_inc = sorted(set(effective_inc))

    # Effective exclude list = defaults + user-provided
    effective_exc = list(DEFAULT_EXCLUDE_KEYWORDS)
    if exclude_keywords:
        effective_exc.extend(exclude_keywords)
    effective_exc = sorted(set(effective_exc))

    # Count matches
    inc_matches = sum(1 for k in effective_inc if k in hay)
    # Require matches if we have any include keywords at all (we always do because of defaults)
    if strict:
        if inc_matches < 2:
            return False
    else:
        if inc_matches < 1:
            return False

    # If ANY exclude keyword matches, drop the article
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
        description="Comma-separated EXTRA keywords that must appear in title/summary/source (added to default AI keywords).",
    ),
    exclude: Optional[str] = Query(
        None,
        description="Comma-separated extra keywords that MUST NOT appear (added to default exclude list).",
    ),
    strict: bool = Query(
        False,
        description="If true, require at least 2 include-keyword matches instead of 1.",
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

    # Keyword filtering with defaults + user-provided
    filtered = [
        art
        for art in raw_items
        if _is_ai_relevant(art, include_keywords=inc_list, exclude_keywords=exc_list, strict=strict)
    ]

    # Per-source cap (after keyword + time filtering)
    if per_source_cap:
        filtered = _apply_per_source_cap(filtered, per_source_cap)

    # Already sorted newest first; slice to requested limit
    return filtered[:limit]
