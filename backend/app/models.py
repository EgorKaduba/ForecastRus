from sqlmodel import SQLModel, Field


class Region(SQLModel, table=True):
    __tablename__ = "regions"
    __table_args__ = {"schema": "demography"}

    region_id: int | None = Field(default=None, primary_key=True)
    region_name: str = Field(index=True)
