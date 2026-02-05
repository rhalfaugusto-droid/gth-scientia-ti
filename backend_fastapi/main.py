from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend_fastapi.database import engine, Base
from backend_fastapi import models


# =============================
# LIFESPAN (startup/shutdown moderno)
# =============================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # cria tabelas apenas 1x no boot
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="GTH FastAPI Backend POC",
    lifespan=lifespan
)


# =============================
# CORS (produção segura)
# =============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://gth-scientia-ti.onrender.com",
        "http://localhost:3000",  # dev local opcional
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================
# ROUTERS
# =============================
from backend_fastapi.routers.auth import router as auth_router
from backend_fastapi.routers.users import router as users_router
from backend_fastapi.routers.companies import router as companies_router
from backend_fastapi.routers.rules import router as rules_router
from backend_fastapi.routers.engine import router as engine_router
from backend_fastapi.routers.admin import router as admin_router
from backend_fastapi.routers.xml_parser import router as parser_router
from backend_fastapi.routers.tax_simulation import router as simulation_router
from backend_fastapi.routers.workflows import router as workflows_router

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(companies_router, prefix="/companies", tags=["companies"])
app.include_router(rules_router, prefix="/rules", tags=["rules"])
app.include_router(engine_router, prefix="/engine", tags=["engine"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(parser_router, prefix="/parser", tags=["parser"])
app.include_router(simulation_router, prefix="/simulation", tags=["simulation"])
app.include_router(workflows_router, prefix="/workflows", tags=["workflows"])


# =============================
# ROOT
# =============================
@app.get("/")
def root():
    return {"msg": "GTH FastAPI Backend online"}


# =============================
# HEALTHCHECK (Render friendly)
# =============================
@app.get("/health")
def health():
    return {"status": "ok"}
