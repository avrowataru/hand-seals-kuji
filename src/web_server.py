"""
Web Server — FastAPI MJPEG Streaming
=====================================
Serves the Shadow Clone Jutsu video feed over HTTP as an MJPEG stream.
The heavy processing runs on the server (Python/NumPy/MediaPipe),
while the browser renders the result in a modern glassmorphism UI.

Endpoints:
    GET /            → index.html (Floating UI)
    GET /video_feed  → MJPEG streaming response
    GET /status      → JSON with current jutsu state & FPS
"""

import cv2
import time
import threading
import numpy as np
import mediapipe as mp
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.utils.camera_check import probe_cameras
from src.engines.gesture_engine import GestureEngine
from src.engines.clone_engine import CloneEngine

# ============================================================
# Global State (Thread-safe via GIL for simple reads/writes)
# ============================================================
_state = {
    "jutsu_active": False,
    "fps": 0,
    "debug_mode": False,
    "camera_index": -1,
    "resolution": "unknown",
    "running": False,
}

_latest_frame = None
_frame_lock = threading.Lock()
_camera_thread = None

# ============================================================
# Camera Processing Thread
# ============================================================
def camera_loop():
    """
    Background thread that captures frames, runs gesture detection
    and clone rendering, and stores the latest JPEG-encoded frame.
    """
    global _latest_frame

    # 1. Camera Init
    try:
        cam_idx = probe_cameras()
        cap = cv2.VideoCapture(cam_idx, cv2.CAP_DSHOW)
        if not cap.isOpened():
            print("[FATAL] Camera failed to open.")
            return
    except Exception as e:
        print(f"[FATAL] Camera probe failed: {e}")
        return

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    _state["camera_index"] = cam_idx
    _state["resolution"] = f"{w}x{h}"
    _state["running"] = True

    print(f"[CAMERA] Index {cam_idx} | {w}x{h} | Backend: {cap.getBackendName()}")

    # 2. Engine Init
    gesture = GestureEngine(touch_threshold=0.05)
    cloner = CloneEngine(offset_x=350, clone_alpha=0.7, tint_bgr=(255, 100, 100))

    prev_time = time.time()
    frame_count = 0

    while _state["running"]:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Gesture Detection
        active, hand_results = gesture.detect(frame_rgb)
        _state["jutsu_active"] = active

        # Clone Rendering
        output = cloner.render(frame, active=active)

        # Debug overlay (optional, toggled via /toggle_debug)
        if _state["debug_mode"]:
            output = gesture.draw_landmarks(output, hand_results)
            status_color = (0, 255, 0) if active else (0, 0, 255)
            label = "JUTSU: ACTIVE" if active else "JUTSU: INACTIVE"
            cv2.putText(output, label, (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)

        # FPS
        now = time.time()
        elapsed = now - prev_time
        fps = 1.0 / elapsed if elapsed > 0 else 0
        prev_time = now
        _state["fps"] = round(fps, 1)
        frame_count += 1

        # FPS overlay
        cv2.putText(output, f"FPS: {int(fps)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        # Encode to JPEG
        _, jpeg = cv2.imencode('.jpg', output, [cv2.IMWRITE_JPEG_QUALITY, 85])

        with _frame_lock:
            _latest_frame = jpeg.tobytes()

        # Periodic log
        if frame_count % 300 == 0:
            print(f"[PERF] Frame {frame_count} | FPS: {int(fps)} | Jutsu: {'ON' if active else 'OFF'}")

    cap.release()
    print("[CAMERA] Released.")


def generate_mjpeg():
    """Generator that yields MJPEG frames for StreamingResponse."""
    while _state["running"]:
        with _frame_lock:
            frame = _latest_frame

        if frame is None:
            time.sleep(0.01)
            continue

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame
            + b"\r\n"
        )
        # Throttle to ~60fps max to avoid overwhelming the client
        time.sleep(0.016)


# ============================================================
# Lifespan (replaces deprecated @app.on_event)
# ============================================================
@asynccontextmanager
async def lifespan(app):
    """Modern lifespan handler — clean startup & shutdown."""
    global _camera_thread

    # — Startup —
    _camera_thread = threading.Thread(target=camera_loop, daemon=True)
    _camera_thread.start()
    print("[SERVER] Camera thread started.")

    yield  # App is running

    # — Shutdown (Ctrl+C) —
    print("[SERVER] Shutting down camera thread...")
    _state["running"] = False
    if _camera_thread is not None:
        _camera_thread.join(timeout=3.0)
    print("[SERVER] Clean shutdown complete.")


# ============================================================
# FastAPI App (with lifespan)
# ============================================================
app = FastAPI(title="Shadow Clone Jutsu", version="2.0.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ============================================================
# Routes
# ============================================================
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Serve the main Floating UI page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/video_feed")
async def video_feed():
    """MJPEG streaming endpoint."""
    return StreamingResponse(
        generate_mjpeg(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.get("/status")
async def status():
    """JSON endpoint for current jutsu state."""
    return JSONResponse({
        "jutsu_active": _state["jutsu_active"],
        "fps": _state["fps"],
        "debug_mode": _state["debug_mode"],
        "camera_index": _state["camera_index"],
        "resolution": _state["resolution"],
        "running": _state["running"],
    })


@app.post("/toggle_debug")
async def toggle_debug():
    """Toggle debug overlay on the video stream."""
    _state["debug_mode"] = not _state["debug_mode"]
    return JSONResponse({
        "debug_mode": _state["debug_mode"]
    })
