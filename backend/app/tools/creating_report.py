from typing import Union
from fastapi import HTTPException, Query
from ..core.db import engine
from sqlalchemy.orm import Session
from fpdf import FPDF
from datetime import date
from io import BytesIO
from .LLM_integration import LLM_request
from .charts import (plot_mortality_rate, plot_birth_rate, plot_population, plot_population_percent_change,
                     plot_migration, plot_natural_growth)
from .get_data import get_population_by_region, get_municipalities_by_id
import os



def center_image(pdf: FPDF, image_path: Union[str, BytesIO], width: int) -> None:
    page_width = 210
    x = (page_width - width) / 2
    pdf.image(image_path, x=x, w=width)


def creat_table(pdf: FPDF, type: str, data: list[dict]) -> None:
    pdf.set_font('TimesNewRoman', '', 10)
    headings = ['Год', 'Численность населения', 'Число родившихся',
                'Число умерших', 'Миграционный прирост', 'Коэффициент смертности',
                'Коэффициент рождаемости', 'Коэффициент миграционного прироста']

    with pdf.table(col_widths=[12, 21, 20, 16, 24, 20, 20, 24], line_height=4, padding=1, text_align='CENTER') as table:
        header = table.row()
        for head in headings:
            header.cell(head, align='C')
        if type == 'municipality':
            for item in data:
                row = table.row()
                row.cell(str(item['year']))
                row.cell(str(item['population']) if item['population'] else '-')
                row.cell(str(item['births']) if item['births'] else '-')
                row.cell(str(item['deaths']) if item['deaths'] else '-')
                row.cell(str(item['migration']) if item['migration'] else '-')
                row.cell(str(item['mortality_rate']) if item['mortality_rate'] else '-')
                row.cell(str(item['birth_rate']) if item['birth_rate'] else '-')
                row.cell(str(item['migration_rate']) if item['migration_rate'] else '-')

        if type == 'region':
            for item in data:
                row = table.row()
                row.cell(str(item['year']))
                row.cell(str(item['total_population']) if item['total_population'] else '-')
                row.cell(str(item['births']) if item['births'] else '-')
                row.cell(str(item['deaths']) if item['deaths'] else '-')
                row.cell(str(item['migration']) if item['migration'] else '-')
                row.cell(str(item['mortality_rate']) if item['mortality_rate'] else '-')
                row.cell(str(item['birth_rate']) if item['birth_rate'] else '-')
                row.cell(str(item['migration_rate']) if item['migration_rate'] else '-')

def add_charts(pdf: FPDF, data: list[dict], type: str) -> None:
    pdf.set_font('TimesNewRoman', 'B', 14)

    buffer = plot_population(data, type)
    if buffer:
        pdf.cell(0, 10, text='Диаграмма динамики изменения населения', align='C')
        pdf.ln(8)
        center_image(pdf, buffer, 160)

    buffer = plot_population_percent_change(data, type, "report")
    if buffer:
        pdf.cell(0, 10, text='Диаграмма динамики изменения населения (в %)', align='C')
        pdf.ln(8)
        center_image(pdf, buffer, 160)

    buffer = plot_birth_rate(data, type)
    if buffer:
        pdf.cell(0, 10, text='Диаграмма динамики изменения коэффициента рождаемости', align='C')
        pdf.ln(8)
        center_image(pdf, buffer, 160)

    buffer = plot_mortality_rate(data, type)
    if buffer:
        pdf.add_page()
        pdf.cell(0, 10, text='Диаграмма динамики изменения коэффициента смертности', align='C')
        pdf.ln(8)
        center_image(pdf, buffer, 160)

    buffer = plot_natural_growth(data, type, "report")
    if buffer:
        pdf.cell(0, 10, text='Диаграмма динамики изменения естественного прироста', align='C')
        pdf.ln(8)
        center_image(pdf, buffer, 160)

    buffer = plot_migration(data, type, "report")
    if buffer:
        pdf.cell(0, 10, text='Диаграмма динамики изменения миграционного прироста', align='C')
        pdf.ln(8)
        center_image(pdf, buffer, 160)


