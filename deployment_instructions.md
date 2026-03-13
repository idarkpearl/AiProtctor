# Step-by-Step Deployment Guide

Follow these steps to deploy your AI Proctoring Backend independently.

## Step 1: Prepare Your Repository
1. Initialize a git repository in your project folder:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for proctoring service"
   ```
2. Create a new repository on **GitHub**.
3. Push your code to GitHub:
   ```bash
   git remote add origin <your-github-repo-url>
   git branch -M main
   git push -u origin main
   ```

## Step 2: Choose a Hosting Platform (Recommend Render or Railway)

### Option A: Deploying on Render (Easiest)
1. Log in to [Render.com](https://render.com).
2. Click **New +** and select **Web Service**.
3. Connect your GitHub repository.
4. **Configuration**:
   - **Runtime**: `Python 3` (or `Docker` if you want to use the Dockerfile).
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
5. **Advanced Settings (CRITICAL)**:
   - **Plan**: Select a plan with at least **2GB RAM** (The AI models need memory to load).
6. Click **Deploy**.

### Option B: Deploying on Railway (Fastest)
1. Log in to [Railway.app](https://railway.app).
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select your repository.
4. Railway will automatically detect the `Dockerfile` and start the build.
5. Click **Deploy Now**.
6. Once finished, it will give you a public URL like `https://project-name.up.railway.app`.

## Step 3: Configure Environment Variables
If you change your port or host, add these in your platform's dashboard:
- `PORT`: `8000`
- `HOST`: `0.0.0.0`

## Step 4: Update Your Next.js App
In your Next.js project, update the API URL to point to your new live server:

```javascript
// Change this line in your Next.js code:
const API_URL = "https://your-deployed-service.render.com/api/v1/analyze";
```

## Step 5: Test the Live Service
1. Open your deployed URL in a browser. You should see a message (or a 404 if no home route is defined, which is fine).
2. Use the `test_frontend.html` by changing the fetch URL to your live URL and verify detections.

---
**Note on Performance**: AI models perform best on servers with more CPU cores or a GPU, but for a single student, a basic 2GB RAM / 1 vCPU instance is usually sufficient.
