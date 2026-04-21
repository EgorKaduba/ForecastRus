from fastapi import FastAPI
from core import config

from functools import lru_cache


@lru_cache
def get_settings():
    return config.Settings()  # type: ignore

settings = get_settings()
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    contact={
        "name": settings.ADMIN_NAME,
        "email": settings.ADMIN_EMAIL
    }
)
