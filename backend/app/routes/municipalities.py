from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select, func

from ..deps import SessionDep
from ..models import Municipality, DemographicData, DemographicDataWithName

mun_router = APIRouter(
    prefix="/municipalities",
    tags=["Муниципалитеты"]
)

@mun_router.get("/top-growth", summary="Топ муниципалитетов с наибольшим ростом населения")
def get_top_growth_municipalities(
        session: SessionDep,
        limit: int = Query(default=10, ge=1, le=50, description="Количество муниципалитетов в топе"),
) -> list[dict]:
    year_from = 2012
    year_to = 2025

    start_data = (
        select(
            DemographicData.municipality_id,
            DemographicData.population.label('population_start')
        )
        .where(DemographicData.year == year_from)
        .where(DemographicData.population.isnot(None))
        .subquery()
    )

    end_data = (
        select(
            DemographicData.municipality_id,
            DemographicData.population.label('population_end')
        )
        .where(DemographicData.year == year_to)
        .where(DemographicData.population.isnot(None))
        .subquery()
    )

    query = (
        select(
            Municipality.municipality_name,
            func.round(
                ((end_data.c.population_end - start_data.c.population_start) /
                 start_data.c.population_start * 100), 2
            ).label('growth_percent')
        )
        .join(start_data, Municipality.municipality_id == start_data.c.municipality_id)
        .join(end_data, Municipality.municipality_id == end_data.c.municipality_id)
        .where(start_data.c.population_start > 0)
        .where(end_data.c.population_end > 0)
        .order_by(func.round(
            ((end_data.c.population_end - start_data.c.population_start) /
             start_data.c.population_start * 100), 2
        ).desc())
        .limit(limit)
    )

    results = session.exec(query).all()

    if not results:
        raise HTTPException(status_code=404, detail="Данные не найдены")

    return [
        {
            'municipality_name': row.municipality_name,
            'growth_percent': float(row.growth_percent)
        }
        for row in results
    ]


@mun_router.get("/top-decline", summary="Топ муниципалитетов с наибольшим снижением населения")
def get_top_decline_municipalities(
        session: SessionDep,
        limit: int = Query(default=10, ge=1, le=50, description="Количество муниципалитетов в топе"),
) -> list[dict]:
    year_from = 2012
    year_to = 2025

    start_data = (
        select(
            DemographicData.municipality_id,
            DemographicData.population.label('population_start')
        )
        .where(DemographicData.year == year_from)
        .where(DemographicData.population.isnot(None))
        .subquery()
    )

    end_data = (
        select(
            DemographicData.municipality_id,
            DemographicData.population.label('population_end')
        )
        .where(DemographicData.year == year_to)
        .where(DemographicData.population.isnot(None))
        .subquery()
    )

    query = (
        select(
            Municipality.municipality_name,
            func.round(
                ((end_data.c.population_end - start_data.c.population_start) /
                 start_data.c.population_start * 100), 2
            ).label('growth_percent')
        )
        .join(start_data, Municipality.municipality_id == start_data.c.municipality_id)
        .join(end_data, Municipality.municipality_id == end_data.c.municipality_id)
        .where(start_data.c.population_start > 0)
        .where(end_data.c.population_end > 0)
        .order_by(func.round(
            ((end_data.c.population_end - start_data.c.population_start) /
             start_data.c.population_start * 100), 2
        ).asc())
        .limit(limit)
    )

    results = session.exec(query).all()

    if not results:
        raise HTTPException(status_code=404, detail="Данные не найдены")

    return [
        {
            'municipality_name': row.municipality_name,
            'decline_percent': abs(float(row.growth_percent))
        }
        for row in results
    ]


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