def create_compact_prompt_for_recommendations(monitoring_data: Union[list[dict], None], forecast_data: list[dict], object_name: str,
                                              year_from: int, year_to: int) -> str:
    if monitoring_data:
        first_pop = monitoring_data[0].get('total_population', monitoring_data[0].get('population', 0))
        last_hist_pop = monitoring_data[-1].get('total_population', monitoring_data[-1].get('population', 0))

        total_births = sum(d.get('births', 0) for d in monitoring_data)
        total_deaths = sum(d.get('deaths', 0) for d in monitoring_data)
        total_migration = sum(d.get('migration', 0) for d in monitoring_data)

        avg_birth = sum(d.get('birth_rate', 0) or 0 for d in monitoring_data) / len(monitoring_data)
        avg_mortality = sum(d.get('mortality_rate', 0) or 0 for d in monitoring_data) / len(monitoring_data)
    else:
        first_pop = last_hist_pop = total_births = total_deaths = total_migration = avg_birth = avg_mortality = 0


    prompt = f"""
Ты эксперт в области демографии, социальной политики и территориального планирования. 
На основе анализа демографических данных региона подготовь РЕКОМЕНДАЦИИ (5-7 предложений) 
по социальной политике и территориальному планированию.
Регион: {object_name}
Период: {year_from}-{2025}
Прогноз до {year_to}

Реальные данные:
- Население: {first_pop:,} → {last_hist_pop:,} чел.
- Средняя рождаемость: {avg_birth:.1f}‰
- Средняя смертность: {avg_mortality:.1f}‰
- Естественный прирост: {total_births - total_deaths:+,} чел.
- Миграция: {total_migration:+,} чел.
Если реальных данных нет, то сделай рекомендации основываясь на прогнозе

Прогнозные данные: {forecast_data}

Требования к ответу:
1. Только текст, без маркдауна и лишних символов
2. Начать с фразы: "На основе анализа демографической ситуации в {object_name}..."
3. Сказать пару слов о прогнозе
3. Учесть соотношение рождаемости/смертности и миграции
4. Дать конкретные рекомендации по направлениям:
   - Социальная политика (поддержка семей, здравоохранение, социальное обслуживание)
   - Территориальное планирование (размещение социальной инфраструктуры, жилищная политика)
5. Упомянуть миграционную политику, если миграция значительно влияет на динамику
6. Объём: 5-7 предложений, не более 800 символов
7. Профессиональный, конструктивный стиль
"""
    return prompt

