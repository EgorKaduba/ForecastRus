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

def create_report(id: int, type: str, year_from: int, year_to: int) -> str:
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
            data = get_municipalities_by_id(session, id, year_from, year_to)
        if len(data[0]['municipality_name'].split(' ')) == 1:
            pdf.cell(0, 10, text=f'{data[0]['municipality_type']} {data[0]['municipality_name']}', align='C')
            object_name = f'{data[0]['municipality_type']} {data[0]['municipality_name']}'
        else:
            pdf.cell(0, 10, text=f'{data[0]['municipality_name']}', align='C')
            object_name = data[0]['municipality_name']

    if type == 'region':
        with Session(engine) as session:
            data = get_population_by_region(session, id, year_from, year_to)

        pdf.cell(0, 10, text=f'{data[0]['region_name']}', align='C')
        object_name = data[0]['region_name']

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
    pdf.cell(0, 10, text=f'{year_from} - {year_to}', align='L')

    pdf.set_y(-35)

    pdf.cell(0, 10, text=f'Москва {formatted_date.split('.')[2]}', align='C')

    pdf.add_page()
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

    pdf.cell(0, 10, text='Таблица демографических показателей', align='C')

    current_y = pdf.get_y()
    pdf.set_y(current_y + 10)

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

    if year_from != year_to:
        pdf.set_font('TimesNewRoman', 'B', 14)
        pdf.ln(8)
        pdf.multi_cell(0, 10, text="Краткое резюме динамики населения", align='C')

        prompt = f"""
        Ты аналитик-демограф. Напиши краткое аналитическое резюме (3-5 предложений) 
        на русском языке о динамике населения региона на основе следующих данных:
    
        Данные по региону:
        - Период анализа: {year_from}-{year_to} гг.
        - Данные за период: {data}, где 'year' - год, population/total_population - Численность населения на 1 января
        соответствующего года, 'deaths' - Число умерших, 'births' - Число родившихся, 'migration' - Миграционный прирост, 
        Общий коэффициент смертности, на 1человеко-год, 'birth_rate' - общий коэффициент рождаемости, на 1 человеко-год,
        'migration_rate' - коэффициент миграционного прироста, на 1 человеко-год.
    
        Требования к ответу:
        1. Только текст, без маркдауна и лишних символов
        2. Начать с фразы: "За период с {year_from} по {year_to} год..."
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

    if not os.path.exists("reports"):
        os.makedirs("reports")

    pdf.output(f"reports/report {object_name} {year_from}-{year_to}.pdf")
    return f"reports/report {object_name} {year_from}-{year_to}.pdf"
