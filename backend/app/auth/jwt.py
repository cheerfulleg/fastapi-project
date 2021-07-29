import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.users.schemas import User, User_Pydantic
from backend.config import settings

router = APIRouter()


async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
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
