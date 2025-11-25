ICMS_RATES = {
    'SP': 18.0,
    'RJ': 18.0,
    'MG': 18.0,
    'BA': 17.0,
    'PR': 18.0,
    'SC': 17.0,
    'RS': 18.0,
    'DEFAULT': 18.0
}

def calc_icms(state: str, product_value: float, icms_base_percent: float = 100.0):
    rate = ICMS_RATES.get(state.upper(), ICMS_RATES['DEFAULT'])
    base = product_value * (icms_base_percent/100.0)
    icms = round(base * (rate/100.0), 2)
    return {'state': state, 'rate': rate, 'base': round(base,2), 'icms': icms}
