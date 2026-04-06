import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Scanner from '../components/Scanner';

const ScanPage = () => {
  const [isScanning, setIsScanning] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleScan = async (url) => {
    setIsScanning(true);
    setError(null);

    try {
      // ✅ Use environment variable for backend URL
      const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

      const response = await fetch(`${API_BASE}/detect`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      console.log("Response:", response); // DEBUG

      if (!response.ok) {
        throw new Error('Server error while analyzing URL');
      }

      const data = await response.json();
      console.log("Data received:", data); // DEBUG

      // ✅ IMPORTANT FIX → pass data correctly
      navigate('/result', { state: data });

    } catch (err) {
      console.error("ERROR:", err);
      setError(err.message || 'Failed to fetch');
      setIsScanning(false);
    }
  };

  return (
    <div className="scan-page-container">
      <h2
        style={{
          textAlign: 'center',
          marginBottom: '2rem',
          color: 'var(--accent-primary)',
        }}
      >
        Threat Scanner
      </h2>

      <Scanner onScan={handleScan} isScanning={isScanning} />

      {/* ❌ Error Message */}
      {error && (
        <div
          className="glass-panel"
          style={{ borderColor: 'red', marginTop: '2rem' }}
        >
          <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>
        </div>
      )}

      {/* 🔄 Loading Animation */}
      {isScanning && (
        <div
          className="glass-panel scanning-container"
          style={{ marginTop: '2rem' }}
        >
          <div className="radar-spinner"></div>
          <p className="status-text">ANALYZING THREAT VECTORS...</p>
        </div>
      )}

      {/* 🔙 Back Button */}
      {!isScanning && (
        <div style={{ textAlign: 'center', marginTop: '2rem' }}>
          <button
            className="scan-btn"
            style={{
              background: 'transparent',
              border: '1px solid var(--border-color)',
              color: 'var(--text-color)',
            }}
            onClick={() => navigate('/')}
          >
            Back to Home
          </button>
        </div>
      )}
    </div>
  );
};

export default ScanPage;
