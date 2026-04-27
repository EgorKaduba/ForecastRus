import { useState } from 'react'
import Header from '../components/Header/Header.jsx'
import Headline from '../components/Headline/Headline.jsx'
import Map from '../components/Map/Map.jsx'
import Analytics from '../components/Analytics/Analytics.jsx'
import SingleYearInfo from '../components/SubjectInfo/SingleYearInfo.jsx'
import CompareYearInfo from '../components/SubjectInfo/CompareYearInfo.jsx'
import TopRaiting from "../components/TopRaiting/TopRaiting.jsx";
import Demographics from "../components/Demographics/Demographics.jsx";
import { searchSubject } from '../services/api.js'
import './ForecastingPage.css'

function ForecastingPage() {
    const [selectedYear, setSelectedYear] = useState(2022);
    const [yearMode, setYearMode] = useState('single')
    const [yearData, setYearData] = useState({
        single: '2023',
        compare: { year1: '2023', year2: '2022' }
    })
    const [subjectData, setSubjectData] = useState(null)
    const [compareData, setCompareData] = useState({ year1: null, year2: null })
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [currentSubject, setCurrentSubject] = useState(null)

    const handleYearChange = (yearInfo) => {
        if (typeof yearInfo === 'string') {
            setYearMode('single')
            setYearData({ ...yearData, single: yearInfo })

            if (currentSubject) {
                handleSearchEnter(currentSubject, yearInfo)
            }
        } else {
            setYearMode('compare')
            setYearData({ ...yearData, compare: yearInfo })

            if (currentSubject) {
                handleCompareSearch(currentSubject, yearInfo.year1, yearInfo.year2)
            }
        }
    }

    const handleSearchEnter = async (query, specificYear = null) => {
        const yearToUse = specificYear || yearData.single
        setLoading(true)
        setError(null)
        setCurrentSubject(query)

        try {
            const data = await searchSubject(query, yearToUse)

            if (data && data.region_name) {
                if (yearMode === 'single') {
                    setSubjectData(data)
                    setCompareData({ year1: null, year2: null })
                }
            } else {
                setError(`Субъект "${query}" не найден за ${yearToUse} год`)
            }
        } catch (err) {
            console.error('Ошибка поиска:', err)
            setError('Произошла ошибка при поиске')
        } finally {
            setLoading(false)
        }
    }

    const handleCompareSearch = async (query, year1, year2) => {
        setLoading(true)
        setError(null)
        setCurrentSubject(query)

        try {
            const [data1, data2] = await Promise.all([
                searchSubject(query, year1),
                searchSubject(query, year2)
            ])

            if (data1 && data1.region_name && data2 && data2.region_name) {
                setCompareData({ year1: data1, year2: data2 })
                setSubjectData(null)
            } else {
                setError(`Данные для "${query}" не найдены за ${year1} или ${year2} год`)
            }
        } catch (err) {
            console.error('Ошибка поиска:', err)
            setError('Произошла ошибка при поиске')
        } finally {
            setLoading(false)
        }
    }

    const handleSearch = (query) => {
        if (yearMode === 'single') {
            handleSearchEnter(query)
        } else {
            handleCompareSearch(query, yearData.compare.year1, yearData.compare.year2)
        }
    }

    const handleCloseInfo = () => {
        setSubjectData(null)
        setCompareData({ year1: null, year2: null })
        setError(null)
        setCurrentSubject(null)
    }

    return (
        <>
            <Header />
            <div className="forecasting-container">
                <Headline
                    onYearChange={handleYearChange}
                    onSearchEnter={handleSearch}
                />
                <Map selectedYear={yearMode === 'single' ? yearData.single : yearData.compare.year1} />
                {selectedYear && (
                    <>
                        <TopRaiting selectedYear={selectedYear} />
                        <Demographics selectedYear={selectedYear} />
                        <Analytics selectedYear={selectedYear}/>
                    </>
                )}
                

                {loading && (
                    <div className="subject-info loading">
                        <div className="subject-info-header">
                            <h3>Загрузка данных...</h3>
                        </div>
                        <div className="spinner"></div>
                    </div>
                )}

                {error && (
                    <div className="subject-info error">
                        <div className="subject-info-header">
                            <h3>Ошибка</h3>
                            <button className="close-btn" onClick={handleCloseInfo}>✕</button>
                        </div>
                        <div className="subject-info-content">
                            <p>{error}</p>
                        </div>
                    </div>
                )}

                {!loading && !error && yearMode === 'single' && subjectData && (
                    <SingleYearInfo data={subjectData} onClose={handleCloseInfo} />
                )}

                {!loading && !error && yearMode === 'compare' && compareData.year1 && compareData.year2 && (
                    <CompareYearInfo
                        dataYear1={compareData.year1}
                        dataYear2={compareData.year2}
                        onClose={handleCloseInfo}
                    />
                )}
            </div>
        </>
    )
}

export default ForecastingPage