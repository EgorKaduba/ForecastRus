from ..deps import SessionDep
from fastapi import HTTPException, Query
from sqlalchemy import select
from ..models import RegionAggregated, Region, DemographicData, Municipality


def get_population_by_region(session: SessionDep, region_id: int, year_from: int, year_to: int) -> list[dict]:
    query = select(
        RegionAggregated.year,
        RegionAggregated.total_population,
        Region.region_name,
        RegionAggregated.total_births,
        RegionAggregated.total_deaths,
        RegionAggregated.total_migration,
        RegionAggregated.avg_birth_rate,
        RegionAggregated.avg_mortality_rate,
        RegionAggregated.avg_migration_rate
    ).join(Region, RegionAggregated.region_id == Region.region_id)

    query = query.where(Region.region_id == region_id)
    query = query.where(RegionAggregated.year >= year_from)
    query = query.where(RegionAggregated.year <= year_to)
    query = query.order_by(RegionAggregated.year.asc())

    results = list(session.execute(query).all())

    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"Нет данных для региона ID={region_id} за {year_from}-{year_to} гг."
        )

    return [
        {
            'year': row.year,
            'total_population': row.total_population,
            'region_name': row.region_name,
            'births': row.total_births,
            'deaths': row.total_deaths,
            'migration': row.total_migration,
            'birth_rate': float(row.avg_birth_rate) if row.avg_birth_rate else None,
            'mortality_rate': float(row.avg_mortality_rate) if row.avg_mortality_rate else None,
            'migration_rate': float(row.avg_migration_rate) if row.avg_migration_rate else None
        }
        for row in results
    ]


def get_municipalities_by_id(session: SessionDep, municipality_id: int, year_from: int, year_to: int) -> list[dict]:
    query = select(
        DemographicData.year,
        DemographicData.population,
        DemographicData.avg_population,
        DemographicData.births,
        DemographicData.deaths,
        DemographicData.migration,
        DemographicData.birth_rate,
        DemographicData.mortality_rate,
        DemographicData.migration_rate,
        Municipality.municipality_id,
        Municipality.municipality_name,
        Municipality.mun_type,
        Region.region_name
    ).join(
        Municipality, DemographicData.municipality_id == Municipality.municipality_id
    ).join(
        Region, Municipality.region_id == Region.region_id
    )

    query = query.where(Municipality.municipality_id == municipality_id)
    query = query.where(DemographicData.year >= year_from)
    query = query.where(DemographicData.year <= year_to)

    query = query.order_by(DemographicData.year.asc())

    results = list(session.execute(query).all())

    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"Нет данных для муниципалитета ID={municipality_id} за {year_from}-{year_to} гг."
        )

    return [
        {
            'year': row.year,
            'municipality_id': row.municipality_id,
            'municipality_name': row.municipality_name,
            'municipality_type': row.mun_type,
            'region_name': row.region_name,
            'population': row.population,
            'avg_population': float(row.avg_population) if row.avg_population else None,
            'births': row.births,
            'deaths': row.deaths,
            'migration': row.migration,
            'birth_rate': float(row.birth_rate) if row.birth_rate else None,
            'mortality_rate': float(row.mortality_rate) if row.mortality_rate else None,
            'migration_rate': float(row.migration_rate) if row.migration_rate else None
        }
        for row in results
    ]