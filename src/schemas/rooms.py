from pydantic import BaseModel, Field


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None
    price: int
    quantity: int


class Room(RoomAdd):
    id: int


