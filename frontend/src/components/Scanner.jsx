import React, { useState } from 'react';

const Scanner = ({ onScan, isScanning }) => {
  const [url, setUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url.trim()) {
      onScan(url.trim());
    }
  };

  return (
    <div className="glass-panel">
      <form onSubmit={handleSubmit} className="input-group">
        <input
          type="text"
          className="url-input"
          placeholder="Paste URL to scan (e.g., https://example.com)"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          disabled={isScanning}
          required
        />
        <button type="submit" className="scan-button" disabled={isScanning || !url.trim()}>
          {isScanning ? 'Scanning...' : 'Scan URL'}
        </button>
      </form>
    </div>
  );
};

export default Scanner;
