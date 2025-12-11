from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, Text

from .db import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    url = Column(String(500), nullable=False, unique=True)
    source = Column(String(200), nullable=False)
    published_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
    summary = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)

class FeedFetchLog(Base):
    __tablename__ = "feed_fetch_log"

    id = Column(Integer, primary_key=True, index=True)

    feed_name = Column(String(255), nullable=False, index=True)
    feed_url = Column(Text, nullable=False)

    status = Column(String(50), nullable=False)  # "success" or "error"
    items_fetched = Column(Integer, nullable=False, default=0)
    inserted = Column(Integer, nullable=False, default=0)
    skipped_existing = Column(Integer, nullable=False, default=0)

    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    error_message = Column(Text, nullable=True)