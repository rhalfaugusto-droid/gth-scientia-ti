from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend_fastapi.services.xml_parser_service import parse_nfe_xml
from backend_fastapi.services.tax_service import calculate_tax
from backend_fastapi.dependencies import get_current_user
from backend_fastapi import database, crud, schemas

router = APIRouter()

@router.post('/seed_tax_rates', summary="Popula o banco de dados com as alíquotas iniciais da Reforma Tributária")
def seed_tax_rates(db: Session = Depends(database.get_db)):
    # Data de referência para o início da transição
    date_2027 = datetime(2027, 1, 1)
    date_2026 = datetime(2026, 1, 1)
    date_2029 = datetime(2029, 1, 1)
    date_2033 = datetime(2033, 1, 1)

    rates_to_seed = [
        # Alíquotas de Referência (Estimadas)
        {'name': 'CBS_PADRAO', 'tax_type': 'CBS', 'rate': '8.8%', 'start_date': date_2027, 'end_date': date_2033, 'is_hybrid': False},
        {'name': 'IBS_PADRAO', 'tax_type': 'IBS', 'rate': '17.7%', 'start_date': date_2033, 'end_date': None, 'is_hybrid': False},
        
        # Alíquotas de Teste (2026)
        {'name': 'CBS_TESTE_2026', 'tax_type': 'CBS', 'rate': '0.9%', 'start_date': date_2026, 'end_date': datetime(2026, 12, 31), 'is_hybrid': False},
        {'name': 'IBS_TESTE_2026', 'tax_type': 'IBS', 'rate': '0.1%', 'start_date': date_2026, 'end_date': datetime(2026, 12, 31), 'is_hybrid': False},
        
        # Alíquotas de Transição (2027-2028)
        {'name': 'CBS_TRANSICAO_2027', 'tax_type': 'CBS', 'rate': '8.7%', 'start_date': date_2027, 'end_date': datetime(2028, 12, 31), 'is_hybrid': False}, # 99.9% da alíquota final - 0.1%
        {'name': 'IBS_TRANSICAO_2027', 'tax_type': 'IBS', 'rate': '0.1%', 'start_date': date_2027, 'end_date': datetime(2028, 12, 31), 'is_hybrid': False},
        
        # Alíquotas de Transição Híbrida (2029) - Exemplo
        {'name': 'IBS_HIBRIDO_2029', 'tax_type': 'IBS', 'rate': '10%', 'start_date': date_2029, 'end_date': datetime(2029, 12, 31), 'is_hybrid': True},
        {'name': 'ICMS_HIBRIDO_2029', 'tax_type': 'ICMS', 'rate': '90%', 'start_date': date_2029, 'end_date': datetime(2029, 12, 31), 'is_hybrid': True},
        {'name': 'ISS_HIBRIDO_2029', 'tax_type': 'ISS', 'rate': '90%', 'start_date': date_2029, 'end_date': datetime(2029, 12, 31), 'is_hybrid': True},
        
        # Alíquotas Reduzidas (Exemplo: Saúde - 60% de redução)
        {'name': 'CBS_SAUDE_60', 'tax_type': 'CBS', 'rate': '3.52%', 'start_date': date_2027, 'end_date': None, 'is_hybrid': False}, # 8.8% * 40%
        {'name': 'IBS_SAUDE_60', 'tax_type': 'IBS', 'rate': '7.08%', 'start_date': date_2033, 'end_date': None, 'is_hybrid': False}, # 17.7% * 40%
    ]

    created_rates = []
    for rate_data in rates_to_seed:
        existing_rate = crud.get_tax_rate_by_name(db, rate_data['name'])
        if not existing_rate:
            rate = crud.create_tax_rate(db, **rate_data)
            created_rates.append(schemas.TaxRateOut.from_orm(rate))
    
    return {'message': f'Seeded {len(created_rates)} new tax rates.', 'rates': created_rates}

@router.post('/seed_tax_regimes', summary="Popula o banco de dados com os regimes tributários iniciais")
def seed_tax_regimes(db: Session = Depends(database.get_db)):
    
    # Busca as alíquotas criadas
    cbs_padrao = crud.get_tax_rate_by_name(db, 'CBS_PADRAO')
    ibs_padrao = crud.get_tax_rate_by_name(db, 'IBS_PADRAO')
    cbs_saude = crud.get_tax_rate_by_name(db, 'CBS_SAUDE_60')
    ibs_saude = crud.get_tax_rate_by_name(db, 'IBS_SAUDE_60')
    
    if not all([cbs_padrao, ibs_padrao, cbs_saude, ibs_saude]):
        raise HTTPException(status_code=400, detail="Execute /seed_tax_rates primeiro para criar as alíquotas necessárias.")

    regimes_to_seed = [
        {
            'name': 'REGIME_GERAL_IVA_PLENO',
            'description': 'Regime geral de tributação com alíquotas padrão de CBS e IBS (a partir de 2033).',
            'rate_ids': [cbs_padrao.id, ibs_padrao.id]
        },
        {
            'name': 'REGIME_SAUDE_60',
            'description': 'Regime com redução de 60% na alíquota para serviços de saúde (a partir de 2027/2033).',
            'rate_ids': [cbs_saude.id, ibs_saude.id]
        }
        # Adicionar mais regimes (ex: transição, serviços profissionais, etc.)
    ]

    created_regimes = []
    for regime_data in regimes_to_seed:
        existing_regime = crud.get_tax_regime_by_name(db, regime_data['name'])
        if not existing_regime:
            regime = crud.create_tax_regime(db, **regime_data)
            created_regimes.append(schemas.TaxRegimeOut.from_orm(regime))
            
    return {'message': f'Seeded {len(created_regimes)} new tax regimes.', 'regimes': created_regimes}
