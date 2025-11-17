# GTH - MVP Full Deploy (GitHub Actions + Render)

## Overview
Projeto scaffold para MVP da plataforma **Governança Tributária Híbrida**.
- Backend: FastAPI + PostgreSQL + Alembic + JWT + RBAC
- Frontend: React + Vite + Tailwind
- CI/CD: GitHub Actions -> Render (deploy via API)
- Database: Render Managed Postgres (recommended) or Docker Compose for local dev

## Quickstart (local)
1. Copy `.env.example` to `.env` and adjust variables.
2. Run `docker-compose up --build` (services: frontend, backend, db).
3. Backend docs: http://localhost:8000/docs
4. Frontend: http://localhost:5173

## GitHub / Render
1. Push this repo to GitHub.
2. Create a Web Service in Render connected to this repo (use Docker Compose or manual services).
3. Create a Postgres instance in Render (managed DB) and set `DATABASE_URL` in Render's Environment variables.
4. In GitHub repo settings -> Secrets, add:
   - RENDER_API_KEY
   - RENDER_SERVICE_ID
5. On push to `main`, GitHub Actions will trigger deployment to Render.

## Admin credentials (dev seed)
- username: admin
- password: admin123

## Useful commands
- Run migrations: `./make_migrations.sh "message"`
- Run tests: `pytest -v` (backend)
