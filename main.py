from fastapi import FastAPI
from routers import auth, users, ai

app = FastAPI(title="GTH Scientia TI")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"status": "online", "message": "API conectada com sucesso!"}
