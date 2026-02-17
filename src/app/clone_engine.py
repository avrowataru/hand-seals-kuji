import cv2
import numpy as np
import mediapipe as mp

class CloneRenderer:
    """
    Handles background segmentation and the 'Shadow Clone' rendering effect.
    Uses NumPy slicing for performance instead of looping or full array rolling.
    """
    def __init__(self):
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        # UDPATE: Use generic model (0 or 1), 0 is general, 1 is landscape. 
        self.segmentation = self.mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
        self.offset_x = 300 # Pixel shift for clones

    def render(self, frame, active=False):
        """
        Applies the clone effect if active.
        """
        if not active:
            return frame

        height, width, _ = frame.shape
        
        # 1. Get Segmentation Mask
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.segmentation.process(frame_rgb)
        mask = results.segmentation_mask
        
        # 2. Refine Mask (Edge Fraying Fix)
        # Apply strict binary threshold to clean up weak confidence areas
        _, binary_mask = cv2.threshold(mask, 0.5, 1.0, cv2.THRESH_BINARY)
        
        # Blur the mask to soften edges (Ghostly effect)
        # Using 5x5 Gaussian Blur as 3x3 might be too subtle for 1080p
        blurred_mask = cv2.GaussianBlur(binary_mask, (5, 5), 0)
        
        # Expand dimensions to match frame for broadcasting
        # mask is (H, W), need (H, W, 3)
        mask_3d = np.repeat(blurred_mask[:, :, np.newaxis], 3, axis=2)
        
        # 3. Create the extracted user (Foreground)
        # We multiply the frame by the mask. 
        # Background pixels become black (0), User pixels remain.
        foreground = frame * mask_3d
        
        # 4. Generate Clones using Slicing
        # Instead of np.roll (which wraps around), we want to SHIFT and CLIP.
        # Shift Left: User moves Left.   [User  ] -> [User  ] (Wait, shift left means x decreases)
        # Shift Right: User moves Right. [  User] 
        
        # Initialize canvas with the original frame (Background + Real User)
        # Note: If we want real user ON TOP of clones, we draw clones first.
        # Logic:
        # Base = Current Frame (Background + Real User)
        # Clone Layer = Shifted Foreground
        # Composite = Base + Clone (where Clone exists)
        
        # We'll create a black canvas for the clones to avoid messing up the background logic
        left_clone = np.zeros_like(frame, dtype=np.float32)
        right_clone = np.zeros_like(frame, dtype=np.float32)
        
        fw = width
        fh = height
        off = self.offset_x
        
        # Create Left Clone (Shift User to Left by 'off')
        # Target: [0 : W-off] receives Source: [off : W]
        if off < fw:
            # We take the pixels from 'off' to 'width' and place them at '0' to 'width-off'
            # This moves the image LEFT.
            left_clone[:, :fw-off] = foreground[:, off:]
            
        # Create Right Clone (Shift User to Right by 'off')
        # Target: [off : W] receives Source: [0 : W-off]
        if off < fw:
            # This moves the image RIGHT.
            right_clone[:, off:] = foreground[:, :fw-off]
            
        # 5. Tinting (Optional but cool)
        # Tint clones blue-ish for "Chakra" effect
        # BGR: Increase B, reduce G/R
        left_clone[:, :, 0] *= 1.5 # Boost Blue
        right_clone[:, :, 0] *= 1.5 # Boost Blue
        
        # 6. Composition
        # We overload the clones onto the main frame.
        # We use cv2.addWeighted for transparency/blending
        
        output = frame.astype(np.float32)
        
        # Add Left Clone (0.5 opacity)
        output = cv2.addWeighted(output, 1.0, left_clone, 0.6, 0.0)
        
        # Add Right Clone (0.5 opacity)
        output = cv2.addWeighted(output, 1.0, right_clone, 0.6, 0.0)
        
        # 7. Re-draw Real User on top? 
        # The 'frame' already contains the real user.
        # However, adding the clones might have brightened the background or the user.
        # Since 'left_clone' has black background (0), adding it to the real background (non-zero) works fine (additive blending).
        # But wait, additive blending (addWeighted) will make the overlapping parts brighter (blow out).
        # A proper alpha blend is better:
        # Result = Clone * Alpha + Background * (1-Alpha)
        # But constructing that is complex with raw numpy in one go.
        # Given "Performance" constraint:
        # Additive blending is fastest. Let's stick to it but maybe clamp to 255.
        
        output = np.clip(output, 0, 255).astype(np.uint8)
        
        return output
