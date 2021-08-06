from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.auth.jwt import auth_jwt
from backend.app.users.schemas import User_Pydantic

token_router = APIRouter()


@token_router.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Generates JWT token pair: access token and refresh token
    """
    user = await auth_jwt.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    user_obj = await User_Pydantic.from_tortoise_orm(user)
    user_dict = user_obj.dict()
    payload = {"id": user_dict.get("id"), "admin": user_dict.get("is_admin")}
    access_token = auth_jwt.create_access_token(payload=payload)
    refresh_token = auth_jwt.create_refresh_token(payload=payload)
    return {"access_token": access_token, "refresh_token": refresh_token}


@token_router.post("/token/refresh")
async def generate_new_access_token(token: str):
    """
    Uses refresh token to generate new access token
    """
    access_token = auth_jwt.create_access_token_from_refresh_token(refresh_token=token)
    return {"access_token": access_token}
