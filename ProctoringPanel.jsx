import React, { useState, useEffect, useRef } from 'react';

/**
 * ProctoringPanel - A reusable component for AI Proctoring.
 * 
 * @param {string} apiUrl - The URL of your deployed AI microservice (e.g., http://localhost:8000/api/v1/analyze)
 * @param {function} onStatusUpdate - Callback function to notify the parent page of suspicion scores.
 */
const ProctoringPanel = ({ apiUrl, onStatusUpdate }) => {
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [report, setReport] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const intervalRef = useRef(null);

  // 1. Initialize Webcam
  useEffect(() => {
    async function startCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
        if (videoRef.current) videoRef.current.srcObject = stream;
      } catch (err) {
        console.error("Camera error:", err);
      }
    }
    startCamera();
    return () => stopMonitoring();
  }, []);

  const startMonitoring = () => {
    setIsMonitoring(true);
    intervalRef.current = setInterval(analyzeFrame, 2000); // 2-second interval
  };

  const stopMonitoring = () => {
    setIsMonitoring(false);
    if (intervalRef.current) clearInterval(intervalRef.current);
  };

  const analyzeFrame = async () => {
    if (!canvasRef.current || !videoRef.current) return;

    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');
    context.drawImage(videoRef.current, 0, 0, 640, 480);
    const base64Image = canvas.toDataURL('image/jpeg', 0.8);

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: base64Image })
      });
      const data = await response.json();
      setReport(data);
      if (onStatusUpdate) onStatusUpdate(data);
    } catch (err) {
      console.error("API error:", err);
    }
  };

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>AI Proctoring</h3>
      
      {/* Video Feed */}
      <div style={styles.videoWrapper}>
        <video 
          ref={videoRef} 
          autoPlay 
          playsInline 
          muted 
          style={styles.video} 
        />
        <canvas ref={canvasRef} style={{ display: 'none' }} width="640" height="480" />
      </div>

      {/* Monitoring Status */}
      <div style={styles.statusRow}>
        <div style={{ ...styles.pulse, backgroundColor: isMonitoring ? '#10b981' : '#64748b' }} />
        <span style={styles.statusText}>{isMonitoring ? 'Monitoring Active' : 'Ready to Start'}</span>
      </div>

      {/* Analytics */}
      {report && (
        <div style={styles.metrics}>
          <div style={styles.metricLabel}>Suspicion Score</div>
          <div style={styles.scoreBarContainer}>
            <div style={{ ...styles.scoreBarFill, width: `${report.suspicion_score}%`, backgroundColor: report.suspicion_score > 60 ? '#ef4444' : '#10b981' }} />
          </div>
          <p style={styles.scoreText}>{report.suspicion_score}% Confidence</p>

          {report.malpractices.length > 0 && (
            <div style={styles.alertList}>
              {report.malpractices.map((m, i) => (
                <div key={i} style={styles.alertItem}>⚠️ {m}</div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Control Buttons */}
      <button 
        onClick={isMonitoring ? stopMonitoring : startMonitoring}
        style={{ ...styles.button, backgroundColor: isMonitoring ? '#ef4444' : '#0284c7' }}
      >
        {isMonitoring ? 'Stop Monitoring' : 'Start Monitoring'}
      </button>
    </div>
  );
};

// Styles (Easy to extract to CSS modules)
const styles = {
  container: {
    width: '100%',
    height: '100%',
    backgroundColor: '#111827',
    color: '#e2e8f0',
    padding: '16px',
    display: 'flex',
    flexDirection: 'column',
    borderLeft: '1px solid #374151',
    boxSizing: 'border-box',
    overflowY: 'auto'
  },
  title: { fontSize: '1.2rem', margin: '0 0 16px 0', color: '#38bdf8' },
  videoWrapper: { width: '100%', borderRadius: '8px', overflow: 'hidden', backgroundColor: '#000', marginBottom: '16px' },
  video: { width: '100%', display: 'block' },
  statusRow: { display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '20px' },
  pulse: { width: '8px', height: '8px', borderRadius: '50%' },
  statusText: { fontSize: '0.85rem', fontWeight: 'bold' },
  metrics: { flexGrow: 1 },
  metricLabel: { fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase', marginBottom: '4px' },
  scoreBarContainer: { height: '8px', backgroundColor: '#374151', borderRadius: '4px', overflow: 'hidden', marginBottom: '8px' },
  scoreBarFill: { height: '100%', transition: 'width 0.5s ease-in-out' },
  scoreText: { fontSize: '0.9rem', fontWeight: 'bold', marginBottom: '16px' },
  alertList: { display: 'flex', flexDirection: 'column', gap: '8px' },
  alertItem: { padding: '8px 12px', backgroundColor: 'rgba(239, 68, 68, 0.1)', color: '#f87171', borderRadius: '6px', fontSize: '0.8rem', borderLeft: '3px solid #ef4444' },
  button: { padding: '10px', borderRadius: '8px', border: 'none', color: 'white', fontWeight: 'bold', cursor: 'pointer', transition: 'all 0.2s' }
};

export default ProctoringPanel;
