import matplotlib
matplotlib.use('Agg')
from typing import Union
from matplotlib.font_manager import FontProperties
from io import BytesIO

import matplotlib.pyplot as plt



def plot_population(data: list[dict], type: str) -> Union[BytesIO, None]:
    if not data:
        print("Нет данных для построения графика")
        return None
    valid_data = None
    if type == "municipality":
        valid_data = [(item['year'], item['population']) for item in data
                      if item['population'] is not None]
    if type == "region":
        valid_data = [(item['year'], item['total_population']) for item in data
                      if item['total_population'] is not None]

    if not valid_data:
        print("Нет валидных данных для построения графика")
        return None

    if len(valid_data) == 1:
        return None

    years = [item[0] for item in valid_data]
    population = [item[1] for item in valid_data]

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(years, population, marker='o', linewidth=2, markersize=6, color='#00C0E8')
    ax.fill_between(years, population, alpha=0.3, color='#00C0E8')

    min_pop = min(population)
    max_pop = max(population)
    ax.set_ylim(min_pop - (max_pop - min_pop) * 0.1, max_pop + (max_pop - min_pop) * 0.1)

    custom_font = FontProperties(fname="fonts/Manrope-Bold.ttf", size=14)

    ax.set_xlabel("Год", fontproperties=custom_font, fontsize=12)
    ax.set_ylabel("Численность населения (чел.)", fontproperties=custom_font, fontsize=12)
    ax.grid(False)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#00B0FF')
    ax.spines['left'].set_color('#00B0FF')

    ax.tick_params(axis='x', color='#00B0FF', width=1)
    ax.tick_params(axis='y', color='#00B0FF', width=1)

    def format_population(value, pos):
        if value >= 1_000_000:
            return f'{value / 1_000_000:.2f} млн'
        elif value >= 1_000:
            return f'{value / 1_000:.1f} тыс'
        return f'{value:.0f}'

    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_population))

    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45)

    for year, pop in zip(years, population):
        if pop >= 1_000_000:
            pop_text = f'{pop / 1_000_000:.2f}M'
        elif pop >= 1_000:
            pop_text = f'{pop / 1_000:.1f}K'
        else:
            pop_text = str(pop)

        ax.annotate(pop_text, (year, pop), xytext=(15, 10), textcoords='offset points',
                    ha='center', fontsize=9, color='#00C0E8',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#00C0E8', alpha=1))

    x_min = min(years)
    x_max = max(years)
    x_margin = (x_max - x_min) * 0.05
    ax.set_xlim(x_min, x_max + x_margin)

    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.92)

    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)

    return buffer


def plot_population_percent_change(data: list[dict], type: str, for_what: str) -> Union[BytesIO, None]:
    if not data:
        print("Нет данных для построения графика")
        return None

    if type == "municipality":
        valid_data = [(item['year'], item['population']) for item in data
                      if item['population'] is not None]
    elif type == "region":
        valid_data = [(item['year'], item['total_population']) for item in data
                      if item['total_population'] is not None]
    else:
        print("Неверный тип данных")
        return None

    if not valid_data:
        print("Нет валидных данных для построения графика")
        return None

    if len(valid_data) == 1:
        return None

    years = [item[0] for item in valid_data]
    population = [item[1] for item in valid_data]

    base_population = population[0]
    percent_changes = [((pop - base_population) / base_population) * 100 for pop in population]

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(years, percent_changes, marker='o', linewidth=2, markersize=6, color='#00B0FF')

    if for_what == "report":
        ax.fill_between(years, percent_changes, 0,
                        where=[p >= 0 for p in percent_changes],
                        alpha=0.3, color='#00C040', interpolate=True)
        ax.fill_between(years, percent_changes, 0,
                        where=[p < 0 for p in percent_changes],
                        alpha=0.3, color='#FF4444', interpolate=True)
    if for_what == "api":
        ax.fill_between(years, percent_changes, 0,
                        alpha=0.3, color='#00C0E8', interpolate=True)
    ax.axhline(y=0, color='gray', linewidth=1, linestyle='--', alpha=0.7)

    min_percent = min(percent_changes)
    max_percent = max(percent_changes)
    margin = (max_percent - min_percent) * 0.15 if max_percent != min_percent else 5
    ax.set_ylim(min_percent - margin, max_percent + margin)

    custom_font = FontProperties(fname="fonts/Manrope-Bold.ttf", size=14)
    ax.set_xlabel("Год", fontproperties=custom_font, fontsize=12)
    ax.set_ylabel("Изменение (%)", fontproperties=custom_font, fontsize=12)
    ax.grid(False)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#00B0FF')
    ax.spines['left'].set_color('#00B0FF')
    ax.tick_params(axis='x', color='#00B0FF', width=1)
    ax.tick_params(axis='y', color='#00B0FF', width=1)

    def format_percent(value, pos):
        return f'{value:+.1f}%'

    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_percent))

    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45)

    if for_what == "report":
        for year, change in zip(years, percent_changes):
            if year != years[0]:
                sign = '+' if change >= 0 else ''
                change_text = f'{sign}{change:.1f}%'
                text_color = '#00C040' if change >= 0 else '#FF4444'
                offset = 12 if change >= 0 else -18

                ax.annotate(change_text, (year, change), xytext=(15, offset),
                            textcoords='offset points', ha='center', fontsize=9,
                            color=text_color,
                            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                      edgecolor=text_color, alpha=1))

    if for_what == "api":
        for year, change in zip(years, percent_changes):
            if year != years[0]:
                sign = '+' if change >= 0 else ''
                change_text = f'{sign}{change:.1f}%'
                text_color = '#00C0E8'
                offset = 12 if change >= 0 else -18

                ax.annotate(change_text, (year, change), xytext=(15, offset),
                            textcoords='offset points', ha='center', fontsize=9,
                            color=text_color,
                            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                      edgecolor=text_color, alpha=1))

    x_min = min(years)
    x_max = max(years)
    x_margin = (x_max - x_min) * 0.05
    ax.set_xlim(x_min, x_max + x_margin)

    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.92)

    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)

    return buffer


