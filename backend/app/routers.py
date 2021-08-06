from fastapi import FastAPI, Depends

from backend.app.admin.admin_router import admin_router
from backend.app.auth.token_routes import token_router
from backend.app.auth.permissions import check_user_is_admin
from backend.app.posts.posts_router import base_posts_router
from backend.app.users.users_router import base_user_router


def register_views(app: FastAPI) -> None:
    app.include_router(token_router, tags=["JWT"])
    app.include_router(
        admin_router,
        prefix="/admin",
        tags=["Admin actions"],
        dependencies=[Depends(check_user_is_admin)],
    )
    app.include_router(base_user_router, tags=["Account user actions"])
    app.include_router(base_posts_router)
