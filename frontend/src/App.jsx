import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import ForecastingPage from './pages/ForecastingPage'

function App() {
    return (
        <div className="app-container">
            <Router>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/forecasting" element={<ForecastingPage />} />
                </Routes>
            </Router>
        </div>
    )
}

export default App