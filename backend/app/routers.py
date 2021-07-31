from fastapi import FastAPI, Depends

from backend.app.admin.admin_router import admin_router
from backend.app.auth.token_routes import token_router
from backend.app.auth.permissions import check_user_is_admin
from backend.app.users.users_router import base_user_router


def register_views(app: FastAPI) -> None:
    app.include_router(token_router, tags=['JWT'])
    app.include_router(admin_router, prefix='/admin', tags=['Admin'], dependencies=[Depends(check_user_is_admin)])
    app.include_router(base_user_router, tags=["User Profile"])
