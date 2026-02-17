# Session History — Shadow Clone Jutsu

> **Complete chronological record** of every significant action, decision, error, and resolution
> during the full development session on **2026-02-17**.
>
> Updated: 2026-02-17T22:57:46+09:00

---

## Session Overview

| Key | Value |
|---|---|
| **Session Date** | 2026-02-17 |
| **Session Start** | 21:18:05 JST |
| **Last Update** | 22:57:46 JST |
| **Duration** | ~1 hour 40 minutes |
| **Agent** | Antigravity (Google DeepMind) |
| **User** | Rambo |
| **Workspace** | `C:\Users\Rambo\Documents\source\shadowclone` |
| **Final Status** | ✅ Web Mode operational at `http://localhost:8000` |
| **Project Version** | v1.0 → v2.0 (FastAPI Web) |

---

## Timeline

### Phase 1: Project Initialization (21:18 – 21:20)

| Time (JST) | Action | Outcome |
|---|---|---|
| 21:18:05 | User submits initial objective: Build Shadow Clone Jutsu effect | — |
| 21:18:05 | Agent reads `project.md` (PRD) and `plan.md` (workflow guide) | Context acquired |
| 21:18:05 | Agent creates `task.md` artifact (10 tasks across 3 phases) | ✅ |
| 21:18:05 | Agent creates `implementation_plan.md` artifact | ✅ |
| 21:18:05 | Agent submits plan for user review | Blocked on user |

### Phase 2: User Refinements & Build Start (21:20 – 21:22)

| Time (JST) | Action | Outcome |
|---|---|---|
| 21:20:57 | User provides 3 critical refinements: | — |
| | — Use `model_complexity=0` for hand tracker (CPU saving) | Applied |
| | — Use NumPy slicing instead of `np.roll` (array perf) | Applied |
| | — Apply Gaussian blur to segmentation mask (edge smoothing) | Applied |
| 21:20:57 | User exits Planning Mode → enters Coding Mode | — |
| 21:20:57 | Agent creates `requirements.txt` v1 (opencv-python, mediapipe, numpy) | ✅ |
| 21:20:57 | Agent creates `src/utils/camera_check.py` | ✅ |
| 21:20:57 | Agent creates `src/app/jutsu_engine.py` | ✅ |
| 21:20:57 | Agent creates `src/app/clone_engine.py` | ✅ |
| 21:20:57 | Agent creates `main.py` (v1) | ✅ |
| 21:20:57 | Agent attempts `python -m venv venv` + `pip install` | ❌ User rejected |

### Phase 3: Environment Setup — Conda (21:22 – 21:35)

| Time (JST) | Action | Outcome |
|---|---|---|
| 21:22:55 | User manually creates conda env: `conda create -n sha python=3.11` | ✅ |
| 21:22:55 | User activates: `conda activate sha` | ✅ |
| 21:22:55 | User instructs: "use the conda env instead of venv" | Directive accepted |
| 21:22:55 | Agent starts `pip install -r requirements.txt` in `sha` env | ⏳ Slow download |
| 21:25:50 | User creates `.gitignore` | ✅ |
| 21:25:50 | Agent creates `__init__.py` files for all packages | ✅ |
| 21:27:52 | pip install still running (mediapipe downloading ~50MB) | ⏳ |
| ~21:35:00 | pip install completes in `sha` env | ✅ |

### Phase 4: First Run Attempts & Failures (21:35 – 21:45)

| Time (JST) | Action | Outcome |
|---|---|---|
| 21:35 | Agent runs `python src/utils/camera_check.py` | ✅ Camera Index 0 found (640×480) |
| 21:35 | Agent runs `python main.py` | ❌ `mp.solutions.hands` → AttributeError |
| 21:35 | **Root Cause:** MediaPipe 0.10.32 loaded from base conda env, not `sha` | Diagnosed |
| 21:38 | Agent pins `mediapipe==0.10.9`, installs via explicit `sha` python path | ✅ |
| 21:38 | Agent runs `verify_env.py` | ❌ `cv2.__version__` AttributeError |
| 21:38 | **Root Cause:** Both `opencv-python` AND `opencv-contrib-python` installed | ❌ **NAMESPACE COLLISION** |

