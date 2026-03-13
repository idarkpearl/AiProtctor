# AI Proctoring Backend Service

An intelligent, real-time microservice for online exam proctoring. It detects suspicious activities using computer vision and behavioral analysis.

## 🚀 Features

- **Gaze Detection**: Monitors eye movement and head pose to detect if the candidate is looking at notes or secondary screens.
- **Multiple Person Detection**: Detects if more than one person is in the frame.
- **Device Detection**: Identifies unauthorized cell phones, tablets, or laptops.
- **Hand Monitoring**: Tracks up to 4 hands to detect external assistance (3+ hands alert).
- **Notebook/Note Detection**: Flags books or cheat sheets displayed to the camera.
- **Talking Detection**: Real-time mouth movement analysis to detect whispering or verbal assistance.
- **Suspicion Index**: A weighted scoring system that aggregates all alerts into a single risk score (0-100%).

## 🛠 Tech Stack

- **FastAPI**: High-performance Python API framework.
- **YOLOv8 (Ultralytics)**: Advanced object detection for devices and people.
- **MediaPipe Tasks**: Modern landmark API for high-precision face and hand tracking.
- **OpenCV**: Image processing and frame decoding.

## 🏗 Setup & Installation

### 1. Prerequisites
- Python 3.9+
- Webcam for testing

### 2. Clone and Install Dependencies
```bash
git clone <your-repo-url>
cd ai_proctoring_service
pip install -r requirements.txt
```

### 3. Model Downloads
The system requires MediaPipe Task files in the `models/` directory:
- `models/face_landmarker.task`
- `models/hand_landmarker.task`

### 4. Run the Server
```bash
python main.py
```
The server will start at `http://localhost:8000`.

---

## 🔗 Next.js Integration Guide

To integrate this service into your Next.js application, follow these steps:

### 1. Setup Camera Capture
Create a component that captures the webcam frame every 1-2 seconds.

```javascript
// components/ProctoringClient.js
import React, { useRef, useEffect } from 'react';

export default function ProctoringClient() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    // 1. Initialize Webcam
    navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
      videoRef.current.srcObject = stream;
    });

    // 2. Poll the Backend
    const interval = setInterval(async () => {
      const canvas = canvasRef.current;
      const context = canvas.getContext('2d');
      context.drawImage(videoRef.current, 0, 0, 640, 480);
      
      const base64Image = canvas.toDataURL('image/jpeg', 0.8);
      
      const response = await fetch('http://localhost:8000/api/v1/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: base64Image })
      });
      
      const result = await response.json();
      console.log('Proctoring Report:', result);
      
      // Handle alerts (e.g., set state to show warnings)
      if (result.suspicion_score > 70) {
        alert("Warning: Suspicious activity detected!");
      }
    }, 2000); // Send every 2 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <video ref={videoRef} autoPlay style={{ width: '400px' }} />
      <canvas ref={canvasRef} style={{ display: 'none' }} width="640" height="480" />
    </div>
  );
}
```

### 2. API Schema
**Endpoint**: `POST /api/v1/analyze`  
**Request**:
```json
{
  "image": "data:image/jpeg;base64,..."
}
```
**Response**:
```json
{
  "face_present": true,
  "multiple_people": false,
  "person_count": 1,
  "phone_detected": false,
  "looking_away": false,
  "gaze_direction": "Center",
  "is_talking": false,
  "suspicion_score": 5,
  "malpractices": []
}
```

## 📜 Malpractice List Explained

| Alert | Trigger Condition |
|-------|-------------------|
| "Face not detected" | No face found in the camera view. |
| "Multiple people detected" | More than 1 person found (e.g., proxy candidate). |
| "Looking away from screen" | Eye/Head orientation strongly shifted left/right/up. |
| "Suspiciously looking down" | Head tilted deeply down (e.g., looking at a phone in lap). |
| "Mouth movement detected" | Excessive jaw movement (talking or whispering). |
| "Suspicious hand count" | 3 or more hands detected (assistance from others). |

## 🚢 Deployment

Since this is a standalone microservice, you can deploy it independently using Docker or direct Python hosting.

### 1. Using Docker (Recommended)
Build and run the container:
```bash
docker build -t ai-proctor-backend .
docker run -p 8000:8000 ai-proctor-backend
```

### 2. Deployment Platforms
- **Render / Railway**: Recommended for easy Python/Docker deployment.
- **AWS / GCP / Azure**: Use **AWS App Runner** or **Google Cloud Run** for high scalability.

> [!NOTE]
> Ensure your deployment environment has at least 2GB of RAM for YOLOv8 model loading.

---
*Created with ❤️ for Advanced Online Assessment.*
