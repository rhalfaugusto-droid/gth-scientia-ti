from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime
from backend_fastapi.services.xml_parser_service import parse_nfe_xml
from backend_fastapi.services.tax_service import calculate_tax
from backend_fastapi.dependencies import get_current_user
from backend_fastapi import database

router = APIRouter()

@router.get("/")
def health():
    return {"status": "tax_simulation ok"}

@router.post('/simulate_nfe', summary="Simula o cálculo tributário IBS/CBS para uma NFe XML")
async def simulate_nfe_tax(file: UploadFile = File(...), db: Session = Depends(database.get_db), current = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Recebe um XML de NFe, extrai os dados e simula o cálculo do IVA Dual (CBS/IBS)
    com base nos regimes tributários cadastrados.
    """
    if file.content_type not in ['application/xml', 'text/xml']:
        raise HTTPException(status_code=400, detail="Tipo de arquivo inválido. Esperado application/xml ou text/xml.")
    
    try:
        xml_content = await file.read()
        xml_str = xml_content.decode('utf-8')
        parsed_data = parse_nfe_xml(xml_str)
        
        if parsed_data is None:
            raise HTTPException(status_code=400, detail="Não foi possível analisar o XML como uma NFe válida.")
        
        # 1. Extrair o valor total da operação (vProd ou vNF)
        operation_value = parsed_data['totais']['vProd'] # Usando valor dos produtos como base
        
        # 2. Extrair a data da operação
        # Simplificação: assume que a data de emissão é a data da operação
        # O formato da data pode variar (ex: 'AAAA-MM-DDThh:mm:ss-03:00' ou 'AAAA-MM-DD')
        date_str = parsed_data['data_emissao'][:10] # Pega apenas a parte da data
        operation_date = datetime.strptime(date_str, '%Y-%m-%d')
        
        # 3. Simular o cálculo para um regime padrão (Ex: REGIME_GERAL_IVA_PLENO)
        # Em um sistema real, o regime seria determinado pelo NCM, CST, ou CNAE da empresa.
        tax_regime_name = 'REGIME_GERAL_IVA_PLENO' 
        
        # O cálculo será feito sobre o valor total da operação
        simulation_result = calculate_tax(
            db,
            operation_value,
            tax_regime_name,
            operation_date
        )
        
        # 4. Consolidar o resultado
        return {
            'status': 'success',
            'nfe_data': {
                'chave_acesso': parsed_data['chave_acesso'],
                'data_emissao': parsed_data['data_emissao'],
                'valor_total_produtos': operation_value,
                'emitente_uf': parsed_data['emitente']['UF'],
                'destinatario_uf': parsed_data['destinatario']['UF'],
            },
            'simulation': simulation_result
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Erro de conversão de dados: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno na simulação: {e}")
