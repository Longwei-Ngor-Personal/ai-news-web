from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db import get_db
from .. import crud
from ..schemas import ArticleOut

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("/", response_model=List[ArticleOut])
def list_articles(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """
    Return the latest articles from the database.
    """
    return crud.get_articles(db=db, limit=limit)
