# Project Metadata — Shadow Clone Jutsu

> **Source of Truth.** This file captures the complete project state.
> Updated: 2026-02-17T22:57:46+09:00

---

## Project Identity

| Key | Value |
|---|---|
| **Project Name** | Shadow Clone Jutsu |
| **Codename** | `shadowclone` |
| **Project Root** | `C:\Users\Rambo\Documents\source\shadowclone` |
| **Repository Type** | Git (local, `.git/` initialized) |
| **Created** | 2026-02-17T21:18:05+09:00 |
| **Last Modified** | 2026-02-17T22:57:46+09:00 |
| **Status** | ✅ Operational (Web + Local modes) |
| **Current Version** | 2.0.0 (FastAPI Web Mode) |

---

## Runtime Configuration

| Key | Value |
|---|---|
| **Python Version** | 3.11.14 |
| **Python Interpreter** | `C:\Users\Rambo\miniconda3\envs\sha\python.exe` |
| **Environment Type** | Conda |
| **Environment Name** | `sha` |
| **Environment Path** | `C:\Users\Rambo\miniconda3\envs\sha` |
| **Site-Packages** | `C:\Users\Rambo\miniconda3\envs\sha\Lib\site-packages` |

### Entry Points

| Mode | Command | Description |
|---|---|---|
| **Web Mode** (primary) | `python run_web.py` | FastAPI + Uvicorn → `http://localhost:8000` |
| **Local OpenCV Mode** | `python main.py` | Standalone cv2.imshow window |
| **CLI Diagnostics** | `python main.py --cli` | Headless environment check |
| **Batch Launcher** | `run_jutsu.bat` | One-click local mode launcher |

---

## Hardware Profile

| Key | Value |
|---|---|
| **OS** | Windows 11 (Native — no WSL) |
| **GPU** | NVIDIA RTX 4070 (8GB) |
| **Camera** | Laptop Webcam (Windows Hello IR + RGB) |
| **Camera Backend** | DirectShow (`cv2.CAP_DSHOW`) |
| **Verified Camera Index** | 0 |
| **Verified Resolution** | 640×480 |
| **Camera Channels** | 3 (BGR) |
| **TFLite Delegate** | XNNPACK (CPU) |
| **Observed FPS Range** | 19–45 FPS (idle), varies under jutsu |

---

## Dependency Manifest (Frozen — 45 packages)

### Core CV Stack

| Package | Version | Role |
|---|---|---|
| `mediapipe` | 0.10.9 | Hand tracking, selfie segmentation |
| `opencv-contrib-python` | 4.13.0.92 | Video capture, rendering, MJPEG encode |
| `numpy` | 2.4.2 | Vectorized array operations |
| `protobuf` | 3.20.3 | MediaPipe model deserialization |

### Web Stack

| Package | Version | Role |
|---|---|---|
| `fastapi` | 0.129.0 | HTTP framework, routing |
| `uvicorn` | 0.41.0 | ASGI server |
| `jinja2` | 3.1.6 | HTML template rendering |
| `python-multipart` | 0.0.22 | Form data parsing |
| `starlette` | 0.52.1 | FastAPI underlying framework |
| `pydantic` | 2.12.5 | Data validation |
| `pydantic_core` | 2.41.5 | Pydantic C-core |

### Web Stack Transitive

| Package | Version |
|---|---|
| `annotated-doc` | 0.0.4 |
| `annotated-types` | 0.7.0 |
| `anyio` | 4.12.1 |
| `click` | 8.3.1 |
| `colorama` | 0.4.6 |
| `h11` | 0.16.0 |
| `httptools` | 0.7.1 |
| `idna` | 3.11 |
| `MarkupSafe` | 3.0.3 |
| `python-dotenv` | 1.2.1 |
| `PyYAML` | 6.0.3 |
| `typing_extensions` | 4.15.0 |
| `typing-inspection` | 0.4.2 |
| `watchfiles` | 1.1.1 |
| `websockets` | 16.0 |

### MediaPipe Transitive

| Package | Version |
|---|---|
| `absl-py` | 2.4.0 |
| `attrs` | 25.4.0 |
| `cffi` | 2.0.0 |
| `contourpy` | 1.3.3 |
| `cycler` | 0.12.1 |
| `flatbuffers` | 25.12.19 |
| `fonttools` | 4.61.1 |
| `kiwisolver` | 1.4.9 |
| `matplotlib` | 3.10.8 |
| `packaging` | 25.0 |
| `pillow` | 12.1.1 |
| `pycparser` | 3.0 |
| `pyparsing` | 3.3.2 |
| `python-dateutil` | 2.9.0.post0 |
| `six` | 1.17.0 |
| `sounddevice` | 0.5.5 |

### Build Tools

| Package | Version |
|---|---|
| `pip` | 26.0.1 |
| `setuptools` | 80.10.2 |
| `wheel` | 0.46.3 |

> ⚠️ **NEVER install `opencv-python` or `opencv-python-headless` into this environment.**

---

## Source Roots & Module Map

### Engine Layer (`src/engines/`)

| Module | Description |
|---|---|
| `gesture_engine.py` | Ram Seal detection — landmarks 8↔12, `model_complexity=0`, threshold=0.05 |
| `clone_engine.py` | Layered alpha compositing — ±350px offset, B:255/G:100/R:100 tint, 3×3 Gaussian blur |

### Web Layer (`src/`)

| Module | Description |
|---|---|
| `web_server.py` | FastAPI app with `/video_feed` MJPEG, `/status` JSON, `/toggle_debug` POST |

