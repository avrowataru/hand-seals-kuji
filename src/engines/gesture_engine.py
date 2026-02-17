"""
Gesture Engine — Ram Seal Detection
====================================
Detects the 'Ram' seal (Index Tip ID 8 + Middle Tip ID 12 proximity)
using MediaPipe Hands with model_complexity=0 for maximum throughput.
"""

import mediapipe as mp
import math


class GestureEngine:
    """
    Detects the 'Ram' seal using MediaPipe Hands.

    Trigger condition: Index Finger Tip (landmark 8) and Middle Finger Tip
    (landmark 12) of the SAME hand within normalized distance of 0.05.
    Also supports two-hand cross detection.
    """

    def __init__(self, touch_threshold=0.05):
        self.mp_hands = mp.solutions.hands
        # OPTIMIZATION: model_complexity=0 — lightest model for 60FPS
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
            model_complexity=0
        )
        self.TOUCH_THRESHOLD = touch_threshold
        self.mp_drawing = mp.solutions.drawing_utils

    def detect(self, frame_rgb):
        """
        Processes an RGB frame and returns (jutsu_active, hand_results).

        Args:
            frame_rgb: numpy array in RGB format.

        Returns:
            (bool, mediapipe results): Whether the seal is active, and raw results.
        """
        results = self.hands.process(frame_rgb)
        jutsu_active = False

        if results.multi_hand_landmarks:
            # Collect all (index_tip, middle_tip) pairs
            tips = []
            for hand_landmarks in results.multi_hand_landmarks:
                # Landmark 8: Index Finger Tip
                # Landmark 12: Middle Finger Tip
                tips.append((hand_landmarks.landmark[8], hand_landmarks.landmark[12]))

            # Intra-hand check: fingers crossed on same hand
            for index_tip, middle_tip in tips:
                dist = math.hypot(
                    index_tip.x - middle_tip.x,
                    index_tip.y - middle_tip.y
                )
                if dist < self.TOUCH_THRESHOLD:
                    jutsu_active = True
                    break

            # Inter-hand check: two hands touching (Naruto style)
            if not jutsu_active and len(tips) == 2:
                # Hand 1 Index → Hand 2 Middle
                d1 = math.hypot(tips[0][0].x - tips[1][1].x, tips[0][0].y - tips[1][1].y)
                # Hand 2 Index → Hand 1 Middle
                d2 = math.hypot(tips[1][0].x - tips[0][1].x, tips[1][0].y - tips[0][1].y)
                if d1 < self.TOUCH_THRESHOLD or d2 < self.TOUCH_THRESHOLD:
                    jutsu_active = True

        return jutsu_active, results

    def draw_landmarks(self, frame, results):
        """Draws hand landmarks onto the frame (debug mode)."""
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
        return frame