def create_report(id: int, type: str, year_from: int, year_to: int) -> str:

    year_monitoring_to = 2025
    if year_to < year_monitoring_to:
        year_monitoring_to = year_to
    year_forecast_from = 2026
    if year_from > year_forecast_from:
        year_forecast_from = year_from
    pdf = FPDF()
    pdf.add_font('TimesNewRoman', '', 'fonts/TimesNewRomanRegular.ttf')
    pdf.add_font('TimesNewRoman', 'B', 'fonts/TimesNewRomanBold.ttf')
    pdf.add_page()
    pdf.set_font('TimesNewRoman', 'B', 16)

    center_image(pdf, 'images/logo.png', 70)

    pdf.multi_cell(0, 8, text='Некоммерческая платформа мониторинга и прогнозирования демографических показателей',
                   align='C')
    pdf.ln(0.1)
    pdf.cell(0, 8, text='«ForecastRus»', align='C')

    current_y = pdf.get_y()
    pdf.set_y(current_y + 70)

    pdf.cell(0, 10, text='«Отчет о численности населения»', align='C')
    pdf.ln(10)
    object_name = None
    if type == 'municipality':
        with Session(engine) as session:
            all_data = get_municipalities_by_id(session, id, year_from, year_to)
        if len(all_data[0]['municipality_name'].split(' ')) == 1:
            pdf.cell(0, 10,
                     text=f'{all_data[0]['municipality_type']} {all_data[0]['municipality_name']}',
                     align='C')
            object_name = f'{all_data[0]['municipality_type']} {all_data[0]['municipality_name']}'
        else:
            pdf.cell(0, 10, text=f'{all_data[0]['municipality_name']}', align='C')
            object_name = all_data[0]['municipality_name']

    if type == 'region':
        with Session(engine) as session:
            all_data = get_population_by_region(session, id, year_from, year_to)
        pdf.cell(0, 10, text=f'{all_data[0]['region_name']}', align='C')
        object_name = all_data[0]['region_name']



    current_y = pdf.get_y()
    pdf.set_y(current_y + 50)

    pdf.set_x(120)

    pdf.set_font('TimesNewRoman', '', 14)
    pdf.cell(0, 10, text='Дата генерации отчета:', align='L')

    pdf.ln(8)
    pdf.set_x(120)
    today = date.today()
    formatted_date = today.strftime("%d.%m.%Y")
    pdf.cell(0, 10, text=formatted_date, align='L')

    pdf.ln(8)
    pdf.set_x(120)
    pdf.cell(0, 10, text='Выбранный период для анализа:', align='L')

    pdf.ln(8)
    pdf.set_x(120)
    if year_from != year_to:
        pdf.cell(0, 10, text=f'{year_from} - {year_to}', align='L')
    else:
        pdf.cell(0, 10, text=f'{year_from}', align='L')

    pdf.set_y(-35)

    pdf.cell(0, 10, text=f'Москва {formatted_date.split('.')[2]}', align='C')

    if year_from <= year_monitoring_to:
        pdf.add_page()

        if type == 'municipality':
            with Session(engine) as session:
                monitoring_data = get_municipalities_by_id(session, id, year_from, year_monitoring_to)

        if type == 'region':
            with Session(engine) as session:
                monitoring_data = get_population_by_region(session, id, year_from, year_monitoring_to)

        add_charts(pdf, monitoring_data, type)

        pdf.cell(0, 10, text='Таблица демографических показателей', align='C')

        current_y = pdf.get_y()
        pdf.set_y(current_y + 10)

        creat_table(pdf, type, monitoring_data)

        if year_from != year_to:
            pdf.set_font('TimesNewRoman', 'B', 14)
            pdf.ln(8)
            pdf.multi_cell(0, 10, text="Краткое резюме динамики населения", align='C')

            prompt = f"""
            Ты аналитик-демограф. Напиши краткое аналитическое резюме (3-5 предложений) 
            на русском языке о динамике населения региона на основе следующих данных:
        
            Данные по региону:
            - Период анализа: {year_from}-{year_monitoring_to} гг.
            - Данные за период: {monitoring_data}, где 'year' - год, population/total_population - Численность населения на 1 января
            соответствующего года, 'deaths' - Число умерших, 'births' - Число родившихся, 'migration' - Миграционный прирост, 
            Общий коэффициент смертности, на 1человеко-год, 'birth_rate' - общий коэффициент рождаемости, на 1 человеко-год,
            'migration_rate' - коэффициент миграционного прироста, на 1 человеко-год.
        
            Требования к ответу:
            1. Только текст, без маркдауна и лишних символов
            2. Начать с фразы: "За период с {year_from} по {year_monitoring_to} год..."
            3. Упомянуть основные тенденции (рост/убыль)
            4. Отметить соотношение рождаемости и смертности
            5. Не более 500 символов
            6. Профессиональный, но доступный стиль
            """
            response = LLM_request(prompt)
            pdf.ln(0.1)
            current_x = pdf.get_x()
            pdf.set_x(current_x + 10)
            pdf.set_font('TimesNewRoman', '', 14)
            pdf.multi_cell(0, 10, text=f"              {response.replace('\u2011', '-')}", align='L')

    else:
        monitoring_data = None

    if year_to > year_monitoring_to:
        pdf.add_page()
        pdf.set_font('TimesNewRoman', 'B', 16)

        if year_forecast_from == year_to:
            pdf.cell(0, 10, text=f'Прогнозная оценка на {year_to} год', align='C')
        elif year_forecast_from > 2026:
            pdf.cell(0, 10, text=f'Прогнозная оценка c {year_forecast_from} до {year_to} года', align='C')
        else:
            pdf.cell(0, 10, text=f'Прогнозная оценка до {year_to} года', align='C')

        pdf.ln(8)

        if type == 'municipality':
            with Session(engine) as session:
                forecast_data = get_municipalities_by_id(session, id, year_forecast_from, year_to)

        if type == 'region':
            with Session(engine) as session:
                forecast_data = get_population_by_region(session, id, year_forecast_from, year_to)

        add_charts(pdf, all_data, type)

        pdf.cell(0, 10, text='Таблица демографических показателей', align='C')
        current_y = pdf.get_y()
        pdf.set_y(current_y + 10)

        creat_table(pdf, type, forecast_data)

        pdf.set_font('TimesNewRoman', 'B', 14)
        pdf.ln(8)
        pdf.multi_cell(0, 10, text="Рекомендации по социальной\nполитике и территориальному планированию", align='C')

        prompt = create_compact_prompt_for_recommendations(monitoring_data, forecast_data, object_name, year_from, year_to)

        response = LLM_request(prompt)
        if response is None:
            response = "Рекомендации временно недоступны. Пожалуйста, обратитесь к демографическим данным для анализа."
        pdf.ln(0.1)
        current_x = pdf.get_x()
        pdf.set_x(current_x + 10)
        pdf.set_font('TimesNewRoman', '', 14)
        pdf.multi_cell(0, 10, text=f"              {response.replace('\u2011', '-')}", align='L')



    if not os.path.exists("reports"):
        os.makedirs("reports")

    pdf.output(f"reports/report {object_name} {year_from}-{year_to}.pdf")
    return f"reports/report {object_name} {year_from}-{year_to}.pdf"
