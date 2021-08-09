import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from fastapi_mail import ConnectionConfig, FastMail

load_dotenv()

TESTING = os.getenv("TESTING", False)

APP_NAME = "FastAPI Tortoise Project"
APP_VERSION = "0.0.1beta"

# Database settings
POSTGRESQL_HOSTNAME = os.getenv("DB_HOST")
POSTGRESQL_USERNAME = os.getenv("DB_USER")
POSTGRESQL_PASSWORD = os.getenv("DB_PASS")
POSTGRESQL_DATABASE = os.getenv("DB_NAME")
if TESTING:
    DB_URI = "sqlite://:memory:"
else:
    DB_URI = f"postgres://{POSTGRESQL_USERNAME}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOSTNAME}:5432/{POSTGRESQL_DATABASE}"

MODELS_LIST = ["backend.app.users.models", "backend.app.posts.models"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT settings
JWT_SECRET = os.getenv("JWT_SECRET")
REFRESH_TOKEN_EXP_HOURS = int(os.getenv("REFRESH_TOKEN_EXP_HOURS"))
ACCESS_TOKEN_EXP_MINUTES = int(os.getenv("ACCESS_TOKEN_EXP_MINUTES"))

# Email settings
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("EMAIL_HOST_USER"),
    MAIL_PASSWORD=os.getenv("EMAIL_HOST_PASSWORD"),
    MAIL_FROM=os.getenv("EMAIL_HOST_USER"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME=os.getenv("EMAIL_HOST_USER"),
    MAIL_TLS=True,
    MAIL_SSL=False,
)

fm = FastMail(conf)

# AWS settings

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")
AWS_BUCKET_FOLDER = "profileImages"

# Celery settings
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")

# Caching settings
REDIS_CACHE_URL = os.getenv("REDIS_CACHE_URL")
