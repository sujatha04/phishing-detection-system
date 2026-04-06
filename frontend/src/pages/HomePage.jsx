import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="home-container" style={{ textAlign: 'center', marginTop: '4rem' }}>
      <p style={{ margin: '1rem auto', maxWidth: '600px', color: 'var(--text-muted)' }}>
        Welcome to the AI-Powered Multi-Layered Threat Analysis tool. 
        Detect malicious URLs using advanced machine learning models and deep content inspection.
      </p>
      
      <button 
        className="scan-btn" 
        onClick={() => navigate('/scan')}
        style={{ marginTop: '2rem', fontSize: '1.2rem', padding: '15px 40px' }}
      >
        START DETECTION
      </button>
    </div>
  );
};

export default HomePage;
