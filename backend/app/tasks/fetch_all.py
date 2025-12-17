# backend/app/tasks/fetch_all.py

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, Dict, Set, List

from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..models import Article, FeedFetchLog
from ..services.fetch_news import fetch_feed
from ..services.rss_feeds import RSS_FEEDS
from ..services.html_sources import HTML_SOURCES
from ..services.fetch_html import fetch_html_source

def _load_existing_urls(db: Session) -> Set[str]:
    """
    Load all existing article URLs into a Python set.
    This lets us dedupe across:
      - items already in the DB
      - items we add in this batch before commit
    """
    rows = db.query(Article.url).all()
    return {row[0] for row in rows if row[0]}


def run_fetch_and_store(db: Optional[Session] = None) -> Dict:
    """
    Fetch all RSS feeds and store new articles in the database.
    If 'db' is not provided, create and manage our own session.
    Returns a summary dict with overall counts + per-feed stats.
    """
    owns_session = False
    if db is None:
        db = SessionLocal()
        owns_session = True

    try:
        # Prepare dedupe set
        seen_urls: Set[str] = _load_existing_urls(db)

        total_fetched = 0
        total_inserted = 0
        total_skipped_existing = 0
        feed_summaries: List[Dict] = []

        sources = []

        # RSS sources
        for f in RSS_FEEDS:
            sources.append(
                {
                    "type": "rss",
                    "name": f["name"],
                    "url": f["url"],
                    "category": f.get("category"),
                    "raw": f,
                }
            )

        # HTML sources
        for s in HTML_SOURCES:
        if not s.get("enabled", True):
            continue
        sources.append(
            {
                "type": "html",
                "name": s["name"],
                "url": s["url"],
                "category": s.get("category"),
                "raw": s,
            }
        )

        for src in sources:
            name = src["name"]
            url = src["url"]
            category = src.get("category")
            src_type = src["type"]

            started_at = datetime.now(timezone.utc)
            status = "success"
            error_message: Optional[str] = None
            items_fetched = 0
            inserted = 0
            skipped_existing = 0

            print(f"[run_fetch_and_store] Fetching {src_type} source: {name} ({url})")

            try:
                if src_type == "rss":
                    items = fetch_feed(name=name, url=url, category=category)
                else:
                    items = fetch_html_source(src["raw"])

                items_fetched = len(items)

            except Exception as e:
                status = "error"
                error_message = str(e)
                items = []
                print(f"[run_fetch_and_store] ERROR fetching {name}: {e}")

            # Insert new articles for this source
            for item in items:
                raw_url = (item.get("url") or "").strip()
                if not raw_url:
                    continue

                if raw_url in seen_urls:
                    skipped_existing += 1
                    continue

                art = Article(
                    title=item["title"],
                    url=raw_url,
                    source=item["source"],
                    published_at=item["published_at"],
                    summary=item.get("summary"),
                    category=item.get("category"),
                )
                db.add(art)
                inserted += 1
                seen_urls.add(raw_url)

            finished_at = datetime.now(timezone.utc)

            # Log per-source result (reusing FeedFetchLog)
            log = FeedFetchLog(
                feed_name=name,
                feed_url=url,
                status=status,
                items_fetched=items_fetched,
                inserted=inserted,
                skipped_existing=skipped_existing,
                started_at=started_at,
                finished_at=finished_at,
                error_message=error_message,
            )
            db.add(log)

            total_fetched += items_fetched
            total_inserted += inserted
            total_skipped_existing += skipped_existing

            feed_summaries.append(
                {
                    "feed_name": name,
                    "feed_url": url,
                    "status": status,
                    "items_fetched": items_fetched,
                    "inserted": inserted,
                    "skipped_existing": skipped_existing,
                    "error_message": error_message,
                    "started_at": started_at.isoformat(),
                    "finished_at": finished_at.isoformat(),
                }
            )

        db.commit()

        summary = {
            "total_fetched": total_fetched,
            "inserted": total_inserted,
            "skipped_existing": total_skipped_existing,
            "feeds": feed_summaries,
        }
        print(f"[run_fetch_and_store] Overall summary: {summary}")
        return summary

    finally:
        if owns_session and db is not None:
            db.close()


if __name__ == "__main__":
    # Allow running this as:
    #   docker compose exec backend python -m app.tasks.fetch_all
    run_fetch_and_store()
