# backend/app/tasks/fetch_all.py

from __future__ import annotations

from typing import Optional, Dict, Set

from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..models import Article
from ..services.fetch_news import fetch_all_feeds


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
    Returns a summary dict with counts.
    """
    owns_session = False
    if db is None:
        db = SessionLocal()
        owns_session = True

    try:
        items = fetch_all_feeds()
        total_fetched = len(items)

        # Load existing URLs once, then keep adding to this set as we insert.
        seen_urls: Set[str] = _load_existing_urls(db)
        inserted = 0
        skipped_existing = 0

        for item in items:
            url = (item.get("url") or "").strip()
            if not url:
                continue

            if url in seen_urls:
                skipped_existing += 1
                continue

            art = Article(
                title=item["title"],
                url=url,
                source=item["source"],
                published_at=item["published_at"],
                summary=item["summary"],
                category=item.get("category"),
            )
            db.add(art)
            inserted += 1
            # Mark as seen so we don't add it again in this batch
            seen_urls.add(url)

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
