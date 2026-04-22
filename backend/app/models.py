from sqlmodel import SQLModel, Field


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
    year: int
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
