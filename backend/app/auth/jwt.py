from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, HTTPException

from backend.app.users.schemas import User
from backend.config import settings

router = APIRouter()


class AuthJWT:
    secret = settings.JWT_SECRET

    def create_access_token(self, payload):
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXP_MINUTES),
            "iat": datetime.utcnow(),
            "scope": "access_token",
            "sub": payload,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            if payload["scope"] == "access_token":
                return payload["sub"]
            raise HTTPException(status_code=401, detail="Scope for the token is invalid")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def create_refresh_token(self, payload):
        payload = {
            "exp": datetime.utcnow() + timedelta(hours=settings.REFRESH_TOKEN_EXP_HOURS),
            "iat": datetime.utcnow(),
            "scope": "refresh_token",
            "sub": payload,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def create_access_token_from_refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, self.secret, algorithms=["HS256"])
            if payload["scope"] == "refresh_token":
                username = payload["sub"]
                new_token = self.create_access_token(username)
                return new_token
            raise HTTPException(status_code=401, detail="Invalid scope for token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    @staticmethod
    async def authenticate_user(username: str, password: str):
        user = await User.get(username=username)
        if not user:
            return False
        if not user.verify_password(password):
            return False
        return user


auth_jwt = AuthJWT()
