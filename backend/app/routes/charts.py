from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select
from ..tools.charts import (plot_migration, plot_natural_growth, plot_birth_rate, plot_mortality_rate,
                            plot_population_percent_change,  plot_population)
from ..tools.get_data import get_population_by_region, get_municipalities_by_id
from ..deps import SessionDep
import base64

ch_router = APIRouter(
    prefix="/charts",
    tags=["Диаграммы"]
)

@ch_router.get("/population", summary="Получить диаграмму динамики изменения населения региона/муниципалитета")
def chart_population(
    session: SessionDep,
    id: int = Query(..., description="ID региона или муниципалитета"),
    type: str = Query(..., description="Тип: 'region' или 'municipality'"),
    year_from: int = Query(..., ge=2010, le=2035),
    year_to: int = Query(..., ge=2010, le=2035)
) -> dict:
    if type == "region":
        data = get_population_by_region(session, id, year_from, year_to)
    elif type == "municipality":
        data = get_municipalities_by_id(session, id, year_from, year_to)
    else:
        raise HTTPException(status_code=400, detail="Неверный тип")

    buffer = plot_population(data, type)
    if buffer is None:
        raise HTTPException(status_code=404, detail="Нет данных для построения графика")

    if buffer:
        base64_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return {"image_base64": base64_string}
    raise HTTPException(404, "График не создан")

@ch_router.get("/percent_population", summary="Получить диаграмму динамики изменения населения "
                                              "региона/муниципалитета в %")
def chart_population_percent(
    session: SessionDep,
    id: int = Query(..., description="ID региона или муниципалитета"),
    type: str = Query(..., description="Тип: 'region' или 'municipality'"),
    year_from: int = Query(..., ge=2010, le=2035),
    year_to: int = Query(..., ge=2010, le=2035)
) -> dict:
    if type == "region":
        data = get_population_by_region(session, id, year_from, year_to)
    elif type == "municipality":
        data = get_municipalities_by_id(session, id, year_from, year_to)
    else:
        raise HTTPException(status_code=400, detail="Неверный тип")

    buffer = plot_population_percent_change(data, type, "api")
    if buffer is None:
        raise HTTPException(status_code=404, detail="Нет данных для построения графика")

    if buffer:
        base64_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return {"image_base64": base64_string}
    raise HTTPException(404, "График не создан")

@ch_router.get("/birth_rate", summary="Получить диаграмму динамики изменения коэффициента "
                                              "рождаемости региона/муниципалитета")
def chart_birth_rate(
    session: SessionDep,
    id: int = Query(..., description="ID региона или муниципалитета"),
    type: str = Query(..., description="Тип: 'region' или 'municipality'"),
    year_from: int = Query(..., ge=2010, le=2035),
    year_to: int = Query(..., ge=2010, le=2035)
) -> dict:
    if type == "region":
        data = get_population_by_region(session, id, year_from, year_to)
    elif type == "municipality":
        data = get_municipalities_by_id(session, id, year_from, year_to)
    else:
        raise HTTPException(status_code=400, detail="Неверный тип")

    buffer = plot_birth_rate(data, type)
    if buffer is None:
        raise HTTPException(status_code=404, detail="Нет данных для построения графика")

    if buffer:
        base64_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return {"image_base64": base64_string}
    raise HTTPException(404, "График не создан")

@ch_router.get("/mortality_rate", summary="Получить диаграмму динамики изменения коэффициента "
                                              "смертности региона/муниципалитета")
def chart_mortality_rate(
    session: SessionDep,
    id: int = Query(..., description="ID региона или муниципалитета"),
    type: str = Query(..., description="Тип: 'region' или 'municipality'"),
    year_from: int = Query(..., ge=2010, le=2035),
    year_to: int = Query(..., ge=2010, le=2035)
) -> dict:
    if type == "region":
        data = get_population_by_region(session, id, year_from, year_to)
    elif type == "municipality":
        data = get_municipalities_by_id(session, id, year_from, year_to)
    else:
        raise HTTPException(status_code=400, detail="Неверный тип")

    buffer = plot_mortality_rate(data, type)
    if buffer is None:
        raise HTTPException(status_code=404, detail="Нет данных для построения графика")

    if buffer:
        base64_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return {"image_base64": base64_string}
    raise HTTPException(404, "График не создан")

@ch_router.get("/natural_growth", summary="Получить диаграмму динамики изменения естественного "
                                              "прироста региона/муниципалитета")
def chart_natural_growth(
    session: SessionDep,
    id: int = Query(..., description="ID региона или муниципалитета"),
    type: str = Query(..., description="Тип: 'region' или 'municipality'"),
    year_from: int = Query(..., ge=2010, le=2035),
    year_to: int = Query(..., ge=2010, le=2035)
) -> dict:
    if type == "region":
        data = get_population_by_region(session, id, year_from, year_to)
    elif type == "municipality":
        data = get_municipalities_by_id(session, id, year_from, year_to)
    else:
        raise HTTPException(status_code=400, detail="Неверный тип")

    buffer = plot_natural_growth(data, type, "api")
    if buffer is None:
        raise HTTPException(status_code=404, detail="Нет данных для построения графика")

    if buffer:
        base64_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return {"image_base64": base64_string}
    raise HTTPException(404, "График не создан")

@ch_router.get("/migration", summary="Получить диаграмму динамики изменения миграционного "
                                              "прироста региона/муниципалитета")
def chart_migration(
    session: SessionDep,
    id: int = Query(..., description="ID региона или муниципалитета"),
    type: str = Query(..., description="Тип: 'region' или 'municipality'"),
    year_from: int = Query(..., ge=2010, le=2035),
    year_to: int = Query(..., ge=2010, le=2035)
) -> dict:
    if type == "region":
        data = get_population_by_region(session, id, year_from, year_to)
    elif type == "municipality":
        data = get_municipalities_by_id(session, id, year_from, year_to)
    else:
        raise HTTPException(status_code=400, detail="Неверный тип")

    buffer = plot_migration(data, type, "api")
    if buffer is None:
        raise HTTPException(status_code=404, detail="Нет данных для построения графика")

    if buffer:
        base64_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return {"image_base64": base64_string}
    raise HTTPException(404, "График не создан")