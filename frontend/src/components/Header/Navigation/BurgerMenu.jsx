import { useState } from 'react'
import './Navigation.css'

function BurgerMenu() {
    const [isOpen, setIsOpen] = useState(false)

    const navItems = [
        { path: "/", label: "Главная" },
        { path: "/forecasting", label: "Мониторинг" }
    ]

    const toggleMenu = () => {
        setIsOpen(!isOpen)
    }

    return (
        <>
            <div className={`burger ${isOpen ? 'active' : ''}`} onClick={toggleMenu}>
                <span></span>
                <span></span>
                <span></span>
            </div>
            <div className={`mobile-menu ${isOpen ? 'open' : ''}`}>
                <nav className="mobile-navigation">
                    {navItems.map((item) => (
                        <a
                            key={item.path}
                            href={item.path}
                            className="mobile-nav-link"
                            onClick={() => setIsOpen(false)}
                        >
                            {item.label}
                        </a>
                    ))}
                </nav>
            </div>
        </>
    )
}

export default BurgerMenu