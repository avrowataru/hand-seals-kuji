"""
Shadow Clone Jutsu — Real-Time Computer Vision
================================================
Entry point for the Shadow Clone Jutsu application.
Supports both GUI mode (default) and CLI-only diagnostic mode (--cli).

Usage:
    python main.py          # Full GUI mode with camera window
    python main.py --cli    # CLI-only: runs diagnostics and exits
"""

import cv2
import sys
import time
import argparse
import numpy as np
import mediapipe as mp
from src.utils.camera_check import probe_cameras
from src.app.jutsu_engine import JutsuDetector
from src.app.clone_engine import CloneRenderer


def log_startup_state(cam_idx, cap):
    """Logs diagnostic information at startup."""
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_cap = cap.get(cv2.CAP_PROP_FPS)
    backend = cap.getBackendName()

    print("=" * 60)
    print("  SHADOW CLONE JUTSU — STARTUP DIAGNOSTICS")
    print("=" * 60)
    print(f"  Python:           {sys.version.split()[0]}")
    print(f"  Python Path:      {sys.executable}")
    print(f"  OpenCV:           {cv2.__version__}")
    print(f"  MediaPipe:        {mp.__version__}")
    print(f"  NumPy:            {np.__version__}")
    print(f"  Camera Index:     {cam_idx}")
    print(f"  Camera Backend:   {backend}")
    print(f"  Resolution:       {width}x{height}")
    print(f"  Camera FPS Cap:   {fps_cap}")
    print(f"  VideoCapture OK:  {hasattr(cv2, 'VideoCapture')}")
    print(f"  Camera Opened:    {cap.isOpened()}")
    print("=" * 60)


def run_cli_mode():
    """
    CLI-only diagnostic mode. No GUI dependencies.
    Verifies camera access, logs state, and exits.
    """
    print("[CLI MODE] Running diagnostics only. No GUI window will open.\n")

    # 1. Environment Check
    print(f"[CHECK] Python:        {sys.version.split()[0]}")
    print(f"[CHECK] Interpreter:   {sys.executable}")
    print(f"[CHECK] cv2 version:   {cv2.__version__}")
    print(f"[CHECK] VideoCapture:  {hasattr(cv2, 'VideoCapture')}")
    print(f"[CHECK] MediaPipe:     {mp.__version__}")
    print(f"[CHECK] mp.solutions:  {hasattr(mp, 'solutions')}")
    print(f"[CHECK] NumPy:         {np.__version__}")

    # 2. Camera Probe
    print("\n[PROBE] Starting camera probe...")
    try:
        cam_idx = probe_cameras()
        cap = cv2.VideoCapture(cam_idx, cv2.CAP_DSHOW)

        if not cap.isOpened():
            print(f"[FAIL] Camera at index {cam_idx} failed to open.")
            return 1

        ret, frame = cap.read()
        if ret and frame is not None:
            h, w = frame.shape[:2]
            channels = frame.shape[2] if len(frame.shape) == 3 else 1
            print(f"[PASS] Camera Index {cam_idx}: {w}x{h}, {channels} channels")
        else:
            print(f"[FAIL] Camera at index {cam_idx} returned no frame.")
            cap.release()
            return 1

        cap.release()

    except Exception as e:
        print(f"[FAIL] Camera probe failed: {e}")
        return 1

    # 3. MediaPipe Quick Check
    print("\n[PROBE] Testing MediaPipe Hands initialization...")
    try:
        hands = mp.solutions.hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            model_complexity=0
        )
        hands.close()
        print("[PASS] MediaPipe Hands initialized and closed successfully.")
    except Exception as e:
        print(f"[FAIL] MediaPipe Hands failed: {e}")
        return 1

    print("\n" + "=" * 60)
    print("  ALL CHECKS PASSED — System ready for GUI mode.")
    print("  Run: python main.py")
    print("=" * 60)
    return 0


def run_gui_mode():
    """
    Full GUI mode with camera window, hand tracking, and clone rendering.
    """
    print("Initializing Shadow Clone Jutsu...")

    # 1. Camera Handling
    try:
        cam_idx = probe_cameras()
        cap = cv2.VideoCapture(cam_idx, cv2.CAP_DSHOW)

        if not cap.isOpened():
            print("FATAL: Camera opened but isOpened() returned False.")
            return

    except Exception as e:
        print(f"FATAL: {e}")
        return

    # Log startup diagnostics
    log_startup_state(cam_idx, cap)

    # 2. Engine Initialization
    detector = JutsuDetector()
    renderer = CloneRenderer()

    # State
    jutsu_active = False
    debug_mode = False

    print("\nSystem Ready.")
    print("Controls: 'q' to Quit, 'd' to toggle Debug Mode.")
    print("Perform the 'Ram' Seal (cross/touch fingers) to activate Jutsu!")

    prev_time = time.time()
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Ignoring empty camera frame.")
            continue

        frame_count += 1

        # Flip the image horizontally for a selfie-view display
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 3. Logic
        # A. Detect Seal
        active_now, hands_results = detector.detect_seal(frame_rgb)

        # Active while seal is detected (HOLD mode)
        jutsu_active = active_now

        # B. Render Clones
        output_frame = renderer.render(frame, active=jutsu_active)

        # 4. Debug UI
        if debug_mode:
            # Draw Hand Landmarks
            if hands_results.multi_hand_landmarks:
                for hand_landmarks in hands_results.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(
                        output_frame,
                        hand_landmarks,
                        mp.solutions.hands.HAND_CONNECTIONS)

            # Draw Status Text
            status_color = (0, 255, 0) if jutsu_active else (0, 0, 255)
            status_text = "ACTIVE" if jutsu_active else "INACTIVE"
            cv2.putText(output_frame, f"Jutsu: {status_text}",
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)

        # FPS Counter
        curr_time = time.time()
        elapsed = curr_time - prev_time
        fps = 1 / elapsed if elapsed > 0 else 0
        prev_time = curr_time
        cv2.putText(output_frame, f"FPS: {int(fps)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Periodic terminal FPS log (every 120 frames)
        if frame_count % 120 == 0:
            print(f"[PERF] Frame {frame_count} | FPS: {int(fps)} | Jutsu: {'ON' if jutsu_active else 'OFF'}")

        # Display
        cv2.imshow('Shadow Clone Jutsu', output_frame)

        key = cv2.waitKey(5) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('d'):
            debug_mode = not debug_mode
            print(f"[UI] Debug Mode: {'ON' if debug_mode else 'OFF'}")

    print(f"\n[EXIT] Processed {frame_count} frames. Releasing camera.")
    cap.release()
    cv2.destroyAllWindows()


def main():
    """Entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Shadow Clone Jutsu — Real-Time Computer Vision",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py          Full GUI mode with camera window
  python main.py --cli    CLI-only diagnostics (no GUI)
        """
    )
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Run in CLI-only diagnostic mode (no GUI window)'
    )

    args = parser.parse_args()

    if args.cli:
        exit_code = run_cli_mode()
        sys.exit(exit_code)
    else:
        run_gui_mode()


if __name__ == "__main__":
    main()