def plot_birth_rate(data: list[dict], type: str) -> Union[BytesIO, None]:
    if not data:
        print("Нет данных для построения графика")
        return None

    if type == "municipality":
        valid_data = [(item['year'], item['birth_rate']) for item in data
                      if item['birth_rate'] is not None]
    elif type == "region":
        valid_data = [(item['year'], item.get('avg_birth_rate', item.get('birth_rate'))) for item in data
                      if item.get('avg_birth_rate') is not None or item.get('birth_rate') is not None]
    else:
        print("Неверный тип данных")
        return None

    if not valid_data:
        print("Нет валидных данных для построения графика")
        return None

    if len(valid_data) == 1:
        return None

    years = [item[0] for item in valid_data]
    birth_rates = [item[1] for item in valid_data]

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(years, birth_rates, marker='o', linewidth=2, markersize=6, color='#00C0E8')
    ax.fill_between(years, birth_rates, alpha=0.3, color='#00C0E8')

    min_rate = min(birth_rates)
    max_rate = max(birth_rates)
    margin = (max_rate - min_rate) * 0.1 if max_rate != min_rate else 1
    ax.set_ylim(min_rate - margin, max_rate + margin)

    custom_font = FontProperties(fname="fonts/Manrope-Bold.ttf", size=14)
    ax.set_xlabel("Год", fontproperties=custom_font, fontsize=12)
    ax.set_ylabel("Коэффициент рождаемости (%)", fontproperties=custom_font, fontsize=12)
    ax.grid(False)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#00B0FF')
    ax.spines['left'].set_color('#00B0FF')

    ax.tick_params(axis='x', color='#00B0FF', width=1)
    ax.tick_params(axis='y', color='#00B0FF', width=1)

    def format_rate(value, pos):
        if value > 0.099:
            return f'{value:.1f}%'
        else:
            return f'{value:.3f}%'

    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_rate))

    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45)

    for year, rate in zip(years, birth_rates):
        if rate > 0.099:
            ax.annotate(f'{rate:.2f}%', (year, rate), xytext=(15, 10), textcoords='offset points',
                        ha='center', fontsize=9, color='#00C0E8',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#00C0E8', alpha=1))
        else:
            ax.annotate(f'{rate:.4f}%', (year, rate), xytext=(15, 10), textcoords='offset points',
                        ha='center', fontsize=9, color='#00C0E8',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#00C0E8', alpha=1))

    x_min = min(years)
    x_max = max(years)
    x_margin = (x_max - x_min) * 0.05
    ax.set_xlim(x_min, x_max + x_margin)

    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.92)

    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)

    return buffer


