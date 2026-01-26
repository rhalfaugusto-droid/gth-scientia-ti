from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend_fastapi.services.xml_parser_service import parse_nfe_xml
from backend_fastapi.services.tax_service import calculate_tax
from backend_fastapi.dependencies import get_current_user
from backend_fastapi import database,schemas, crud


router = APIRouter()

class RuleIn(BaseModel):
    name: str
    description: str | None = None

class RuleVersionIn(BaseModel):
    rule_id: int | None = None
    version: str
    content: dict  # arbitrary json describing the rule formula / metadata

@router.post('/', response_model=schemas.RuleOut)
def create_rule(data: RuleIn, db: Session = Depends(database.get_db), current = Depends(get_current_user)):
    return crud.create_rule(db, data.name, data.description or '')

@router.post('/{rule_id}/versions', response_model=schemas.RuleVersionOut)
def create_rule_version(rule_id: int, data: RuleVersionIn, db: Session = Depends(database.get_db), current = Depends(get_current_user)):
    return crud.create_rule_version(db, rule_id, data.version, data.content)
