from ultralytics import YOLO
import cv2

class PersonPhoneDetector:
    def __init__(self):
        # Load the pre-trained YOLOv8 nano model (efficient for CPU)
        # Note: This will download the weights automatically on first run
        # Upgrade to Small model for better accuracy than Nano
        self.model = YOLO('yolov8s.pt') 
        # COCO class IDs: 0 for person, 67 for cell phone, 73 for book, 63 for laptop
        self.target_classes = [0, 67, 73, 63]
        self.conf_threshold = 0.20 # Lowered for better recall of small devices

    def detect(self, frame):
        """
        Detects people and cell phones in the frame.
        Returns detection counts and presence.
        """
        results = self.model(frame, classes=self.target_classes, conf=self.conf_threshold, verbose=False)[0]
        
        person_count = 0
        phone_detected = False
        book_detected = False
        laptop_detected = False
        
        for box in results.boxes:
            cls_id = int(box.cls[0].item())
            if cls_id == 0:
                person_count += 1
            elif cls_id == 67:
                phone_detected = True
            elif cls_id == 73:
                book_detected = True
            elif cls_id == 63:
                laptop_detected = True
        
        return {
            "person_count": person_count,
            "multiple_people": person_count > 1,
            "phone_detected": phone_detected,
            "book_detected": book_detected,
            "laptop_detected": laptop_detected
        }
