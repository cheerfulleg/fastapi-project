from typing import List

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from backend.users.schemas import User_Pydantic, UserIn_Pydantic, User, UserInNoPassword_Pydantic
from backend.utils.utils import create_password_hash

user_router = APIRouter()


@user_router.post('', response_model=User_Pydantic)
async def create_user(new_user: UserIn_Pydantic):
    user_obj = User(username=new_user.username, password_hash=await create_password_hash(new_user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)


@user_router.get('/{user_id}', response_model=User_Pydantic)
async def get_user_by_id(user_id: int):
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


@user_router.get('', response_model=List[User_Pydantic])
async def get_users_list():
    return await User_Pydantic.from_queryset(User.all())


@user_router.put('/{user_id}', response_model=User_Pydantic)
async def update_user_by_id(user: UserInNoPassword_Pydantic, user_id: str):
    await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


@user_router.delete('/{user_id}')
async def delete_user_by_id(user_id: int):
    await User.filter(id=user_id).delete()
    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'User deleted successfully'})
