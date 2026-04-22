from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select

from ..deps import SessionDep
from ..models import Municipality

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

@mun_router.get("/{municipality_name}", summary="Поиск муниципалитета по названию")
def read_municipality(
    municipality_name: str,
    session: SessionDep
) -> Municipality:
    municipality = session.exec(select(Municipality).where(Municipality.municipality_name == municipality_name)).first()
    if not municipality:
        raise HTTPException(status_code=404, detail=f"Муниципалитет с названием [{municipality_name}] не найден")
    return municipality
