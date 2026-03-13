import logging

class BehaviorAnalyzer:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("BehaviorAnalyzer")

    def analyze(self, face_gaze_results, person_results, hand_results):
        """
        Aggregates detections and determines specific malpractices.
        """
        score = 0
        malpractices = []
        
        # 1. Face Presence
        if not face_gaze_results["face_present"]:
            score += 40
            malpractices.append("Face not detected (Candidate might have left or camera obscured)")

        # 2. Multiple People
        if person_results["multiple_people"]:
            score += 50
            malpractices.append(f"Multiple people detected ({person_results['person_count']} persons)")

        # 3. Phone/Device Detection
        if person_results["phone_detected"]:
            score += 60
            malpractices.append("Mobile phone detected in frame")
        
        if person_results.get("laptop_detected"):
            score += 30
            malpractices.append("Secondary screen/laptop detected")

        # 4. Notebook / Copy Detection
        if person_results.get("book_detected"):
            score += 45
            malpractices.append("Notebook/Book/Cheat-sheet detected")

        # 5. Gaze Direction & "Looking Down" Logic
        if face_gaze_results["looking_away"]:
            direction = face_gaze_results["gaze_direction"]
            pitch = face_gaze_results.get("pitch_score", 0)
            
            # Contextual "Looking Down" (Threshold for suspicious looking vs typing)
            if direction == "Down":
                # If pitch is extremely high, it's likely notes on lap, not just keyboard
                if pitch > 0.65: 
                    score += 30
                    malpractices.append("Suspiciously looking down (Potential hidden notes)")
                else:
                    # Mild looking down could be typing
                    score += 5 
                    # We don't necessarily flag as alert unless it's frequent (tracked in future temporal logic)
            else:
                score += 20
                malpractices.append(f"Looking away from screen (Direction: {direction})")

        # 6. Talking / Mouth Movement
        if face_gaze_results["is_talking"]:
            score += 15
            malpractices.append("Mouth movement detected (Talking/Whispering)")

        # 7. Hand Count (3rd Hand Detection)
        hand_count = hand_results["hand_count"]
        if hand_count > 2:
            score += 40
            malpractices.append(f"Suspicious hand count: {hand_count} hands detected (Possible assistance)")

        final_score = min(score, 100)
        
        # Log findings
        if malpractices:
            self.logger.warning(f"Malpractices: {', '.join(malpractices)}")

        return {
            "face_present": face_gaze_results["face_present"],
            "multiple_people": person_results["multiple_people"],
            "person_count": person_results["person_count"],
            "phone_detected": person_results["phone_detected"],
            "book_detected": person_results.get("book_detected", False),
            "looking_away": face_gaze_results["looking_away"],
            "gaze_direction": face_gaze_results["gaze_direction"],
            "pitch_score": face_gaze_results.get("pitch_score", 0),
            "is_talking": face_gaze_results["is_talking"],
            "hands_count": hand_count,
            "suspicion_score": final_score,
            "malpractices": malpractices
        }