### Phase 5: cv2 Namespace Collision — Resolution (21:42 – 21:48)

| Time (JST) | Action | Outcome |
|---|---|---|
| 21:42 | Agent uninstalls `opencv-python`, keeps `opencv-contrib-python` | ✅ |
| 21:45 | `cv2.VideoCapture` still missing → hollow namespace | ❌ Residual corruption |
| 21:47 | Agent uninstalls ALL opencv packages | ✅ Purged |
| 21:47 | Agent reinstalls `opencv-contrib-python` only | ✅ |
| 21:48 | `verify_env.py` passes: cv2=4.13.0, mp=0.10.9, mp.solutions=Found | ✅ |
| 21:48 | `main.py` launches successfully | ✅ |
| 21:48 | Console: `INFO: Created TensorFlow Lite XNNPACK delegate for CPU.` | ✅ Expected |
| 21:48 | App terminated via agent signal after verification | ✅ |

### Phase 6: Documentation Generation (21:50 – 21:55)

| Time (JST) | Action | Outcome |
|---|---|---|
| 21:50 | Agent provides project status summary | ✅ |
| 21:50 | Agent creates `run_jutsu.bat` | ✅ |
| 21:55 | User requests 3 documentation files | — |
| 21:55 | Agent audits all source files, captures pip list | ✅ |
| 21:55 | Agent generates `README.md` (9,029 bytes) | ✅ |
| 21:55 | Agent generates `execution.md` (6,874 bytes) | ✅ |
| 21:55 | Agent generates `troubleshoot.md` (11,071 bytes) | ✅ |

### Phase 7: CRAFT Protocol Execution (22:03 – 22:09)

| Time (JST) | Action | Outcome |
|---|---|---|
| 22:03 | User creates `codex.md` with CRAFT master prompt | — |
| 22:03 | User instructs: "execute the proof check prompt craft" | — |
| 22:04 | **Phase 1:** Detect interpreter → `sha` env, Python 3.11.14 | ✅ |
| 22:04 | **Phase 1:** Full OpenCV purge (uninstall all variants) | ✅ |
| 22:04 | **Phase 1:** Purge residual `site-packages/cv2/` directory | ✅ |
| 22:04 | **Phase 1:** Verify `import cv2` FAILS (clean slate) | ✅ |
| 22:05 | **Phase 2:** Install `mediapipe==0.10.9` (pulls opencv-contrib) | ✅ |
| 22:05 | **Phase 2:** Verify: `VideoCapture Exists: True`, `Camera Opened: True` | ✅ |
| 22:06 | **Phase 3:** Project structure verified | ✅ |
| 22:06 | **Phase 4:** `requirements.txt` pinned with safety headers | ✅ |
| 22:06 | **Phase 5:** All 3 documentation files confirmed | ✅ |
| 22:07 | **Phase 6:** `main.py` hardened with `--cli` flag, startup diagnostics | ✅ |
| 22:08 | **Phase 7:** `python main.py --cli` → ALL CHECKS PASSED | ✅ |
| 22:08 | CRAFT COMPLETE: Zero conflicts, zero drift | ✅ |

### Phase 8: .idea/ Metadata Generation (22:09 – 22:19)

| Time (JST) | Action | Outcome |
|---|---|---|
| 22:09 | User requests `.idea/` directory with full session data | — |
| 22:09 | Agent audits final state (pip list, directory tree) | ✅ |
| 22:10 | Agent generates `.idea/project_metadata.md` (4,855 bytes) | ✅ |
| 22:10 | Agent generates `.idea/session_history.md` (7,337 bytes) | ✅ |
| 22:10 | Agent generates `.idea/decisions.md` (8,530 bytes) | ✅ |
| 22:10 | Agent generates `.idea/errors.md` (7,743 bytes) | ✅ |
| 22:19 | User reviews `.idea/` files, notes `.gitignore` excludes `.idea/` | Acknowledged |

