import jwt
from fastapi import HTTPException, Depends
from starlette import status

from backend.app.users.models import User
from backend.app.users.schemas import User_Pydantic
from backend.config import settings


async def get_current_user(token: str = Depends(settings.oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except jwt.exceptions.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')

    return await User_Pydantic.from_tortoise_orm(user)


async def check_user_is_admin(user: User_Pydantic = Depends(get_current_user)):
    if user.is_admin is not True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permissions to access")
    return user