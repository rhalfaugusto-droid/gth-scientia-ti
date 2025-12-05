from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login")
def login(data: dict):
    return {"message": "Login realizado", "data": data}
