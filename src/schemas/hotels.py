from pydantic import BaseModel, Field


class HotelAdd(BaseModel):
    title: str
    location: str


class Hotel(HotelAdd):
    id: int


class HotelPATCH(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)


class HotelFilter(BaseModel):
    id: int | None = Field(None)
    title: str | None = Field(None)
    location: str | None = Field(None)
