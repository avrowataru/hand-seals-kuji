import mediapipe as mp
import math

class JutsuDetector:
    """
    Detects the 'Ram' seal (Hand Clasp / Cross) using MediaPipe Hands.
    Logic: Checks if Index Finger Tip (8) and Middle Finger Tip (12) are touching/crossed.
    """
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        # OPTIMIZATION: model_complexity=0 for speed on Windows Python
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
            model_complexity=0
        )
        # Threshold for "touching" in normalized coordinates
        self.TOUCH_THRESHOLD = 0.04 

    def detect_seal(self, frame_rgb):
        """
        Processes frame and returns (jutsu_active, results).
        """
        results = self.hands.process(frame_rgb)
        jutsu_active = False

        if results.multi_hand_landmarks:
            # Check for the specific gesture
            # We need at least one hand, but ideally we check if fingers are crossed.
            # Simplified "Ram" Seal: Index and Middle fingers of the SAME hand or DIFFERENT hands are close.
            # Let's support a single hand 'crossing' fingers (easy) or two hands touching (Naruto style).
            # For robustness, we'll check if ANY Index Tip is close to ANY Middle Tip (on same or different hand).
            
            # Extract all tips
            tips = []
            for hand_landmarks in results.multi_hand_landmarks:
                # Landmark 8: Index Tip
                # Landmark 12: Middle Tip
                tips.append((hand_landmarks.landmark[8], hand_landmarks.landmark[12]))

            # Check intra-hand (crossing fingers on one hand)
            for index_tip, middle_tip in tips:
                dist = math.hypot(index_tip.x - middle_tip.x, index_tip.y - middle_tip.y)
                if dist < self.TOUCH_THRESHOLD:
                    jutsu_active = True
                    break
            
            # If not active yet, check inter-hand (if 2 hands detected)
            if not jutsu_active and len(tips) == 2:
                # Hand 1 Index to Hand 2 Middle
                dist_1 = math.hypot(tips[0][0].x - tips[1][1].x, tips[0][0].y - tips[1][1].y)
                # Hand 2 Index to Hand 1 Middle
                dist_2 = math.hypot(tips[1][0].x - tips[0][1].x, tips[1][0].y - tips[0][1].y)
                
                if dist_1 < self.TOUCH_THRESHOLD or dist_2 < self.TOUCH_THRESHOLD:
                    jutsu_active = True

        return jutsu_active, results
