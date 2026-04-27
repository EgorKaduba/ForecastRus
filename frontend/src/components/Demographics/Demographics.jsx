import { useState, useEffect } from "react";
import "./Demographics.css";

function Demographics({ selectedYear }) {
  const [demographicsData, setDemographicsData] = useState(null);
  const [loading, setLoading] = useState(false);

  // Моковые данные (потом заменишь на API)
  const mockData = {
    2023: {
      year: "2023",
      population: "14.000.000",
      birthRate: "8.5",
      deathRate: "6.2",
      naturalIncrease: "2.3",
      migration: "1.8",
      populationDesc:
        "Численность населения выросла на 2.3% по сравнению с 2022 годом",
      birthDesc: "Рождаемость стабильно растёт благодаря мерам поддержки семей",
      deathDesc: "Смертность снизилась на 0.5% благодаря улучшению медицины",
      naturalDesc: "Естественный прирост положительный второй год подряд",
      migrationDesc:
        "Миграционный прирост обеспечил приток населения из регионов",
    },
    2022: {
      year: "2022",
      population: "13.680.000",
      birthRate: "7.8",
      deathRate: "6.8",
      naturalIncrease: "1.0",
      migration: "1.2",
      populationDesc: "Численность населения показала небольшой рост",
      birthDesc: "Рождаемость вернулась к допандемийным показателям",
      deathDesc: "Смертность остаётся на стабильном уровне",
      naturalDesc: "Естественный прирост незначительный, но положительный",
      migrationDesc: "Миграция компенсирует естественную убыль",
    },
    2021: {
      year: "2021",
      population: "13.400.000",
      birthRate: "7.2",
      deathRate: "7.5",
      naturalIncrease: "-0.3",
      migration: "0.8",
      populationDesc: "Численность населения снизилась из-за пандемии",
      birthDesc: "Рождаемость упала на фоне экономической нестабильности",
      deathDesc: "Смертность выросла в период пандемии",
      naturalDesc:
        "Естественная убыль населения зафиксирована впервые за 5 лет",
      migrationDesc: "Миграционный прирост частично компенсировал убыль",
    },
  };

  useEffect(() => {
    if (!selectedYear) return;

    setLoading(true);

    const timer = setTimeout(() => {
      const data = mockData[selectedYear] || mockData["2023"];
      setDemographicsData(data);
      setLoading(false);
    }, 300);

    return () => clearTimeout(timer);
  }, [selectedYear]);

  if (loading) {
    return (
      <section className="demographics">
        <div className="demographics-header">
          <h2 className="demographics-subtitle">Загрузка...</h2>
        </div>
      </section>
    );
  }

  if (!demographicsData) {
    return null; // не рендерим ничего, пока нет данных
  }

  const cards = [
    {
      id: 1,
      titleFirst: "Численность",
      titleSecond: "Населения",
      value: demographicsData.population,
      description: demographicsData.populationDesc,
    },
    {
      id: 2,
      titleFirst: "Коэффициент",
      titleSecond: "рождаемости",
      value: demographicsData.birthRate,
      description: demographicsData.birthDesc,
    },
    {
      id: 3,
      titleFirst: "Коэффициент",
      titleSecond: "смертности",
      value: demographicsData.deathRate,
      description: demographicsData.deathDesc,
    },
    {
      id: 4,
      titleFirst: "Естественный",
      titleSecond: "прирост",
      value: demographicsData.naturalIncrease,
      description: demographicsData.naturalDesc,
    },
    {
      id: 5,
      titleFirst: "Миграция",
      titleSecond: "",
      value: demographicsData.migration,
      description: demographicsData.migrationDesc,
    },
  ];

  return (
    <section className="demographics">
      <div className="demographics-header">
        <h2 className="demographics-subtitle">ДЕМОГРАФИЧЕСКИЕ</h2>
        <div className="demographics-title-wrapper">
          <span className="demographics-year">{demographicsData.year}</span>
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
                  {card.value}
                  {card.id !== 1 && card.id !== 5 && "‰"}
                  {card.id === 4 && parseFloat(card.value) > 0 && "+"}
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

export default Demographics;
