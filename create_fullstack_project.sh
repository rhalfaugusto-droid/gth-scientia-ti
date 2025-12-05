#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)/gth-scientia-ti"
echo "Criando/mesclando projeto em $ROOT"
mkdir -p "$ROOT"
cd "$ROOT"

# -------------------------------
# ROOT files
# -------------------------------
cat > .gitignore <<'EOF'
__pycache__/
.venv/
node_modules/
dist/
.env
uploads/
.DS_Store
.vscode/
EOF

cat > README.md <<'EOF'
GTH Scientia TI - Fullstack (FastAPI + React + Vite)
This scaffold includes:
- backend (FastAPI, SQLAlchemy, OCR via Tesseract, AI integration)
- frontend (React + Vite)
- Dockerfiles and docker-compose for local dev

Local:
  docker-compose up --build

Backend:
  http://localhost:8000/health

Frontend:
  http://localhost:3000/

Env vars:
  - DATABASE_URL
  - SECRET_KEY
  - OPENAI_API_KEY
EOF

# -------------------------------
# backend
# -------------------------------
mkdir -p backend routers models services static uploads

cat > backend/requirements.txt <<'EOF'
fastapi==0.100.0
uvicorn[standard]==0.22.0
SQLAlchemy==2.1.0
psycopg2-binary==2.9.6
python-jose==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
pydantic==1.10.9
python-multipart==0.0.6
Pillow==10.0.0
pytesseract==0.3.10
httpx==0.24.1
EOF

cat > backend/Dockerfile <<'EOF'
FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gcc tesseract-ocr tesseract-ocr-eng && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]
EOF

cat > backend/main.py <<'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
load_dotenv()

# routers
from routers import auth, users, ia, docs

app = FastAPI(title="GTH Scientia TI")
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://admin:admin@db:5432/gth_db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.on_event('startup')
def startup():
    try:
        from models.base import Base
        Base.metadata.create_all(bind=engine)
    except Exception:
        pass

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(ia.router)
app.include_router(docs.router)

@app.get('/health')
def health():
    return {'status':'ok'}
EOF

cat > backend/models/base.py <<'EOF'
from sqlalchemy.orm import declarative_base
Base = declarative_base()
EOF

cat > backend/models/user.py <<'EOF'
from sqlalchemy import Column, Integer, String, Boolean
from .base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
EOF

cat > backend/routers/__init__.py <<'EOF'
# routers package
EOF

cat > backend/routers/auth.py <<'EOF'
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt, os, datetime
from sqlalchemy.orm import Session
from main import SessionLocal
from models.user import User

router = APIRouter(prefix='/auth', tags=['auth'])
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET_KEY = os.getenv('SECRET_KEY', 'devsecret')

