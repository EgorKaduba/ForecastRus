import './FilterSelect.css'

function FilterSelect({ label, options, value, onChange }) {
    console.log(`${label} options:`, options)  // Добавьте для проверки

    const handleChange = (e) => {
        const selectedValue = e.target.value
        if (onChange) {
            onChange(selectedValue === label ? '' : selectedValue)
        }
    }

    return (
        <select className="filter-select" value={value || label} onChange={handleChange}>
            <option value={label}>{label}</option>
            {options && options.map((option, index) => (
                <option key={index} value={option}>
                    {option}
                </option>
            ))}
        </select>
    )
}

export default FilterSelect