import './Filters.css'

function FilterSelect({ label, options }) {
    return (
        <select className="Filter-select">
            <option>{label}</option>
            {options.map((option, index) => (
                <option key={index} value={option}>
                    {option}
                </option>
            ))}
        </select>
    )
}

export default FilterSelect