# 🥷 Shadow Clone Jutsu — Real-Time Computer Vision

> *"Kage Bunshin no Jutsu!"* — A real-time body-cloning effect powered by Python, OpenCV, and MediaPipe. Now available in both **Terminal GUI** and **Web Browser** modes.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13.0-green?logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-orange?logo=google)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?logo=fastapi)
![Platform](https://img.shields.io/badge/Platform-Windows%2011-0078D6?logo=windows)
![GPU](https://img.shields.io/badge/GPU-RTX%204070-76B900?logo=nvidia)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Execution Modes](#execution-modes)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Controls](#controls)
- [Architecture](#architecture)
- [Project Metadata](#project-metadata)
- [Related Documentation](#related-documentation)

---

## Overview

Shadow Clone Jutsu is a **dual-mode** real-time computer vision application that detects a specific hand gesture (the **"Ram" Seal** from Naruto) and renders two translucent body clones to the left and right of the user. It uses **MediaPipe** for hand tracking and selfie segmentation, **NumPy** for high-performance pixel manipulation, and **OpenCV** for rendering — all running at real-time framerates on consumer hardware.

## Execution Modes

### 🖥️ Terminal GUI Mode (`main.py`)
Traditional OpenCV window with local rendering. Ideal for testing, debugging, and offline use.

### 🌐 Web Application Mode (`run_web.py`)
Modern browser-based interface with:
- **FastAPI backend** for MJPEG streaming
- **Glassmorphism UI** with floating panels and animated backgrounds
- **Real-time status indicators** (FPS, jutsu activation, camera info)
- **Responsive design** for desktop and mobile viewing
- **Debug mode toggle** and fullscreen support

### Key Features

| Feature | Implementation |
|---|---|
| **Windows Hello Camera Support** | Auto-probes indices 0–4, skips IR (single-channel) streams |
| **Ram Seal Detection** | Index Tip (ID 8) ↔ Middle Tip (ID 12) proximity check |
| **Shadow Clones** | NumPy slicing-based horizontal shift (±300px) with additive blending |
| **Edge Smoothing** | 5×5 Gaussian blur on segmentation mask to prevent fraying |
| **Chakra Tint** | Blue channel boost (×1.5) on clone layers for visual distinction |
| **Debug Mode** | Press `d` to overlay hand landmarks and activation status |
| **Performance** | `model_complexity=0` for hand tracker; vectorized NumPy ops only |

---

## Tech Stack

### Core Computer Vision Stack
| Layer | Technology | Version | Role |
|---|---|---|---|
| **Runtime** | Python | 3.11.14 | Language runtime |
| **Environment** | Conda (`sha`) | — | Isolated dependency management |
| **Vision** | OpenCV (contrib) | 4.13.0.92 | Video capture (`CAP_DSHOW`), rendering, display |
| **AI / ML** | MediaPipe | 0.10.9 | Hand landmark detection, selfie segmentation |
| **Compute** | NumPy | 2.4.2 | Vectorized array operations for clone rendering |
| **Serialization** | Protobuf | 3.20.3 | MediaPipe model deserialization |

### Web Application Stack (New)
| Layer | Technology | Version | Role |
|---|---|---|---|
| **Backend** | FastAPI | Latest | Async web framework for MJPEG streaming |
| **ASGI Server** | Uvicorn | Latest | Production-grade async server |
| **Templating** | Jinja2 | Latest | HTML template rendering |
| **Frontend** | HTML5 + Vanilla CSS + JS | — | Glassmorphism UI with real-time updates |
| **Fonts** | Google Fonts (Outfit, JetBrains Mono) | — | Premium typography |

### Hardware & OS
| Layer | Technology | Version | Role |
|---|---|---|---|
| **Hardware** | NVIDIA RTX 4070 | — | GPU-accelerated rendering pipeline |
| **OS** | Windows 11 | Native | DirectShow camera backend |

> ⚠️ **Critical Dependency Note:** This project uses `opencv-contrib-python` **exclusively**. Installing `opencv-python` alongside it causes a **namespace collision** where `cv2.VideoCapture` becomes undefined. See [`troubleshoot.md`](troubleshoot.md) for details.

---

## Project Structure

```
shadowclone/
│
├── main.py                         # 🎮 Terminal GUI entry point (OpenCV window)
├── run_web.py                      # 🌐 Web application launcher (FastAPI)
├── requirements.txt                # 📦 Pinned dependencies (CV + Web stack)
├── run_jutsu.bat                   # ⚡ One-click Windows launcher (terminal mode)
├── verify_env.py                   # 🔍 Environment sanity checker
├── README.md                       # 📖 This file
├── execution.md                    # 🚀 Execution workflow guide
├── troubleshoot.md                 # 🔧 Debugging & cv2 conflict resolution
├── plan.md                         # 📝 Original project planning docs
├── project.md                      # 📋 Project specification / PRD
├── implementation_plan.md          # 🏗️ Technical implementation plan
├── codex.md                        # 📚 CRAFT master prompt for stabilization
├── walkthrough.md                  # 🚶 Step-by-step usage guide
│
├── src/
│   ├── __init__.py
│   ├── web_server.py               # 🌐 FastAPI app with lifespan & MJPEG streaming
│   ├── engines/                    # 🔧 Core CV processing engines
│   │   ├── __init__.py
│   │   ├── gesture_engine.py       # 🖐️ Hand detection & Ram Seal logic
│   │   └── clone_engine.py         # 👤 Segmentation & clone rendering
│   ├── app/                        # 📁 Legacy engine directory (deprecated)
│   │   ├── __init__.py
│   │   ├── jutsu_engine.py         # 🖐️ [OLD] Use engines/gesture_engine.py
│   │   └── clone_engine.py         # 👤 [OLD] Use engines/clone_engine.py
│   └── utils/
│       ├── __init__.py
│       └── camera_check.py         # 📷 Windows Hello camera probe
│
├── templates/                      # 🎨 Web UI templates
│   └── index.html                  # Main glassmorphism interface
│
├── static/                         # 🎨 Static web assets
│   ├── css/
│   │   └── style.css               # Glassmorphism design system
│   └── js/
│       └── app.js                  # Client-side status polling & interactions
│
├── .gitignore
└── .agent/                         # Agent workflow definitions
```

---

## Quick Start

### Installation (One-Time Setup)
```powershell
# 1. Clone or navigate to the project
cd C:\Users\Rambo\Documents\source\shadowclone

# 2. Activate the Conda environment
conda activate sha

# 3. Install dependencies (first time only)
pip install -r requirements.txt

# 4. Verify the environment (optional but recommended)
python verify_env.py
# Expected: CV2 Version: 4.13.0 | MediaPipe Version: 0.10.9 | MP Solutions: Found
```

### 🖥️ Terminal GUI Mode (Traditional)

```powershell
# Run the OpenCV window application
python main.py

# Or use the batch launcher
.\run_jutsu.bat

# CLI diagnostics mode (no GUI)
python main.py --cli
```

**Controls:**
- `q` — Quit
- `d` — Toggle Debug Mode (shows hand landmarks)

### 🌐 Web Application Mode (Modern)

```powershell
# Start the web server
python run_web.py

# Custom port
python run_web.py --port 9000

# Development mode (auto-reload)
python run_web.py --reload
```

Then open your browser to:
- **http://localhost:8000** (default)
- **http://localhost:9000** (custom port)

**Features:**
- 🎨 Glassmorphism UI with animated backgrounds
- 📊 Real-time FPS and jutsu status indicators
- 🔍 Debug mode toggle (shows MediaPipe landmarks on video)
- ⛶ Fullscreen mode
- 📱 Responsive design (works on mobile!)

---

## Controls

### 🖥️ Terminal GUI Mode
| Key | Action |
|---|---|
| `q` | Gracefully quit — releases camera and destroys all windows |
| `d` | Toggle Debug Mode — shows hand landmarks, connections, and `JUTSU: ACTIVE/INACTIVE` overlay |

### 🌐 Web Application Mode
**On-Screen Controls:**
- **🔍 Debug Mode** — Toggle MediaPipe landmark overlay on video stream
- **⛶ Fullscreen** — Expand video feed to fullscreen

**API Endpoints:**
- `GET /` — Main glassmorphism interface
- `GET /video_feed` — MJPEG streaming endpoint
- `GET /status` — JSON status (FPS, jutsu state, camera info)
- `POST /toggle_debug` — Toggle debug overlay programmatically

### Performing the Jutsu

1. Stand in front of the camera with your upper body visible.
2. Bring your **Index** and **Middle** finger tips together (cross or touch them).
3. Works with **one hand** (crossing fingers) or **two hands** (touching tips across hands).
4. Clones appear while the seal is held; release to dismiss.

---

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│            SHADOW CLONE JUTSU — DUAL-MODE ARCHITECTURE              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📷 CAMERA LAYER                                                │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  camera_check.py → Probe indices 0-4 (DSHOW backend)  │  │
│  │  Returns first 3-channel BGR stream (640x480)            │  │
│  └───────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              │                                  │
│  🤖 PROCESSING ENGINES                   │                   │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  GestureEngine (gesture_engine.py)                   │  │
│  │  └─ MediaPipe Hands (model_complexity=0)            │  │
│  │  └─ Ram Seal: Index(8) ↔ Middle(12) proximity    │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │  CloneEngine (clone_engine.py)                       │  │
│  │  └─ Selfie Segmentation (MediaPipe)                │  │
│  │  └─ NumPy array slicing (±350px horizontal shift) │  │
│  │  └─ Gaussian blur (5x5) on mask edges              │  │
│  │  └─ Chakra tint (blue channel boost)               │  │
│  └─────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              │                                  │
│  📺 OUTPUT MODES                        │                   │
│                              ├──────────────────────────────────┐
│                              │                                  │
│  ┌──────────────────────────────┐  │                                  │
│  │   🖥️ TERMINAL GUI MODE    │  │  🌐 WEB APPLICATION MODE       │
│  │   (main.py)             │  │  (run_web.py → web_server.py) │
│  ├──────────────────────────────┤  ├──────────────────────────────────┤
│  │ ✔ Direct cv2.imshow()  │  │ ✔ FastAPI + Uvicorn           │
│  │ ✔ Local rendering      │  │ ✔ MJPEG Streaming (60fps)     │
│  │ ✔ Keyboard controls    │  │ ✔ Jinja2 Templates            │
│  │ ✔ CLI diagnostics mode │  │ ✔ Glassmorphism UI            │
│  └──────────────────────────────┘  │ ✔ RESTful status endpoints     │
│                              │ ✔ Responsive design            │
│                              └──────────────────────────────────┘
└─────────────────────────────────────────────────────────────────┘
```

**Shared Data Flow (Both Modes):**
1. **Camera Probe** → `camera_check.py` finds first 3-channel BGR stream (DirectShow backend)
2. **Gesture Detection** → `GestureEngine` processes RGB frame through MediaPipe Hands
3. **Clone Rendering** → If gesture active: `CloneEngine` segments → threshold → blur mask → slice & shift → tint → blend
4. **Output Compositing** → FPS counter, optional debug overlay, final frame delivery

**Mode-Specific Delivery:**
- **Terminal**: `cv2.imshow()` → OpenCV window with keyboard controls
- **Web**: JPEG encode → MJPEG stream → FastAPI endpoint → HTML `<img>` tag + JavaScript status polling

---

## Project Metadata

> *This section acts as the structured "Source of Truth" equivalent to `.idea/project_metadata.xml`.*

### Core Configuration
| Key | Value |
|---|---|
| **Project Name** | Shadow Clone Jutsu |
| **Project Root** | `C:\Users\Rambo\Documents\source\shadowclone` |
| **Python Interpreter** | `C:\Users\Rambo\miniconda3\envs\sha\python.exe` |
| **Python Version** | 3.11.14 |
| **Environment Type** | Conda (`sha`) |
| **SDK** | Python 3.11 (Miniconda3) |
| **Source Roots** | `src/` |
| **Content Roots** | Project root |
| **VCS** | Git (`.gitignore` present) |

### Hardware & Camera
| Key | Value |
|---|---|
| **Camera Backend** | DirectShow (`cv2.CAP_DSHOW`) |
| **Verified Camera Index** | 0 (640×480 BGR) |
| **GPU** | NVIDIA RTX 4070 |
| **OS** | Windows 11 |

### Execution Modes
| Mode | Entry Point | Port/Display | UI Type |
|---|---|---|---|
| **Terminal GUI** | `main.py` | OpenCV Window | Native OS window with keyboard controls |
| **Web Application** | `run_web.py` | http://localhost:8000 | Browser-based glassmorphism interface |

### Status
| Key | Value |
|---|---|
| **Last Verified** | 2026-02-17T23:12:40+09:00 |
| **Architecture Status** | ✅ Dual-mode (Terminal + Web) operational |
| **Web Stack Status** | ✅ FastAPI + MJPEG streaming functional |

### Frozen Dependency Snapshot

**Core CV Stack:**
```
mediapipe             0.10.9
numpy                 2.4.2
opencv-contrib-python 4.13.0.92
protobuf              3.20.3
```

**Web Stack:**
```
fastapi               (latest)
uvicorn[standard]     (latest)
jinja2                (latest)
python-multipart      (latest)
```

---

## Related Documentation

| Document | Purpose |
|---|---|
| [`execution.md`](execution.md) | Step-by-step execution workflow and camera verification |
| [`troubleshoot.md`](troubleshoot.md) | cv2 namespace conflict resolution and "Scorched Earth" recovery |
| [`walkthrough.md`](walkthrough.md) | Quick walkthrough for installation and usage |
| [`project.md`](project.md) | Original project specification / PRD |
| [`implementation_plan.md`](implementation_plan.md) | Technical implementation plan |
| [`plan.md`](plan.md) | Antigravity agent workflow planning guide |
| [`codex.md`](codex.md) | CRAFT master prompt for environment stabilization |

---

<p align="center"><em>Built with 🍥 chakra and Python on Windows 11 | Now streaming in your browser!</em></p>
