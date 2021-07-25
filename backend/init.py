from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from backend.config import settings


def create_app() -> FastAPI:
    app = FastAPI(docs_url="/", title=settings.APP_NAME, version=settings.APP_VERSION)

    register_tortoise(
        app,
        db_url=get_db_uri(
            user=settings.POSTGRESQL_USERNAME,
            passwd=settings.POSTGRESQL_PASSWORD,
            host=settings.POSTGRESQL_HOSTNAME,
            db=settings.POSTGRESQL_DATABASE
        ),
        modules={"models": ["backend.users.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    register_views(app=app)

    return app


def get_db_uri(user, passwd, host, db):
    return f"postgres://{user}:{passwd}@{host}:5432/{db}"


def register_views(app: FastAPI):
    from backend.users.views import router as users_router
    from .auth import router as auth
    app.include_router(auth, tags=['JWT'])
    app.include_router(users_router, prefix="/users", tags=["Users"])
