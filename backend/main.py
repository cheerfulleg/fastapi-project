from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from backend.app.routers import register_views
from backend.config import settings

app = FastAPI(docs_url="/", title=settings.APP_NAME, version=settings.APP_VERSION)

register_tortoise(
    app,
    db_url=settings.DB_URI,
    modules={"models": settings.MODELS_LIST},
    generate_schemas=True,
    add_exception_handlers=True,
)

register_views(app=app)

