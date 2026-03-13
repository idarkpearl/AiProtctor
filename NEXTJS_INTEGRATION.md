# Easy Next.js Integration Guide

Follow this guide to add the AI Proctoring side-panel to your existing assessment page without changing your original code.

## 1. Add the Component
Copy the file `ProctoringPanel.jsx` (which I created in your project folder) into your Next.js `components/` directory.

## 2. Integrated Layout Example
In your Assessment Page (e.g., `pages/test.js`), use a `flex` layout to split the screen into **80% Assessment** and **20% Proctoring**.

```jsx
import ProctoringPanel from '../components/ProctoringPanel';

export default function AssessmentPage() {
  
  // This function handles alerts from the proctoring service
  const handleProctoringUpdate = (report) => {
    if (report.suspicion_score > 80) {
      console.warn("CRITICAL: Candidate flagged for cheating!");
      // You can trigger your own "Submit Test Early" logic here
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>
      
      {/* 1. LEFT SIDE: 80% ASSESSMENT SCREEN */}
      <div style={{ width: '80%', padding: '20px', overflowY: 'auto' }}>
        <h2>Assessment Section</h2>
        {/* --- YOUR ORIGINAL EXAM CODE GOES HERE --- */}
        <div>
           {/* Questions, MCQ, Editor, etc. */}
        </div>
      </div>

      {/* 2. RIGHT SIDE: 20% AI PROCTORING PANEL */}
      <div style={{ width: '20%', minWidth: '250px' }}>
        <ProctoringPanel 
            apiUrl="http://localhost:8000/api/v1/analyze" 
            onStatusUpdate={handleProctoringUpdate}
        />
      </div>

    </div>
  );
}
```

## 3. Why This Works
- **Encapsulated**: All camera logic, API calls, and styling are inside `ProctoringPanel.jsx`.
- **Minimal Changes**: You only need to wrap your existing content in a flexbox `div`.
- **Communication**: The `onStatusUpdate` prop lets you listen for cheating alerts without modifying the proctoring component's internal code.

---
**Deployment Tip**: When you deploy the Python backend, remember to update the `apiUrl` in your Next.js page to point to your live URL instead of `localhost`.
