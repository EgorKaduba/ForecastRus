from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select
import os

from ..tools.creating_report import get_population_by_region, get_municipalities_by_id, create_report
from ..deps import SessionDep

rep_router = APIRouter(
    prefix="/report",
    tags=["Отчет"]
)

@rep_router.get("/", summary="Сгенерировать отчет")
def generate_report(
        session: SessionDep,
        id: int = Query(..., description="ID региона или муниципалитета"),
        type: str = Query(..., description="Тип: 'region' или 'municipality'"),
        year_from: int = Query(..., ge=2010, le=2035),
        year_to: int = Query(..., ge=2010, le=2035)
) -> str:
    try:
        if type == "region":
            data = get_population_by_region(session, id, year_from, year_to)
        elif type == "municipality":
            data = get_municipalities_by_id(session, id, year_from, year_to)
        else:
            raise HTTPException(status_code=400, detail="Неверный тип. Используйте 'region' или 'municipality'")

        if not data:
            raise HTTPException(status_code=404, detail="Нет данных для указанного периода")

        file_name = create_report(id, type, year_from, year_to)

        path = file_name
        if os.path.exists(path):
            return path
        else:
            raise HTTPException(status_code=500, detail="Ошибка при генерации отчёта")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")