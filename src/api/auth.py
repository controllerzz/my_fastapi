from fastapi import APIRouter

from src.database import session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth")

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = pwd_context.hash(data.password)

    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with session_maker() as session:
        await UsersRepository(session).add(data=new_user_data)
        await session.commit()
    return {"status": "OK"}