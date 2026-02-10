from fastapi import APIRouter, Depends
from pydantic import BaseModel

from backend_fastapi.services.ai_service import gerar_resposta
from backend_fastapi.dependencies import get_current_user


router = APIRouter(prefix="/ia", tags=["IA"])


# =============================
# SCHEMAS
# =============================
class ChatIn(BaseModel):
    mensagem: str


class ChatOut(BaseModel):
    resposta: str


# =============================
# ROUTE
# =============================
@router.post("/chat", response_model=ChatOut)
def chat(
    data: ChatIn,
    current=Depends(get_current_user),  # 🔐 protege endpoint
):
    resposta = gerar_resposta(data.mensagem)
    return {"resposta": resposta}
