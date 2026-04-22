from fastapi import FastAPI

from .core.config import settings
from .routes.main import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    contact={
        "name": settings.ADMIN_NAME,
        "email": settings.ADMIN_EMAIL
    },
    debug=settings.DEBUG
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)
