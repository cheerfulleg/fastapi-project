from fastapi.security import OAuth2PasswordBearer

from pydantic import BaseSettings
import os
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Tortoise Project"
    APP_VERSION: str = "0.0.1beta"
    POSTGRESQL_HOSTNAME: str = os.getenv('DB_HOST')
    POSTGRESQL_USERNAME: str = os.getenv('DB_USER')
    POSTGRESQL_PASSWORD: str = os.getenv('DB_PASS')
    POSTGRESQL_DATABASE: str = os.getenv('DB_NAME')
    JWT_SECRET: str = os.getenv('JWT_SECRET')


settings = Settings()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
