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
        limit: int = Query(default=100, le=100)
) -> list[Municipality]:
    municipalities = list(session.exec(select(Municipality).offset(offset).limit(limit)).all())
    if not municipalities:
        raise HTTPException(status_code=404, detail="Муниципалитеты не найдены")
    return municipalities
