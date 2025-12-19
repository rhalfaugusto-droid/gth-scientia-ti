from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import database, schemas, crud
from dependencies import get_current_user

router = APIRouter()

class CompanyIn(BaseModel):
    name: str
    cnpj: str | None = None
    area: str | None = None

@router.post('/', response_model=schemas.CompanyOut)
def create_company(data: CompanyIn, db: Session = Depends(database.get_db), current = Depends(get_current_user)):
    return crud.create_company(db, data.name, data.cnpj, data.area)
