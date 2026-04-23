from fastapi import APIRouter, Query
from typing import Annotated

from ..models import RegionColor


heatmap_router = APIRouter(
    prefix="/heatmap",
    tags=["heatmap"]
)

@heatmap_router.get("/")
def get_heatmap(
        year_from: Annotated[int, Query(ge=2013, le=2023)],
        year_to: Annotated[int | None, Query(default=None, ge=2013, le=2023)]
) -> list[RegionColor]:
    pass