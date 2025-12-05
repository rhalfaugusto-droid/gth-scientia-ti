from fastapi import APIRouter
from services.ai_service import gerar_resposta

router = APIRouter(prefix="/ia", tags=["IA"])

@router.post("/chat")
def chat(prompt: dict):
    texto = prompt["mensagem"]
    resposta = gerar_resposta(texto)
    return {"resposta": resposta}
