from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any
import crud
import decimal

# Configura a precisão decimal para cálculos financeiros
decimal.getcontext().prec = 28

def parse_rate(rate_str: str) -> decimal.Decimal:
    """Converte a string de alíquota (ex: '8.8%') para Decimal (ex: 0.088)."""
    if rate_str.endswith('%'):
        return decimal.Decimal(rate_str.strip('%')) / 100
    return decimal.Decimal(rate_str)

def calculate_tax(db: Session, operation_value: float, tax_regime_name: str, operation_date: datetime) -> Dict[str, Any]:
    """
    Calcula os tributos (IBS, CBS, IS, e antigos) para uma operação,
    considerando o regime tributário e a data da operação (transição).
    """
    operation_value_dec = decimal.Decimal(str(operation_value))
    
    # 1. Buscar o regime tributário
    regime = crud.get_tax_regime_by_name(db, tax_regime_name)
    if not regime:
        raise ValueError(f"Regime tributário '{tax_regime_name}' não encontrado.")

    # 2. Buscar as alíquotas aplicáveis
    rate_ids = regime.rate_ids
    tax_rates = {}
    for rate_id in rate_ids:
        rate_obj = crud.get_tax_rate_by_id(db, rate_id)
        if rate_obj and rate_obj.start_date <= operation_date and (rate_obj.end_date is None or rate_obj.end_date >= operation_date):
            tax_rates[rate_obj.tax_type] = {
                'rate_str': rate_obj.rate,
                'rate_dec': parse_rate(rate_obj.rate),
                'is_hybrid': rate_obj.is_hybrid
            }

    if not tax_rates:
        return {
            'total_tax': 0.0,
            'breakdown': {},
            'evidence': {'regime': tax_regime_name, 'message': 'Nenhuma alíquota aplicável encontrada para a data.'}
        }

    # 3. Lógica de Cálculo Híbrido (Foco 2027-2032)
    
    total_tax_dec = decimal.Decimal(0)
    breakdown = {}
    
    # Prioriza o cálculo do IVA Dual (CBS/IBS)
    for tax_type in ['CBS', 'IBS', 'IS']:
        if tax_type in tax_rates:
            rate_info = tax_rates[tax_type]
            tax_amount = operation_value_dec * rate_info['rate_dec']
            total_tax_dec += tax_amount
            breakdown[tax_type] = {
                'rate': rate_info['rate_str'],
                'amount': float(tax_amount.quantize(decimal.Decimal('0.01')))
            }

    # Lógica de transição (ICMS/ISS/PIS/COFINS)
    # Se houver alíquotas híbridas, o cálculo é mais complexo e depende da regra de transição
    # Exemplo: 2029 (10% IBS + 90% ICMS/ISS)
    
    # Para simplificar o MVP, vamos considerar apenas o cálculo direto das alíquotas encontradas.
    # A lógica de "hibridismo" será implementada no motor de regras (engine.py) que chamará este serviço.
    # Por enquanto, este serviço retorna o cálculo simples das alíquotas ativas.
    
    # 4. Retornar o resultado
    return {
        'total_tax': float(total_tax_dec.quantize(decimal.Decimal('0.01'))),
        'breakdown': breakdown,
        'evidence': {'regime': tax_regime_name, 'rates_applied': {k: v['rate_str'] for k, v in tax_rates.items()}}
    }
