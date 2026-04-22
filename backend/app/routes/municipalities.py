from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select

from ..deps import SessionDep
from ..models import Municipality, DemographicData, DemographicDataWithName

mun_router = APIRouter(
    prefix="/municipalities",
    tags=["Муниципалитеты"]
)


@mun_router.get("/", summary="Получение всех муниципалитетов РФ")
def read_municipalities(
        session: SessionDep,
        offset: int = 0,
        limit: int = Query(default=100, le=500)
) -> list[Municipality]:
    municipalities = list(session.exec(select(Municipality).offset(offset).limit(limit)).all())
    if not municipalities:
        raise HTTPException(status_code=404, detail="Муниципалитеты не найдены")
    return municipalities


@mun_router.get("/types", summary="Получить все типы муниципалитетов")
def get_municipalities_types(session: SessionDep) -> list[str]:
    types = list(session.exec(select(Municipality.mun_type).distinct()).all())
    if not types:
        raise HTTPException(status_code=404, detail="Типы муниципалитетов не найдены")
    return types


@mun_router.get("/types/{municipality_type}", summary="Поиск муниципалитетов по типу")
def get_municipalities_by_type(municipality_type: str, session: SessionDep) -> list[Municipality]:
    municipalities = list(session.exec(select(Municipality).where(Municipality.mun_type == municipality_type)).all())
    if not municipalities:
        raise HTTPException(status_code=404, detail=f"Муниципалитеты с типом [{municipality_type}] не найдены")
    return municipalities


@mun_router.get("/{municipality_name}", summary="Поиск муниципалитета по названию")
def read_municipality(
        municipality_name: str,
        session: SessionDep
) -> Municipality:
    municipality = session.exec(select(Municipality).where(Municipality.municipality_name == municipality_name)).first()
    if not municipality:
        raise HTTPException(status_code=404, detail=f"Муниципалитет с названием [{municipality_name}] не найден")
    return municipality


@mun_router.get("/{municipality_id}/{year}", summary="Получить информацию о муниципалитете за определённый год")
def get_municipality_data(
        municipality_id: int,
        year: int,
        session: SessionDep
) -> DemographicDataWithName:
    statement = select(DemographicData).where(DemographicData.municipality_id == municipality_id,
                                              DemographicData.year == year)
    municipality_data = session.exec(statement).first()
    municipality_name = session.get(Municipality, municipality_id)
    data_dict = municipality_data.dict()
    data_dict["municipality_name"] = municipality_name.municipality_name
    if not municipality_data:
        raise HTTPException(status_code=404,
                            detail=f"Информация о муниципалитете с id={municipality_id} за {year} год не найдена")
    return DemographicDataWithName(**data_dict)
