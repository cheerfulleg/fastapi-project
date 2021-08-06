from typing import List

from fastapi import APIRouter, HTTPException, Path
from starlette import status
from starlette.responses import JSONResponse

from backend.app.users.models import User
from backend.app.users.schemas import (
    Profile_Pydantic,
    Profile,
    ProfileInWithUserId_Pydantic,
)

profile_router = APIRouter()


@profile_router.get("", response_model=List[Profile_Pydantic])
async def get_profile_list():
    """
    **Admin permission required**

     Get list of existing profiles
    """
    return await Profile_Pydantic.from_queryset(Profile.all())


@profile_router.get("/{profile_id}", response_model=Profile_Pydantic)
async def get_profile_by_id(profile_id: int = Path(..., gt=0)):
    """
    **Admin permission required**

    Get profile details
    """
    return await Profile_Pydantic.from_queryset_single(Profile.get(id=profile_id))


@profile_router.post("", response_model=Profile_Pydantic, status_code=201)
async def create_profile(profile: ProfileInWithUserId_Pydantic):
    """
    **Admin permission required**

    Create profile
    - **first_name**: user's first name, 60 characters (no validation)
    - **last_name**: user's last name, 60 characters (no validation)
    - **date_of_birth**: user's date of birth (no validation)
    - **user_id**: profile relation to user
    """
    profile_obj = await Profile.create(**profile.dict(exclude_unset=True))
    return await Profile_Pydantic.from_tortoise_orm(profile_obj)


@profile_router.put("/{profile_id}", response_model=Profile_Pydantic)
async def update_profile_by_id(profile: ProfileInWithUserId_Pydantic, profile_id: int = Path(..., gt=0)):
    """
    **Admin permission required**

    Update profile
    - **first_name**: user's first name, 60 characters (no validation)
    - **last_name**: user's last name, 60 characters (no validation)
    - **date_of_birth**: user's date of birth (no validation)
    - **user_id**: profile relation to user
    """
    user_obj = await User.get(id=profile.dict().get("user_id"))
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await Profile.filter(id=profile_id).update(**profile.dict(exclude_unset=True))
    return await Profile_Pydantic.from_queryset_single(Profile.get(id=profile_id))


@profile_router.delete("/{profile_id}")
async def delete_profile_by_id(profile_id: int = Path(..., gt=0)):
    """
    **Admin permission required**

    Delete profile
    """
    deleted_count = await Profile.filter(id=profile_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Profile not found")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Profile deleted successfully"},
    )
