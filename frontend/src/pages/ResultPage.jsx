import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const ResultPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // ✅ Fix: Access state directly (ScanPage passes object as state)
  const data = location.state;

  // Redirect if no data (user opened /result directly)
  useEffect(() => {
    if (!data) {
      navigate('/scan');
    }
  }, [data, navigate]);

  if (!data) return null;

  // Extract prediction values safely
  const isPhishing = data.prediction?.is_phishing;
  const isWhitelisted = data.prediction?.is_whitelisted;
  const probability = data.prediction?.phishing_probability;
  const confidencePercent = Math.round(probability * 100);

  // Determine color based on safety
  const statusColor = isPhishing ? 'var(--danger-color)' : 'var(--safe-color)';
  const statusText = isPhishing ? 'Phishing Detected' : 'Legitimate Site';
  const statusIcon = isPhishing ? '⚠️' : '🛡️';

  return (
    <div className="result-container">
      <div className="glass-panel verdict-section">
        <div 
          className="verdict-badge" 
          style={{ 
            color: isWhitelisted ? 'var(--accent-primary)' : statusColor, 
            borderColor: isWhitelisted ? 'var(--accent-primary)' : statusColor,
            marginBottom: '1.5rem',
            display: 'inline-block'
          }}
        >
          {isWhitelisted ? '🛡️ VERIFIED LEGITIMATE' : `${statusIcon} ${statusText.toUpperCase()}`}
        </div>

        <h2 className="verdict-title">
          {isPhishing 
            ? "THIS URL IS UNSAFE" 
            : "THIS URL IS SAFE TO VISIT"}
        </h2>

        <div className="url-display">
          {data.url}
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <span className="stat-value" style={{ color: statusColor }}>
              {confidencePercent}%
            </span>
            <span className="stat-label">Confidence Score</span>
          </div>
          
          <div className="stat-card">
            <span className="stat-value" style={{ color: isPhishing ? 'var(--danger-color)' : 'var(--safe-color)' }}>
              {isPhishing ? 'HIGH' : 'LOW'}
            </span>
            <span className="stat-label">Risk Level</span>
          </div>

          <div className="stat-card">
            <span className="stat-value" style={{ color: 'var(--accent)' }}>
              ML-ENSEMBLE
            </span>
            <span className="stat-label">Detection Engine</span>
          </div>
        </div>
      </div>

      {data.features_breakdown && (
        <div className="glass-panel">
          <h3 style={{ marginBottom: '1.5rem', color: 'var(--accent)' }}>Technical Breakdown</h3>
          <div className="features-grid">
            <div className="feature-card">
              <h3>URL Analysis</h3>
              <div className="feature-list">
                {Object.entries(data.features_breakdown.url_based).map(([key, val]) => (
                  <div key={key} className="feature-item">
                    <span className="feature-name">{key.replace(/_/g, ' ')}</span>
                    <span className="feature-val">{val.toString()}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="feature-card">
              <h3>Content Analysis</h3>
              <div className="feature-list">
                 <div className="feature-item">
                    <span className="feature-name">Visual Similarity</span>
                    <span className="feature-val">{(data.features_breakdown.visual_similarity * 100).toFixed(1)}%</span>
                  </div>
                {Object.entries(data.features_breakdown.content_based).map(([key, val]) => (
                  <div key={key} className="feature-item">
                    <span className="feature-name">{key.replace(/_/g, ' ')}</span>
                    <span className="feature-val">{val.toString()}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="action-bar">
        <button className="btn-secondary" onClick={() => navigate('/scan')}>
          Scan Another URL
        </button>
        <button className="btn-primary" onClick={() => navigate('/')}>
          Return Home
        </button>
      </div>
    </div>
  );
};

export default ResultPage;
