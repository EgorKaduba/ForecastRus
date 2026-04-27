import "./Analytics.css";
import analyticsPhoto from "../../assets/TopBG.png"; 

function Analytics() {
  const handleDownload = () => {
    // Ссылка на файл отчёта (замени на свой путь)
    const reportUrl = "/reports/demographic-report.pdf";
    const link = document.createElement("a");
    link.href = reportUrl;
    link.download = "analiticheskiy-otchet.pdf";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
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

        <div className="analytics-card" onClick={handleDownload}>
          <div className="analytics-card-left">
            <span className="button-text">отчетность</span>
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