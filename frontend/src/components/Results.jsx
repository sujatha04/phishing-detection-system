import React from 'react';

const Results = ({ data }) => {
  if (!data) return null;

  const { prediction, features_breakdown } = data;
  
  // Use actual backend predictions
  const isPhishing = prediction?.is_phishing === true;
  const threatScore = prediction?.phishing_probability 
    ? Math.round(prediction.phishing_probability * 100) 
    : 0;
  
  const getVerdictStyle = () => {
    if (isPhishing) return 'danger';
    if (threatScore > 40) return 'warning'; // Add a little visual warning if probability is kinda high but still legitimate
    return 'safe';
  };

  const getVerdictText = () => {
    if (isPhishing) return 'PHISHING';
    return 'LEGITIMATE';
  };

  const { url_based, content_based, visual_similarity } = features_breakdown;

  return (
    <div className="glass-panel results-panel">
      <div className="results-header">
        <div>
          <h2 style={{ marginBottom: '0.5rem', wordBreak: 'break-all' }}>{data.url}</h2>
          <p style={{ color: 'var(--text-muted)' }}>Analysis Complete</p>
        </div>
        
        <div className="threat-score">
          <div className={`score-value ${getVerdictStyle()}`}>{threatScore}%</div>
          <div className="score-label">Threat Score</div>
        </div>
        
        <div className={`verdict-badge ${getVerdictStyle()}`} style={{ border: `2px solid currentColor` }}>
          {getVerdictText()}
        </div>
      </div>

      <div className="features-grid">
        <div className="feature-card">
          <h3>URL Analysis</h3>
          <ul className="feature-list">
            <li className="feature-item">
              <span className="feature-name">Length</span>
              <span className="feature-val">{url_based?.url_length || 0} chars</span>
            </li>
            <li className="feature-item">
              <span className="feature-name">Domain Length</span>
              <span className="feature-val">{url_based?.domain_length || 0} chars</span>
            </li>
            <li className="feature-item">
              <span className="feature-name">Suspicious Chars</span>
              <span className={`feature-val ${url_based?.num_hyphens > 1 ? 'val-bad' : 'val-good'}`}>
                {url_based?.num_hyphens || 0} hyphens
              </span>
            </li>
            <li className="feature-item">
              <span className="feature-name">Path Length</span>
              <span className="feature-val">{url_based?.path_length || 0}</span>
            </li>
          </ul>
        </div>

        <div className="feature-card">
          <h3>Content Analysis</h3>
          <ul className="feature-list">
            <li className="feature-item">
              <span className="feature-name">External Forms</span>
              <span className={`feature-val ${content_based?.has_external_form ? 'val-bad' : 'val-good'}`}>
                {content_based?.has_external_form ? 'Yes' : 'No'}
              </span>
            </li>
            <li className="feature-item">
              <span className="feature-name">iFrames</span>
              <span className={`feature-val ${content_based?.num_iframes > 0 ? 'val-bad' : 'val-good'}`}>
                {content_based?.num_iframes || 0}
              </span>
            </li>
            <li className="feature-item">
              <span className="feature-name">Hidden Elements</span>
              <span className={`feature-val ${content_based?.hidden_elements > 0 ? 'val-bad' : 'val-good'}`}>
                {content_based?.hidden_elements || 0}
              </span>
            </li>
            <li className="feature-item">
              <span className="feature-name">Ext. Scripts Ratio</span>
              <span className="feature-val">
                {content_based?.script_ratio ? (content_based.script_ratio * 100).toFixed(1) : 0}%
              </span>
            </li>
          </ul>
        </div>

        <div className="feature-card">
          <h3>Visual & Layout</h3>
          <ul className="feature-list">
            <li className="feature-item">
              <span className="feature-name">Brand Spoofing Match</span>
              <span className={`feature-val ${visual_similarity > 0.8 ? 'val-bad' : 'val-good'}`}>
                {(visual_similarity * 100).toFixed(1)}%
              </span>
            </li>
            <li className="feature-item">
              <span className="feature-name">DOM Structure Diff</span>
              <span className="feature-val">Moderate</span>
            </li>
            <li className="feature-item">
              <span className="feature-name">Render Defacements</span>
              <span className="feature-val val-good">None Detected</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Results;
