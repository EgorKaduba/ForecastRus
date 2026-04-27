// Demographics.jsx
import "./Demographics.css";

function Demographics({
                        subjectData,      // данные выбранного субъекта (один год)
                        compareData,      // данные для сравнения (два года)
                        loading,          // флаг загрузки поиска
                        error,            // ошибка поиска
                        onCloseSubject    // закрытие
                      }) {

  // Если нет данных субъекта и нет режима сравнения — НИЧЕГО НЕ ПОКАЗЫВАЕМ
  if (!subjectData && !compareData) {
    return null;
  }

  // Функция для расчета коэффициента на 1000 человек
  const calculateRate = (value, population) => {
    if (!value || !population || population === 0) return null;
    return ((value / population) * 1000).toFixed(1);
  };

  // Если идёт загрузка поиска
  if (loading) {
    return (
        <section className="demographics">
          <div className="demographics-header">
            <h2 className="demographics-subtitle">ДЕМОГРАФИЧЕСКИЕ</h2>
            <div className="demographics-title-wrapper">
            <span className="demographics-year">
              {subjectData?.year || compareData?.year1?.year || '—'}
            </span>
              <h1 className="demographics-title">Характеристики</h1>
            </div>
          </div>
          <div className="demographics-loading">
            <div className="spinner"></div>
          </div>
        </section>
    );
  }

  // Если ошибка поиска
  if (error) {
    return (
        <section className="demographics">
          <div className="demographics-header">
            <h2 className="demographics-subtitle">ДЕМОГРАФИЧЕСКИЕ</h2>
            <div className="demographics-title-wrapper">
            <span className="demographics-year">
              {subjectData?.year || compareData?.year1?.year || '—'}
            </span>
              <h1 className="demographics-title">Характеристики</h1>
            </div>
          </div>
          <div className="demographics-error-content">
            <p>{error}</p>
          </div>
        </section>
    );
  }

  // Режим сравнения (если нужен будет позже)
  if (compareData && compareData.year1 && compareData.year2) {
    // TODO: режим сравнения
    return null;
  }

  // Режим одного года (данные субъекта)
  if (subjectData) {
    const population = subjectData.total_population;

    // Рассчитываем коэффициенты на 1000 человек
    const birthRate = calculateRate(subjectData.total_births, population);
    const deathRate = calculateRate(subjectData.total_deaths, population);
    const naturalIncreaseRate = calculateRate(
        (subjectData.total_births || 0) - (subjectData.total_deaths || 0),
        population
    );
    const migrationRate = calculateRate(subjectData.total_migration, population);

    const cards = [
      {
        id: 1,
        titleFirst: "Численность",
        titleSecond: "Населения",
        value: population?.toLocaleString(),
        unit: "чел.",
        description: `Численность населения за ${subjectData.year} год`,
      },
      {
        id: 2,
        titleFirst: "Коэффициент",
        titleSecond: "рождаемости",
        value: birthRate,
        unit: "‰",
        description: `Количество родившихся на 1000 человек за ${subjectData.year} год`,
      },
      {
        id: 3,
        titleFirst: "Коэффициент",
        titleSecond: "смертности",
        value: deathRate,
        unit: "‰",
        description: `Количество умерших на 1000 человек за ${subjectData.year} год`,
      },
      {
        id: 4,
        titleFirst: "Естественный",
        titleSecond: "прирост",
        value: naturalIncreaseRate,
        unit: "‰",
        description: `Естественный прирост на 1000 человек за ${subjectData.year} год`,
      },
      {
        id: 5,
        titleFirst: "Миграция",
        titleSecond: "",
        value: migrationRate,
        unit: "‰",
        description: `Миграционный прирост на 1000 человек за ${subjectData.year} год`,
      },
    ];

    return (
        <section className="demographics">
          <div className="demographics-header">
            <h2 className="demographics-subtitle">ДЕМОГРАФИЧЕСКИЕ</h2>
            <div className="demographics-title-wrapper">
              <span className="demographics-year">{subjectData.year}</span>
              <h1 className="demographics-title">Характеристики</h1>
            </div>
          </div>

          <div className="demographics-grid">
            {cards.map((card) => (
                <div key={card.id} className="demographics-card">
                  <div className="card-content">
                    <div className="card-titles">
                      <span className="card-title-first">{card.titleFirst}</span>
                      {card.titleSecond && (
                          <span className="card-title-second">{card.titleSecond}</span>
                      )}
                    </div>
                    <div className="card-value-wrapper">
                  <span className="card-value">
                    {card.value || '—'}
                    {card.value && card.value !== '—' && ` ${card.unit}`}
                    {card.id === 4 && parseFloat(card.value) > 0 && card.value !== '—' && (card.value.startsWith('-') ? '' : '+')}
                  </span>
                    </div>
                    <p className="card-description">{card.description}</p>
                  </div>
                </div>
            ))}
          </div>
        </section>
    );
  }

  return null;
}

export default Demographics;