import './App.css'

import Header from "./components/Header/Header.jsx";
import Headline from "./components/Headline/Headline.jsx";
import Map from "./components/Map/Map.jsx";

function App() {
    return (
        <div className="App">
            <Header />
            <Headline/>
            <Map/>
        </div>
    )
}

export default App;