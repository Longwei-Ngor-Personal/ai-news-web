# backend/app/routes/admin.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..tasks.fetch_all import run_fetch_and_store

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/fetch-now")
def admin_fetch_now(db: Session = Depends(get_db)):
    """
    Trigger RSS fetch + store. For now, this is open; you can add auth later.
    """
    result = run_fetch_and_store(db=db)
    return {"status": "ok", "result": result}
