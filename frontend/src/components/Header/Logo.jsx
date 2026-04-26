import './Logo.css'

function Logo() {
    return (
        <div className="logo">
            <img
                src="/src/assets/logo.svg"
                alt="Логотип"
                className="logo_image"
            />
            <span className="logo_text">ForecastRus</span>
        </div>
    )
}

export default Logo