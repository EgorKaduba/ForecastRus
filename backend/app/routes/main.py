from fastapi import APIRouter

from . import regions, municipalities, heatmap, report

api_router = APIRouter()
api_router.include_router(regions.reg_router)
api_router.include_router(municipalities.mun_router)
api_router.include_router(heatmap.heatmap_router)
api_router.include_router(report.rep_router)