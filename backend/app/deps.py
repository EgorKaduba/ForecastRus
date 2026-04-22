from fastapi import Depends
from sqlmodel import Session

from typing import Annotated
from .core import db


def get_session():
    with Session(db.engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
