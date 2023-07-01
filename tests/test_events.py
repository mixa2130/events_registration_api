import httpx

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
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

updated_event = {
    "name": "Runderground jubilee event 2023",
    "start_date": "2023-02-25T18:02:13Z",
    "place": "Moscow, mukomolny passage 2",
    "price": 120,
    "max_players": 77
}


async def test_add_role(async_client: httpx.AsyncClient, session: AsyncSession):
    stmt = insert(RoleTbl).values({'id': 1, 'name': 'admin'})
    await session.execute(stmt)
    await session.commit()

    _res = await session.execute(select(RoleTbl))
    assert _res.all() == [(1, 'admin')], 'Роль не добавлялась'


async def test_add_event(jwt_authorized_async_client: httpx.AsyncClient, session: AsyncSession):
    response = await jwt_authorized_async_client.post('/events', json=test_event)

    assert response.status_code == 201

    stmt = select(EventsTbl).where(
        (EventsTbl.c.name == test_event['name']) &
        (EventsTbl.c.start_date == isoparse(test_event['start_date'])) &
        (EventsTbl.c.place == test_event['place'])
    )
    _res = await session.execute(stmt)
    event = _res.all()

    assert len(event) == 1

    # Event already exists
    al_response = await jwt_authorized_async_client.post('/events', json=test_event)
    assert al_response.status_code == 400


async def test_add_event_unauthorized(async_client: httpx.AsyncClient):
    response = await async_client.post('/events', json=test_event)
    assert response.status_code == 401


async def test_get_event_base(async_client: httpx.AsyncClient):
    response = await async_client.get('/events/1')
    assert response.status_code == 200

    event = response.json()
    assert event['place'] == test_event['place']
    assert event['name'] == test_event['name']


async def test_update_event(async_client: httpx.AsyncClient, session: AsyncSession):
    response = await async_client.put('/events/1', json=updated_event)
    assert response.status_code == 200

    stmt = select(EventsTbl.c.name, EventsTbl.c.start_date, EventsTbl.c.price).where(
        (EventsTbl.c.name == updated_event['name']) &
        (EventsTbl.c.start_date == isoparse(updated_event['start_date'])) &
        (EventsTbl.c.place == updated_event['place'])
    )
    _res = await session.execute(stmt)
    event = _res.one()

    assert (updated_event['name'], isoparse(updated_event['start_date']), int(updated_event['price'])) == \
           (event[0], event[1], int(event[2]))


async def test_delete_event(async_client: httpx.AsyncClient, session: AsyncSession):
    response = await async_client.delete('/events/1')
    assert response.status_code == 204

    response = await async_client.delete('/events/1')
    assert response.status_code == 404

    stmt = select(EventsTbl.c.name, EventsTbl.c.start_date, EventsTbl.c.price).where(
        (EventsTbl.c.name == updated_event['name']) &
        (EventsTbl.c.start_date == isoparse(updated_event['start_date'])) &
        (EventsTbl.c.place == updated_event['place'])
    )
    _res = await session.execute(stmt)
    event = _res.first()
    assert event is None
