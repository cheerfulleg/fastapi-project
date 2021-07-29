from typing import List

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from backend.users.models import User
from backend.users.schemas import Profile_Pydantic, Profile, ProfileInWithUserId_Pydantic

profile_router = APIRouter()


@profile_router.get('', response_model=List[Profile_Pydantic])
async def get_profile_list():
    return await Profile_Pydantic.from_queryset(Profile.all())


@profile_router.get('/{profile_id}', response_model=Profile_Pydantic)
async def get_profile_by_id(profile_id: int):
    return Profile_Pydantic.from_queryset_single(Profile.get(id=profile_id))


@profile_router.post('', response_model=Profile_Pydantic)
async def create_profile(profile: ProfileInWithUserId_Pydantic):
    profile_obj = await Profile.create(**profile.dict(exclude_unset=True))
    return await Profile_Pydantic.from_tortoise_orm(profile_obj)


@profile_router.put('/{profile_id}', response_model=Profile_Pydantic)
async def update_profile_by_id(profile: ProfileInWithUserId_Pydantic, profile_id: int):
    await Profile.filter(id=profile_id).update(**profile.dict(exclude_unset=True))
    return await Profile_Pydantic.from_queryset_single(Profile.get(id=profile_id))


@profile_router.delete('/{profile}')
async def delete_profile_by_id(profile_id: int):
    await Profile.filter(id=profile_id).delete()
    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Profile deleted successfully'})
