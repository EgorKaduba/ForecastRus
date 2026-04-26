import './Headline.css'
import Filters from './Filters/Filters.jsx'
import Heading from "./Heading.jsx"

function Headline({ onYearChange }) {
    return (
        <div className="Headline">
            <div className="Headline-filters">
                <Filters onYearChange={onYearChange} />
            </div>
            <Heading />
        </div>
    )
}

export default Headline