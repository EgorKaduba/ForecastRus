// SingleYearInfo.jsx
import './SubjectInfo.css'

function SingleYearInfo({ data, onClose }) {
    if (!data) return null

    return (
        <div className="subject-info">
            <div className="subject-info-header">
                <h3>{data.region_name} ({data.year})</h3>
                <button className="close-btn" onClick={onClose}>✕</button>
            </div>
            <div className="subject-info-content">
                <div className="info-grid">
                    <div className="info-item">
                        <span className="info-label">Численность населения:</span>
                        <span className="info-value">{data.total_population?.toLocaleString() || '—'} чел.</span>
                    </div>

                    {data.municipalities_count && (
                        <div className="info-item">
                            <span className="info-label">Муниципальных образований:</span>
                            <span className="info-value">{data.municipalities_count}</span>
                        </div>
                    )}

                    {data.total_births !== null && (
                        <div className="info-item">
                            <span className="info-label">Родилось:</span>
                            <span className="info-value">{data.total_births?.toLocaleString() || '—'} чел.</span>
                        </div>
                    )}

                    {data.total_deaths !== null && (
                        <div className="info-item">
                            <span className="info-label">Умерло:</span>
                            <span className="info-value">{data.total_deaths?.toLocaleString() || '—'} чел.</span>
                        </div>
                    )}

                    {data.total_migration !== null && (
                        <div className="info-item">
                            <span className="info-label">Миграционный прирост:</span>
                            <span className="info-value">
                                {data.total_migration > 0 ? '+' : ''}
                                {data.total_migration?.toLocaleString() || '—'} чел.
                            </span>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default SingleYearInfo