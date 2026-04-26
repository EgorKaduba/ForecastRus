import './App.css'
import Header from "./components/Header/Header.jsx"
import HeroSection from "./components/HeroSection/HeroSection.jsx"  
import TeamSection from './components/TeamSection/TeamSection.jsx'

function App() {
    return (
        <div className="App">
            <Header />
            <HeroSection />  
            <TeamSection/>
        </div>
    )
}

export default App