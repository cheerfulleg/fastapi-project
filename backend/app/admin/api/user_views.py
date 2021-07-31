from typing import List

from fastapi import APIRouter, Path
from starlette import status
from starlette.responses import JSONResponse

from backend.app.users.schemas import User_Pydantic, UserIn_Pydantic, User, UserInNoPassword_Pydantic
from backend.app.users.utils import create_password_hash

user_router = APIRouter()


@user_router.post('', response_model=User_Pydantic, status_code=201)
async def create_user(new_user: UserIn_Pydantic):
    """
    **Admin permission required**

    Create new user
    - **username**: string 50 characters (no validation)
    - **email**: string 120 characters (validating)
    - **password_hash**: any password that will be hashed
    - **is_admin**: admin rights access flag
    """
    password_hash = await create_password_hash(new_user.password_hash)
    user_obj = await User.create(username=new_user.username, email=new_user.email, password_hash=password_hash)
    return await User_Pydantic.from_tortoise_orm(user_obj)


@user_router.get('/{user_id}', response_model=User_Pydantic)
async def get_user_by_id(user_id: int = Path(..., gt=0)):
    """
    **Admin permission required**

    Get user details
    """
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


@user_router.get('', response_model=List[User_Pydantic])
async def get_users_list():
    """
    **Admin permission required**

    Get list of users
    """
    return await User_Pydantic.from_queryset(User.all())


@user_router.put('/{user_id}', response_model=User_Pydantic)
async def update_user_by_id(user: UserInNoPassword_Pydantic, user_id: int = Path(..., gt=0)):
    """
    **Admin permission required**

    Update user
    - **username**: string 50 characters (no validation)
    - **is_admin**: admin rights access flag
    """
    await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


@user_router.delete('/{user_id}')
async def delete_user_by_id(user_id: int):
    """
    **Admin permission required**

    Delete user
    """
    await User.filter(id=user_id).delete()
    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'User deleted successfully'})
