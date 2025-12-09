from datetime import datetime

from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: str
    url: str
    source: str
    published_at: datetime
    summary: str | None = None
    category: str | None = None


class ArticleOut(ArticleBase):
    id: int

    class Config:
        from_attributes = True  # allow Pydantic to read from ORM objects
