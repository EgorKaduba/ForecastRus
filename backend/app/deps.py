from fastapi import Depends
from sqlmodel import Session

from collections.abc import Generator
from typing import Annotated
from .core import db


def get_session() -> Generator[Session, None, None]:
    with Session(db.engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
