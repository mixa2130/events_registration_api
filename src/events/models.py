from datetime import datetime

from sqlalchemy.sql import sqltypes as sa_types
from sqlalchemy import schema as sa

from src.context import APP_CTX
from src.auth.models import RoleTbl

EventsTbl = sa.Table(
    'event',
    APP_CTX.sa_metadata,
    sa.Column('id', sa_types.Integer, autoincrement=True, primary_key=True, index=True),
    sa.Column('name', sa_types.String(length=70), nullable=False),
    sa.Column('date', sa_types.TIMESTAMP),
    sa.Column('place', sa_types.String(length=100)),
    sa.Column('price', sa_types.NUMERIC(4, 2), default=0.0),
    sa.Column('max_players', sa_types.INT, default=1000),
    sa.Column('created_at', sa_types.TIMESTAMP, default=datetime.utcnow),
    sa.UniqueConstraint('name', 'place', 'date', name='uq__event__name__place__date')
)

EventsAccessRightsTbl = sa.Table(
    'event_access_rights',
    APP_CTX.sa_metadata,
    sa.Column('id', sa_types.Integer, autoincrement=True, primary_key=True, index=True),
    sa.Column('role_id', sa.ForeignKey(RoleTbl.c.id)),
    sa.Column('event_id', sa.ForeignKey(EventsTbl.c.id))
)
