from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from typing import Dict, Any
from ..services.xml_parser_service import parse_nfe_xml
from dependencies import get_current_user

router = APIRouter()

@router.post('/nfe', summary="Processa um arquivo XML de NFe e extrai dados fiscais")
async def process_nfe_xml_file(file: UploadFile = File(...), current = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Recebe um arquivo XML de NFe, faz o parsing e retorna os dados fiscais estruturados.
    """
    if file.content_type != 'application/xml' and file.content_type != 'text/xml':
        raise HTTPException(status_code=400, detail="Tipo de arquivo inválido. Esperado application/xml ou text/xml.")
    
    try:
        xml_content = await file.read()
        
        # Tenta decodificar o conteúdo, assumindo UTF-8 como padrão
        try:
            xml_str = xml_content.decode('utf-8')
        except UnicodeDecodeError:
            # Tenta ISO-8859-1 se UTF-8 falhar
            xml_str = xml_content.decode('iso-8859-1')
            
        parsed_data = parse_nfe_xml(xml_str)
        
        if parsed_data is None:
            raise HTTPException(status_code=400, detail="Não foi possível analisar o XML como uma NFe válida.")
            
        return {'status': 'success', 'data': parsed_data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar o XML: {e}")
