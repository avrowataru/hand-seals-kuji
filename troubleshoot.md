# 🔧 Troubleshooting Guide — Shadow Clone Jutsu

> This document provides **definitive resolution** for the `cv2` namespace collision and other common failure modes encountered during development.

---

## 📋 Table of Contents

- [🔴 Critical: The cv2 Namespace Collision](#-critical-the-cv2-namespace-collision)
- [🟡 Scorched Earth Protocol](#-scorched-earth-protocol)
- [🟢 Verification One-Liners](#-verification-one-liners)
- [Common Failure Modes](#common-failure-modes)
- [Project Metadata Reference](#project-metadata-reference)
- [Incident Timeline](#incident-timeline)

---

## 🔴 Critical: The cv2 Namespace Collision

### The Problem

On Windows, `pip install opencv-python` and `pip install opencv-contrib-python` both install a package that occupies the **same** `cv2` namespace in `site-packages`. When both are installed:

```
site-packages/
├── cv2/                    ← ONE namespace, TWO packages fighting for it
│   ├── __init__.py         ← May point to wrong .pyd binary
│   └── cv2.pyd             ← The actual compiled module
├── opencv_python-4.13.0.92.dist-info/
└── opencv_contrib_python-4.13.0.92.dist-info/
```

### The Symptom

```python
>>> import cv2
>>> cv2.VideoCapture(0)
AttributeError: module 'cv2' has no attribute 'VideoCapture'
```

Or even more deceptively:

```python
>>> import cv2
>>> cv2.__version__
AttributeError: module 'cv2' has no attribute '__version__'
```

### Root Cause Analysis

| Scenario | What Happens | Result |
|---|---|---|
| Only `opencv-python` installed | cv2 namespace → core OpenCV | ✅ Works |
| Only `opencv-contrib-python` installed | cv2 namespace → OpenCV + contrib modules | ✅ Works |
| **Both installed** | pip uninstalls one's `.pyd`, leaves the other's `.dist-info` | ❌ **Broken** — `cv2` folder exists but is hollow |
| Uninstall one, reinstall other | Residual `__pycache__` or `.pyd` fragments may persist | ⚠️ **May still be broken** |

### The Rule (Non-Negotiable)

> **You must NEVER have both `opencv-python` and `opencv-contrib-python` installed in the same environment.**
>
> This project uses **`opencv-contrib-python` exclusively**.

---

## 🟡 Scorched Earth Protocol

When the `cv2` namespace is corrupted beyond simple `pip uninstall`, follow this nuclear recovery procedure.

### Step 1: Full Uninstallation

```powershell
# Activate the target environment
conda activate sha

# Uninstall ALL OpenCV variants
pip uninstall -y opencv-python opencv-contrib-python opencv-python-headless opencv-contrib-python-headless

# Verify removal
pip list | findstr opencv
# Expected: (no output)
```

### Step 2: Purge Residual Files

```powershell
# Navigate to the environment's site-packages
$sitePackages = "C:\Users\Rambo\miniconda3\envs\sha\Lib\site-packages"

# Remove any residual cv2 directory
Remove-Item -Recurse -Force "$sitePackages\cv2" -ErrorAction SilentlyContinue

# Remove any residual dist-info directories
Remove-Item -Recurse -Force "$sitePackages\opencv_python*" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$sitePackages\opencv_contrib*" -ErrorAction SilentlyContinue

# Verify the directory is gone
Test-Path "$sitePackages\cv2"
# Expected: False
```

### Step 3: Clean Reinstall

```powershell
# Install ONLY opencv-contrib-python (includes everything opencv-python has + extra modules)
pip install opencv-contrib-python==4.13.0.92

# Verify
python -c "import cv2; print(cv2.__version__); print(cv2.VideoCapture)"
# Expected:
# 4.13.0
# <built-in function VideoCapture>
```

### Step 4: Reinstall Full Stack

```powershell
# Install all project dependencies (requirements.txt already specifies opencv-contrib-python)
pip install -r requirements.txt

# Run the verification script
python verify_env.py
# Expected:
# CV2 Version: 4.13.0
# MediaPipe Version: 0.10.9
# MP Solutions: Found
```

### Step 5: Validate Camera Access

```powershell
python src/utils/camera_check.py
# Expected:
# Probing camera indices...
# Checking index 0...
# Index 0: Found valid BGR stream (640x480).
# SUCCESS: Selected Camera Index 0
```

---

## 🟢 Verification One-Liners

Copy-paste these one at a time to confirm your environment is healthy:

```powershell
# ✅ Check 1: Python version
python --version
# Expected: Python 3.11.x

# ✅ Check 2: cv2 imports and has VideoCapture
python -c "import cv2; print(f'cv2 OK: {cv2.__version__}')"
# Expected: cv2 OK: 4.13.0

# ✅ Check 3: cv2.VideoCapture is a callable
python -c "import cv2; assert callable(cv2.VideoCapture), 'BROKEN'; print('VideoCapture: OK')"
# Expected: VideoCapture: OK

# ✅ Check 4: No duplicate opencv packages
pip list | findstr opencv
# Expected: ONLY opencv-contrib-python    4.13.0.92

# ✅ Check 5: MediaPipe solutions accessible
python -c "import mediapipe as mp; assert hasattr(mp, 'solutions'); print('MediaPipe Solutions: OK')"
# Expected: MediaPipe Solutions: OK

# ✅ Check 6: Full integration test
python -c "import cv2, mediapipe, numpy; print(f'cv2={cv2.__version__} mp={mediapipe.__version__} np={numpy.__version__}')"
# Expected: cv2=4.13.0 mp=0.10.9 np=2.4.2

# ✅ Check 7: Camera accessible (quick open/close)
python -c "import cv2; c=cv2.VideoCapture(0,cv2.CAP_DSHOW); print(f'Camera Open: {c.isOpened()}'); c.release()"
# Expected: Camera Open: True
```

### Health Status Table

Run all checks and fill in:

| # | Check | Command | Status |
|---|---|---|---|
| 1 | Python 3.11 | `python --version` | ⬜ |
| 2 | cv2 import | `python -c "import cv2; print(cv2.__version__)"` | ⬜ |
| 3 | VideoCapture exists | `python -c "import cv2; print(callable(cv2.VideoCapture))"` | ⬜ |
| 4 | No duplicate opencv | `pip list \| findstr opencv` | ⬜ |
| 5 | MediaPipe solutions | `python -c "import mediapipe as mp; print(hasattr(mp, 'solutions'))"` | ⬜ |
| 6 | Camera opens | `python -c "import cv2; c=cv2.VideoCapture(0,cv2.CAP_DSHOW); print(c.isOpened()); c.release()"` | ⬜ |

---

## Common Failure Modes

### 1. `ModuleNotFoundError: No module named 'cv2'`

| Cause | Fix |
|---|---|
| Wrong Python interpreter | Use `c:\Users\Rambo\miniconda3\envs\sha\python.exe` explicitly |
| Conda env not activated | `conda activate sha` |
| cv2 not installed in `sha` | `pip install opencv-contrib-python` |

### 2. `AttributeError: module 'cv2' has no attribute 'VideoCapture'`

| Cause | Fix |
|---|---|
| Namespace collision (see above) | Run [Scorched Earth Protocol](#-scorched-earth-protocol) |
| Stale `__pycache__` | Delete `site-packages/cv2/__pycache__/` |

### 3. `AttributeError: module 'mediapipe' has no attribute 'solutions'`

| Cause | Fix |
|---|---|
| MediaPipe version too new (0.10.10+) | `pip install mediapipe==0.10.9` |
| Protobuf version mismatch | `pip install protobuf==3.20.3` |
| Corrupted install | `pip uninstall mediapipe && pip install mediapipe==0.10.9` |

### 4. Camera Shows Black / No Frame

| Cause | Fix |
|---|---|
| Wrong camera index (IR selected) | Run `python src/utils/camera_check.py` to find correct index |
| Another app using camera | Close Zoom, Teams, OBS, etc. |
| Windows Hello lock | Restart the application; camera may need to be released |
| Privacy settings | Windows Settings → Privacy → Camera → Allow desktop apps |

### 5. `INFO: Created TensorFlow Lite XNNPACK delegate for CPU.`

This is **not an error**. It's an informational message from MediaPipe confirming it's using the CPU-based XNNPACK delegate for TFLite inference. This is expected behavior on Windows Python.

### 6. Low FPS (< 30)

| Cause | Fix |
|---|---|
| `model_complexity` too high | Ensure `model_complexity=0` in `jutsu_engine.py` |
| High resolution camera | Set `cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)` in `main.py` |
| Background applications | Close resource-heavy apps |
| Power saving mode | Plug in laptop; set Windows power plan to "High Performance" |

### 7. Web Application Issues (run_web.py)

| Symptom | Cause | Fix |
|---|---|---|
| `[Errno 10048] Address already in use` | Port 8000 is taken | Kill the process or use `python run_web.py --port 9000` |
| Video feed spins forever | Camera locked by another app | Close other apps, or ensure `main.py` isn't running simultaneously |
| Styling looks broken | `static/css` not loading | Ensure you are running `run_web.py` from the project root |
| "Connection Refused" | Server not running | Validated `python run_web.py` is active in terminal |

---

## Incident Timeline

> *A historical record of the cv2 collision and its resolution during initial development.*

| Timestamp (JST) | Event | Outcome |
|---|---|---|
| `2026-02-17 21:18` | Project initialized with `requirements.txt` containing `opencv-python` | — |
| `2026-02-17 21:22` | Conda env `sha` created (Python 3.11) | ✅ |
| `2026-02-17 21:35` | First `main.py` run → `mp.solutions.hands` → AttributeError | ❌ MediaPipe 0.10.32 (wrong version from base env) |
| `2026-02-17 21:42` | Both `opencv-python` and `opencv-contrib-python` installed | ❌ **Collision** |
| `2026-02-17 21:47` | Uninstalled `opencv-python`, kept `opencv-contrib-python` only | ✅ Resolved |
| `2026-02-17 23:00` | **Web migration** initiated | ✅ FastAPI + Glassmorphism UI added |

### Lessons Learned

1. **Never install `opencv-python` alongside `opencv-contrib-python`** — they share the `cv2` namespace.
2. **Always use the full interpreter path** (`c:\...\envs\sha\python.exe`) when debugging environment issues to avoid Conda base shadowing.
3. **Pin MediaPipe to `0.10.9`** — later versions on Windows may break `mp.solutions` access.
4. **Pin Protobuf to `3.20.3`** — MediaPipe 0.10.9 is sensitive to Protobuf version changes.
5. **Release Camera Resources** — Always ensure `cap.release()` is called, especially when switching between Terminal and Web modes.

---

## Project Metadata Reference

> *Consistent with `.idea/project_metadata.xml` equivalent.*

| Key | Value |
|---|---|
| **Project Name** | Shadow Clone Jutsu |
| **Project Root** | `C:\Users\Rambo\Documents\source\shadowclone` |
| **Python Interpreter** | `C:\Users\Rambo\miniconda3\envs\sha\python.exe` |
| **Python Version** | 3.11.14 |
| **Environment Type** | Conda (`sha`) |
| **Environment Path** | `C:\Users\Rambo\miniconda3\envs\sha` |
| **Site-Packages** | `C:\Users\Rambo\miniconda3\envs\sha\Lib\site-packages` |
| **Camera Backend** | `cv2.CAP_DSHOW` (DirectShow) |
| **Last Incident** | 2026-02-17 — cv2 namespace collision (resolved) |
| **Current Status** | ✅ Operational (Dual Mode) |

### Frozen Dependency Snapshot (Known Good)

```
mediapipe             0.10.9
numpy                 2.4.2
opencv-contrib-python 4.13.0.92
protobuf              3.20.3
fastapi               0.110.0+
uvicorn               0.27.0+
```

> To restore this exact state at any time:
> ```powershell
> pip install opencv-contrib-python==4.13.0.92 mediapipe==0.10.9 numpy==2.4.2 protobuf==3.20.3 fastapi uvicorn jinja2 python-multipart
> ```

---

## Related Documents

| Document | Purpose |
|---|---|
| [`README.md`](README.md) | Project overview and architecture |
| [`execution.md`](execution.md) | Step-by-step execution workflow |
| [`walkthrough.md`](walkthrough.md) | Quick start guide |
