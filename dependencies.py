from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
import os
from pydantic import BaseModel
from sqlalchemy.orm import Session
import database, crud

SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_change')
ALGORITHM = 'HS256'

class CurrentUser(BaseModel):
    id: int
    email: str
    name: str | None = None

def get_current_user(db: Session = Depends(database.get_db)):
    def _inner(request: Request):
        auth = request.headers.get('authorization')
        if not auth or not auth.startswith('Bearer '):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
        token = auth.split(' ',1)[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
        user = crud.get_user_by_email(db, payload.get('sub'))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
        return CurrentUser(id=user.id, email=user.email, name=user.name)
    return _inner
