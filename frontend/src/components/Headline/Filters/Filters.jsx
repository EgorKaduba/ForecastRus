import { useState, useEffect } from 'react'
import './Filters.css'
import FilterSelect from './FilterSelect.jsx'
import {
    fetchLands,
    fetchRegions,
    fetchArea,
    fetchFederalCity,
    fetchRepublic
} from '../../../services/api.js'

function Filters() {
    const [regions, setRegions] = useState([])
    const [lands, setLands] = useState([])
    const [areas, setAreas] = useState([])
    const [republics, setRepublics] = useState([])
    const [federalCity, setFederalCity] = useState([])

    const [selectedRegion, setSelectedRegion] = useState('')
    const [selectedLand, setSelectedLand] = useState('')
    const [selectedArea, setSelectedArea] = useState('')
    const [selectedRepublic, setSelectedRepublic] = useState('')
    const [selectedFederalCity, setSelectedFederalCity] = useState('')
    const [searchQuery, setSearchQuery] = useState('')

    useEffect(() => {
        const loadData = async () => {
            const [
                regionData,
                landsData,
                areasData,
                republicsData,
                federalCityData
            ] = await Promise.all([
                fetchRegions(),
                fetchLands(),
                fetchArea(),
                fetchRepublic(),
                fetchFederalCity()
            ])
            setRegions(regionData)
            setLands(landsData)
            setAreas(areasData)
            setRepublics(republicsData)
            setFederalCity(federalCityData)
        }
        loadData()
    }, [])

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
                    label="Город ФН"
                    options={federalCity}
                    value={selectedFederalCity}
                    onChange={setSelectedFederalCity}
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