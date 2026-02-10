from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend_fastapi import database, schemas, crud
from backend_fastapi.dependencies import get_current_user


router = APIRouter()


# =========================
# MODELOS
# =========================

class RuleIn(BaseModel):
    name: str
    description: str | None = None


class RuleVersionIn(BaseModel):
    version: str
    content: dict  # JSON com fórmula/metadados


# =========================
# ROTAS
# =========================

@router.post("/", response_model=schemas.RuleOut)
def create_rule(
    data: RuleIn,
    db: Session = Depends(database.get_db),
    current=Depends(get_current_user),
):
    return crud.create_rule(db, data.name, data.description or "")


@router.post("/{rule_id}/versions", response_model=schemas.RuleVersionOut)
def create_rule_version(
    rule_id: int,
    data: RuleVersionIn,
    db: Session = Depends(database.get_db),
    current=Depends(get_current_user),
):
    rule = crud.get_rule(db, rule_id)

    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    return crud.create_rule_version(db, rule_id, data.version, data.content)
