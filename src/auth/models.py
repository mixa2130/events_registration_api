from datetime import datetime

import fastapi_users_db_sqlalchemy
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.sql import sqltypes as sa_types
from sqlalchemy import schema as sa

from src.config import POSTGRES_INDEXES_NAMING_CONVENTION


metadata = sa.MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION, schema='events')
Base: DeclarativeMeta = declarative_base(metadata=metadata)

RoleTbl = sa.Table(
    'role',
    metadata,
    sa.Column('id', sa_types.Integer, autoincrement=True, primary_key=True, index=True),
    sa.Column('name', sa_types.String(length=35), unique=True, nullable=False),
)


class User(SQLAlchemyBaseUserTableUUID, Base):
    # Other attributes will be added from base class
    __tablename__ = "user"

    registered_at = sa.Column(sa_types.TIMESTAMP, default=datetime.utcnow)
    role_id = sa.Column(sa_types.Integer, sa.ForeignKey(RoleTbl.c.id))
