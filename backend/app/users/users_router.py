from fastapi import APIRouter

from backend.app.users.api.profile_views import profile_router
from backend.app.users.api.user_views import user_router

base_user_router = APIRouter()

base_user_router.include_router(user_router, prefix="/user", tags=["Anonymous user actions"])
base_user_router.include_router(profile_router, prefix="/profile", tags=["Profile actions"])
