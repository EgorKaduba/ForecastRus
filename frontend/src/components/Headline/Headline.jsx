import './Headline.css'

import Filters from './Filters/Filters.jsx'
import Heading from "./Heading.jsx";


function Headline() {
    return (
        <div className="Headline">
            <Filters/>
            <Heading/>
        </div>
    )
}

export default Headline