from fastapi import APIRouter

from . import regions, municipalities

api_router = APIRouter()
api_router.include_router(regions.reg_router)
api_router.include_router(municipalities.mun_router)