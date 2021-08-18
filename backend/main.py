import aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_pagination import add_pagination
from tortoise.contrib.fastapi import register_tortoise

from backend.app.routers import register_views
from backend.config import settings

app = FastAPI(docs_url="/", title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    db_url=settings.DB_URI,
    modules={"models": settings.MODELS_LIST},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(settings.REDIS_CACHE_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


register_views(app)
add_pagination(app)
