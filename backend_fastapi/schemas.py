from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class UserOut(BaseModel):
    id: int
    email: str
    name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyOut(BaseModel):
    id: int
    name: str
    cnpj: Optional[str] = None
    area: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class RuleOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class RuleVersionOut(BaseModel):
    id: int
    rule_id: int
    version: str
    content: dict

    model_config = ConfigDict(from_attributes=True)


class TaxRateBase(BaseModel):
    name: str
    tax_type: str
    rate: str
    start_date: datetime
    end_date: Optional[datetime] = None
    is_hybrid: bool = False


class TaxRateIn(TaxRateBase):
    pass


class TaxRateOut(TaxRateBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TaxRegimeBase(BaseModel):
    name: str
    description: Optional[str] = None
    rate_ids: list[int]


class TaxRegimeIn(TaxRegimeBase):
    pass


class TaxRegimeOut(TaxRegimeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
