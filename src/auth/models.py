from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from sqlalchemy.sql import sqltypes as sa_types
from sqlalchemy import schema as sa

from src.context import APP_CTX

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
    sa.Column('role_id', sa.ForeignKey(RoleTbl.c.id)),
    sa.UniqueConstraint('user_id', 'role_id', name='uq__user_id__role_id')
)
