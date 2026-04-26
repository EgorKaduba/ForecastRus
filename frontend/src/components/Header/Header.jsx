import Logo from "./Logo.jsx";
import './Header.css'
import Navigation from "../Navigation/Navigation.jsx";

function Header() {
    return (
        <header>
            <Logo/>
            <Navigation/>
        </header>
    )
}

export default Header