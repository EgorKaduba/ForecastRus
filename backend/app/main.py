from fastapi import FastAPI

from .core.config import settings
from .routes.main import api_router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    contact={
        "name": settings.ADMIN_NAME,
        "email": settings.ADMIN_EMAIL
    },
    debug=settings.DEBUG
)

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(api_router, prefix=settings.API_V1_PREFIX)
