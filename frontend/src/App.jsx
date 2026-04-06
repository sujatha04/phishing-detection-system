import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ScanPage from './pages/ScanPage';
import ResultPage from './pages/ResultPage';

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <header>
          <h1>Phishing Detection System</h1>
          <p>AI-Powered Multi-Layered Threat Analysis</p>
        </header>

        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/scan" element={<ScanPage />} />
          <Route path="/result" element={<ResultPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
