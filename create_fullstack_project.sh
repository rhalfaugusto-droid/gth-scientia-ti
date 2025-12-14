#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)/gth_fullstack_both"
echo "Criando scaffold em $ROOT"
mkdir -p "$ROOT"
cd "$ROOT"

# ---------------- FRONTEND ----------------
mkdir -p frontend/src/components frontend/src/pages

cat > frontend/package.json <<'JSON'
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
    "axios": "^1.4.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-dnd": "^16.0.1",
    "react-dnd-html5-backend": "^16.0.1",
    "react-router-dom": "^6.11.2"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.0.0"
  }
}
JSON

cat > frontend/index.html <<'HTML'
<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
    <title>GTH - Frontend</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
HTML

cat > frontend/vite.config.js <<'JS'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
export default defineConfig({
  plugins: [react()],
  server: { port: 3000 }
})
JS

cat > frontend/src/main.jsx <<'JS'
import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './styles.css'
createRoot(document.getElementById('root')).render(<App/>)
JS

cat > frontend/src/styles.css <<'CSS'
body{margin:0;font-family:Arial,sans-serif;background:#f7fafc;} .container{max-width:1100px;margin:0 auto;padding:20px;}
CSS

cat > frontend/src/App.jsx <<'JS'
import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import CadastroEmpresa from './pages/CadastroEmpresa'
import CadastroTributario from './pages/CadastroTributario'
import Workspace from './pages/Workspace'
import Builder from './pages/Builder'
import Nav from './components/Nav'

export default function App(){
  return (
    <BrowserRouter>
      <Nav/>
      <Routes>
        <Route path='/' element={<Login/>}/>
        <Route path='/cadastro-empresa' element={<CadastroEmpresa/>}/>
        <Route path='/cadastro-tributario' element={<CadastroTributario/>}/>
        <Route path='/workspace' element={<Workspace/>}/>
        <Route path='/builder' element={<Builder/>}/>
      </Routes>
    </BrowserRouter>
  )
}
JS

cat > frontend/src/components/Nav.jsx <<'JS'
import React from 'react'
import { Link } from 'react-router-dom'
export default function Nav(){ return (<nav style={{background:'#0f172a',padding:12}}><div style={{maxWidth:1100,margin:'0 auto',display:'flex',gap:12}}><Link to='/' style={{color:'#fff'}}>GTH</Link><Link to='/workspace' style={{color:'#9ca3af'}}>Workspace</Link><Link to='/builder' style={{color:'#9ca3af'}}>Builder</Link></div></nav>) }
JS

cat > frontend/src/pages/Login.jsx <<'JS'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

export default function Login(){
  const navigate = useNavigate()
  const [email,setEmail]=useState('')
  const [password,setPassword]=useState('')
  const [error,setError]=useState('')

  const handleLogin = async () => {
    setError('')
    try {
      // try Node backend
      const nodeRes = await axios.post('http://localhost:4000/auth/login',{ email, password })
      if(nodeRes?.data?.token){ localStorage.setItem('token', nodeRes.data.token); localStorage.setItem('backend','node'); return navigate('/workspace') }
    } catch(e){}
    try {
      const pyRes = await axios.post('http://localhost:8000/auth/login',{ email, password })
      if(pyRes?.data?.access_token){ localStorage.setItem('token', pyRes.data.access_token); localStorage.setItem('backend','python'); return navigate('/workspace') }
    } catch(e){}
    setError('Credenciais inválidas')
  }

  const quick = ()=>{ localStorage.setItem('token','dev'); localStorage.setItem('backend','none'); navigate('/workspace') }

  return (
    <div style={{display:'flex',height:'80vh',alignItems:'center',justifyContent:'center'}}>
      <div style={{width:360,background:'#fff',padding:20,borderRadius:8}}>
        <h2>Login</h2>
        {error && <div style={{color:'red'}}>{error}</div>}
        <input placeholder='E-mail' value={email} onChange={e=>setEmail(e.target.value)} style={{width:'100%',padding:8,marginTop:8}}/>
        <input placeholder='Senha' type='password' value={password} onChange={e=>setPassword(e.target.value)} style={{width:'100%',padding:8,marginTop:8}}/>
        <button onClick={handleLogin} style={{width:'100%',marginTop:12}}>Entrar</button>
        <button onClick={quick} style={{width:'100%',marginTop:8}}>Entrar sem backend (teste)</button>
        <div style={{marginTop:8,fontSize:12,color:'#666'}}>Node default: http://localhost:4000 | Python default: http://localhost:8000</div>
      </div>
    </div>
  )
}
JS

cat > frontend/src/pages/CadastroEmpresa.jsx <<'JS'
import { useState } from 'react'
export default function CadastroEmpresa(){ const [empresa,setEmpresa]=useState({nome:'',cnpj:'',areaAtuacao:''}); const next=()=>{ localStorage.setItem('empresa',JSON.stringify(empresa)); window.location.href='/cadastro-tributario' }; return (<div className='container'><h1>Cadastro da Empresa</h1><input placeholder='Nome' value={empresa.nome} onChange={e=>setEmpresa({...empresa,nome:e.target.value})} style={{width:'100%',padding:10}}/><input placeholder='CNPJ' value={empresa.cnpj} onChange={e=>setEmpresa({...empresa,cnpj:e.target.value})} style={{width:'100%',padding:10,marginTop:8}}/><input placeholder='Área de atuação' value={empresa.areaAtuacao} onChange={e=>setEmpresa({...empresa,areaAtuacao:e.target.value})} style={{width:'100%',padding:10,marginTop:8}}/><button onClick={next} style={{marginTop:12,padding:10}}>Próximo</button></div>) }
JS

cat > frontend/src/pages/CadastroTributario.jsx <<'JS'
import { useState } from 'react'
export default function CadastroTributario(){ const [regime,setRegime]=useState(''); const concluir=()=>{ localStorage.setItem('regimeTributario',regime); window.location.href='/workspace' }; return (<div className='container'><h1>Selecione o Regime Tributário</h1><select value={regime} onChange={e=>setRegime(e.target.value)} style={{width:'100%',padding:10}}><option value=''>Selecione...</option><option value='simples'>Simples Nacional</option><option value='presumido'>Lucro Presumido</option><option value='real'>Lucro Real</option><option value='hibrido'>Período Híbrido 2026-2033</option></select><button onClick={concluir} style={{marginTop:12,padding:10}}>Concluir</button></div>) }
JS

cat > frontend/src/pages/Workspace.jsx <<'JS'
import React, {useState} from 'react'
export default function Workspace(){ const [area,setArea]=useState([]); const add=(w)=>{ if(!area.includes(w)) setArea([...area,w]) }; const widgets=['Resumo Tributário','Documentos Pendentes','Notas Importadas','Créditos / Débitos','Alertas da IA Fiscal']; return (<div style={{display:'flex',height:'90vh'}}><aside style={{width:260,background:'#f1f5f9',padding:12}}><h3>Módulos</h3>{widgets.map(w=> <button key={w} onClick={()=>add(w)} style={{display:'block',width:'100%',marginTop:8,padding:8}}>{w}</button>)}</aside><main style={{flex:1,padding:20}}><h2>Área de Trabalho</h2>{area.length===0 && <div>Selecione módulos ao lado.</div>}<div style={{display:'grid',gridTemplateColumns:'repeat(2,1fr)',gap:12,marginTop:12}}>{area.map(a=> <div key={a} style={{background:'#fff',padding:12,borderRadius:8}}>{a}</div>)}</div></main></div>) }
JS

cat > frontend/src/pages/Builder.jsx <<'JS'
import React, {useState} from 'react'
import { DndProvider, useDrag, useDrop } from 'react-dnd'
import { HTML5Backend } from 'react-dnd-html5-backend'
const ItemType='STEP'
function Step({name}){ const [{isDragging},drag]=useDrag(()=>({type:ItemType,item:{name}}),[name]); return <div ref={drag} style={{padding:8,background:'#fff',borderRadius:6}}>{name}</div> }
function Canvas({flow,setFlow}){ const [,drop]=useDrop(()=>({accept:ItemType, drop:(item)=> setFlow([...flow, item.name])}),[flow]); return <div ref={drop} style={{minHeight:300,background:'#f8fafc',padding:12,borderRadius:6}}>{flow.map((s,i)=> <div key={i} style={{padding:8,background:'#fff',marginTop:8,borderRadius:6}}>{i+1}. {s}</div>)}</div> }
export default function Builder(){ const steps=['Importar Nota','Validar XML','Classificar Tributação','Calcular Imposto','Gerar Relatório','Enviar para Contabilidade']; const [flow,setFlow]=useState([]); return (<DndProvider backend={HTML5Backend}><div style={{display:'flex',height:'90vh'}}><aside style={{width:280,padding:12,background:'#f1f5f9'}}><h3>Ações</h3>{steps.map(s=> <div key={s} style={{marginTop:8}}><Step name={s} /></div>)}</aside><main style={{flex:1,padding:20}}><h2>Montagem de Fluxo</h2><Canvas flow={flow} setFlow={setFlow} /></main></div></DndProvider>) }
JS

cat > frontend/Dockerfile <<'DOCKER'
FROM node:18-alpine as build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
RUN npm run build
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx","-g","daemon off;"]
DOCKER

# ---------------- BACKEND_NODE ----------------
mkdir -p backend_node/src
cat > backend_node/package.json <<'JSON'
{
  "name": "gth-backend-node",
  "version": "0.1.0",
  "scripts": {
    "dev": "ts-node-dev --respawn --transpile-only src/server.ts"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "body-parser": "^1.20.2",
    "jsonwebtoken": "^9.0.0",
    "bcryptjs": "^2.4.3",
    "sqlite3": "^5.1.6"
  },
  "devDependencies": {
    "ts-node-dev": "^2.0.0",
    "typescript": "^5.5.6",
    "@types/express": "^4.17.21",
    "@types/node": "^20.5.1"
  }
}
JSON

cat > backend_node/tsconfig.json <<'JSON'
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "CommonJS",
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true
  }
}
JSON

