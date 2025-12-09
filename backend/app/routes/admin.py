# backend/app/routes/admin.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..tasks.fetch_all import run_fetch_and_store

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/fetch-now")
def admin_fetch_now(db: Session = Depends(get_db)):
    """
    Trigger RSS fetch + store. For now, this is open; you can add auth later.
    """
    try:
        result = run_fetch_and_store(db=db)
        return {"status": "ok", "result": result}
    except Exception as e:
        # This will show in docker logs
        print("[admin_fetch_now] ERROR during fetch:", repr(e))
        # And this will show in the HTTP response
        raise HTTPException(
            status_code=500,
            detail=f"Fetch failed: {e.__class__.__name__}: {e}",
        )
