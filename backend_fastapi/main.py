from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend_fastapi.routers import (
    auth,
    users,
    companies,
    rules,
    engine,
    admin,
    xml_parser,
    tax_simulation,
)

app = FastAPI(title="GTH FastAPI Backend POC")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/v1/users", tags=["users"])
app.include_router(companies.router, prefix="/v1/companies", tags=["companies"])
app.include_router(rules.router, prefix="/v1/rules", tags=["rules"])
app.include_router(engine.router, prefix="/v1/engine", tags=["engine"])
app.include_router(admin.router, prefix="/v1/admin", tags=["admin"])
app.include_router(xml_parser.router, prefix="/v1/parser", tags=["parser"])
app.include_router(tax_simulation.router, prefix="/v1/simulation", tags=["simulation"])



@app.get("/")
def root():
    return {"msg": "GTH FastAPI Backend POC"}
