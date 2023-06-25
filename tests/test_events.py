import httpx

from sqlalchemy import insert, select
from dateutil.parser import isoparse

from src.auth.models import RoleTbl
from src.events.models import EventsTbl

test_event = {
    "name": "Runderground jubilee event 2023",
    "start_date": "2023-02-20T18:02:13Z",
    "place": "Moscow, mukomolny passage 2",
    "price": 2400,
    "max_players": 77
}


async def test_add_role(async_client, session):
    stmt = insert(RoleTbl).values({'id': 1, 'name': 'admin'})
    await session.execute(stmt)
    await session.commit()

    _res = await session.execute(select(RoleTbl))
    assert _res.all() == [(1, 'admin')], 'Роль не добавлялась'


async def test_add_event(authorized_async_client: httpx.AsyncClient, session):
    response = await authorized_async_client.post('/events', json=test_event)

    assert response.status_code == 201

    stmt = select(EventsTbl).where(
        (EventsTbl.c.name == test_event['name']) &
        (EventsTbl.c.start_date == isoparse(test_event['start_date'])) &
        (EventsTbl.c.place == test_event['place'])
    )
    _res = await session.execute(stmt)
    event = _res.all()

    assert len(event) == 1
