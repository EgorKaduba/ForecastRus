// Headline.jsx
import './Headline.css'
import Filters from './Filters/Filters.jsx'
import Heading from "./Heading.jsx"

function Headline({ onYearChange, onRegionChange, onSearch, onSearchEnter }) {
    return (
        <div className="Headline">
            <div className="Headline-filters">
                <Filters
                    onYearChange={onYearChange}
                    onRegionChange={onRegionChange}
                    onSearch={onSearch}
                    onSearchEnter={onSearchEnter}
                />
            </div>
            <Heading />
        </div>
    )
}

export default Headline