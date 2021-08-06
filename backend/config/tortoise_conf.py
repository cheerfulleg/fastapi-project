from backend.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.DB_URI},
    "apps": {
        "models": {
            "models": settings.MODELS_LIST + ["aerich.models"],
            "default_connection": "default",
        },
    },
}
