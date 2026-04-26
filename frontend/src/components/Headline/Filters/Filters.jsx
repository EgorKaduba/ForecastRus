import {useState, useEffect} from 'react'
import './Filters.css'
import FilterSelect from './FilterSelect.jsx'
import {
    fetchLands,
    fetchRegions,
    fetchArea,
    fetchRepublic
} from '../../../services/api.js'

function Filters({onYearChange}) {
    const [regions, setRegions] = useState([])
    const [lands, setLands] = useState([])
    const [areas, setAreas] = useState([])
    const [republics, setRepublics] = useState([])
    const [years, setYears] = useState([])

    const [selectedRegion, setSelectedRegion] = useState('')
    const [selectedLand, setSelectedLand] = useState('')
    const [selectedArea, setSelectedArea] = useState('')
    const [selectedRepublic, setSelectedRepublic] = useState('')
    const [selectedYear, setSelectedYear] = useState('2023')
    const [searchQuery, setSearchQuery] = useState('')
    const generateYearsList = () => {
        const startYear = 2010
        const endYear = 2023
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
    const handleYearChange = (value) => {
        setSelectedYear(value)
        if (onYearChange) {
            onYearChange(value)
        }
    }
    return (
        <div className="filters">
            <div className="filters-container">
                <FilterSelect
                    label="ВСЕ"
                    options={regions}
                    value={selectedRegion}
                    onChange={setSelectedRegion}
                />
                <FilterSelect
                    label="Край"
                    options={lands}
                    value={selectedLand}
                    onChange={setSelectedLand}
                />
                <FilterSelect
                    label="Область"
                    options={areas}
                    value={selectedArea}
                    onChange={setSelectedArea}
                />
                <FilterSelect
                    label="Республика"
                    options={republics}
                    value={selectedRepublic}
                    onChange={setSelectedRepublic}
                />

                <FilterSelect
                    label="ГОД"
                    options={years}
                    value={selectedYear}
                    onChange={handleYearChange}
                />

                <input
                    type="text"
                    className="filter-search"
                    placeholder="ПОИСК"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
            </div>
        </div>
    )
}

export default Filters