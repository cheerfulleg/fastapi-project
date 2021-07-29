import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

TESTING = os.getenv('TESTING', False)

APP_NAME = "FastAPI Tortoise Project"
APP_VERSION = "0.0.1beta"

# Database settings
POSTGRESQL_HOSTNAME = os.getenv('DB_HOST')
POSTGRESQL_USERNAME = os.getenv('DB_USER')
POSTGRESQL_PASSWORD = os.getenv('DB_PASS')
POSTGRESQL_DATABASE = os.getenv('DB_NAME')
if TESTING:
    DB_URI = "sqlite://:memory:"
else:
    DB_URI = f"postgres://{POSTGRESQL_USERNAME}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOSTNAME}:5432/{POSTGRESQL_DATABASE}"

JWT_SECRET: str = os.getenv('JWT_SECRET')

MODELS_LIST = [
    "backend.app.users.models",
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
