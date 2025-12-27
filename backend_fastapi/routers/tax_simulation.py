from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from typing import Dict, Any
from datetime import datetime

# === IMPORTS DO MVP (SIMPLIFICADO) ===
from services.tax_engine import SimplesNacionalEngine, TaxInput

# === IMPORTS AVANÇADOS (XML / FUTURO) ===
from sqlalchemy.orm import Session
from services.xml_parser_service import parse_nfe_xml
from services.tax_service import calculate_tax
from dependencies import get_current_user
import database

router = APIRouter(prefix="/simulation", tags=["Simulação Tributária"])

# ==========================================================
# MVP — SIMULAÇÃO SIMPLES NACIONAL (USAR AGORA)
# ==========================================================

engine = SimplesNacionalEngine()

@router.post(
    "/simples",
    summary="Simula tributação pelo Simples Nacional (MVP)",
    description="Calcula Anexo, Fator R, alíquota efetiva e DAS estimado"
)
def simular_simples(data: TaxInput):
    """
    Endpoint MVP — NÃO usa XML, NÃO usa banco, NÃO exige autenticação.
    Ideal para frontend, IA e venda do produto.
    """
    try:
        return engine.calcular(data)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro na simulação do Simples Nacional: {str(e)}"
        )


# ==========================================================
# EXPERIMENTAL — SIMULAÇÃO VIA XML (DESATIVADO NO MVP)
# ==========================================================
# ⚠ Este endpoint é avançado e NÃO deve ser usado no MVP inicial
# ⚠ Mantido apenas para evolução futura do produto

@router.post(
    "/simulate_nfe",
    summary="(Experimental) Simula cálculo tributário via XML de NFe",
    include_in_schema=False  # Oculta do Swagger por enquanto
)
async def simulate_nfe_tax(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current = Depends(get_current_user)
) -> Dict[str, Any]:

    if file.content_type not in ['application/xml', 'text/xml']:
        raise HTTPException(
            status_code=400,
            detail="Tipo de arquivo inválido. Envie um XML de NFe."
        )

    try:
        xml_content = await file.read()
        xml_str = xml_content.decode('utf-8')

        parsed_data = parse_nfe_xml(xml_str)
        if not parsed_data:
            raise HTTPException(
                status_code=400,
                detail="XML inválido ou não reconhecido como NFe."
            )

        operation_value = parsed_data['totais']['vProd']
        date_str = parsed_data['data_emissao'][:10]
        operation_date = datetime.strptime(date_str, '%Y-%m-%d')

        tax_regime_name = 'REGIME_GERAL_IVA_PLENO'

        simulation_result = calculate_tax(
            db=db,
            base_value=operation_value,
            regime_name=tax_regime_name,
            operation_date=operation_date
        )

        return {
            "status": "success",
            "nfe": {
                "chave_acesso": parsed_data['chave_acesso'],
                "data_emissao": parsed_data['data_emissao'],
                "valor_total": operation_value,
                "emitente_uf": parsed_data['emitente']['UF'],
                "destinatario_uf": parsed_data['destinatario']['UF'],
            },
            "simulation": simulation_result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno na simulação via XML: {str(e)}"
        )
