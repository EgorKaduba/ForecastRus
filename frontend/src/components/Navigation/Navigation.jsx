import './Navigation.css'
import BurgerMenu from './BurgerMenu'

function Navigation() {
    const navItems = [
        { path: "", label: "Главная" },
        { path: "/forecasting", label: "Мониторинг" }
    ]

    return (
        <>
            <nav className="navigation">
                {navItems.map((item) => (
                    <a
                        key={item.path}
                        href={item.path}
                        className="navigation-link"
                    >
                        {item.label}
                    </a>
                ))}
            </nav>
            <BurgerMenu />
        </>
    )
}

export default Navigation