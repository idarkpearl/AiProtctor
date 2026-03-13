import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np
import os

class FaceLandmarkDetector:
    def __init__(self, model_path='models/face_landmarker.task'):
        # Initialize MediaPipe Face Landmarker
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
            num_faces=1
        )
        self.detector = vision.FaceLandmarker.create_from_options(options)

    def detect(self, frame):
        """
        Detects face landmarks and returns gaze + mouth statistics.
        """
        # Convert frame to MediaPipe Image
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        results = self.detector.detect(mp_image)
        
        face_present = False
        looking_away = False
        gaze_direction = "Center"
        is_talking = False
        mouth_open_ratio = 0
        
        if results.face_landmarks:
            face_present = True
            landmarks = results.face_landmarks[0]
            
            # 1. Gaze / Head Direction (Simplified using Blendshapes if available)
            if results.face_blendshapes:
                blendshapes = {b.category_name: b.score for b in results.face_blendshapes[0]}
                
                # Yaw (Looking Left/Right)
                eye_look_in_left = blendshapes.get('eyeLookInLeft', 0)
                eye_look_in_right = blendshapes.get('eyeLookInRight', 0)
                eye_look_out_left = blendshapes.get('eyeLookOutLeft', 0)
                eye_look_out_right = blendshapes.get('eyeLookOutRight', 0)

                if eye_look_out_left > 0.4 or eye_look_in_right > 0.4:
                    gaze_direction = "Left"
                    looking_away = True
                elif eye_look_out_right > 0.4 or eye_look_in_left > 0.4:
                    gaze_direction = "Right"
                    looking_away = True
                
                # Pitch (Looking Up/Down)
                eye_look_up_left = blendshapes.get('eyeLookUpLeft', 0)
                eye_look_up_right = blendshapes.get('eyeLookUpRight', 0)
                eye_look_down_left = blendshapes.get('eyeLookDownLeft', 0)
                eye_look_down_right = blendshapes.get('eyeLookDownRight', 0)

                # Normalized pitch score (positive = down, negative = up)
                pitch_score = (eye_look_down_left + eye_look_down_right) / 2 - (eye_look_up_left + eye_look_up_right) / 2

                if pitch_score > 0.4: # Increased from 0.3
                    gaze_direction = "Down"
                    looking_away = True
                elif pitch_score < -0.4: # Increased from 0.3
                    gaze_direction = "Up"
                    looking_away = True

                # 2. Talking Detection (using Jaw Open blendshape)
                jaw_open = blendshapes.get('jawOpen', 0)
                mouth_open_ratio = jaw_open
                if jaw_open > 0.08: # Lowered from 0.15 for better sensitivity
                    is_talking = True

        return {
            "face_present": face_present,
            "looking_away": looking_away,
            "gaze_direction": gaze_direction,
            "pitch_score": round(float(pitch_score if face_present else 0), 2),
            "is_talking": is_talking,
            "mouth_open_ratio": round(float(mouth_open_ratio), 2)
        }
