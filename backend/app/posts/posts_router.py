from fastapi import APIRouter
from .api.posts_views import posts_router

base_posts_router = APIRouter()


base_posts_router.include_router(posts_router, prefix="/posts", tags=["Post actions"])
