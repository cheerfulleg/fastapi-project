import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.users.schemas import User, User_Pydantic
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
        user = await User.get(id=payload.get('id'))
    except jwt.exceptions.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')

    return await User_Pydantic.from_tortoise_orm(user)


async def check_user_is_admin(user: User_Pydantic = Depends(get_current_user)):
    if user.is_admin is not True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permissions to access")
    return user


@router.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')
    user_obj = await User_Pydantic.from_tortoise_orm(user)
    user_dict = user_obj.dict()
    payload = {'id': user_dict.get('id'), 'admin': user_dict.get('admin')}
    token = jwt.encode(payload, settings.JWT_SECRET)

    return {'access_token': token, 'token_type': 'bearer'}
