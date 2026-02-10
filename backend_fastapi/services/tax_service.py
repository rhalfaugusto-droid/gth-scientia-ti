from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any
from decimal import Decimal, getcontext, ROUND_HALF_UP

from backend_fastapi import crud

# precisão alta p/ financeiro
getcontext().prec = 28


CENT = Decimal("0.01")

TAX_ORDER = ["CBS", "IBS", "IS", "ICMS", "ISS", "PIS", "COFINS"]


def parse_rate(rate_str: str) -> Decimal:
    """
    "8.8%" -> Decimal('0.088')
    "0.088" -> Decimal('0.088')
    """
    rate_str = rate_str.strip()

    if rate_str.endswith("%"):
        return (Decimal(rate_str[:-1]) / Decimal("
