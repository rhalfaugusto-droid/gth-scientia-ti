
# Plataforma de Governança Tributária Híbrida — Starter (Option D)

Este repositório é um *starter full* para acelerar o desenvolvimento e deploy no GitHub + Render.

**O que inclui**
- Frontend: React + Vite + TypeScript (SPA)
- Backend: Node.js + Express + TypeScript (API)
- Dockerfiles (frontend & backend)
- SQL migrations (Postgres)
- OpenAPI spec (openapi.yaml)
- GitHub Actions CI (build & tests)
- render.yaml (serviços para Render)
- Documentação básica: SECURITY.md, DEVOPS.md, BACKLOG.md

> Observação: este é um scaffold inicial. Funcionalidades fiscais (rules engine, parser XML, IA) estão esboçadas como stubs e precisam implementação.

## Como usar localmente (dev)
1. Instale Node.js (v18+) e Docker.
2. Crie arquivo `.env` na raiz com:
   ```
   DATABASE_URL=postgres://postgres:postgres@localhost:5432/tributario
   JWT_SECRET=uma-chave-secreta
   ```
3. Para rodar backend em dev:
   ```
   cd backend
   npm install
   npm run dev
   ```
4. Para rodar frontend em dev:
   ```
   cd frontend
   npm install
   npm run dev
   ```

## Deploy no Render (resumo)
1. Crie repositório no GitHub e suba estes arquivos.
2. Conecte o repo no Render.
3. Na UI do Render, crie um **Managed Postgres** (ou use o serviço do render.yaml).
4. Crie Web Service (backend) apontando para backend/Dockerfile e Static Site (frontend) apontando para frontend/Dockerfile ou usar build command.
5. Configure variáveis de ambiente no Render (DATABASE_URL, JWT_SECRET, OPENAI_KEY...).

Mais detalhes no SECURITY.md e DEVOPS.md.
# gth-scientia-ti

# gth-scientia-ti
Plataforma de Governança Tributária Híbrida pra a transição ao novo modelo do IBS e CBS (2026–2033).




GTH Scientia TI - FastAPI backend scaffold (POC)
------------------------------------------------

This scaffold provides a minimal FastAPI backend with:
- JWT authentication (register/login)
- SQLite dev database with SQLAlchemy
- User and Company models
- Rules and RuleVersion endpoints (skeleton)
- A very small Rule Engine POC: evaluates simple JSON 'formula' using a safe eval approach
- Seeded admin user: email `admin@local`, password `admin123`

How to run (local dev)
----------------------
1. Create a virtual environment and activate it:
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # Windows CMD:
   .venv\Scripts\activate.bat
   # macOS / Linux:
   source .venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Run the app:
   uvicorn main:app --reload --port 8000

4. Open docs:
   http://localhost:8000/docs

Notes
-----
- This is a POC scaffold: extend models, add migrations, and secure secrets before production.
- The rule engine is intentionally simple for POC. For production, consider a DSL or sandboxed evaluator.

