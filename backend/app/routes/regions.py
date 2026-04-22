from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select

from ..deps import SessionDep
from ..models import Region

reg_router = APIRouter(
    prefix="/regions",
    tags=["Регионы"]
)


@reg_router.get("/", summary="Получить список всех субъектов РФ")
def read_regions(
        session: SessionDep,
        offset: int = 0,
        limit:int = Query(default=100, le=100)
) -> list[Region]:
    regions = list(session.exec(select(Region).offset(offset).limit(limit)).all())
    if regions:
        return regions
    raise HTTPException(status_code=404, detail="Субъекты не найдены")
