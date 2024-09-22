from fastapi import Query, APIRouter, Body
from src.database import session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["rooms"])


@router.get("{hotel_id}/rooms/")
async def get_rooms(hotel_id: int):
    async with session_maker() as session:
        return await RoomsRepository(session).get_all()


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("{hotel_id}/rooms/")
async def create_room(hotel_id: int, room_data_req: RoomAddRequest = Body()):

    room_data = RoomAdd(
        **room_data_req.model_dump(),
        hotel_id=hotel_id
    )

    async with session_maker() as session:
        room = await RoomsRepository(session).add(data=room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(hotel_id: int, room_id: int, room_data_req: RoomAddRequest):

    room_data = RoomAdd(
        **room_data_req.model_dump(),
        hotel_id=hotel_id
    )

    async with session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data_req: RoomPatchRequest = Body()
):
    room_data = RoomPatch(
        hotel_id=hotel_id,
        **room_data_req.model_dump(exclude_unset=True),
    )

    async with session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
        hotel_id: int,
        room_id: int
):
    async with session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}