class LoginIn(BaseModel):
    email: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/login')
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email==data.email).first()
    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    payload = {'sub': user.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return {'access_token': token, 'token_type': 'bearer'}
EOF

cat > backend/routers/users.py <<'EOF'
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from main import SessionLocal
from sqlalchemy.orm import Session
from models.user import User
from passlib.context import CryptContext

router = APIRouter(prefix='/users', tags=['users'])
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class CreateUser(BaseModel):
    email: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/create')
def create_user(data: CreateUser, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email==data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail='Email already exists')
    user = User(email=data.email, hashed_password=pwd_context.hash(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {'id': user.id, 'email': user.email}
EOF

cat > backend/services/ai_service.py <<'EOF'
import os, httpx
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

async def call_openai(prompt: str):
    if not OPENAI_API_KEY:
        raise RuntimeError('OPENAI_API_KEY not set')
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {'Authorization': f'Bearer {OPENAI_API_KEY}', 'Content-Type': 'application/json'}
    payload = {
        'model': 'gpt-4o-mini',
        'messages': [{'role':'user','content': prompt}],
        'max_tokens': 400
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()
        try:
            return data['choices'][0]['message']['content']
        except Exception:
            return str(data)
EOF

cat > backend/routers/ia.py <<'EOF'
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ai_service import call_openai

router = APIRouter(prefix='/ia', tags=['ia'])

class PromptIn(BaseModel):
    prompt: str

@router.post('/assist')
async def assist(data: PromptIn):
    try:
        resp = await call_openai(data.prompt)
        return {'result': resp}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
EOF

cat > backend/routers/docs.py <<'EOF'
from fastapi import APIRouter, UploadFile, File, HTTPException
import pytesseract
from PIL import Image
import io, os, uuid

router = APIRouter(prefix='/docs', tags=['docs'])

@router.post('/upload')
async def upload_doc(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        img = Image.open(io.BytesIO(contents))
        text = pytesseract.image_to_string(img, lang='eng')
        folder = os.getenv('UPLOAD_DIR', '/tmp/uploads')
        os.makedirs(folder, exist_ok=True)
        filename = f"{uuid.uuid4().hex}_{file.filename}"
        path = os.path.join(folder, filename)
        with open(path, 'wb') as f:
            f.write(contents)
        return {'filename': filename, 'text': text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
EOF

cat > backend/.env.example <<'EOF'
DATABASE_URL=postgresql://admin:admin@db:5432/gth_db
SECRET_KEY=change_me
OPENAI_API_KEY=
UPLOAD_DIR=/tmp/uploads
EOF

# -------------------------------
# frontend (React + Vite)
# -------------------------------
mkdir -p frontend/src/components frontend/public

cat > frontend/package.json <<'EOF'
{
  "name": "gth-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.4.0"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.0.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0"
  }
}
EOF

cat > frontend/index.html <<'EOF'
<!doctype html>
<html>
  <head><meta charset="utf-8"><title>GTH Frontend</title></head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
EOF

cat > frontend/src/main.jsx <<'EOF'
import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './styles.css'
createRoot(document.getElementById('root')).render(<App />)
EOF

cat > frontend/src/App.jsx <<'EOF'
import React, {useState} from 'react'
import axios from 'axios'

export default function App(){
  const [file, setFile] = useState(null)
  const [text, setText] = useState('')
  const upload = async () => {
    if(!file) return alert('select file')
    const fd = new FormData()
    fd.append('file', file)
    const r = await axios.post('/docs/upload', fd, { headers: {'Content-Type':'multipart/form-data'} })
    setText(r.data.text || 'no text')
  }
  return (<div style={{padding:20,fontFamily:'Arial'}}>
    <h1>GTH - Upload OCR</h1>
    <input type="file" onChange={e=>setFile(e.target.files[0])} />
    <button onClick={upload}>Upload</button>
    <pre>{text}</pre>
  </div>)
}
EOF

cat > frontend/src/styles.css <<'EOF'
body{margin:0;font-family:Arial, Helvetica, sans-serif;}
EOF

cat > frontend/Dockerfile <<'EOF'
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx","-g","daemon off;"]
EOF

# -------------------------------
# docker-compose
# -------------------------------
cat > docker-compose.yml <<'EOF'
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin
      POSTGRES_DB: gth_db
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://admin:admin@db:5432/gth_db
      SECRET_KEY: devsecret
      OPENAI_API_KEY: ''
      UPLOAD_DIR: /tmp/uploads
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
volumes:
  db_data:
EOF

# -------------------------------
# favicon placeholder
# -------------------------------
mkdir -p frontend/public
cat > frontend/public/favicon.ico <<'EOF'
placeholder-favicon
EOF

# -------------------------------
# Final messages
# -------------------------------
echo "Scaffold criado em $ROOT"
echo ""
echo "Comandos recomendados:"
echo "  cd $ROOT"
echo "  docker-compose up --build"
echo ""
echo "Depois, adicione, commit e push para seu repo:"
echo "  git add ."
echo "  git commit -m \"Add fullstack scaffold (FastAPI + React + Docker)\""
echo "  git push origin main"
echo ""
echo "Lembre-se de configurar OPENAI_API_KEY se usar a integração com IA."
