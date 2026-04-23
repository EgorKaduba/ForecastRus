from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select, func
from typing import Annotated

from ..deps import SessionDep
from ..models import RegionColor, RegionAggregated, Region

heatmap_router = APIRouter(
    prefix="/heatmap",
    tags=["heatmap"]
)


@heatmap_router.get("/")
def get_heatmap(
        session: SessionDep,
        year_from: Annotated[int, Query(ge=2013, le=2023)],
        year_to: Annotated[int | None, Query(ge=2013, le=2023)] = None
) -> list[RegionColor]:
    if year_to and year_to != year_from:
        if year_to < year_from:
            raise HTTPException(status_code=400,
                                detail=f"Год окончания анализа меньше года начала анализа ({year_from} < {year_to})")
        statement = (select(
            RegionAggregated.region_id, func.sum(RegionAggregated.total_population).label("total_population")).where(
            RegionAggregated.year >= year_from).where(RegionAggregated.year <= year_to).group_by(
            RegionAggregated.region_id))
    else:
        statement = select(RegionAggregated.region_id, RegionAggregated.total_population).where(
            RegionAggregated.year == year_from
        )
    res = list(session.exec(statement).all())
    response = list()
    if res:
        for region in res:
            name = session.exec(select(Region.region_name).where(Region.region_id == region[0])).first()
            response.append(RegionColor(code="", name=name, population=region[1], color=""))
    return response
