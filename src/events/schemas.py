from datetime import datetime

from pydantic import BaseModel, Field


class EventSchema(BaseModel):
    id: int
    name: str
    date: datetime
    place: str
    price: float = Field(ge=0.0, default=0.0)
    max_players: int = Field(ge=1, default=100)
    created_at: datetime


class AddEventSchema(BaseModel):
    name: str
    date: datetime
    place: str
    price: float = Field(ge=0.0, default=0.0)
    max_players: int = Field(ge=1, default=100)


class EventAlreadyExistsSchema(BaseModel):
    detail: str = "Event {} already exists"


class EventNotFound(BaseModel):
    detail: str = "Event {} not found"


class CreatedEventResponseSchema(BaseModel):
    id: int
