from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy.sql as sa

from .models import EventsTbl


async def add_event(session: AsyncSession, event: dict) -> int:
    async with session.begin() as connection:
        stmt = (
            EventsTbl.insert()
            .values(event)
            .returning(EventsTbl.c.id)
        )

        res = await connection.session.execute(stmt)
        return res.one()[0]


async def get_event_by_id(session: AsyncSession, event_id: int):
    stmt = sa.select(EventsTbl).where(EventsTbl.c.id == event_id)
    res = await session.execute(stmt)
    return res.one()[0]
