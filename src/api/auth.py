from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, HTTPException, Response, Request

from src.config import settings
from src.database import session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from passlib.context import CryptContext
import jwt

from src.services.auth import AuthService

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(data.password)

    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with session_maker() as session:
        await UsersRepository(session).add(data=new_user_data)
        await session.commit()
    return {"status": "OK"}


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response,
):
    async with session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect User")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/only_auth")
async def only_auth(
        request: Request
):
    access_token = request.cookies.get("access_token")
    print(access_token)

