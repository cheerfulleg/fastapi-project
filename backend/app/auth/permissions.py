from fastapi import HTTPException, Depends
from starlette import status

from backend.app.auth.jwt import auth_jwt
from backend.app.users.models import User, Profile
from backend.app.users.schemas import User_Pydantic, Profile_Pydantic
from backend.config import settings


async def get_current_user(token: str = Depends(settings.oauth2_scheme)):
    token_data = auth_jwt.decode_token(token)
    user = await User.get(id=token_data.get("id"))
    return await User_Pydantic.from_tortoise_orm(user)


async def check_user_is_admin(user: User_Pydantic = Depends(get_current_user)):
    if user.is_admin is not True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permissions to access",
        )
    return user


async def has_profile(user: User_Pydantic = Depends(get_current_user)):
    profile = await Profile.filter(user_id=user.dict().get("id"))
    if not profile:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You didn't created profile")
    return await Profile_Pydantic.from_tortoise_orm(profile[0])
