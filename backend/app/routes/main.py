from fastapi import APIRouter

from . import regions

api_router = APIRouter()
api_router.include_router(regions.reg_router)