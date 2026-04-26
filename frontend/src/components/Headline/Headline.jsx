import './Headline.css'
import Filters from './Filters/Filters.jsx'
import Heading from "./Heading.jsx"

function Headline() {
    return (
        <div className="Headline">
            <div className="Headline-filters">
                <Filters />
            </div>
            <Heading />
        </div>
    )
}

export default Headline