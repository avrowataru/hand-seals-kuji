# 🚀 Execution Workflow — Shadow Clone Jutsu

> This document defines the **exact procedure** for running the application in both **Terminal GUI** and **Web Application** modes. Follow the appropriate section for your desired experience.

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
| 8 | Web dependencies | `pip show fastapi uvicorn` | Both packages listed |
| 9 | Camera physically available | Visual check | Webcam LED indicator accessible |

> ⚠️ If check #7 shows **both** `opencv-python` and `opencv-contrib-python`, **STOP** and follow [`troubleshoot.md`](troubleshoot.md).

---

## Phase 1: Camera Verification (Recommended)

Run the camera probe **before** launching either mode to confirm the correct index is selected.

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

---

## Phase 2: Execution Modes

### Option A: Terminal GUI Mode (Classic)

Best for low-latency testing and debugging.

```powershell
# Ensure environment is active
conda activate sha

# Launch
python main.py
```

**Expected Window Behavior:**
| State | What You See |
|---|---|
| **Idle** | Live webcam feed with yellow FPS counter in top-left |
| **Debug Mode (`d`)** | Hand landmarks drawn, `Jutsu: INACTIVE` in red text |
| **Seal Detected** | Two translucent blue-tinted clones appear ±300px from user |
| **Debug + Active** | Landmarks + `Jutsu: ACTIVE` in green + clones visible |

### Option B: Web Application Mode (Modern)

Best for user experience and visual presentation.

```powershell
# Ensure environment is active
conda activate sha

# Launch Server
python run_web.py
```

**Accessing the App:**
1. Open your browser to **http://localhost:8000**
2. The Glassmorphism UI should load immediately.
3. Allow camera access if prompted by the browser.

**Web Dashboard Features:**
- **Live Video Feed**: Centered MJPEG stream.
- **Status Panel**: Real-time indicators for Camera, Engine, Jutsu State, and FPS.
- **Controls**: Toggle Debug Mode or specific effects directly from the UI.

---

## Phase 3: Runtime Verification

### 3.1 — FPS Monitoring

| FPS Range | Assessment | Action |
|---|---|---|
| **45–60+** | ✅ Excellent | No action needed |
| **25–44** | ⚠️ Acceptable | Consider reducing resolution |
| **< 25** | ❌ Poor | Check CPU load; see optimization notes below |

### 3.2 — Gesture Verification

1. Hold your hand in front of the camera, palm facing outward.
2. Slowly bring your **Index** and **Middle** finger tips together.
3. **Terminal**: Watch for `Jutsu: ACTIVE` (press `d` to see status).
4. **Web**: Watch the "Jutsu Status" indicator turn **Cyan** and pulse.

### 3.3 — Clone Quality Check

| Observation | Root Cause | Fix |
|---|---|---|
| Clones have jagged edges | Mask blur too low | Increase kernel in `src/engines/clone_engine.py` |
| Clones are too faint | Blend alpha too low | Increase `0.6` weight in `addWeighted` calls |
| Clones overlap the real user | Offset too small | Increase `self.offset_x` in `CloneEngine` |

---

## Phase 4: Graceful Shutdown

| Mode | Action | Result |
|---|---|---|
| **Terminal** | Press `q` in the OpenCV window | Windows close, camera releases |
| **Web** | `Ctrl+C` in the terminal | Server stops, camera releases |

> **Always ensure the camera is released.** If the camera LED stays on after exit, you may need to plug/unplug the camera or restart the computer.

---

## Alternative Launch: Batch Script

For quick access to the **Terminal Mode**:

```powershell
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
| MJPEG Throttling | ✅ Active | Web stream limited to ~60fps to save bandwidth |

---

## Project Metadata Reference

> *Consistent with `.idea/project_metadata.xml` equivalent.*

| Key | Value |
|---|---|
| **Entry Points** | `main.py` (GUI), `run_web.py` (Web) |
| **Python Interpreter** | `C:\Users\Rambo\miniconda3\envs\sha\python.exe` |
| **Working Directory** | `C:\Users\Rambo\Documents\source\shadowclone` |
| **Camera Backend** | `cv2.CAP_DSHOW` (DirectShow) |
| **Verified Camera Index** | 0 |
| **Verified Resolution** | 640×480 |
| **Last Verified** | 2026-02-17T23:18:01+09:00 |

---

## Related Documents

| Document | Purpose |
|---|---|
| [`README.md`](README.md) | Project overview and architecture |
| [`troubleshoot.md`](troubleshoot.md) | cv2 conflict resolution and recovery |
| [`walkthrough.md`](walkthrough.md) | Quick start guide |
