from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date
from . import models


def get_articles(db: Session, limit: int = 50):
    stmt = select(models.Article).order_by(models.Article.published_at.desc()).limit(limit)
    return db.scalars(stmt).all()


def get_articles_by_date(db: Session, target_date: date, limit: int = 100):
    # For SQLite, we can compare date part by using DATE() in SQL, but for now keep it simple:
    stmt = (
        select(models.Article)
        .where(models.Article.published_at >= target_date)
        .order_by(models.Article.published_at.desc())
        .limit(limit)
    )
    return db.scalars(stmt).all()
