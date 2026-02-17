"""
Clone Engine — Shadow Clone Rendering
======================================
Extracts user via SelfieSegmentation, generates two horizontally-shifted
clones with blue chakra tint and smooth alpha blending.

Performance: NumPy slicing only. Zero Python loops in the render path.
"""

import cv2
import numpy as np
import mediapipe as mp


class CloneEngine:
    """
    Handles real-time body segmentation and shadow clone compositing.

    Pipeline:
        1. SelfieSegmentation → raw mask
        2. Binary threshold → Gaussian blur (edge smoothing)
        3. Extract foreground
        4. Slice-shift to ±offset positions
        5. Apply blue tint + alpha blend
        6. Composite: Background → Clones → Real User (layered)
    """

    def __init__(self, offset_x=350, clone_alpha=0.7, tint_bgr=(255, 100, 100)):
        self.mp_seg = mp.solutions.selfie_segmentation
        # model_selection=1 is landscape-optimized
        self.segmentor = self.mp_seg.SelfieSegmentation(model_selection=1)
        self.offset_x = offset_x
        self.clone_alpha = clone_alpha
        # BGR tint color for "chakra" effect
        self.tint_b = tint_bgr[0] / 255.0
        self.tint_g = tint_bgr[1] / 255.0
        self.tint_r = tint_bgr[2] / 255.0

    def render(self, frame, active=False):
        """
        Applies the shadow clone effect if active.

        Args:
            frame: BGR numpy array from camera.
            active: Whether JUTSU_ACTIVE is True.

        Returns:
            Composited BGR frame.
        """
        if not active:
            return frame

        h, w, _ = frame.shape
        off = self.offset_x

        # --- Layer 0: Background (original frame) ---
        # We'll use this as the base canvas.

        # --- Segmentation ---
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        seg_result = self.segmentor.process(frame_rgb)
        raw_mask = seg_result.segmentation_mask  # float32 (H, W), range [0, 1]

        # --- Mask Refinement (Edge Smoothing) ---
        # Binary threshold to kill weak confidence areas
        _, binary_mask = cv2.threshold(raw_mask, 0.5, 1.0, cv2.THRESH_BINARY)
        # 3x3 Gaussian blur on mask edges for smooth "ghostly" boundaries
        smooth_mask = cv2.GaussianBlur(binary_mask, (3, 3), 0)
        # Expand to 3-channel for broadcasting: (H, W) → (H, W, 3)
        mask_3d = smooth_mask[:, :, np.newaxis]  # broadcasts automatically with *

        # --- Layer 2: Extract Foreground (Real User) ---
        fg = frame.astype(np.float32)
        foreground = fg * mask_3d  # user pixels only, background = 0

        # --- Layer 1: Generate Clones via Slicing ---
        # Left clone: shift user pixels LEFT by 'off'
        # Right clone: shift user pixels RIGHT by 'off'
        left_clone = np.zeros_like(fg)
        right_clone = np.zeros_like(fg)

        if off < w:
            # Left: src[off:] → dst[:w-off]  (move image leftward)
            left_clone[:, :w - off] = foreground[:, off:]
            # Right: src[:w-off] → dst[off:]  (move image rightward)
            right_clone[:, off:] = foreground[:, :w - off]

        # --- Blue Chakra Tint ---
        # Multiply each channel by the tint ratio
        # BGR order: index 0=B, 1=G, 2=R
        left_clone[:, :, 0] *= self.tint_b   # Blue
        left_clone[:, :, 1] *= self.tint_g   # Green
        left_clone[:, :, 2] *= self.tint_r   # Red
        right_clone[:, :, 0] *= self.tint_b
        right_clone[:, :, 1] *= self.tint_g
        right_clone[:, :, 2] *= self.tint_r

        # --- Compositing (Layered Alpha Blend) ---
        # Build clone masks for proper alpha compositing
        # Clone mask = shifted version of the user mask
        left_mask = np.zeros_like(smooth_mask)
        right_mask = np.zeros_like(smooth_mask)
        if off < w:
            left_mask[:, :w - off] = smooth_mask[:, off:]
            right_mask[:, off:] = smooth_mask[:, :w - off]

        left_mask_3d = left_mask[:, :, np.newaxis] * self.clone_alpha
        right_mask_3d = right_mask[:, :, np.newaxis] * self.clone_alpha
        user_mask_3d = mask_3d  # full opacity for real user

        # Start with background
        output = fg.copy()

        # Blend left clone: output = output * (1 - alpha) + clone * alpha  (where clone exists)
        output = output * (1 - left_mask_3d) + left_clone * left_mask_3d

        # Blend right clone
        output = output * (1 - right_mask_3d) + right_clone * right_mask_3d

        # Re-draw real user on TOP (full opacity over clones)
        output = output * (1 - user_mask_3d) + fg * user_mask_3d

        # Clamp and convert
        output = np.clip(output, 0, 255).astype(np.uint8)
        return output
