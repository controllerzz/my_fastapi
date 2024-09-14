from fastapi import Query, APIRouter
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["hotels"])


hotels = [
    {"id": 1, "city": "Sochi", "title": "Sochi1"},
    {"id": 2, "city": "Sochi", "title": "Sochi2"},
    {"id": 3, "city": "Dubai", "title": "Dubai1"},
    {"id": 4, "city": "dubai", "title": "Dubai2"},
    {"id": 5, "city": "Moscow", "title": "Moscow1"},
]


@router.get("")
def get_hotels(
        id: int | None = Query(None, description="id"),
        city: str | None = Query(None, description="Hotel City"),
        page: int | None = Query(None, description="Page"),
        per_page: int | None = Query(None, description="Per PAge"),
):
    hotels_result = []
    for hotel in hotels:
        if id is not None and hotel["id"] != id:
            continue
        if city is not None and hotel["city"].lower() != city.lower():
            continue

        hotels_result.append(hotel)

    if page and per_page:
        index_start = (page - 1) * per_page
        index_end = (page - 1) * per_page + per_page
        hotels_result = hotels_result[index_start:index_end]

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
