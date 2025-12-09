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
