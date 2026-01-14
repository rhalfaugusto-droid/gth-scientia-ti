from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime
from pydantic import BaseModel

from backend_fastapi.services.xml_parser_service import parse_nfe_xml
from backend_fastapi.services.tax_service import calculate_tax
from backend_fastapi.services.simples_service import simular_simples_nacional
from backend_fastapi.dependencies import get_current_user
from backend_fastapi.database import get_db

router = APIRouter()

# =========================
# Simples Nacional
# =========================

class SimplesRequest(BaseModel):
    faturamento_mensal: float
    anexo: str
    uf: str


@router.post("/simples", summary="Simulação do Simples Nacional")
def simular_simples(payload: SimplesRequest):
    try:
        return simular_simples_nacional(
            faturamento_mensal=payload.faturamento_mensal,
            anexo=payload.anexo,
            uf=payload.uf,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# =========================
# Simulação NFe (IVA Dual)
# =========================

@router.post(
    "/simulate_nfe",
    summary="Simula o cálculo tributário IBS/CBS para uma NFe XML",
)
async def simulate_nfe_tax(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current=Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Recebe um XML de NFe, extrai os dados e simula o cálculo do IVA Dual (CBS/IBS).
    """

    if file.content_type not in ("application/xml", "text/xml"):
        raise HTTPException(
            status_code=400,
            detail="Tipo de arquivo inválido. Esperado application/xml ou text/xml.",
        )

    try:
        xml_content = await file.read()
        xml_str = xml_content.decode("utf-8")

        parsed_data = parse_nfe_xml(xml_str)
        if parsed_data is None:
            raise HTTPException(
                status_code=400,
                detail="Não foi possível analisar o XML como uma NFe válida.",
            )

        operation_value = parsed_data["totais"]["vProd"]

        date_str = parsed_data["data_emissao"][:10]
        operation_date = datetime.strptime(date_str, "%Y-%m-%d")

        tax_regime_name = "REGIME_GERAL_IVA_PLENO"

        simulation_result = calculate_tax(
            db=db,
            operation_value=operation_value,
            tax_regime_name=tax_regime_name,
            operation_date=operation_date,
        )

        return {
            "status": "success",
            "nfe_data": {
                "chave_acesso": parsed_data["chave_acesso"],
                "data_emissao": parsed_data["data_emissao"],
                "valor_total_produtos": operation_value,
                "emitente_uf": parsed_data["emitente"]["UF"],
                "destinatario_uf": parsed_data["destinatario"]["UF"],
            },
            "simulation": simulation_result,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro de conversão de dados: {e}",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno na simulação: {e}",
        )