### Legacy Local Layer (`src/app/`)

| Module | Description |
|---|---|
| `jutsu_engine.py` | Original hand detector (v1, threshold=0.04) |
| `clone_engine.py` | Original clone renderer (v1, np.roll-based, additive blending) |

### Utilities (`src/utils/`)

| Module | Description |
|---|---|
| `camera_check.py` | Windows Hello probe (indices 0–4, skips IR) |

### Frontend (`templates/` + `static/`)

| File | Description |
|---|---|
| `templates/index.html` | Glassmorphism Floating UI with video, status indicator, controls |
| `static/css/style.css` | Dark mode theme, animated glows, responsive layout |
| `static/js/app.js` | Status polling (250ms), keyboard shortcuts (D/F) |

---

## Complete File Inventory

| File | Size | Type |
|---|---|---|
| `main.py` | 7,779 B | Python — Local mode entry point (GUI + CLI) |
| `run_web.py` | 1,085 B | Python — FastAPI web launcher |
| `src/__init__.py` | 0 B | Package marker |
| `src/web_server.py` | 6,592 B | Python — FastAPI MJPEG streaming server |
| `src/engines/__init__.py` | 0 B | Package marker |
| `src/engines/gesture_engine.py` | 3,197 B | Python — Ram Seal detection |
| `src/engines/clone_engine.py` | 4,858 B | Python — Shadow clone compositing |
| `src/app/__init__.py` | 0 B | Package marker |
| `src/app/jutsu_engine.py` | 2,679 B | Python — Legacy hand detector |
| `src/app/clone_engine.py` | 4,861 B | Python — Legacy clone renderer |
| `src/utils/__init__.py` | 0 B | Package marker |
| `src/utils/camera_check.py` | 2,047 B | Python — Camera probe |
| `templates/index.html` | 4,833 B | HTML — Floating UI |
| `static/css/style.css` | — | CSS — Glassmorphism theme |
| `static/js/app.js` | — | JS — Client controller |
| `verify_env.py` | 621 B | Python — Environment sanity check |
| `requirements.txt` | 336 B | Text — Pinned dependencies |
| `run_jutsu.bat` | 59 B | Batch — One-click launcher |
| `.gitignore` | 142 B | Git ignore rules |
| `README.md` | 9,029 B | Markdown — Project overview |
| `execution.md` | 6,874 B | Markdown — Execution workflow |
| `troubleshoot.md` | 11,071 B | Markdown — cv2 conflict guide |
| `codex.md` | 5,438 B | Markdown — CRAFT master prompt |
| `project.md` | 3,101 B | Markdown — Original PRD |
| `plan.md` | 4,329 B | Markdown — Workflow plan |
| `implementation_plan.md` | 3,065 B | Markdown — Technical plan |
| `walkthrough.md` | 1,708 B | Markdown — User walkthrough |
| `save.txt` | 38,835 B | Text — Raw terminal/session log |

---

## API Endpoints (Web Mode)

| Method | Path | Content-Type | Description |
|---|---|---|---|
| `GET` | `/` | `text/html` | Floating UI page |
| `GET` | `/video_feed` | `multipart/x-mixed-replace` | MJPEG stream |
| `GET` | `/status` | `application/json` | Current state JSON |
| `POST` | `/toggle_debug` | `application/json` | Toggle debug overlay |

---

## Project Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            run_web.py                                   │
│                        (uvicorn launcher)                               │
│                               │                                         │
│                     ┌─────────▼──────────┐                              │
│                     │   web_server.py     │                              │
│                     │   (FastAPI App)     │                              │
│                     │                    │                              │
│                     │  Routes:           │                              │
│                     │  GET /             │──▶ templates/index.html      │
│                     │  GET /video_feed   │──▶ MJPEG StreamingResponse   │
│                     │  GET /status       │──▶ JSON state                │
│                     │  POST /toggle_debug│                              │
│                     └────────┬───────────┘                              │
│                              │                                          │
│                    ┌─────────▼──────────┐                               │
│                    │  camera_loop()     │ (background thread)            │
│                    │                    │                                │
│    ┌───────────┐   │  ┌──────────────┐  │   ┌─────────────────────┐     │
│    │ Camera    │──▶│  │GestureEngine │──│──▶│   CloneEngine       │     │
│    │ Probe     │   │  │(Hands 0.10.9)│  │   │ (SelfieSegmentation)│     │
│    │ (DSHOW)   │   │  │complexity=0  │  │   │ + NumPy Slicing     │     │
│    └───────────┘   │  └──────────────┘  │   └─────────────────────┘     │
│                    │         │           │            │                  │
│                    │  jutsu_active       │     output_frame              │
│                    │         │           │            │                  │
│                    │         ▼           │            ▼                  │
│                    │   cv2.imencode()  ──│──▶  _latest_frame (JPEG)      │
│                    └────────────────────┘                                │
│                                                                         │
│    Browser (localhost:8000)                                              │
│    ┌────────────────────────────────────────────────────┐                │
│    │  ┌──────────────────────┐  ┌───────────────────┐  │                │
│    │  │   <img /video_feed>  │  │  Control Panel    │  │                │
│    │  │   90% viewport       │  │  (Glassmorphism)  │  │                │
│    │  │                      │  │  Status / Debug   │  │                │
│    │  │  [JUTSU INDICATOR]   │  │  Instructions     │  │                │
│    │  │  [FPS BADGE]         │  │                   │  │                │
│    │  └──────────────────────┘  └───────────────────┘  │                │
│    └────────────────────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────────────────────┘
```
