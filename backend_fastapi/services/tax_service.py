from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any
from backend_fastapi import crud
import decimal

# Precisão adequada para cálculos financeiros
decimal.getcontext().prec = 28


def parse_rate(rate_str: str) -> decimal.Decimal:
    """
    Converte '8.8%' -> Decimal('0.088')
    ou '0.088' -> Decimal('0.088')
    """
    if rate_str.endswith('%'):
        return decimal.Decimal(rate_str.strip('%')) / decimal.Decimal(100)
    return decimal.Decimal(rate_str)


def calculate_tax(
    db: Session,
    operation_value: float,
    tax_regime_name: str,
    operation_date: datetime
) -> Dict[str, Any]:
    """
    Calcula tributos (CBS, IBS, IS, etc) com base:
    - regime tributário
    - data da operação
    - alíquotas ativas

    Retorna breakdown detalhado + total.
    """

    operation_value_dec = decimal.Decimal(str(operation_value))

    # =========================
    # 1) Regime
    # =========================
    regime = crud.get_tax_regime_by_name(db, tax_regime_name)
    if not regime:
        raise ValueError(f"Regime tributário '{tax_regime_name}' não encontrado.")

    # =========================
    # 2) Alíquotas aplicáveis
    # =========================
    rate_ids = regime.rate_ids or []   # <-- proteção contra None

    tax_rates = {}

    for rate_id in rate_ids:
        rate_obj = crud.get_tax_rate_by_id(db, rate_id)

        if not rate_obj:
            continue

        if (
            rate_obj.start_date <= operation_date
            and (rate_obj.end_date is None or rate_obj.end_date >= operation_date)
        ):
            tax_rates[rate_obj.tax_type] = {
                "rate_str": rate_obj.rate,
                "rate_dec": parse_rate(rate_obj.rate),
                "is_hybrid": rate_obj.is_hybrid,
            }

    # =========================
    # 3) Nenhuma alíquota
    # =========================
    if not tax_rates:
        return {
            "total_tax": 0.0,
            "breakdown": {},
            "evidence": {
                "regime": tax_regime_name,
                "message": "Nenhuma alíquota aplicável encontrada para a data.",
            },
        }

    # =========================
    # 4) Cálculo
    # =========================
    total_tax_dec = decimal.Decimal("0")
    breakdown: Dict[str, Any] = {}

    # ordem lógica do IVA dual
    for tax_type in ["CBS", "IBS", "IS", "ICMS", "ISS", "PIS", "COFINS"]:
        if tax_type not in tax_rates:
            continue

        rate_info = tax_rates[tax_type]

        tax_amount = operation_value_dec * rate_info["rate_dec"]
        tax_amount = tax_amount.quantize(decimal.Decimal("0.01"))

        total_tax_dec += tax_amount

        breakdown[tax_type] = {
            "rate": rate_info["rate_str"],
            "amount": float(tax_amount),
        }

    # =========================
    # 5) Resultado
    # =========================
    total_tax_dec = total_tax_dec.quantize(decimal.Decimal("0.01"))

    return {
        "total_tax": float(total_tax_dec),
        "breakdown": breakdown,
        "evidence": {
            "regime": tax_regime_name,
            "rates_applied": {k: v["rate_str"] for k, v in tax_rates.items()},
        },
    }
