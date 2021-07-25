from fastapi import APIRouter, Depends
from passlib.handlers.bcrypt import bcrypt
from starlette import status
from starlette.responses import JSONResponse

from .models import User_Pydantic, UserIn_Pydantic, User, Profile_Pydantic, ProfileIn_Pydantic, Profile
from ..auth import get_current_user

router = APIRouter()


@router.post('', response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.post('/profile', response_model=Profile_Pydantic)
async def create_user_profile(profile: ProfileIn_Pydantic, user: User = Depends(get_current_user)):
    user_obj = await User.get(id=user.id)
    profile_obj = Profile(
        **profile.dict(exclude_unset=True),
        user=user_obj
    )
    await profile_obj.save()
    return await Profile_Pydantic.from_tortoise_orm(profile_obj)


@router.get('/profile', response_model=Profile_Pydantic)
async def get_user_profile(user: User_Pydantic = Depends(get_current_user)):
    profile_obj = await Profile.get(user_id=user.id)
    return await Profile_Pydantic.from_tortoise_orm(profile_obj)


@router.put('/profile', response_model=Profile_Pydantic)
async def update_user_profile(profile: ProfileIn_Pydantic, user: User = Depends(get_current_user)):
    user_id = user.id
    await Profile.filter(user_id=user_id).update(**profile.dict(exclude_unset=True))
    return await Profile_Pydantic.from_queryset_single(Profile.get(user_id=user_id))


@router.delete('/profile', response_model=Profile_Pydantic)
async def update_user_profile(user: User = Depends(get_current_user)):
    await Profile.filter(user_id=user.id).delete()
    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'profile deleted'})
