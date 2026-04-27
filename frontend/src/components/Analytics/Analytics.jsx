import { useState } from "react";
import "./Analytics.css";

function Analytics({ selectedYear }) {
  const [isLoading, setIsLoading] = useState(false);

  const handleDownload = async () => {
    if (!selectedYear) {
      console.error("Год не выбран");
      return;
    }

    setIsLoading(true);

    try {
      // 1. Получаем путь к файлу от API
      const response = await fetch(`http://localhost:8000/api/v1/report?year=${selectedYear}`);

      if (!response.ok) {
        throw new Error(`Ошибка: ${response.status}`);
      }

      const data = await response.json();
      const fileUrl = data.report_url || data.file_path || data.url; // подставьте правильное поле

      // 2. Скачиваем файл по полученному пути
      const fileResponse = await fetch(fileUrl);
      const blob = await fileResponse.blob();

      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `analiticheskiy-otchet-${selectedYear}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(link.href);

    } catch (error) {
      console.error("Ошибка при скачивании отчёта:", error);
      alert("Не удалось скачать отчёт. Попробуйте позже.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
      <section className="analytics">
        <div className="analytics-container">
          <div className="analytics-content">
            <h1 className="analytics-title">АНАЛИТИЧЕСКАЯ ОТЧЕТНОСТЬ</h1>
            <p className="analytics-description">
              Для получения сводной информации по демографическим показателям за выбранный год скачайте аналитический отчёт
            </p>
          </div>

          <div
              className={`analytics-card ${isLoading ? 'loading' : ''}`}
              onClick={!isLoading ? handleDownload : undefined}
          >
            <div className="analytics-card-left">
            <span className="button-text">
              {isLoading ? "ЗАГРУЗКА..." : "отчетность"}
            </span>
              <div className="arrow-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
            </div>
            <div className="analytics-card-right"></div>
          </div>
        </div>
      </section>
  );
}

export default Analytics;