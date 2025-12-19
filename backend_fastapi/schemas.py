from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserOut(BaseModel):
    id: int
    email: str
    name: Optional[str] = None

    class Config:
        from_attributes = True

class CompanyOut(BaseModel):
    id: int
    name: str
    cnpj: Optional[str] = None
    area: Optional[str] = None
    class Config:
        from_attributes = True

class RuleOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    class Config:
        from_attributes = True

class RuleVersionOut(BaseModel):
    id: int
    rule_id: int
    version: str
    content: dict
    class Config:
        from_attributes = True

from datetime import datetime

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
    class Config:
        from_attributes = True

class TaxRegimeBase(BaseModel):
    name: str
    description: Optional[str] = None
    rate_ids: list[int]

class TaxRegimeIn(TaxRegimeBase):
    pass

class TaxRegimeOut(TaxRegimeBase):
    id: int
    class Config:
        from_attributes = True

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}
