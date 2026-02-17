# Next Steps — Shadow Clone Jutsu

> **Backlog of planned enhancements, optimizations, and hardening tasks.**
> Prioritized by impact. Generated from session context.
> Updated: 2026-02-17T22:57:46+09:00

---

## Priority Legend

| Tag | Meaning |
|---|---|
| 🔴 P0 | Critical — blocks usage or demo readiness |
| 🟡 P1 | High — significant UX or performance improvement |
| 🟢 P2 | Medium — polish and refinement |
| ⚪ P3 | Low — nice-to-have / future exploration |

---

## Backlog

### 🔴 P0 — Critical

| # | Task | Rationale | Files Affected |
|---|---|---|---|
| NS-001 | **Smoke/Poof transition effect** when clones first appear | Clones appear instantly — feels abrupt. A 3-frame smoke overlay would sell the "jutsu" illusion. | `src/engines/clone_engine.py`, `static/assets/smoke.png` |
| NS-002 | **Resolution upgrade** from 640×480 to 1280×720 | Default camera resolution is low. RTX 4070 has headroom. Uncomment `cap.set()` lines. | `src/web_server.py` |

### 🟡 P1 — High Impact

| # | Task | Rationale | Files Affected |
|---|---|---|---|
| NS-003 | **WebSocket for status** instead of HTTP polling | Reduce latency from 250ms to real-time. Uvicorn already supports WebSockets. | `src/web_server.py`, `static/js/app.js` |
| NS-004 | **Jutsu toggle mode** (one seal → clones stay; second seal → clones vanish) | HOLD mode requires sustained gesture. Toggle would free user's hands. Add a settings toggle in the UI. | `src/engines/gesture_engine.py`, `templates/index.html` |
| NS-005 | **Clone offset slider** in the UI panel | Let users adjust clone spacing (currently hardcoded ±350px) without restarting. | `src/web_server.py`, `static/js/app.js`, `templates/index.html` |
| NS-006 | **Frame skipping** for segmentation | Run segmentation every 2nd frame; re-use mask on alternate frames. Would ~double FPS. | `src/engines/clone_engine.py` |
| NS-007 | **GPU acceleration** with `cv2.UMat` | OpenCV's Transparent API could offload JPEG encoding and Gaussian blur to the RTX 4070. | `src/web_server.py`, `src/engines/clone_engine.py` |

### 🟢 P2 — Polish

| # | Task | Rationale | Files Affected |
|---|---|---|---|
| NS-008 | **Clone fade-in animation** (alpha ramp from 0→0.7 over 10 frames) | Instant 70% opacity is jarring. A smooth ramp would look cinematic. | `src/engines/clone_engine.py` |
| NS-009 | **Sound effects** (play a "jutsu activation" audio clip in browser) | Audio feedback enhances immersion. Use `<audio>` element triggered by JS status poll. | `templates/index.html`, `static/js/app.js`, `static/audio/` |
| NS-010 | **Multiple jutsu gestures** (different seals → different effects) | Expand beyond Ram Seal. E.g., "Tiger" seal → zoom effect, "Snake" seal → blur effect. | `src/engines/gesture_engine.py` |
| NS-011 | **Mobile-responsive UI** refinement | Current CSS handles mobile but hasn't been tested on actual phones. | `static/css/style.css` |
| NS-012 | **Dark/Light theme toggle** in the panel | Some users may prefer light mode for bright environments. | `static/css/style.css`, `static/js/app.js` |
| NS-013 | **Recording mode** — save output frames to video file | Let users record their jutsu session as an MP4. Add /start_record and /stop_record endpoints. | `src/web_server.py` |
| NS-014 | **Multi-user support** — separate video streams per browser session | Currently single-camera, single-stream. Would need session-based camera isolation. | `src/web_server.py` |

### ⚪ P3 — Future Exploration

| # | Task | Rationale | Files Affected |
|---|---|---|---|
| NS-015 | **Docker container** for portable deployment | `Dockerfile` with Python 3.11, headless OpenCV, exposed port 8000. | `Dockerfile`, `docker-compose.yml` |
| NS-016 | **GitHub Actions CI** for automated testing | Lint + `main.py --cli` health check on every push. | `.github/workflows/ci.yml` |
| NS-017 | **3D clone positioning** using depth estimation | Use MediaPipe Face Mesh depth for Z-axis clone offsets. | `src/engines/clone_engine.py` |
| NS-018 | **ONNX Runtime** for GPU-accelerated MediaPipe | Replace TFLite XNNPACK with ONNX GPU backend for full RTX 4070 utilization. | `src/engines/gesture_engine.py`, `src/engines/clone_engine.py` |
| NS-019 | **Makefile** for one-command setup/run | `make install`, `make run`, `make test` for scripted workflows. | `Makefile` |
| NS-020 | **GitHub-ready production layout** | Standardize with `pyproject.toml`, proper `src/` packaging, `tests/` directory. | Root directory restructure |

---

## Recommended Execution Order

```
Phase A (Demo-Ready):  NS-002 → NS-001 → NS-008
Phase B (Web Polish):  NS-003 → NS-005 → NS-004
Phase C (Performance): NS-006 → NS-007
Phase D (Expansion):   NS-009 → NS-010 → NS-013
Phase E (DevOps):      NS-015 → NS-016 → NS-019 → NS-020
```

---

## Dependencies

```
NS-001 (Smoke) depends on: generate_image tool or user-provided smoke.png
NS-003 (WebSocket) depends on: no external deps (uvicorn supports WS natively)
NS-007 (cv2.UMat) depends on: OpenCV built with CUDA (current pip build may not have it)
NS-018 (ONNX RT) depends on: onnxruntime-gpu pip package + CUDA 11.x/12.x toolkit
```
