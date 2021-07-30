from fastapi import APIRouter

from backend.app.users.schemas import User_Pydantic, User, UserDefaultIn_Pydantic
from backend.app.users.utils import create_password_hash

user_router = APIRouter()


@user_router.post('', response_model=User_Pydantic)
async def create_user(new_user: UserDefaultIn_Pydantic):
    """
    Create new user
    - **username**: string 50 characters (no validation)
    - **password_hash**: any password that will be hashed
    """
    user_obj = User(username=new_user.username, password_hash=await create_password_hash(new_user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)
