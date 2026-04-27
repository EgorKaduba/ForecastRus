// CompareYearInfo.jsx
import './SubjectInfo.css'

function CompareYearInfo({ dataYear1, dataYear2, onClose }) {
    if (!dataYear1 || !dataYear2) return null

    const calculateDifference = (value1, value2, isPercentage = false) => {
        if (value1 === null || value2 === null) return null
        const diff = value2 - value1
        if (isPercentage) {
            return ((diff / value1) * 100).toFixed(1)
        }
        return diff
    }

    const getDiffClass = (diff) => {
        if (diff > 0) return 'positive'
        if (diff < 0) return 'negative'
        return 'neutral'
    }

    return (
        <div className="subject-info compare">
            <div className="subject-info-header">
                <h3>Сравнение: {dataYear1.region_name}</h3>
                <button className="close-btn" onClick={onClose}>✕</button>
            </div>

            <div className="compare-table">
                <table>
                    <thead>
                    <tr>
                        <th>Показатель</th>
                        <th>{dataYear1.year}</th>
                        <th>{dataYear2.year}</th>
                        <th>Изменение</th>
                    </tr>
                    </thead>
                    <tbody>
                    {/* Численность населения */}
                    <tr>
                        <td>Численность населения</td>
                        <td>{dataYear1.total_population?.toLocaleString() || '—'}</td>
                        <td>{dataYear2.total_population?.toLocaleString() || '—'}</td>
                        <td className={getDiffClass(calculateDifference(
                            dataYear1.total_population,
                            dataYear2.total_population
                        ))}>
                            {calculateDifference(dataYear1.total_population, dataYear2.total_population) > 0 ? '+' : ''}
                            {calculateDifference(dataYear1.total_population, dataYear2.total_population)?.toLocaleString() || '—'}
                            {dataYear1.total_population && (
                                <span className="percentage">
                                        ({calculateDifference(
                                    dataYear1.total_population,
                                    dataYear2.total_population,
                                    true
                                )}%)
                                    </span>
                            )}
                        </td>
                    </tr>

                    {/* Рождаемость */}
                    {dataYear1.total_births !== null && dataYear2.total_births !== null && (
                        <tr>
                            <td>Родилось</td>
                            <td>{dataYear1.total_births?.toLocaleString() || '—'}</td>
                            <td>{dataYear2.total_births?.toLocaleString() || '—'}</td>
                            <td className={getDiffClass(calculateDifference(
                                dataYear1.total_births,
                                dataYear2.total_births
                            ))}>
                                {calculateDifference(dataYear1.total_births, dataYear2.total_births) > 0 ? '+' : ''}
                                {calculateDifference(dataYear1.total_births, dataYear2.total_births)?.toLocaleString() || '—'}
                            </td>
                        </tr>
                    )}

                    {/* Смертность */}
                    {dataYear1.total_deaths !== null && dataYear2.total_deaths !== null && (
                        <tr>
                            <td>Умерло</td>
                            <td>{dataYear1.total_deaths?.toLocaleString() || '—'}</td>
                            <td>{dataYear2.total_deaths?.toLocaleString() || '—'}</td>
                            <td className={getDiffClass(calculateDifference(
                                dataYear1.total_deaths,
                                dataYear2.total_deaths
                            ))}>
                                {calculateDifference(dataYear1.total_deaths, dataYear2.total_deaths) > 0 ? '+' : ''}
                                {calculateDifference(dataYear1.total_deaths, dataYear2.total_deaths)?.toLocaleString() || '—'}
                            </td>
                        </tr>
                    )}

                    {/* Естественный прирост */}
                    {dataYear1.total_births !== null && dataYear1.total_deaths !== null &&
                        dataYear2.total_births !== null && dataYear2.total_deaths !== null && (
                            <tr className="highlight">
                                <td>Естественный прирост</td>
                                <td>
                                    {((dataYear1.total_births || 0) - (dataYear1.total_deaths || 0)).toLocaleString()}
                                </td>
                                <td>
                                    {((dataYear2.total_births || 0) - (dataYear2.total_deaths || 0)).toLocaleString()}
                                </td>
                                <td className={getDiffClass(
                                    ((dataYear2.total_births || 0) - (dataYear2.total_deaths || 0)) -
                                    ((dataYear1.total_births || 0) - (dataYear1.total_deaths || 0))
                                )}>
                                    {((dataYear2.total_births || 0) - (dataYear2.total_deaths || 0) -
                                        ((dataYear1.total_births || 0) - (dataYear1.total_deaths || 0))) > 0 ? '+' : ''}
                                    {((dataYear2.total_births || 0) - (dataYear2.total_deaths || 0) -
                                        ((dataYear1.total_births || 0) - (dataYear1.total_deaths || 0))).toLocaleString()}
                                </td>
                            </tr>
                        )}

                    {/* Миграция */}
                    {dataYear1.total_migration !== null && dataYear2.total_migration !== null && (
                        <tr>
                            <td>Миграционный прирост</td>
                            <td>
                                {dataYear1.total_migration > 0 ? '+' : ''}
                                {dataYear1.total_migration?.toLocaleString() || '—'}
                            </td>
                            <td>
                                {dataYear2.total_migration > 0 ? '+' : ''}
                                {dataYear2.total_migration?.toLocaleString() || '—'}
                            </td>
                            <td className={getDiffClass(calculateDifference(
                                dataYear1.total_migration,
                                dataYear2.total_migration
                            ))}>
                                {calculateDifference(dataYear1.total_migration, dataYear2.total_migration) > 0 ? '+' : ''}
                                {calculateDifference(dataYear1.total_migration, dataYear2.total_migration)?.toLocaleString() || '—'}
                            </td>
                        </tr>
                    )}
                    </tbody>
                </table>
            </div>
        </div>
    )
}

export default CompareYearInfo