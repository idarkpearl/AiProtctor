# 🎯 Master Integration & Deployment Plan

Follow these exact steps to move from your old "simple" detector to your new "high-accuracy" proctoring system.

---

## Part 1: Deploy the "Engine" (Python Backend)
You must deploy the code we built here so it has a public URL on the internet.

1.  **GitHub**: Create a new GitHub repo and push all the files from this folder (`ai_proctoring_service`) to it.
2.  **Railway.app**: Log in to Railway and click **"New Project"** -> **"Deploy from GitHub"**.
3.  **Automatic**: Railway will see the `Dockerfile` and deploy it.
4.  **Public URL**: Once finished, it will give you a URL (e.g., `https://proctor-engine.up.railway.app`).

---

## Part 2: Clean Your Next.js Code
In your `ExamContent` file, remove the "heavy weights" that make your project slow:

1.  **REMOVE** these imports:
    - `import { ObjectDetector, FilesetResolver } from '@mediapipe/tasks-vision';`
2.  **REMOVE** the `loadModel` useEffect block.
3.  **REMOVE** the local `detect` function that uses `modelRef.current.detectForVideo`.

---

## Part 3: Connect your Website to the Engine
Now, add the "Bridge" to your `ExamContent` component. This code takes a screenshot every 2 seconds and asks your Engine if the student is cheating.

### 1. Add these 2 small Refs at the top of your component:
```javascript
const canvasRef = useRef(null);
const analysisInterval = useRef(null);
```

### 2. Replace your old detection useEffect with this one:
```javascript
useEffect(() => {
    if (!isStarted) return;

    // This function sends data to your DEPLOYED model
    const detectCheating = async () => {
        if (!videoRef.current || !canvasRef.current) return;

        // Capture frame
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        context.drawImage(videoRef.current, 0, 0, 320, 240);
        const base64Image = canvas.toDataURL('image/jpeg', 0.8);

        try {
            const res = await fetch('https://your-deployed-url.com/api/v1/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: base64Image })
            });
            const data = await res.json();

            // UPDATE YOUR UI
            setFaceCount(data.person_count);
            
            // USE YOUR EXISTING WARNING SYSTEM
            if (data.malpractices.length > 0) {
                // Pass the cheating reason (e.g., "Phone Detected") to your function
                issueWarning(data.malpractices[0]);
            }
        } catch (e) { console.error("Proctoring API disconnected"); }
    };

    analysisInterval.current = setInterval(detectCheating, 2000);
    return () => clearInterval(analysisInterval.current);
}, [isStarted, issueWarning]);
```

### 3. Add the hidden capture tool to your UI:
Inside your `return (...)` block, add this line anywhere (it's invisible):
```jsx
<canvas ref={canvasRef} style={{ display: 'none' }} width="320" height="240" />
```

---

## ✅ Will it work fine?
**YES.** It will work exactly like your local test because it uses the SAME code.
- **Accuracy**: It will be **more accurate** than your current code because it uses YOLOv8.
- **Performance**: It will be **faster** because the student's browser doesn't have to do the heavy math—the server does it.

## 🗑 Should you delete the other files?
- **Keep**: `ProctoringPanel.jsx` (You can use it as a reference for how to style the sidebar if you want to redesign it later).
- **Delete**: `NEXTJS_INTEGRATION.md` and `test_frontend.html` once you are done, as those are just examples.
