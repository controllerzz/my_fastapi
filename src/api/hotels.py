from fastapi import Query, APIRouter

from src.api.dependencies import PaginationDep
from src.database import session_maker
from src.models.hotels import HotelsModel
from src.schemas.hotels import Hotel, HotelPATCH

from sqlalchemy import insert, select

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Hotel Location"),
        title: str | None = Query(None, description="Hotel Title"),
):
    per_page = pagination.per_page or 10
    async with session_maker() as session:
        query = select(HotelsModel)

        if location:
            query = query.filter(HotelsModel.location.contains(location))

        if title:
            query = query.filter(HotelsModel.title.contains(title))

        query = (
            query
            .offset(per_page * (pagination.page - 1))
            .limit(per_page)
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


@router.post("/hotels")
async def create_hotel(hotel_data: Hotel):
    global hotels

    async with session_maker() as session:
        add_hotel_stmt = insert(HotelsModel).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))

        await session.execute(add_hotel_stmt)
        await session.commit()
        return {"status": "OK"}

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
