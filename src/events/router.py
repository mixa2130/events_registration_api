from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy.exc as sa_exc
import asyncpg.exceptions as pg_exc

from src.context import APP_CTX
from . import schemas
from . import service

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.get('/{event_id}',
            response_model=schemas.EventSchema,
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_404_NOT_FOUND: {
                    "model": schemas.EventNotFound,
                    "description": "Event already exists"
                }
            })
async def get_event(event_id: int,
                    session: AsyncSession = Depends(APP_CTX.pg_controller.get_session)):
    try:
        event = await service.get_event_by_id(session, event_id)
    except sa_exc.NoResultFound:
        APP_CTX.logger.warning(f"No result found for event with id {event_id}")
        return HTTPException(status_code=404, detail=f"Id {event_id} not found")

    return schemas.EventSchema(**{k: v for k, v in zip(schemas.EventSchema.__fields__.keys(), event)})


@router.post(
    "/",
    response_model=schemas.CreatedEventResponseSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": schemas.EventAlreadyExistsSchema,
            "description": "Event already exists"
        }
    })
async def add_event(event: schemas.AddEventSchema, session: AsyncSession = Depends(APP_CTX.pg_controller.get_session)):
    event_dict = event.dict()

    try:
        event_id = await service.add_event(session, event_dict)
    except sa_exc.IntegrityError as exc:
        APP_CTX.logger.warning(f"Exception during insert f{event_dict}: {exc}")
        await session.rollback()

        if exc.orig.__cause__.__class__ == pg_exc.UniqueViolationError:
            raise HTTPException(status_code=400, detail=f"Event {event.name} already exists")
        raise exc.orig

    return schemas.CreatedEventResponseSchema(id=event_id)


@router.put('/{event_id}')
async def update_event(event_id: int,
                       session: AsyncSession = Depends(APP_CTX.pg_controller.get_session)):
    pass