cat > backend_node/src/server.ts <<'TS'
import express from 'express'
import cors from 'cors'
import bodyParser from 'body-parser'
import jwt from 'jsonwebtoken'
import bcrypt from 'bcryptjs'
import path from 'path'
import sqlite3 from 'sqlite3'

const app = express()
app.use(cors())
app.use(bodyParser.json())

const DB_FILE = path.join(__dirname,'..','data.sqlite')
const SECRET = process.env.SECRET_KEY || 'node_dev_secret'
const db = new sqlite3.Database(DB_FILE)
db.serialize(()=>{
  db.run('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT, name TEXT)')
  db.get("SELECT COUNT(*) as c FROM users", (err,row)=>{
    if(!err && row.c===0){
      const hashed=bcrypt.hashSync('admin123',8)
      db.run("INSERT INTO users (email,password,name) VALUES (?,?,?)",['admin@local',hashed,'Admin'])
    }
  })
})

app.post('/auth/login', (req,res)=>{
  const {email,password}=req.body
  db.get("SELECT * FROM users WHERE email = ?", [email], (err,row)=>{
    if(err || !row) return res.status(401).json({ message: 'Credenciais inválidas' })
    const ok = bcrypt.compareSync(password, row.password)
    if(!ok) return res.status(401).json({ message: 'Credenciais inválidas' })
    const token = jwt.sign({ sub: row.email, id: row.id }, SECRET, { expiresIn: '8h' })
    res.json({ token })
  })
})

