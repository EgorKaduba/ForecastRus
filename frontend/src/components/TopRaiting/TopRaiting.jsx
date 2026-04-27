// TopRaiting.jsx
import { useState, useEffect } from "react";
import "./TopRaiting.css";

function TopRaiting({ selectedYear }) {
  const [declineData, setDeclineData] = useState([]);
  const [growthData, setGrowthData] = useState([]);
  const [loading, setLoading] = useState(false);

  const mockData = {
    "2023": {
      decline: [
        { city: "Москва", percent: -10 },
        { city: "Чебоксары", percent: -20 },
        { city: "Мурманск", percent: -15 },
      ],
      growth: [
        { city: "Москва", percent: 100 },
        { city: "Чебоксары", percent: 20 },
        { city: "Мурманск", percent: 0 },
      ],
    },
    "2022": {
      decline: [
        { city: "Санкт-Петербург", percent: -8 },
        { city: "Казань", percent: -12 },
        { city: "Новосибирск", percent: -5 },
      ],
      growth: [
        { city: "Краснодар", percent: 25 },
        { city: "Сочи", percent: 15 },
        { city: "Екатеринбург", percent: 10 },
      ],
    },
    "2021": {
      decline: [
        { city: "Нижний Новгород", percent: -3 },
        { city: "Самара", percent: -7 },
        { city: "Омск", percent: -2 },
      ],
      growth: [
        { city: "Грозный", percent: 30 },
        { city: "Махачкала", percent: 18 },
        { city: "Тюмень", percent: 12 },
      ],
    },
    "2020": {
      decline: [
        { city: "Ростов-на-Дону", percent: -4 },
        { city: "Уфа", percent: -6 },
        { city: "Волгоград", percent: -1 },
      ],
      growth: [
        { city: "Севастополь", percent: 22 },
        { city: "Симферополь", percent: 14 },
        { city: "Калининград", percent: 8 },
      ],
    },
  };


  useEffect(() => {
    if (!selectedYear) return;
    
    setLoading(true);
    
    // Имитация загрузки с API
    setTimeout(() => {
      const data = mockData[selectedYear] || mockData["2023"];
      setDeclineData(data.decline);
      setGrowthData(data.growth);
      setLoading(false);
    }, 300);
  }, [selectedYear]);

  return (
    <section className="top-raiting">
      <div className="top-container">
        <div className="top-header">
          <h1 className="top-title">ТОП–5 МУНИЦИПАЛИТЕТОВ</h1>
          <h2 className="top-subtitle">По росту и снижению населения</h2>
        </div>

        {loading ? (
          <div className="loading-spinner">Загрузка...</div>
        ) : (
          <div className="top-tables">
            {/* Таблица снижения */}
            <div className="top-table decline-table">
              <div className="table-header decline-header">
                <span className="header-title">Снижение</span>
              </div>
              <div className="table-row header-row">
                <div className="cell city-cell">Город</div>
                <div className="cell percent-cell">Процент</div>
              </div>
              {declineData.map((item, index) => (
                <div className="table-row" key={index}>
                  <div className="cell city-cell">{item.city}</div>
                  <div className="cell percent-cell">{item.percent}%</div>
                </div>
              ))}
            </div>

            {/* Таблица роста */}
            <div className="top-table growth-table">
              <div className="table-header growth-header">
                <span className="header-title">Рост</span>
              </div>
              <div className="table-row header-row">
                <div className="cell city-cell">Город</div>
                <div className="cell percent-cell">Процент</div>
              </div>
              {growthData.map((item, index) => (
                <div className="table-row" key={index}>
                  <div className="cell city-cell">{item.city}</div>
                  <div className="cell percent-cell">{item.percent}%</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}

export default TopRaiting;