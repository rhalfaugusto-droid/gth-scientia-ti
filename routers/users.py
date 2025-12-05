from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Usuários"])

@router.get("/")
def list_users():
    return [{"id": 1, "nome": "Admin"}]
