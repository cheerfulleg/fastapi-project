from fastapi import APIRouter

from backend.app.users.schemas import User_Pydantic, UserIn_Pydantic, User
from backend.app.users.utils import create_password_hash

user_router = APIRouter()


@user_router.post('', response_model=User_Pydantic)
async def create_user(new_user: UserIn_Pydantic):
    user_obj = User(username=new_user.username, password_hash=await create_password_hash(new_user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)
