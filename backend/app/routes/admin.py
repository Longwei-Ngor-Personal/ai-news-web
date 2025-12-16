# backend/app/routes/admin.py

from datetime import datetime
from typing import List, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import FeedFetchLog, Article
from ..tasks.fetch_all import run_fetch_and_store
from ..services.rss_feeds import RSS_FEEDS
from ..services.html_sources import HTML_SOURCES


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/fetch-now")
def admin_fetch_now(db: Session = Depends(get_db)):
    """
    Trigger RSS fetch + store. For now, this is open; you can add auth later.
    """
    try:
        result = run_fetch_and_store(db=db)
        return {"status": "ok", "result": result}
    except Exception as e:
        print("[admin_fetch_now] ERROR during fetch:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=f"Fetch failed: {e.__class__.__name__}: {e}",
        )


@router.get("/feed-stats")
def admin_feed_stats(db: Session = Depends(get_db)) -> List[Dict]:
    """
    Return the latest fetch status for each configured feed, plus article counts.
    """
    results: List[Dict] = []

    all_sources = RSS_FEEDS + HTML_SOURCES

    for feed in all_sources:
        name = feed["name"]
        url = feed["url"]

        # Latest log entry for this feed (if any)
        log: Optional[FeedFetchLog] = (
            db.query(FeedFetchLog)
            .filter(FeedFetchLog.feed_name == name)
            .order_by(FeedFetchLog.started_at.desc())
            .first()
        )

        # Count how many articles we have for this source
        total_articles = db.query(Article).filter(Article.source == name).count()

        entry: Dict = {
            "feed_name": name,
            "feed_url": url,
            "total_articles": total_articles,
            "last_status": None,
            "last_items_fetched": None,
            "last_inserted": None,
            "last_skipped_existing": None,
            "last_started_at": None,
            "last_finished_at": None,
            "last_error_message": None,
        }

        if log:
            entry.update(
                {
                    "last_status": log.status,
                    "last_items_fetched": log.items_fetched,
                    "last_inserted": log.inserted,
                    "last_skipped_existing": log.skipped_existing,
                    "last_started_at": log.started_at.isoformat() if log.started_at else None,
                    "last_finished_at": log.finished_at.isoformat() if log.finished_at else None,
                    "last_error_message": log.error_message,
                }
            )

        results.append(entry)

    return results
