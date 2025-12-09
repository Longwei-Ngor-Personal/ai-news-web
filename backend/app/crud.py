from sqlalchemy.orm import Session
from sqlalchemy import select

from . import models


def get_articles(db: Session, limit: int = 50):
    """
    Return the latest articles, newest first, up to 'limit'.
    """
    stmt = (
        select(models.Article)
        .order_by(models.Article.published_at.desc())
        .limit(limit)
    )
    return db.scalars(stmt).all()
