import os
from databases import Database
from sqlalchemy import (MetaData, Table, Column, Integer, String, Text, JSON, ForeignKey, Boolean, create_engine)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/gth')
database = Database(DATABASE_URL)
metadata = MetaData()

tenants = Table(
    'tenants', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, unique=True, nullable=False)
)

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('tenant_id', Integer, ForeignKey('tenants.id')),
    Column('username', String, unique=True, nullable=False),
    Column('password_hash', String, nullable=False),
    Column('is_admin', Boolean, default=False)
)

flows = Table(
    'flows', metadata,
    Column('id', Integer, primary_key=True),
    Column('tenant_id', Integer, ForeignKey('tenants.id')),
    Column('name', String, nullable=False),
    Column('data', JSON, nullable=False)
)

# sync engine for alembic / migrations convenience
engine = create_engine(DATABASE_URL.replace('+asyncpg',''), echo=False)
