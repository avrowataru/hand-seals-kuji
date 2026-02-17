import cv2
import numpy as np

def probe_cameras(max_indices=5):
    """
    Probes camera indices 0-4 to find a valid BGR stream (excluding IR/Greyscale).
    Returns the optimal index or raises Exception.
    """
    print("Probing camera indices...")
    for idx in range(max_indices):
        print(f"Checking index {idx}...")
        # Enforce DirectShow for Windows 11 compatibility
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        
        if not cap.isOpened():
            print(f"Index {idx}: Failed to open.")
            cap.release()
            continue
            
        # Warmup and read
        for _ in range(5):
            cap.read()
        ret, frame = cap.read()
        
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        cap.release()
        
        if ret and frame is not None:
            # Check frame channels
            # Windows Hello IR cameras often appear as single channel or very low variance 3-channel
            # Simple heuristic: If it's valid BGR, we take it.
            # User rule: "If a frame is single-channel (grayscale), it is the IR sensor."
            
            if len(frame.shape) == 2:
                 print(f"Index {idx}: Skipped (Single Channel / Grayscale IR).")
                 continue
                 
            if len(frame.shape) == 3 and frame.shape[2] == 3:
                # Additional check: Some IR cameras return 3 channels but are visually greyscale.
                # We can check for color variance but let's stick to the explicit rule first.
                print(f"Index {idx}: Found valid BGR stream ({int(width)}x{int(height)}).")
                return idx
            
        print(f"Index {idx}: Skipped (No frame or invalid format).")
    
    raise Exception("No valid BGR camera found in indices 0-4.")

if __name__ == "__main__":
    try:
        idx = probe_cameras()
        print(f"SUCCESS: Selected Camera Index {idx}")
    except Exception as e:
        print(f"ERROR: {e}")
