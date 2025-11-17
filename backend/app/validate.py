from typing import Dict, Any
from . import rules

def validate_nfe(parsed: Dict[str, Any]) -> Dict:
    issues = []
    totals = parsed.get('totals', {})
    items = parsed.get('items', [])
    try:
        sum_items = sum(float(i.get('vProd') or 0) for i in items)
        vnf = float(totals.get('vNF') or 0 or 0)
        if abs(sum_items - vnf) > 0.5:
            issues.append({'code':'SUM_MISMATCH', 'message': f'Soma dos itens ({sum_items}) difere de vNF ({vnf})'})
    except Exception as e:
        issues.append({'code':'SUM_ERROR', 'message': str(e)})
    for it in items:
        cfop = (it.get('CFOP') or '').strip()
        if cfop and len(cfop) != 4:
            issues.append({'code':'CFOP_INVALID', 'message': f'CFOP inválido para item {it.get("cProd")}: {cfop}'})
    if items:
        first = items[0]
        prod_value = float(first.get('vProd') or 0)
        state = parsed.get('emit_state') or 'DEFAULT'
        icms_calc = rules.calc_icms(state, prod_value)
    else:
        icms_calc = {}
    return {'issues': issues, 'icms_example': icms_calc}
