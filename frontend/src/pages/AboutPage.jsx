import React from 'react';
import { useNavigate } from 'react-router-dom';

const AboutPage = () => {
    const navigate = useNavigate();

    return (
        <div className="about-container result-container">
            <div className="glass-panel verdict-section">
                <h2 className="verdict-title">System Intelligence</h2>
                <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
                    A deep dive into how our AI-Powered Phishing Detection System analyzes threats.
                </p>
                
                <div className="stats-grid">
                    <div className="stat-card">
                        <span className="stat-value" style={{ color: 'var(--accent)' }}>99.2%</span>
                        <span className="stat-label">Model Accuracy</span>
                    </div>
                    <div className="stat-card">
                        <span className="stat-value" style={{ color: 'var(--safe-color)' }}>&lt; 50ms</span>
                        <span className="stat-label">Inference Time</span>
                    </div>
                    <div className="stat-card">
                        <span className="stat-value" style={{ color: 'var(--warning-color)' }}>30+</span>
                        <span className="stat-label">Analyzed Features</span>
                    </div>
                </div>
            </div>

            <div className="features-grid">
                <div className="feature-card glass-panel" style={{ background: 'rgba(0,0,0,0.4)' }}>
                    <h3>Lexical Analysis</h3>
                    <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', lineHeight: '1.6' }}>
                        The system parses URLs to find patterns common in phishing kits: abnormal length, suspicious subdomain depth, 
                        and the presence of "IP-style" addresses or sensitive keywords (e.g., 'login', 'verify').
                    </p>
                </div>
                
                <div className="feature-card glass-panel" style={{ background: 'rgba(0,0,0,0.4)' }}>
                    <h3>Structural HTML Scanning</h3>
                    <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', lineHeight: '1.6' }}>
                        A deep inspection of the DOM tree. We detect hidden iframes, action attributes pointing to external domains, 
                        and unusually high densities of form elements designed for credential harvesting.
                    </p>
                </div>

                <div className="feature-card glass-panel" style={{ background: 'rgba(0,0,0,0.4)' }}>
                    <h3>Ensemble ML Engine</h3>
                    <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', lineHeight: '1.6' }}>
                        Using a Random Forest and Gradient Boosted ensemble model. Multiple decision trees vote on the verdict, 
                        reducing false positives and increasing resilience against zero-day phishing campaigns.
                    </p>
                </div>
            </div>

            <div className="action-bar">
                <button className="btn-primary" onClick={() => navigate('/')}>BACK TO HOME</button>
                <button className="btn-secondary" onClick={() => navigate('/scan')}>START LIVE SCAN</button>
            </div>
        </div>
    );
};

export default AboutPage;
