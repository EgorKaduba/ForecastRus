from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class Region(SQLModel, table=True):
    __tablename__ = "regions"
    __table_args__ = {"schema": "demography"}

    region_id: int | None = Field(default=None, primary_key=True)
    region_name: str = Field(index=True)


class RegionAggregated(SQLModel, table=True):
    __tablename__ = "region_aggregated"
    __table_args__ = {"schema": "demography"}

    region_agg_id: int | None = Field(default=None, primary_key=True)
    region_id: int | None = Field(default=None, foreign_key="regions.region_id")
    year: int = Field(index=True)
    total_population: int = Field(default=0)
    total_births: int = Field(default=0)
    total_deaths: int = Field(default=0)
    total_migration: int = Field(default=0)
    avg_birth_rate: float = Field(default=0.0, max_digits=10, decimal_places=3)
    avg_mortality_rate: float = Field(default=0.0, max_digits=10, decimal_places=3)
    avg_migration_rate: float = Field(default=0.0, max_digits=10, decimal_places=3)
    municipalities_count: int = Field(default=0)


class RegionDataWithName(RegionAggregated):
    region_name: str | None = Field(default=None)


class Municipality(SQLModel, table=True):
    __tablename__ = "municipalities"
    __table_args__ = {"schema": "demography"}

    municipality_id: int | None = Field(default=None, primary_key=True)
    oktmo_code: str
    municipality_name: str
    region_id: int | None = Field(default=None, foreign_key="regions.region_id")
    mun_type: str
    is_zato: bool = Field(default=False)


class DemographicData(SQLModel, table=True):
    __tablename__ = "demographic_data"
    __table_args__ = {"schema": "demography"}

    data_id: int | None = Field(default=None, primary_key=True)
    municipality_id: int | None = Field(default=None, foreign_key="municipalities.municipality_id")
    year: int = Field(index=True)
    population: int = Field(default=0)
    avg_population: float = Field(default=0.0, max_digits=12, decimal_places=1)
    births: int = Field(default=0)
    deaths: int = Field(default=0)
    migration: int = Field(default=0)
    birth_rate: float = Field(default=0.0, max_digits=10, decimal_places=3)
    mortality_rate: float = Field(default=0.0, max_digits=10, decimal_places=3)
    migration_rate: float = Field(default=0.0, max_digits=10, decimal_places=3)


class DemographicDataWithName(DemographicData):
    municipality_name: str


class RegionColor(BaseModel):
    code: str
    name: str
    population: int
    color: str
