from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.image_utils import decode_base64_image
from detection.face_landmark_detector import FaceLandmarkDetector
from detection.person_phone_detector import PersonPhoneDetector
from detection.hand_detector import HandDetector
from services.behavior_analyzer import BehaviorAnalyzer

router = APIRouter()

# Initialize detectors (using unified Landmark detector for Face and Gaze)
landmark_detector = FaceLandmarkDetector()
person_phone_detector = PersonPhoneDetector()
hand_detector = HandDetector()
analyzer = BehaviorAnalyzer()

class FrameData(BaseModel):
    image: str # Base64 encoded string

@router.post("/analyze")
async def analyze_frame(data: FrameData):
    frame = decode_base64_image(data.image)
    if frame is None:
        raise HTTPException(status_code=400, detail="Invalid image data")

    # 1. Run Detectors
    face_gaze_results = landmark_detector.detect(frame)
    person_results = person_phone_detector.detect(frame)
    hand_results = hand_detector.detect(frame)

    # 2. Analyze Behavior
    report = analyzer.analyze(
        face_gaze_results, 
        person_results, 
        hand_results
    )

    return report
