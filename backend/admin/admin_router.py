from fastapi import APIRouter

from .profile_views import profile_router
from .user_views import user_router

admin_router = APIRouter()

admin_router.include_router(user_router, prefix='/users')
admin_router.include_router(profile_router, prefix='/profile')
