from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_users():
    return [{"id": 1, "nome": "Admin"}]
