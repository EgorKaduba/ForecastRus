import { useState } from "react"; // Важно: импортируем useState
import "./App.css";
import Header from "./components/Header/Header.jsx";
import Headline from "./components/Headline/Headline.jsx";
import Map from "./components/Map/Map.jsx";
import TopRaiting from "./components/TopRaiting/TopRaiting.jsx";
import Demographics from "./components/Demographics/Demographics.jsx";
import Analytics from "./components/Analytics/Analytics.jsx";

function App() {
  const [selectedYear, setSelectedYear] = useState(2022);

  const handleYearChange = (year) => {
    setSelectedYear(year);
  };

  return (
    <div className="App">
      <Header />
      <Headline onYearChange={handleYearChange} />
      <Map selectedYear={selectedYear} />
      {selectedYear && (
        <>
          <TopRaiting selectedYear={selectedYear} />
          <Demographics selectedYear={selectedYear} />
        </>
      )}
      <Analytics/>
    </div>
  );
}

export default App;
