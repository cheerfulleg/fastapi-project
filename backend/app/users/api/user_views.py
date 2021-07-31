from fastapi import APIRouter

from backend.app.users.schemas import User_Pydantic, User, UserDefaultIn_Pydantic
from backend.app.users.utils import create_password_hash

user_router = APIRouter()


@user_router.post('', response_model=User_Pydantic, status_code=201)
async def create_user(new_user: UserDefaultIn_Pydantic):
    """
    Register new user
    - **username**: string 50 characters (no validation)
    - **email**: string 120 characters (validating)
    - **password_hash**: any password that will be hashed
    """
    password_hash = await create_password_hash(new_user.password_hash)
    user_obj = await User.create(username=new_user.username, email=new_user.email, password_hash=password_hash)
    return await User_Pydantic.from_tortoise_orm(user_obj)