def plot_mortality_rate(data: list[dict], type: str) -> Union[BytesIO, None]:
    if not data:
        print("Нет данных для построения графика")
        return None

    if type == "municipality":
        valid_data = [(item['year'], item['mortality_rate']) for item in data
                      if item['mortality_rate'] is not None]
    elif type == "region":
        valid_data = [(item['year'], item.get('avg_mortality_rate', item.get('mortality_rate'))) for item in data
                      if item.get('avg_mortality_rate') is not None or item.get('mortality_rate') is not None]
    else:
        print("Неверный тип данных")
        return None

    if not valid_data:
        print("Нет валидных данных для построения графика")
        return None

    if len(valid_data) == 1:
        return None

    years = [item[0] for item in valid_data]
    mortality_rates = [item[1] for item in valid_data]

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(years, mortality_rates, marker='o', linewidth=2, markersize=6, color='#00C0E8')
    ax.fill_between(years, mortality_rates, alpha=0.3, color='#00C0E8')

    min_rate = min(mortality_rates)
    max_rate = max(mortality_rates)
    margin = (max_rate - min_rate) * 0.1 if max_rate != min_rate else 1
    ax.set_ylim(min_rate - margin, max_rate + margin)

    custom_font = FontProperties(fname="fonts/Manrope-Bold.ttf", size=14)
    ax.set_xlabel("Год", fontproperties=custom_font, fontsize=12)
    ax.set_ylabel("Коэффициент смертности (%)", fontproperties=custom_font, fontsize=12)
    ax.grid(False)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#00B0FF')
    ax.spines['left'].set_color('#00B0FF')

    ax.tick_params(axis='x', color='#00B0FF', width=1)
    ax.tick_params(axis='y', color='#00B0FF', width=1)

    def format_rate(value, pos):
        if value > 0.099:
            return f'{value:.1f}%'
        else:
            return f'{value:.3f}%'

    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_rate))

    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45)

    for year, rate in zip(years, mortality_rates):
        if rate > 0.099:
            ax.annotate(f'{rate:.2f}%', (year, rate), xytext=(15, 10), textcoords='offset points',
                        ha='center', fontsize=9, color='#00C0E8',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#00C0E8', alpha=1))
        else:
            ax.annotate(f'{rate:.4f}%', (year, rate), xytext=(15, 10), textcoords='offset points',
                        ha='center', fontsize=9, color='#00C0E8',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#00C0E8', alpha=1))

    x_min = min(years)
    x_max = max(years)
    x_margin = (x_max - x_min) * 0.05
    ax.set_xlim(x_min, x_max + x_margin)

    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.92)

    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)

    return buffer

def plot_natural_growth(data: list[dict], type: str, for_what: str) -> Union[BytesIO, None]:
    if not data:
        print("Нет данных для построения графика")
        return None

    if type == "municipality":
        valid_data = [(item['year'], item['births'], item['deaths']) for item in data
                      if item['births'] is not None and item['deaths'] is not None]
    elif type == "region":
        valid_data = [(item['year'], item.get('total_births', item.get('births')),
                       item.get('total_deaths', item.get('deaths'))) for item in data
                      if (item.get('total_births') is not None or item.get('births') is not None)
                      and (item.get('total_deaths') is not None or item.get('deaths') is not None)]
    else:
        print("Неверный тип данных")
        return None

    if not valid_data:
        print("Нет валидных данных для построения графика")
        return None

    if len(valid_data) == 1:
        return None

    years = [item[0] for item in valid_data]
    natural_growth = [(item[1] - item[2]) for item in valid_data]

    fig, ax = plt.subplots(figsize=(12, 6))

    for i in range(len(years) - 1):
        ax.plot([years[i], years[i + 1]], [natural_growth[i], natural_growth[i + 1]],
                linewidth=2, color='#00B0FF')

    ax.plot(years, natural_growth, marker='o', linewidth=2, markersize=6, color='#00B0FF')
    if for_what == "report":
        ax.fill_between(years, natural_growth, 0,
                        where=[p >= 0 for p in natural_growth],
                        alpha=0.3, color='#00C040', interpolate=True)
        ax.fill_between(years, natural_growth, 0,
                        where=[p < 0 for p in natural_growth],
                        alpha=0.3, color='#FF4444', interpolate=True)
    if for_what == "api":
        ax.fill_between(years, natural_growth, 0,
                        alpha=0.3, color='#00C0E8', interpolate=True)

    ax.axhline(y=0, color='gray', linewidth=1, linestyle='--', alpha=0.7)

    min_growth = min(natural_growth)
    max_growth = max(natural_growth)
    margin = (max_growth - min_growth) * 0.15 if max_growth != min_growth else 1000
    ax.set_ylim(min_growth - margin, max_growth + margin)

    custom_font = FontProperties(fname="fonts/Manrope-Bold.ttf", size=14)
    ax.set_xlabel("Год", fontproperties=custom_font, fontsize=12)
    ax.set_ylabel("Естественный прирост (чел.)", fontproperties=custom_font, fontsize=12)
    ax.grid(False)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#00B0FF')
    ax.spines['left'].set_color('#00B0FF')

    ax.tick_params(axis='x', color='#00B0FF', width=1)
    ax.tick_params(axis='y', color='#00B0FF', width=1)

    def format_growth(value, pos):
        if value >= 0:
            return f'+{value:,.0f}'
        return f'{value:,.0f}'

    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_growth))

    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45)

    if for_what == "report":
        for year, growth in zip(years, natural_growth):
            sign = '+' if growth >= 0 else ''
            growth_text = f'{sign}{growth:,.0f}'
            text_color = '#00C040' if growth >= 0 else '#FF4444'
            offset = 15 if growth >= 0 else -20

            ax.annotate(growth_text, (year, growth), xytext=(15, offset),
                        textcoords='offset points', ha='center', fontsize=9,
                        color=text_color,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                  edgecolor=text_color, alpha=1))

    if for_what == "api":
        for year, growth in zip(years, natural_growth):
            sign = '+' if growth >= 0 else ''
            growth_text = f'{sign}{growth:,.0f}'
            text_color = '#00C0E8'
            offset = 15 if growth >= 0 else -20

            ax.annotate(growth_text, (year, growth), xytext=(15, offset),
                        textcoords='offset points', ha='center', fontsize=9,
                        color=text_color,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                  edgecolor=text_color, alpha=1))

    x_min = min(years)
    x_max = max(years)
    x_margin = (x_max - x_min) * 0.05
    ax.set_xlim(x_min, x_max + x_margin)

    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.92)

    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)

    return buffer


