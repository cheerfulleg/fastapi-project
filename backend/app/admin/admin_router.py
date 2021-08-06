from fastapi import APIRouter

from backend.app.admin.api.posts_views import posts_router
from backend.app.admin.api.profile_views import profile_router
from backend.app.admin.api.user_views import user_router

admin_router = APIRouter()

admin_router.include_router(user_router, prefix="/users", tags=["User management"])
admin_router.include_router(profile_router, prefix="/profile", tags=["Profile management"])
admin_router.include_router(posts_router, prefix="/posts", tags=["Posts management"])
