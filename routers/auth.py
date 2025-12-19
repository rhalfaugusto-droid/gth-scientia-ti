
from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login")
def login(data: dict):
    return {"message": "Login realizado", "data": data}

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import models, schemas, database, crud, os

router = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_change')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '480'))

class LoginIn(BaseModel):
    email: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = 'bearer'

@router.post('/login', response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(database.get_db)):
    user = crud.get_user_by_email(db, data.email)
    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Credenciais inválidas')
    to_encode = {'sub': user.email, 'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {'access_token': token}

class RegisterIn(BaseModel):
    email: str
    password: str
    name: str = ''

@router.post('/register', response_model=schemas.UserOut)
def register(data: RegisterIn, db: Session = Depends(database.get_db)):
    existing = crud.get_user_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=400, detail='Usuário já existe')
    user = crud.create_user(db, data.email, data.password, data.name)
    return user
#(Initial FastAPI backend setup)
