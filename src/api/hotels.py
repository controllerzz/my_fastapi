from fastapi import Query, APIRouter

from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["hotels"])


hotels = [
    {"id": 1, "city": "Sochi", "title": "Sochi1"},
    {"id": 2, "city": "Sochi", "title": "Sochi2"},
    {"id": 3, "city": "Dubai", "title": "Dubai1"},
    {"id": 4, "city": "dubai", "title": "Dubai2"},
    {"id": 5, "city": "Moscow", "title": "Moscow1"},
]

page: int | None = Query(None, gt=0, description="Page"),
per_page: int | None = Query(None, gt=0, lt=50, description="Per PAge"),
@router.get("")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="id"),
        city: str | None = Query(None, description="Hotel City"),

):
    hotels_result = []
    for hotel in hotels:
        if id is not None and hotel["id"] != id:
            continue
        if city is not None and hotel["city"].lower() != city.lower():
            continue

        hotels_result.append(hotel)

    if pagination.page is not None and pagination.per_page is not None:
        index_start = (pagination.page - 1) * pagination.per_page
        hotels_result = hotels_result[index_start:][:pagination.per_page]

    return hotels_result


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels =  [hotel for hotel in hotels if hotel["id"] != hotel_id]

    return {"status": "OK"}


@router.post("/hotels")
def create_hotel(hotel_data: Hotel):
    global hotels

    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "city": hotel_data.city,
        "title": hotel_data.title
    })

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
