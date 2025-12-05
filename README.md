
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
