from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal

router = APIRouter(tags=["Simulação Tributária"])

# ======================================================
# MODELO DE ENTRADA (MVP)
# ======================================================

class SimplesInput(BaseModel):
    faturamento_mensal: float
    anexo: Literal["I", "II", "III", "IV", "V"]
    uf: str

# ======================================================
# ENDPOINT MVP — SIMPLES NACIONAL
# ======================================================

@router.post("/simples", summary="Simulação tributária Simples Nacional (MVP)")
def simular_simples(data: SimplesInput):
    """
    MVP tributário:
    - NÃO usa XML
    - NÃO consulta SEFAZ
    - NÃO substitui contador
    """

    if data.faturamento_mensal <= 0:
        raise HTTPException(status_code=400, detail="Faturamento inválido")

    # Regra simplificada (exemplo realista)
    aliquotas = {
        "I": 0.06,
        "II": 0.112,
        "III": 0.135,
        "IV": 0.165,
        "V": 0.19,
    }

    aliquota = aliquotas[data.anexo]
    das_estimado = data.faturamento_mensal * aliquota

    return {
        "regime": "Simples Nacional",
        "anexo": data.anexo,
        "uf": data.uf,
        "faturamento_mensal": data.faturamento_mensal,
        "aliquota_estimada": aliquota,
        "das_estimado": round(das_estimado, 2),
        "observacao": "Simulação estimada. Não substitui apuração contábil oficial."
    }
