// YearSelector.jsx
import { useState } from 'react'
import './YearSelector.css'

function YearSelector({ years, onYearChange, onCompareMode }) {
    const [mode, setMode] = useState('single') // 'single' или 'compare'
    const [year1, setYear1] = useState('2023')
    const [year2, setYear2] = useState('2022')

    const handleModeChange = (newMode) => {
        setMode(newMode)
        if (onCompareMode) {
            onCompareMode(newMode)
        }

        if (newMode === 'single') {
            onYearChange(year1)
        } else {
            onYearChange({ year1, year2 })
        }
    }

    const handleYear1Change = (e) => {
        const value = e.target.value
        setYear1(value)
        if (mode === 'single') {
            onYearChange(value)
        } else {
            onYearChange({ year1: value, year2 })
        }
    }

    const handleYear2Change = (e) => {
        const value = e.target.value
        setYear2(value)
        onYearChange({ year1, year2: value })
    }

    return (
        <div className="year-selector">
            <div className="mode-buttons">
                <button
                    className={`mode-btn ${mode === 'single' ? 'active' : ''}`}
                    onClick={() => handleModeChange('single')}
                >
                    ОДИН ГОД
                </button>
                <button
                    className={`mode-btn ${mode === 'compare' ? 'active' : ''}`}
                    onClick={() => handleModeChange('compare')}
                >
                    СРАВНИТЬ ГОДА
                </button>
            </div>

            {mode === 'single' ? (
                <select
                    className="year-select"
                    value={year1}
                    onChange={handleYear1Change}
                >
                    {years.map(year => (
                        <option key={year} value={year}>{year}</option>
                    ))}
                </select>
            ) : (
                <div className="year-pair">
                    <select
                        className="year-select"
                        value={year1}
                        onChange={handleYear1Change}
                    >
                        {years.map(year => (
                            <option key={year} value={year}>{year}</option>
                        ))}
                    </select>
                    <select
                        className="year-select"
                        value={year2}
                        onChange={handleYear2Change}
                    >
                        {years.map(year => (
                            <option key={year} value={year}>{year}</option>
                        ))}
                    </select>
                </div>
            )}
        </div>
    )
}

export default YearSelector