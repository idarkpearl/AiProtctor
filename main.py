from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as proctor_router
import uvicorn
import os

# Suppress TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

app = FastAPI(title="AI Proctoring Backend Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(proctor_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "AI Proctoring Service is running"}

if __name__ == "__main__":
    # Use reload=False to avoid issues with MediaPipe initialization in some environments
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
