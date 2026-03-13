import mediapipe as mp
import sys
import os

print(f"Python version: {sys.version}")
print(f"MediaPipe version: {getattr(mp, '__version__', 'unknown')}")
print(f"MediaPipe path: {mp.__path__}")
print(f"Attributes in mp: {dir(mp)}")
try:
    print(f"Attributes in mp.solutions: {dir(mp.solutions)}")
except Exception as e:
    print(f"Error accessing mp.solutions: {e}")

try:
    import mediapipe.python.solutions.face_detection as fd
    print("Successfully imported mediapipe.python.solutions.face_detection")
except Exception as e:
    print(f"Error importing mediapipe.python: {e}")
