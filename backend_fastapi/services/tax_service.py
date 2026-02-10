from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any
from decimal import Decimal, getcontext, ROUND_HALF_UP

from backend_fastapi import crud


# precisão alta p/ cálculos financeiros
getcontext().prec = 28

CENT = Decimal("0.01")

TAX_ORDER = ["CBS", "IBS", "IS", "ICMS", "ISS", "PIS", "COFINS"]


def parse_rate(rate_str: str) -> Decimal:
    """
    Converte:
    "8.8%" -> Decimal('0.088')
    "0.088" -> Decimal('0.088')
    """
    rate_str = rate_str.strip()

    if rate_str.endswith("%"):
        return Decimal(rate_str[:-1]) / Decimal("100")

    return Decimal(rate_str)


def calculate_tax(
    db: Session,
    operation_value: float,
    tax_regime_name: str,
    operation_date: datetime,
) -> Dict[str, Any]:

    operation_value_dec = Decimal(str(operation_value))

    regime = crud.get_tax_regime_by_name(db, tax_regime_name)
    if not regime:
        raise ValueError(f"Regime tributário '{tax_regime_name}' não encontrado.")

    rate_ids = regime.rate_ids or []

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
            }

    if not tax_rates:
        return {
            "total_tax": 0.0,
            "breakdown": {},
            "evidence": {
                "regime": tax_regime_name,
                "message": "Nenhuma alíquota aplicável encontrada.",
            },
        }

    total_tax = Decimal("0")
    breakdown: Dict[str, Any] = {}

    for tax_type in TAX_ORDER:
        if tax_type not in tax_rates:
            continue

        rate_info = tax_rates[tax_type]

        tax_amount = (operation_value_dec * rate_info["rate_dec"]).quantize(
            CENT, rounding=ROUND_HALF_UP
        )

        total_tax += tax_amount

        breakdown[tax_type] = {
            "rate": rate_info["rate_str"],
            "amount": float(tax_amount),
        }

    total_tax = total_tax.quantize(CENT, rounding=ROUND_HALF_UP)

    return {
        "total_tax": float(total_tax),
        "breakdown": breakdown,
        "evidence": {
            "regime": tax_regime_name,
            "rates_applied": {k: v["rate_str"] for k, v in tax_rates.items()},
        },
    }
