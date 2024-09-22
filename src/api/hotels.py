from fastapi import Query, APIRouter

from src.api.dependencies import PaginationDep
from src.database import session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelPatch, HotelAdd

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


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        return {"status": "OK", "data": hotel}


@router.post("/hotels")
async def create_hotel(hotel_data: HotelAdd):
    async with session_maker() as session:
        hotel = await HotelsRepository(session).add(data=hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}")
async def put_hotel(
        hotel_id: int,
        hotel_data: HotelAdd
):
    async with session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPatch
):
    async with session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}
