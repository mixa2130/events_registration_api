from datetime import datetime

from pydantic import BaseModel, Field


class EventSchema(BaseModel):
    id: int
    name: str
    start_date: datetime
    place: str
    price: float = Field(ge=0.0, default=0.0)
    max_players: int = Field(ge=1, default=100)
    created_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": 119,
                "name": "Runderground jubilee event 2023",
                "date": "2023-02-20T18:02:13Z",
                "place": "Moscow, mukomolny passage 2",
                "price": 2400,
                "max_players": 77,
                "created_at": "2023-02-10T15:02:13Z"
            }
        }


class NewEventSchema(BaseModel):
    name: str
    start_date: datetime = Field(description="ISO 8601 formatted date time")
    place: str
    price: float = Field(ge=0.0, default=0.0)
    max_players: int = Field(ge=1, default=100)

    class Config:
        schema_extra = {
            "example": {
                "name": "Runderground jubilee event 2023",
                "start_date": "2023-02-20T18:02:13Z",
                "place": "Moscow, mukomolny passage 2",
                "price": 2400,
                "max_players": 77
            }
        }


class EventAlreadyExistsSchema(BaseModel):
    detail: str = "Event {} already exists"


class EventNotFound(BaseModel):
    detail: str = "Event {} not found"


class CreatedEventResponseSchema(BaseModel):
    id: int