### Phase 9: Web Transition — FastAPI + Floating UI (22:49 – 22:57)

| Time (JST) | Action | Outcome |
|---|---|---|
| 22:49 | User submits comprehensive web transition directive | — |
| | — Transition to FastAPI MJPEG streaming | — |
| | — Glassmorphism "Floating UI" design | — |
| | — Updated clone engine specs (±350px, B:255/G:100/R:100 tint) | — |
| | — GestureEngine threshold raised to 0.05 | — |
| | — Layered alpha compositing (Background → Clones → User) | — |
| 22:50 | Agent installs FastAPI + uvicorn + jinja2 + python-multipart | ✅ |
| 22:50 | Agent creates `src/engines/` directory (gesture_engine, clone_engine v2) | ✅ |
| 22:50 | Agent creates `src/engines/gesture_engine.py` — threshold=0.05, complexity=0 | ✅ |
| 22:50 | Agent creates `src/engines/clone_engine.py` — layered alpha blend, no blowout | ✅ |
| 22:51 | Agent creates `src/web_server.py` — FastAPI with MJPEG, /status, /toggle_debug | ✅ |
| 22:51 | Agent creates `templates/index.html` — Floating UI with glassmorphism panel | ✅ |
| 22:51 | Agent creates `static/css/style.css` — Dark mode, animated glows, responsive | ✅ |
| 22:51 | Agent creates `static/js/app.js` — Status polling (250ms), keyboard shortcuts | ✅ |
| 22:52 | Agent creates `run_web.py` — Uvicorn launcher with --port flag | ✅ |
| 22:52 | Agent updates `requirements.txt` with web dependencies | ✅ |
| 22:53 | Agent launches `python run_web.py --port 8000` | ✅ |
| 22:53 | Server: `Uvicorn running on http://0.0.0.0:8000` | ✅ |
| 22:53 | Camera: `Index 0, 640x480, DSHOW` | ✅ |
| 22:53 | TFLite: `XNNPACK delegate for CPU` | ✅ |
| 22:54 | Agent verifies `/status` API: `jutsu_active: false, fps: 23.6, running: true` | ✅ |
| 22:54 | Agent verifies `GET /` returns HTML with "影分身の術" | ✅ |
| 22:54 | FPS logs: 19–45 FPS range (idle) across 3900+ frames | ✅ |
| 22:54 | Browser agent fails (Playwright not installed) — verified via HTTP instead | ⚠️ |

### Phase 10: .idea/ Metadata Refresh (22:57)

| Time (JST) | Action | Outcome |
|---|---|---|
| 22:57 | User requests full `.idea/` refresh with web transition included | — |
| 22:57 | Agent audits: 6 directories, 15 root files, 45 pip packages | ✅ |
| 22:57 | Agent regenerates all 4 `.idea/` files with complete v2.0 data | ✅ |

---

## Key Statistics

| Metric | Value |
|---|---|
| Total files created | 28 |
| Total errors encountered | 6 |
| Total errors resolved | 6 |
| Unresolved errors | 0 |
| pip install executions | 6 |
| main.py versions | 2 (v1 basic → v2 hardened with --cli) |
| clone_engine versions | 2 (v1 additive → v2 layered alpha) |
| Documentation files | 8 (README, execution, troubleshoot, walkthrough, project, plan, implementation_plan, codex) |
| .idea/ metadata files | 4 (project_metadata, session_history, decisions, errors) |
| Project modes | 3 (Web, Local GUI, CLI diagnostics) |
| API endpoints | 4 (/, /video_feed, /status, /toggle_debug) |
| CRAFT phases executed | 7/7 |
| CRAFT phases passed | 7/7 |
| Architecture transitions | 1 (Local OpenCV → FastAPI Web) |
| Session phases | 10 |
