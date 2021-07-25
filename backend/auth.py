import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.users.models import User, User_Pydantic
from .config import settings, oauth2_scheme

router = APIRouter()


async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        print(payload)
        user = await User.get(id=payload.get('id'))
    except jwt.exceptions.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')

    return await User_Pydantic.from_tortoise_orm(user)


@router.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')
    user_obj = await User_Pydantic.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), settings.JWT_SECRET)

    return {'access_token': token, 'token_type': 'bearer'}
