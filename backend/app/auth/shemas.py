from pydantic import BaseModel


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class AccessToken(BaseModel):
    access_token: str
