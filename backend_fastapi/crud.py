from sqlalchemy.orm import Session
from backend_fastapi import models
import datetime
from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =========================
# USERS
# =========================

def create_user(db: Session, email: str, password: str, name: str = ""):
    hashed = pwd.hash(password)
    u = models.User(email=email, hashed_password=hashed, name=name)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session):
    return db.query(models.User).all()


# =========================
# COMPANY
# =========================

def create_company(db: Session, name: str, cnpj: str | None = None, area: str | None = None):
    c = models.Company(name=name, cnpj=cnpj, area=area)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


# =========================
# RULES
# =========================

def create_rule(db: Session, name: str, description: str = ""):
    r = models.Rule(name=name, description=description)
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


def create_rule_version(db: Session, rule_id: int, version: str, content: dict):
    rv = models.RuleVersion(rule_id=rule_id, version=version, content=content)
    db.add(rv)
    db.commit()
    db.refresh(rv)
    return rv


def get_rule_version(db: Session, rv_id: int):
    return db.query(models.RuleVersion).filter(models.RuleVersion.id == rv_id).first()


# =========================
# WORKFLOWS
# =========================

def create_workflow(db: Session, name: str, owner_email: str | None, data: dict):
    w = models.Workflow(name=name, owner_email=owner_email, data=data)
    db.add(w)
    db.commit()
    db.refresh(w)
    return w


def get_workflows_by_owner(db: Session, owner_email: str):
    return db.query(models.Workflow).filter(models.Workflow.owner_email == owner_email).all()


def get_workflow(db: Session, wf_id: int):
    return db.query(models.Workflow).filter(models.Workflow.id == wf_id).first()


def update_workflow(db: Session, wf_id: int, data: dict, name: str | None = None):
    w = get_workflow(db, wf_id)
    if not w:
        return None

    w.data = data
    if name:
        w.name = name

    db.commit()
    db.refresh(w)
    return w


# =========================
# TAX RATE
# =========================

def create_tax_rate(
    db: Session,
    name: str,
    tax_type: str,
    rate: str,
    start_date: datetime.datetime,
    end_date: datetime.datetime | None = None,
    is_hybrid: bool = False,
):
    tr = models.TaxRate(
        name=name,
        tax_type=tax_type,
        rate=rate,
        start_date=start_date,
        end_date=end_date,
        is_hybrid=is_hybrid,
    )
    db.add(tr)
    db.commit()
    db.refresh(tr)
    return tr


def get_tax_rate_by_name(db: Session, name: str):
    return db.query(models.TaxRate).filter(models.TaxRate.name == name).first()


def get_tax_rate_by_id(db: Session, tr_id: int):
    return db.query(models.TaxRate).filter(models.TaxRate.id == tr_id).first()


# =========================
# TAX REGIME
# =========================

def create_tax_regime(db: Session, name: str, description: str, rate_ids: list[int]):
    tr = models.TaxRegime(name=name, description=description, rate_ids=rate_ids)
    db.add(tr)
    db.commit()
    db.refresh(tr)
    return tr


def get_tax_regime_by_name(db: Session, name: str):
    return db.query(models.TaxRegime).filter(models.TaxRegime.name == name).first()


def get_tax_regime_by_id(db: Session, tr_id: int):
    return db.query(models.TaxRegime).filter(models.TaxRegime.id == tr_id).first()