app.get('/users', (req,res)=>{ db.all("SELECT id,email,name FROM users", [], (e,rows)=> res.json(rows)) })

const PORT = process.env.PORT || 4000
app.listen(PORT, ()=> console.log('Node backend listening on',PORT))
TS

cat > backend_node/Dockerfile <<'DOCKER'
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm","run","dev"]
DOCKER

# ---------------- BACKEND_PYTHON ----------------
mkdir -p backend_python
cat > backend_python/requirements.txt <<'REQ'
fastapi
uvicorn[standard]
sqlalchemy
passlib[bcrypt]
python-jose
python-dotenv
pydantic
REQ

cat > backend_python/main.py <<'PY'
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
import os

app = FastAPI(title='GTH Python Backend')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

DATABASE_URL = os.getenv('DATABASE_URL','sqlite:///./gth_py.db')
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(bind=engine)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

metadata = MetaData()
users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('email', String, unique=True),
              Column('hashed_password', String),
              Column('name', String)
)
metadata.create_all(engine)
with engine.connect() as conn:
    r = conn.execute(users.select().limit(1)).fetchone()
    if not r:
        hashed = pwd_context.hash('admin123')
        conn.execute(users.insert().values(email='admin@py', hashed_password=hashed, name='AdminPy'))

from pydantic import BaseModel
class LoginIn(BaseModel):
    email: str
    password: str

@app.post('/auth/login')
def login(data: LoginIn):
    with engine.connect() as conn:
        row = conn.execute(users.select().where(users.c.email==data.email)).fetchone()
        if not row or not pwd_context.verify(data.password, row.hashed_password):
            raise HTTPException(status_code=401, detail='Credenciais inválidas')
        return {'access_token': 'pytoken-demo', 'token_type': 'bearer'}
PY

cat > backend_python/Dockerfile <<'DOCKER'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]
DOCKER

# ---------------- docker-compose ----------------
cat > docker-compose.yml <<'YML'
version: '3.8'
services:
  node_backend:
    build: ./backend_node
    ports:
      - "4000:4000"
  python_backend:
    build: ./backend_python
    ports:
      - "8000:8000"
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
YML

echo "Scaffold criado em $ROOT"
echo "Leia o README.md em $ROOT para instruções de execução."
