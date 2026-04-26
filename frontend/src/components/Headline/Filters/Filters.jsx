import { useState, useEffect } from 'react'
import './Filters.css'
import FilterSelect from './FilterSelect.jsx'
import {
    fetchLands,
    fetchRegions,
    fetchArea,
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
    const [searchQuery, setSearchQuery] = useState('')

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