from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select

from ..deps import SessionDep
from ..models import Region, RegionAggregated, RegionDataWithName

reg_router = APIRouter(
    prefix="/regions",
    tags=["Регионы"]
)


@reg_router.get("/", summary="Получить список всех субъектов РФ")
def read_regions(
        session: SessionDep,
        offset: int = 0,
        limit: int = Query(default=100, le=100)
) -> list[Region]:
    regions = list(session.exec(select(Region).offset(offset).limit(limit)).all())
    if regions:
        return regions
    raise HTTPException(status_code=404, detail="Субъекты РФ не найдены")


@reg_router.get("/{region_name}")
def read_region(
        region_name: str,
        session: SessionDep
) -> Region:
    region = session.exec(select(Region).where(Region.region_name == region_name)).first()
    if not region:
        raise HTTPException(status_code=404, detail=f'Субъект РФ с названием "{region_name}" не найден')
    return region


@reg_router.get("/{region_id}/{year}")
def get_region_data(
        region_id: int,
        year: int,
        session: SessionDep
) -> RegionDataWithName:
    statement = select(RegionAggregated).where(RegionAggregated.region_id == region_id, RegionAggregated.year == year)
    region_data = session.exec(statement).first()
    region_name = session.get(Region, region_id)
    data_dict = region_data.dict()
    data_dict["region_name"] = region_name.region_name
    if not region_data:
        raise HTTPException(status_code=404, detail=f'Информация о субъекте с id={region_id} за {year} год не найдена')
    return RegionDataWithName(**data_dict)
