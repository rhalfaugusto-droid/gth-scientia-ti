from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, crud, schemas
from dependencies import get_current_user

router = APIRouter()

@router.get('/me', response_model=schemas.UserOut)
def me(current = Depends(get_current_user)):
    return current

@router.get('/', response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(database.get_db)):
    return crud.get_users(db)
