from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from backend.app.auth.permissions import get_current_user
from backend.app.users.schemas import User_Pydantic, User, Profile_Pydantic, ProfileIn_Pydantic, Profile

profile_router = APIRouter()


@profile_router.post('', response_model=Profile_Pydantic)
async def create_user_profile(profile: ProfileIn_Pydantic, user: User = Depends(get_current_user)):
    """
    **Login required**

    Create profile
    - **first_name**: user's first name, 60 characters (no validation)
    - **last_name**: user's last name, 60 characters (no validation)
    - **date_of_birth**: user's date of birth (no validation)
    - **user_id**: profile relation to user
    """
    user_obj = await User.get(id=user.id)
    profile_obj = Profile(
        **profile.dict(exclude_unset=True),
        user=user_obj
    )
    await profile_obj.save()
    return await Profile_Pydantic.from_tortoise_orm(profile_obj)


@profile_router.get('', response_model=Profile_Pydantic)
async def get_user_profile(user: User_Pydantic = Depends(get_current_user)):
    """
    **Login required**

    Get current user profile details
    """
    profile_obj = await Profile.get(user_id=user.id)
    return await Profile_Pydantic.from_tortoise_orm(profile_obj)


@profile_router.put('', response_model=Profile_Pydantic)
async def update_user_profile(profile: ProfileIn_Pydantic, user: User = Depends(get_current_user)):
    """
    **Login required**

    Update profile
    - **first_name**: user's first name, 60 characters (no validation)
    - **last_name**: user's last name, 60 characters (no validation)
    - **date_of_birth**: user's date of birth (no validation)
    - **user_id**: profile relation to user
    """
    user_id = user.id
    await Profile.filter(user_id=user_id).update(**profile.dict(exclude_unset=True))
    return await Profile_Pydantic.from_queryset_single(Profile.get(user_id=user_id))


@profile_router.delete('')
async def update_user_profile(user: User = Depends(get_current_user)):
    """
    **Login required**

    Delete profile
    """
    await Profile.filter(user_id=user.id).delete()
    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Profile deleted successfully'})