def plot_migration(data: list[dict], type: str, for_what: str) -> Union[BytesIO, None]:
    if not data:
        print("Нет данных для построения графика")
        return None

    if type == "municipality":
        valid_data = [(item['year'], item['migration']) for item in data
                      if item['migration'] is not None]
    elif type == "region":
        valid_data = [(item['year'], item.get('total_migration', item.get('migration'))) for item in data
                      if item.get('total_migration') is not None or item.get('migration') is not None]
    else:
        print("Неверный тип данных")
        return None

    if not valid_data:
        print("Нет валидных данных для построения графика")
        return None

    if len(valid_data) == 1:
        return None

    years = [item[0] for item in valid_data]
    migration = [item[1] for item in valid_data]

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(years, migration, marker='o', linewidth=2, markersize=6, color='#00B0FF')

    if for_what == "report":
        ax.fill_between(years, migration, 0,
                        where=[p >= 0 for p in migration],
                        alpha=0.3, color='#00C040', interpolate=True)
        ax.fill_between(years, migration, 0,
                        where=[p < 0 for p in migration],
                        alpha=0.3, color='#FF4444', interpolate=True)
    if for_what == "api":
        ax.fill_between(years, migration, 0,
                        alpha=0.3, color='#00C0E8', interpolate=True)

    ax.axhline(y=0, color='gray', linewidth=1, linestyle='--', alpha=0.7)

    min_mig = min(migration)
    max_mig = max(migration)
    margin = (max_mig - min_mig) * 0.15 if max_mig != min_mig else 1000
    ax.set_ylim(min_mig - margin, max_mig + margin)

    custom_font = FontProperties(fname="fonts/Manrope-Bold.ttf", size=14)
    ax.set_xlabel("Год", fontproperties=custom_font, fontsize=12)
    ax.set_ylabel("Миграционный прирост (чел.)", fontproperties=custom_font, fontsize=12)
    ax.grid(False)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#00B0FF')
    ax.spines['left'].set_color('#00B0FF')

    ax.tick_params(axis='x', color='#00B0FF', width=1)
    ax.tick_params(axis='y', color='#00B0FF', width=1)

    def format_migration(value, pos):
        if value >= 0:
            return f'+{value:.0f}'
        return f'{value:.0f}'

    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_migration))

    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45)
    if for_what == "report":
        for year, mig in zip(years, migration):
            sign = '+' if mig >= 0 else ''
            mig_text = f'{sign}{mig:.0f}'
            text_color = '#00C040' if mig >= 0 else '#FF4444'
            offset = 15 if mig >= 0 else -20

            ax.annotate(mig_text, (year, mig), xytext=(15, offset),
                        textcoords='offset points', ha='center', fontsize=9,
                        color=text_color,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                  edgecolor=text_color, alpha=1))
    if for_what == "api":
        for year, mig in zip(years, migration):
            sign = '+' if mig >= 0 else ''
            mig_text = f'{sign}{mig:.0f}'
            text_color = '#00C0E8'
            offset = 15 if mig >= 0 else -20

            ax.annotate(mig_text, (year, mig), xytext=(15, offset),
                        textcoords='offset points', ha='center', fontsize=9,
                        color=text_color,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                  edgecolor=text_color, alpha=1))

    x_min = min(years)
    x_max = max(years)
    x_margin = (x_max - x_min) * 0.05
    ax.set_xlim(x_min, x_max + x_margin)

    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.92)

    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)

    return buffer