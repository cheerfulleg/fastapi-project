from fastapi import FastAPI, Depends
from tortoise.contrib.fastapi import register_tortoise

from backend.auth import check_user_is_admin
from backend.config import settings

MODELS_LIST = ["backend.users.models"]


def get_db_uri(user: str, passwd: str, host: str, db: str) -> str:
    return f"postgres://{user}:{passwd}@{host}:5432/{db}"


def register_views(app: FastAPI) -> None:
    from .admin.admin_router import admin_router
    from .users.views import router as users_router
    from .auth import router as auth
    app.include_router(auth, tags=['JWT'])
    app.include_router(admin_router, prefix='/admin', tags=['Admin'], dependencies=[Depends(check_user_is_admin)])
    app.include_router(users_router, tags=["User Profile"])


DB_URI = get_db_uri(
    user=settings.POSTGRESQL_USERNAME,
    passwd=settings.POSTGRESQL_PASSWORD,
    host=settings.POSTGRESQL_HOSTNAME,
    db=settings.POSTGRESQL_DATABASE
)

TORTOISE_ORM = {
    "connections": {"default": DB_URI},
    "apps": {
        "models": {
            "models": MODELS_LIST + ["aerich.models"],
            "default_connection": "default",
        },
    },
}


def create_app() -> FastAPI:
    app = FastAPI(docs_url="/", title=settings.APP_NAME, version=settings.APP_VERSION)

    register_tortoise(
        app,
        db_url=DB_URI,
        modules={"models": MODELS_LIST},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    register_views(app=app)

    return app
