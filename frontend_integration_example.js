/**
 * Example Next.js/React Component for AI Proctoring Integration
 * 
 * Requirements:
 * npm install react-webcam
 */

import React, { useRef, useCallback, useEffect, useState } from 'react';
import Webcam from 'react-webcam';

const ProctoringSystem = () => {
    const webcamRef = useRef(null);
    const [report, setReport] = useState(null);
    const [isMonitoring, setIsMonitoring] = useState(false);

    const captureAndAnalyze = useCallback(async () => {
        if (webcamRef.current) {
            const imageSrc = webcamRef.current.getScreenshot();
            
            if (imageSrc) {
                try {
                    const response = await fetch('http://localhost:8000/api/v1/analyze', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ image: imageSrc }),
                    });

                    const data = await response.json();
                    setReport(data);
                    
                    // Logic to handle high suspicion
                    if (data.suspicion_score > 70) {
                        console.warn("HIGH SUSPICION ALERT!");
                        // triggerAlert(data);
                    }
                } catch (error) {
                    console.error("Error sending frame to AI backend:", error);
                }
            }
        }
    }, [webcamRef]);

    useEffect(() => {
        let interval;
        if (isMonitoring) {
            // Analyze a frame every 3 seconds (adjust for performance/cost)
            interval = setInterval(captureAndAnalyze, 3000);
        }
        return () => clearInterval(interval);
    }, [isMonitoring, captureAndAnalyze]);

    return (
        <div className="proctoring-container" style={{ padding: '20px', textAlign: 'center' }}>
            <h1>AI Exam Proctoring</h1>
            
            <div style={{ position: 'relative', display: 'inline-block' }}>
                <Webcam
                    audio={false}
                    ref={webcamRef}
                    screenshotFormat="image/jpeg"
                    width={640}
                    height={480}
                    style={{ borderRadius: '10px', border: '3px solid #333' }}
                />
                
                {report && (
                    <div className="status-overlay" style={{
                        position: 'absolute',
                        top: '10px',
                        left: '10px',
                        background: 'rgba(0,0,0,0.7)',
                        color: 'white',
                        padding: '10px',
                        borderRadius: '5px',
                        textAlign: 'left',
                        fontSize: '12px'
                    }}>
                        <p>Face: {report.face_present ? "✅" : "❌"}</p>
                        <p>Gaze: {report.gaze_direction}</p>
                        <p>Phone: {report.phone_detected ? "📱 ALERT" : "No"}</p>
                        <p>People: {report.person_count}</p>
                        <p style={{ color: report.suspicion_score > 50 ? 'red' : 'white', fontWeight: 'bold' }}>
                            Suspicion: {report.suspicion_score}%
                        </p>
                    </div>
                )}
            </div>

            <div style={{ marginTop: '20px' }}>
                <button 
                    onClick={() => setIsMonitoring(!isMonitoring)}
                    style={{
                        padding: '10px 20px',
                        fontSize: '16px',
                        backgroundColor: isMonitoring ? '#ff4d4d' : '#4CAF50',
                        color: 'white',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer'
                    }}
                >
                    {isMonitoring ? "Stop Proctoring" : "Start Proctoring"}
                </button>
            </div>

            {report && report.suspicion_score > 50 && (
                <div style={{ color: 'red', marginTop: '10px' }}>
                    <strong>Warning: Suspicious behavior detected!</strong>
                </div>
            )}
        </div>
    );
};

export default ProctoringSystem;
