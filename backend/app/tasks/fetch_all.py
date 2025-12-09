# backend/app/tasks/fetch_all.py

from __future__ import annotations

from typing import Optional, Dict

from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..models import Article
from ..services.fetch_news import fetch_all_feeds


def run_fetch_and_store(db: Optional[Session] = None) -> Dict:
    """
    Fetch all RSS feeds and store new articles in the database.
    If 'db' is not provided, create and manage our own session.
    Returns a summary dict with counts.
    """
    owns_session = False
    if db is None:
        db = SessionLocal()
        owns_session = True

    try:
        items = fetch_all_feeds()
        total_fetched = len(items)
        inserted = 0
        skipped_existing = 0

        for item in items:
            # Skip if URL already exists
            existing = db.query(Article).filter(Article.url == item["url"]).first()
            if existing:
                skipped_existing += 1
                continue

            art = Article(
                title=item["title"],
                url=item["url"],
                source=item["source"],
                published_at=item["published_at"],
                summary=item["summary"],
                category=item.get("category"),
            )
            db.add(art)
            inserted += 1

        db.commit()

        summary = {
            "total_fetched": total_fetched,
            "inserted": inserted,
            "skipped_existing": skipped_existing,
        }
        print(f"[run_fetch_and_store] {summary}")
        return summary

    finally:
        if owns_session and db is not None:
            db.close()


if __name__ == "__main__":
    # Allow running this as:
    #   docker compose exec backend python -m app.tasks.fetch_all
    run_fetch_and_store()
