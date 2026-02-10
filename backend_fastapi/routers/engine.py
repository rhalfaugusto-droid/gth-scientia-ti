from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any
import ast
import operator as op

from backend_fastapi import database, crud
from backend_fastapi.dependencies import get_current_user
from backend_fastapi.services.tax_service import calculate_tax
from backend_fastapi.services.xml_parser_service import parse_nfe_xml


router = APIRouter()


# =========================
# MODELOS
# =========================

class EngineIn(BaseModel):
    rule_version_id: int
    input_data: Dict[str, Any]


class EngineOut(BaseModel):
    result: Dict[str, Any]
    evidence: Dict[str, Any]


class TaxCalculationIn(BaseModel):
    operation_value: float
    tax_regime_name: str
    operation_date: datetime = Field(default_factory=datetime.utcnow)


class TaxCalculationOut(BaseModel):
    total_tax: float
    breakdown: Dict[str, Any]
    evidence: Dict[str, Any]


# =========================
# EXPRESSÃO SEGURA
# =========================

SAFE_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def eval_expr(expr: str, names: Dict[str, Any]):
    node = ast.parse(expr, mode="eval").body

    def _eval(n):
        if isinstance(n, ast.Constant):
            return n.value

        if isinstance(n, ast.Name):
            return names.get(n.id, 0)

        if isinstance(n, ast.BinOp):
            operator_fn = SAFE_OPERATORS.get(type(n.op))
            if not operator_fn:
                raise ValueError("Operador não permitido")
            return operator_fn(_eval(n.left), _eval(n.right))

        if isinstance(n, ast.UnaryOp):
            operator_fn = SAFE_OPERATORS.get(type(n.op))
            if not operator_fn:
                raise ValueError("Operador não permitido")
            return operator_fn(_eval(n.operand))

        raise ValueError(f"Expressão não suportada: {type(n).__name__}")

    return _eval(node)


# =========================
# ROTAS
# =========================

@router.post("/run", response_model=EngineOut)
def run_engine(
    payload: EngineIn,
    db: Session = Depends(database.get_db),
    current=Depends(get_current_user),
):
    rv = crud.get_rule_version(db, payload.rule_version_id)

    if not rv:
        raise HTTPException(status_code=404, detail="Rule version not found")

    expr = rv.content.get("expr") if isinstance(rv.content, dict) else None
    if not expr:
        raise HTTPException(
            status_code=400,
            detail="No expression in rule version content",
        )

    try:
        result = eval_expr(expr, payload.input_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=400, detail="Evaluation error")

    evidence = {
        "expr": expr,
        "input": payload.input_data,
        "output": result,
    }

    return {
        "result": {"value": result},
        "evidence": evidence,
    }


@router.post("/calculate_tax", response_model=TaxCalculationOut)
def calculate_tax_endpoint(
    payload: TaxCalculationIn,
    db: Session = Depends(database.get_db),
    current=Depends(get_current_user),
):
    try:
        return calculate_tax(
            db,
            payload.operation_value,
            payload.tax_regime_name,
            payload.operation_date,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno no cálculo tributário: {e}",
        )
