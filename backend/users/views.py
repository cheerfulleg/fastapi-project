from fastapi import APIRouter, Depends
from passlib.handlers.bcrypt import bcrypt

from .models import User_Pydantic, UserIn_Pydantic, User
from ..auth import get_current_user

router = APIRouter()


@router.post('/', response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.get('/me', response_model=User_Pydantic)
async def get_me(user: User_Pydantic = Depends(get_current_user)):
    return user
