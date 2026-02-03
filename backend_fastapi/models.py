from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
import datetime

from backend_fastapi.database import Base   # ⭐ ESSA LINHA É A CHAVE

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cnpj = Column(String, nullable=True)
    area = Column(String, nullable=True)

class Rule(Base):
    __tablename__ = 'rules'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

class RuleVersion(Base):
    __tablename__ = 'rule_versions'
    id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(Integer, ForeignKey('rules.id'))
    version = Column(String, nullable=False)
    content = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    rule = relationship('Rule', backref='versions')

class TaxRate(Base):
    __tablename__ = 'tax_rates'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) # Ex: CBS_PADRAO, IBS_REDUZIDO_60, IS_CIGARRO
    tax_type = Column(String, nullable=False) # Ex: CBS, IBS, IS, ICMS, PIS, COFINS
    rate = Column(String, nullable=False) # Alíquota em string (ex: '8.8%', '17.7%', '0.1%')
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    is_hybrid = Column(Boolean, default=False) # Se é uma alíquota de transição (ex: 10% IBS + 90% ICMS)

class TaxRegime(Base):
    __tablename__ = 'tax_regimes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) # Ex: REGIME_GERAL, REGIME_SERVICOS_PROFISSIONAIS, REGIME_CONSTRUCAO_CIVIL
    description = Column(Text, nullable=True)
    rate_ids = Column(JSON, nullable=True) # Lista de IDs de TaxRate aplicáveis a este regime

class Workflow(Base):
    __tablename__ = 'workflows'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_email = Column(String, nullable=True)
    data = Column(JSON, nullable=True)  # armazena o fluxo (blocos + conexões) em JSON
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

