from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend_fastapi import database

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", status_code=200)
def healthcheck(db: Session = Depends(database.get_db)):
    """
    Healthcheck simples:
    - valida que API está viva
    - testa conexão com banco
    """

    try:
        db.execute("SELECT 1")
    except Exception:
        raise HTTPException(status_code=503, detail="Database unavailable")

    return {"status": "ok"}
