from fastapi import Query, APIRouter

from src.database import session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import *

router = APIRouter(prefix="/hotels", tags=["rooms"])


@router.get("/rooms/")
async def get_rooms():
    async with session_maker() as session:
        return await RoomsRepository(session).get_all()


@router.post("/rooms/")
async def create_room(room_data: RoomAdd):
    async with session_maker() as session:
        hotel = await RoomsRepository(session).add(data=room_data)
        await session.commit()
    return {"status": "OK", "data": hotel}
