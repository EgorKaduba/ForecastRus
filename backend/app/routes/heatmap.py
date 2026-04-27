import json

from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select, func
from typing import Annotated

from ..deps import SessionDep
from ..models import RegionColor, RegionAggregated, Region

heatmap_router = APIRouter(
    prefix="/heatmap",
    tags=["heatmap"]
)


@heatmap_router.get("/", summary="Получить цвета для хитмапа")
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
    with open("app/data/regions.json", mode="r", encoding="utf-8") as file:
        codes = json.load(file)
    min_pop = min(x[1] for x in res)
    max_pop = max(x[1] for x in res)

    color_1 = (0.8, 0.8, 0.8)
    color_2 = (0.02, 0.04, 0.26)

    if res:
        for region in res:
            name = session.exec(select(Region.region_name).where(Region.region_id == region[0])).first()
            population = region[1]
            code = codes[name]

            t = (population - min_pop) / (max_pop - min_pop)
            t = max(0, min(1, t))

            r = color_1[0] + t * (color_2[0] - color_1[0])
            g = color_1[1] + t * (color_2[1] - color_1[1])
            b = color_1[2] + t * (color_2[2] - color_1[2])

            color = f"{int(r * 255)}, {int(g * 255)}, {int(b * 255)}"

            response.append(RegionColor(code=code, name=name, population=population, color=color))
    return response
