// SubjectInfo.jsx
import './SubjectInfo.css'

function SubjectInfo({ data, loading, error, onClose }) {
    if (loading) {
        return (
            <div className="subject-info loading">
                <div className="subject-info-header">
                    <h3>Загрузка данных...</h3>
                </div>
                <div className="spinner"></div>
            </div>
        )
    }

    if (error) {
        return (
            <div className="subject-info error">
                <div className="subject-info-header">
                    <h3>Ошибка</h3>
                    <button className="close-btn" onClick={onClose}>✕</button>
                </div>
                <div className="subject-info-content">
                    <p>{error}</p>
                </div>
            </div>
        )
    }

    if (!data) return null

    return (
        <div className="subject-info">
            <div className="subject-info-header">
                <h3>{data.region_name || 'Информация о субъекте'}</h3>
                <button className="close-btn" onClick={onClose}>✕</button>
            </div>
            <div className="subject-info-content">
                <div className="info-grid">
                    {/* Основная информация */}
                    <div className="info-item">
                        <span className="info-label">Год данных:</span>
                        <span className="info-value">{data.year || '—'}</span>
                    </div>

                    {data.total_population && (
                        <div className="info-item">
                            <span className="info-label">Численность населения:</span>
                            <span className="info-value">{data.total_population.toLocaleString()} чел.</span>
                        </div>
                    )}

                    {data.municipalities_count && (
                        <div className="info-item">
                            <span className="info-label">Количество муниципальных образований:</span>
                            <span className="info-value">{data.municipalities_count}</span>
                        </div>
                    )}

                    {/* Демографические показатели (если есть) */}
                    {data.total_births !== null && data.total_births !== undefined && (
                        <div className="info-item">
                            <span className="info-label">Рождаемость:</span>
                            <span className="info-value">{data.total_births.toLocaleString()} чел.</span>
                        </div>
                    )}

                    {data.total_deaths !== null && data.total_deaths !== undefined && (
                        <div className="info-item">
                            <span className="info-label">Смертность:</span>
                            <span className="info-value">{data.total_deaths.toLocaleString()} чел.</span>
                        </div>
                    )}

                    {data.avg_birth_rate !== null && data.avg_birth_rate !== undefined && (
                        <div className="info-item">
                            <span className="info-label">Средний коэффициент рождаемости:</span>
                            <span className="info-value">{data.avg_birth_rate}</span>
                        </div>
                    )}

                    {data.avg_mortality_rate !== null && data.avg_mortality_rate !== undefined && (
                        <div className="info-item">
                            <span className="info-label">Средний коэффициент смертности:</span>
                            <span className="info-value">{data.avg_mortality_rate}</span>
                        </div>
                    )}

                    {data.avg_migration_rate !== null && data.avg_migration_rate !== undefined && (
                        <div className="info-item">
                            <span className="info-label">Средний коэффициент миграции:</span>
                            <span className="info-value">{data.avg_migration_rate}</span>
                        </div>
                    )}

                    {data.total_migration !== null && data.total_migration !== undefined && (
                        <div className="info-item">
                            <span className="info-label">Миграционный прирост:</span>
                            <span className="info-value">{data.total_migration.toLocaleString()} чел.</span>
                        </div>
                    )}
                </div>

                {/* Дополнительная информация с ID региона */}
                <div className="additional-info">
                    <h4>Техническая информация</h4>
                    <ul>
                        <li><strong>ID региона:</strong> {data.region_id || '—'}</li>
                        <li><strong>ID агрегации региона:</strong> {data.region_agg_id || '—'}</li>
                    </ul>
                </div>
            </div>
        </div>
    )
}

export default SubjectInfo