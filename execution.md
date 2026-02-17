# 🚀 Execution Workflow — Shadow Clone Jutsu

> This document defines the **exact procedure** for running `main.py` and verifying the camera/video stream. Follow each phase sequentially.

---

## 📋 Pre-Flight Checklist

Before executing, confirm every item below:

| # | Check | Command / Action | Expected Result |
|---|---|---|---|
| 1 | Conda env exists | `conda env list` | `sha` appears in the list |
| 2 | Conda env active | `conda activate sha` | Prompt shows `(sha)` |
| 3 | Python version | `python --version` | `Python 3.11.x` |
| 4 | OpenCV installed | `python -c "import cv2; print(cv2.__version__)"` | `4.13.0` |
| 5 | MediaPipe installed | `python -c "import mediapipe as mp; print(mp.__version__)"` | `0.10.9` |
| 6 | Solutions accessible | `python -c "import mediapipe as mp; print(hasattr(mp, 'solutions'))"` | `True` |
| 7 | No opencv-python conflict | `pip list \| findstr opencv` | **Only** `opencv-contrib-python` listed |
| 8 | Camera physically available | Visual check | Webcam LED indicator accessible |

> ⚠️ If check #7 shows **both** `opencv-python` and `opencv-contrib-python`, **STOP** and follow [`troubleshoot.md`](troubleshoot.md).

---

## Phase 1: Camera Verification (Standalone)

Run the camera probe **before** launching the main app to confirm the correct index is selected.

```powershell
# Activate environment
conda activate sha

# Run the probe
python src/utils/camera_check.py
```

### Expected Output

```
Probing camera indices...
Checking index 0...
Index 0: Found valid BGR stream (640x480).
SUCCESS: Selected Camera Index 0
```

### Interpreting Results

| Output Pattern | Meaning | Action |
|---|---|---|
| `Found valid BGR stream (WxH)` | ✅ Color camera detected | Proceed to Phase 2 |
| `Skipped (Single Channel / Grayscale IR)` | ⚠️ IR sensor (Windows Hello) | Normal — probe continues to next index |
| `Failed to open` | ❌ No device at this index | Normal — probe continues |
| `No valid BGR camera found` | ❌ Fatal — no usable camera | Check physical connection, drivers, or other apps using the camera |

### Camera Index Reference

| Index | Typical Device (Windows Hello Laptop) | Channels | Action |
|---|---|---|---|
| 0 | IR Camera (Windows Hello) | 1 (Grayscale) | Skip |
| 1 | RGB Webcam | 3 (BGR) | **Use this** |
| 2 | Secondary / External | 3 (BGR) | Fallback |
| 3–4 | Virtual / Unused | — | Skip |

> **Note:** On this machine, Index 0 returned a valid BGR stream. This is because the current laptop's camera driver exposes the color stream first. This may differ on other hardware.

---

## Phase 2: Full Application Launch

```powershell
# Ensure environment is active
conda activate sha

# Launch
python main.py
```

### Expected Console Output

```
Initializing Shadow Clone Jutsu...
Probing camera indices...
Checking index 0...
Index 0: Found valid BGR stream (640x480).
System Ready.
Controls: 'q' to Quit, 'd' to toggle Debug Mode.
Perform the 'Ram' Seal (cross/touch fingers) to activate Jutsu!
INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
```

### Expected Window Behavior

| State | What You See |
|---|---|
| **Idle** | Live webcam feed with yellow FPS counter in top-left |
| **Debug Mode (`d`)** | Hand landmarks drawn, `Jutsu: INACTIVE` in red text |
| **Seal Detected** | Two translucent blue-tinted clones appear ±300px from user |
| **Debug + Active** | Landmarks + `Jutsu: ACTIVE` in green + clones visible |

---

## Phase 3: Runtime Verification

### 3.1 — FPS Monitoring

The FPS counter is rendered at `(10, 30)` on every frame in yellow (`0, 255, 255`).

| FPS Range | Assessment | Action |
|---|---|---|
| **45–60+** | ✅ Excellent | No action needed |
| **25–44** | ⚠️ Acceptable | Consider reducing resolution |
| **< 25** | ❌ Poor | Check CPU load; see optimization notes below |

### 3.2 — Gesture Verification

1. Hold your hand in front of the camera, palm facing outward.
2. Slowly bring your **Index** and **Middle** finger tips together.
3. In debug mode (`d`), watch for `Jutsu: ACTIVE` to appear.
4. If it doesn't trigger, try adjusting `TOUCH_THRESHOLD` in `src/app/jutsu_engine.py` (default: `0.04`).

### 3.3 — Clone Quality Check

| Observation | Root Cause | Fix |
|---|---|---|
| Clones have jagged edges | Mask blur too low | Increase kernel in `clone_engine.py` from `(5, 5)` to `(9, 9)` |
| Clones are too faint | Blend alpha too low | Increase `0.6` weight in `addWeighted` calls |
| Clones are blown out (white) | Additive blending overflow | Already handled by `np.clip(output, 0, 255)` |
| Clones overlap the real user | Offset too small | Increase `self.offset_x` from `300` to `400+` |

---

## Phase 4: Graceful Shutdown

| Method | Key / Action | Behavior |
|---|---|---|
| **Normal** | Press `q` in the OpenCV window | `cap.release()` + `cv2.destroyAllWindows()` |
| **Force** | `Ctrl+C` in terminal | `KeyboardInterrupt` — camera released but window may linger |
| **Emergency** | Close terminal | Camera released by OS; may need to restart for next run |

> **Always prefer pressing `q`** to ensure the camera is properly released. Failure to release can lock the camera for subsequent runs.

---

## Alternative Launch: Batch Script

For convenience, a one-click launcher is provided:

```powershell
# From project root
.\run_jutsu.bat
```

This activates the `sha` conda environment and runs `main.py` automatically.

---

## Optimization Notes (RTX 4070)

| Technique | Status | Notes |
|---|---|---|
| `model_complexity=0` | ✅ Active | Hand tracker uses lightest model |
| NumPy vectorized slicing | ✅ Active | No Python `for` loops in render pipeline |
| `cv2.UMat` (Transparent API) | ⬜ Available | Can wrap frames in `cv2.UMat()` for GPU-backed OpenCV ops |
| Resolution scaling | ⬜ Available | Uncomment lines 18–19 in `main.py` for 1280×720 |
| Frame skipping | ⬜ Not implemented | Process every Nth frame for segmentation if needed |

---

## Project Metadata Reference

> *Consistent with `.idea/project_metadata.xml` equivalent.*

| Key | Value |
|---|---|
| **Entry Point** | `main.py` |
| **Python Interpreter** | `C:\Users\Rambo\miniconda3\envs\sha\python.exe` |
| **Working Directory** | `C:\Users\Rambo\Documents\source\shadowclone` |
| **Camera Backend** | `cv2.CAP_DSHOW` (DirectShow) |
| **Verified Camera Index** | 0 |
| **Verified Resolution** | 640×480 |
| **TFLite Delegate** | XNNPACK (CPU) |
| **Last Successful Run** | 2026-02-17T21:48:49+09:00 |

---

## Related Documents

| Document | Purpose |
|---|---|
| [`README.md`](README.md) | Project overview and architecture |
| [`troubleshoot.md`](troubleshoot.md) | cv2 conflict resolution and recovery |
