import typing as tp

import sqlalchemy.sql as sa
import sqlalchemy.exc as sa_exc
from sqlalchemy.inspection import inspect as sa_inspect
from sqlalchemy.ext.asyncio import AsyncSession

from .models import EventsTbl, EventsAccessRightsTbl


async def add_event(session: AsyncSession, event: dict) -> int:
    async with session.begin():
        event_stmt = (
            EventsTbl.insert()
            .values(event)
            .returning(EventsTbl.c.id)
        )

        _res = await session.execute(event_stmt)
        event_id = _res.one()[0]

        rights_stmt = (
            EventsAccessRightsTbl.insert()
            .values({'event_id': event_id, 'role_id': 1})
        )
        await session.execute(rights_stmt)

    return event_id


async def get_event_by_id(session: AsyncSession, event_id: int):
    stmt = sa.select(EventsTbl).where(EventsTbl.c.id == event_id)
    res = await session.execute(stmt)
    event = res.one()

    if event is None:
        raise sa_exc.NoResultFound
    return event


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


async def delete_event(session: AsyncSession, event_id: int) -> int:
    async with session.begin():
        get_rights_stmt = sa.select(EventsAccessRightsTbl.c.id).where(EventsAccessRightsTbl.c.event_id == event_id)
        _res = await session.execute(get_rights_stmt)
        ids = [el[0] for el in _res.all()]

        del_rights_stmt = sa.delete(EventsAccessRightsTbl).where(EventsAccessRightsTbl.c.id.in_(ids))
        await session.execute(del_rights_stmt)

        del_event_stmt = sa.delete(EventsTbl).where(EventsTbl.c.id == event_id).returning(EventsTbl.c.id)
        ev_id = await session.execute(del_event_stmt)
        return ev_id.one()
