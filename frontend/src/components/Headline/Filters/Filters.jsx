// Filters.jsx - добавлен YearSelector
import { useState, useEffect } from 'react'
import './Filters.css'
import FilterSelect from './FilterSelect.jsx'
import YearSelector from './YearSelector.jsx'
import {
    fetchLands,
    fetchRegions,
    fetchArea,
    fetchRepublic
} from '../../../services/api.js'

function Filters({ onYearChange, onRegionChange, onSearch, onSearchEnter }) {
    const [regions, setRegions] = useState([])
    const [lands, setLands] = useState([])
    const [areas, setAreas] = useState([])
    const [republics, setRepublics] = useState([])
    const [years, setYears] = useState([])
    const [compareMode, setCompareMode] = useState('single')

    const [selectedRegion, setSelectedRegion] = useState('')
    const [selectedLand, setSelectedLand] = useState('')
    const [selectedArea, setSelectedArea] = useState('')
    const [selectedRepublic, setSelectedRepublic] = useState('')
    const [searchQuery, setSearchQuery] = useState('')

    const generateYearsList = () => {
        const startYear = 2010
        const endYear = 2035
        const yearsList = []
        for (let year = startYear; year <= endYear; year++) {
            yearsList.push(year.toString())
        }
        return yearsList
    }

    useEffect(() => {
        const loadData = async () => {
            const [
                regionData,
                landsData,
                areasData,
                republicsData
            ] = await Promise.all([
                fetchRegions(),
                fetchLands(),
                fetchArea(),
                fetchRepublic()
            ])
            setRegions(regionData)
            setLands(landsData)
            setAreas(areasData)
            setRepublics(republicsData)
            setYears(generateYearsList())
        }
        loadData()
    }, [])

    // Обработчик выбора КРАЯ
    const handleLandChange = (value) => {
        setSelectedLand(value)
        if (value) {
            // При выборе края сбрасываем область и республику
            setSelectedArea('')
            setSelectedRepublic('')
        }
    }

    // Обработчик выбора ОБЛАСТИ
    const handleAreaChange = (value) => {
        setSelectedArea(value)
        if (value) {
            // При выборе области сбрасываем край и республику
            setSelectedLand('')
            setSelectedRepublic('')
        }
    }

    // Обработчик выбора РЕСПУБЛИКИ
    const handleRepublicChange = (value) => {
        setSelectedRepublic(value)
        if (value) {
            // При выборе республики сбрасываем край и область
            setSelectedLand('')
            setSelectedArea('')
        }
    }

    const handleYearChangeWrapper = (yearData) => {
        if (onYearChange) {
            onYearChange(yearData)
        }
    }

    const handleCompareModeChange = (mode) => {
        setCompareMode(mode)
    }

    const handleSearchKeyPress = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault()
            const query = searchQuery.trim()
            if (query && onSearchEnter) {
                onSearchEnter(query)
            }
        }
    }

    const handleSearchChange = (e) => {
        const value = e.target.value
        setSearchQuery(value)
        if (onSearch) {
            onSearch(value)
        }
    }

    return (
        <div className="filters">
            <div className="filters-container">
                <YearSelector
                    years={years}
                    onYearChange={handleYearChangeWrapper}
                    onCompareMode={handleCompareModeChange}
                />

                <FilterSelect
                    label="ВСЕ"
                    options={regions}
                    value={selectedRegion}
                    onChange={setSelectedRegion}
                />
                <FilterSelect
                    label="КРАЙ"
                    options={lands}
                    value={selectedLand}
                    onChange={handleLandChange}
                />
                <FilterSelect
                    label="ОБЛАСТЬ"
                    options={areas}
                    value={selectedArea}
                    onChange={handleAreaChange}
                />
                <FilterSelect
                    label="РЕСПУБЛИКА"
                    options={republics}
                    value={selectedRepublic}
                    onChange={handleRepublicChange}
                />

                <div className="search-wrapper">
                    <img
                        src="/src/assets/search-icon.svg"
                        alt="поиск"
                        className="search-icon"
                    />
                    <input
                        type="text"
                        className="filter-search"
                        placeholder="ПОИСК"
                        value={searchQuery}
                        onChange={handleSearchChange}
                        onKeyPress={handleSearchKeyPress}
                    />
                </div>
            </div>
        </div>
    )
}

export default Filters