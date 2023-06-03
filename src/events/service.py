import sqlalchemy.sql as sa
from sqlalchemy.inspection import inspect as sa_inspect
from sqlalchemy.ext.asyncio import AsyncSession

from .models import EventsTbl


async def add_event(session: AsyncSession, event: dict) -> int:
    async with session.begin():
        stmt = (
            EventsTbl.insert()
            .values(event)
            .returning(EventsTbl.c.id)
        )

        res = await session.execute(stmt)
        return res.one()[0]


async def get_event_by_id(session: AsyncSession, event_id: int):
    stmt = sa.select(EventsTbl).where(EventsTbl.c.id == event_id)
    res = await session.execute(stmt)
    return res.all()[0]


async def update_event(session: AsyncSession, event: dict, event_id: int):
    async with session.begin():
        stmt = (
            EventsTbl.update()
            .values(event)
            .where(EventsTbl.c.id == event_id)
            .returning(*[column for column in sa_inspect(EventsTbl).c])
        )

        res = await session.execute(stmt)
        return res.all()
