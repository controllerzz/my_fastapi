from fastapi import Query, APIRouter

from src.api.dependencies import PaginationDep
from src.database import session_maker
from src.models.hotels import HotelsModel
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH

from sqlalchemy import insert, select, func

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Hotel Location"),
        title: str | None = Query(None, description="Hotel Title"),
):
    per_page = pagination.per_page or 10
    offset = pagination.per_page * (pagination.page - 1)

    async with session_maker() as session:
        return await HotelsRepository(session).get_all(
            location,
            title,
            limit=per_page,
            offset=offset
        )


@router.post("/hotels")
async def create_hotel(hotel_data: Hotel):
    async with session_maker() as session:
        hotel = await HotelsRepository(session).add(add_data=hotel_data)
        await session.commit()
        return {"status": "OK", "data": hotel}

    return {"status": "ERROR"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels =  [hotel for hotel in hotels if hotel["id"] != hotel_id]

    return {"status": "OK"}


@router.put("/{hotel_id}")
def put_hotel(
        hotel_id: int,
        hotel_data: Hotel
):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["city"] = hotel_data.city
            hotel["title"] = hotel_data.title
            return {"status": "OK"}

    return {"status": "ERROR"}


@router.patch("/{hotel_id}")
def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_id.city is not None:
                hotel["city"] = hotel_id.city
            if hotel_id.title is not None:
                hotel["title"] = hotel_id.title

            return {"status": "OK"}

    return {"status": "ERROR"}
