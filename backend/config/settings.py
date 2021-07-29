import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

APP_NAME: str = "FastAPI Tortoise Project"
APP_VERSION: str = "0.0.1beta"

# Database settings
POSTGRESQL_HOSTNAME: str = os.getenv('DB_HOST')
POSTGRESQL_USERNAME: str = os.getenv('DB_USER')
POSTGRESQL_PASSWORD: str = os.getenv('DB_PASS')
POSTGRESQL_DATABASE: str = os.getenv('DB_NAME')
DB_URI = f"postgres://{POSTGRESQL_USERNAME}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOSTNAME}:5432/{POSTGRESQL_DATABASE}"


JWT_SECRET: str = os.getenv('JWT_SECRET')

MODELS_LIST = [
    "backend.app.users.models",
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
