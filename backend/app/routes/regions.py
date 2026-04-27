from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select

from ..deps import SessionDep
from ..models import Region, RegionAggregated, RegionDataWithName

reg_router = APIRouter(
    prefix="/regions",
    tags=["Регионы"]
)

@reg_router.get("/krais", summary="Получить список всех краев")
def get_krais(session: SessionDep)->list[Region]:
    statement = select(Region).where(Region.region_name.like("%край%"))
    krais = list(session.exec(statement).all())

    if not krais:
        raise HTTPException(status_code=404, detail="Края не найдены")

    return krais


@reg_router.get("/obls", summary="Получить список всех областей")
def get_obls(session: SessionDep)->list[Region]:
    statement = select(Region).where(Region.region_name.like("%область%"))
    obls = list(session.exec(statement).all())

    if not obls:
        raise HTTPException(status_code=404, detail="Области не найдены")

    return obls


@reg_router.get("/republics", summary="Получить список всех республик")
def get_republics(session: SessionDep)->list[Region]:
    statement = select(Region).where(Region.region_name.like("%Республика%"))
    republics = list(session.exec(statement).all())

    if not republics:
        raise HTTPException(status_code=404, detail="Республики не найдены")

    return republics


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


@reg_router.get("/{region_name}", summary="Получение региона по названию")
def read_region(
        region_name: str,
        session: SessionDep
) -> Region:
    region = session.exec(select(Region).where(Region.region_name == region_name)).first()
    if not region:
        raise HTTPException(status_code=404, detail=f'Субъект РФ с названием "{region_name}" не найден')
    return region


@reg_router.get("/{region_id}/{year}", summary="Получение информации о регионе по id за определенный год")
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
