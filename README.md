# 🥷 Shadow Clone Jutsu — Real-Time Computer Vision

> *"Kage Bunshin no Jutsu!"* — A real-time body-cloning effect powered by Python, OpenCV, and MediaPipe.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13.0-green?logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-orange?logo=google)
![Platform](https://img.shields.io/badge/Platform-Windows%2011-0078D6?logo=windows)
![GPU](https://img.shields.io/badge/GPU-RTX%204070-76B900?logo=nvidia)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Controls](#controls)
- [Architecture](#architecture)
- [Project Metadata](#project-metadata)
- [Related Documentation](#related-documentation)

---

## Overview

Shadow Clone Jutsu is a real-time computer vision application that detects a specific hand gesture (the **"Ram" Seal** from Naruto) and renders two translucent body clones to the left and right of the user. It uses **MediaPipe** for hand tracking and selfie segmentation, **NumPy** for high-performance pixel manipulation, and **OpenCV** for rendering — all running at real-time framerates on consumer hardware.

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

| Layer | Technology | Version | Role |
|---|---|---|---|
| **Runtime** | Python | 3.11.14 | Language runtime |
| **Environment** | Conda (`sha`) | — | Isolated dependency management |
| **Vision** | OpenCV (contrib) | 4.13.0.92 | Video capture (`CAP_DSHOW`), rendering, display |
| **AI / ML** | MediaPipe | 0.10.9 | Hand landmark detection, selfie segmentation |
| **Compute** | NumPy | 2.4.2 | Vectorized array operations for clone rendering |
| **Serialization** | Protobuf | 3.20.3 | MediaPipe model deserialization |
| **Hardware** | NVIDIA RTX 4070 | — | GPU-accelerated display pipeline |
| **OS** | Windows 11 | Native | DirectShow camera backend |

> ⚠️ **Critical Dependency Note:** This project uses `opencv-contrib-python` **exclusively**. Installing `opencv-python` alongside it causes a **namespace collision** where `cv2.VideoCapture` becomes undefined. See [`troubleshoot.md`](troubleshoot.md) for details.

---

## Project Structure

```
shadowclone/
│
├── main.py                         # 🎮 Application entry point & main loop
├── requirements.txt                # 📦 Pinned dependencies
├── run_jutsu.bat                   # ⚡ One-click Windows launcher
├── verify_env.py                   # 🔍 Environment sanity checker
├── README.md                       # 📖 This file
├── execution.md                    # 🚀 Execution workflow guide
├── troubleshoot.md                 # 🔧 Debugging & cv2 conflict resolution
│
├── src/
│   ├── __init__.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── jutsu_engine.py         # 🖐️ Hand detection & Ram Seal logic
│   │   └── clone_engine.py         # 👤 Segmentation & clone rendering
│   └── utils/
│       ├── __init__.py
│       └── camera_check.py         # 📷 Windows Hello camera probe
│
├── .gitignore
└── .agent/                         # Agent workflow definitions
```

---

## Quick Start

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

# 5. Run the application
python main.py
```

Or simply double-click **`run_jutsu.bat`**.

---

## Controls

| Key | Action |
|---|---|
| `q` | Gracefully quit — releases camera and destroys all windows |
| `d` | Toggle Debug Mode — shows hand landmarks, connections, and `JUTSU: ACTIVE/INACTIVE` overlay |

### Performing the Jutsu

1. Stand in front of the camera with your upper body visible.
2. Bring your **Index** and **Middle** finger tips together (cross or touch them).
3. Works with **one hand** (crossing fingers) or **two hands** (touching tips across hands).
4. Clones appear while the seal is held; release to dismiss.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         main.py                                 │
│  ┌──────────┐    ┌───────────────┐    ┌──────────────────────┐  │
│  │ Camera   │───▶│ JutsuDetector │───▶│   CloneRenderer      │  │
│  │ Probe    │    │ (Hands 0.10.9)│    │ (SelfieSegmentation) │  │
│  │ (DSHOW)  │    │ complexity=0  │    │ + NumPy Slicing      │  │
│  └──────────┘    └───────────────┘    └──────────────────────┘  │
│       │                │                        │               │
│       ▼                ▼                        ▼               │
│  ┌──────────┐    ┌───────────┐         ┌──────────────┐        │
│  │ BGR Frame│    │ jutsu_    │         │ output_frame │        │
│  │ 640x480  │    │ active    │         │ (composited) │        │
│  └──────────┘    └───────────┘         └──────────────┘        │
│                                              │                  │
│                                              ▼                  │
│                                     cv2.imshow(window)          │
└─────────────────────────────────────────────────────────────────┘
```

**Data Flow:**
1. `camera_check.py` → Probes indices 0–4, returns first 3-channel BGR stream.
2. `jutsu_engine.py` → Processes RGB frame through MediaPipe Hands, checks landmark distances.
3. `clone_engine.py` → If active: segment → threshold → blur mask → slice & shift → tint → blend.
4. `main.py` → Composites FPS counter, optional debug overlay, displays via `cv2.imshow`.

---

## Project Metadata

> *This section acts as the structured "Source of Truth" equivalent to `.idea/project_metadata.xml`.*

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
| **Camera Backend** | DirectShow (`cv2.CAP_DSHOW`) |
| **Verified Camera Index** | 0 (640×480 BGR) |
| **Last Verified** | 2026-02-17T21:48:49+09:00 |
| **Status** | ✅ Operational |

### Frozen Dependency Snapshot

```
mediapipe             0.10.9
numpy                 2.4.2
opencv-contrib-python 4.13.0.92
protobuf              3.20.3
```

---

## Related Documentation

| Document | Purpose |
|---|---|
| [`execution.md`](execution.md) | Step-by-step execution workflow and camera verification |
| [`troubleshoot.md`](troubleshoot.md) | cv2 namespace conflict resolution and "Scorched Earth" recovery |
| [`project.md`](project.md) | Original project specification / PRD |
| [`implementation_plan.md`](implementation_plan.md) | Technical implementation plan |

---

<p align="center"><em>Built with 🍥 chakra and Python on Windows 11</em></p>
