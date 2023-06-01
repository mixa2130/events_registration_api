from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.sql import sqltypes as sa_types
from sqlalchemy import schema as sa

# from src.config import POSTGRES_INDEXES_NAMING_CONVENTION
from src.context import APP_CTX

#
# metadata = sa.MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION, schema=APP_CTX.PG_SCHEMA)
# Base: DeclarativeMeta = declarative_base(metadata=metadata)

RoleTbl = sa.Table(
    'role',
    APP_CTX.sa_metadata,
    sa.Column('id', sa_types.Integer, autoincrement=True, primary_key=True, index=True),
    sa.Column('name', sa_types.String(length=35), unique=True, nullable=False),
)


class User(SQLAlchemyBaseUserTableUUID, APP_CTX.sa_base):
    # Other attributes will be added from base class
    __tablename__ = "user"

    registered_at = sa.Column(sa_types.TIMESTAMP, default=datetime.utcnow)


UserPrivilegesTbl = sa.Table(
    'user_privileges',
    APP_CTX.sa_metadata,
    sa.Column('id', sa_types.Integer, autoincrement=True, primary_key=True, index=True),
    sa.Column('user_id', sa.ForeignKey(User.id)),
    sa.Column('role_id', sa.ForeignKey(RoleTbl.c.id))
)
