import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2

class HandDetector:
    def __init__(self, model_path='models/hand_landmarker.task'):
        # Initialize MediaPipe Hand Landmarker
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=4, 
            min_hand_detection_confidence=0.3
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def detect(self, frame):
        """
        Detects hands in the frame.
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        results = self.detector.detect(mp_image)
        
        hand_count = 0
        if results.hand_landmarks:
            hand_count = len(results.hand_landmarks)
            
        return {
            "hands_visible": hand_count > 0,
            "hand_count": hand_count
        }
