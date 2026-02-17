# Architecture Decisions Record — Shadow Clone Jutsu

> **ADR (Architecture Decision Record)** capturing every significant technical decision.
> Updated: 2026-02-17T22:57:46+09:00

---

## ADR-001: Conda over venv

| Field | Value |
|---|---|
| **Date** | 2026-02-17T21:22:55+09:00 |
| **Status** | ✅ Accepted |
| **Decision** | Use Conda environment (`sha`) instead of Python `venv` |
| **Context** | Agent initially attempted `python -m venv venv`. User had already created `conda create -n sha python=3.11`. |
| **Rationale** | User preference. Conda provides better isolation for mixed C++/Python stacks on Windows. |
| **Alternatives** | `python -m venv venv` (rejected by user) |
| **Consequence** | All commands use explicit interpreter path or `conda activate sha`. |

---

## ADR-002: opencv-contrib-python over opencv-python

| Field | Value |
|---|---|
| **Date** | 2026-02-17T21:42:00+09:00 |
| **Status** | ✅ Accepted (post-collision) |
| **Decision** | Use `opencv-contrib-python` exclusively. **Never** install `opencv-python`. |
| **Context** | Both packages share the `cv2` namespace. Co-installation corrupted the module. |
| **Rationale** | `opencv-contrib-python` is a superset. MediaPipe depends on it. |
| **Alternatives** | `opencv-python` (conflicts with MediaPipe's dep chain) |
| **Consequence** | `requirements.txt` has explicit safety headers. |

---

## ADR-003: MediaPipe 0.10.9 (Pinned)

| Field | Value |
|---|---|
| **Date** | 2026-02-17T21:38:00+09:00 |
| **Status** | ✅ Accepted |
| **Decision** | Pin MediaPipe to `0.10.9` |
| **Context** | Base env had 0.10.32 which broke `mp.solutions`. Later versions may restructure. |
| **Rationale** | 0.10.9 is the last stable version with reliable `mp.solutions.hands` on Windows. |
| **Consequence** | Protobuf pinned to `3.20.3` for compatibility. |

---

## ADR-004: model_complexity=0 for Hand Tracker

| Field | Value |
|---|---|
| **Date** | 2026-02-17T21:20:57+09:00 |
| **Status** | ✅ Accepted |
| **Decision** | Initialize MediaPipe Hands with `model_complexity=0` |
| **Context** | User directive: MediaPipe Python on Windows runs CPU inference only. |
| **Rationale** | Lightest model. Ram Seal only checks 2 landmarks. Saves CPU for segmentation. |
| **Consequence** | Faster hand detection, more CPU budget for SelfieSegmentation. |

---

## ADR-005: NumPy Slicing over np.roll

| Field | Value |
|---|---|
| **Date** | 2026-02-17T21:20:57+09:00 |
| **Status** | ✅ Accepted |
| **Decision** | Use NumPy array slicing instead of `np.roll` |
| **Context** | `np.roll` re-allocates entire array. Slow for 1080p+. |
| **Rationale** | Slicing only copies foreground pixels. O(foreground) vs O(total). |
| **Implementation** | `left_clone[:, :w-off] = foreground[:, off:]` |
| **Consequence** | No wrap-around artifacts at frame edges. |

---

## ADR-006: Gaussian Blur on Segmentation Mask

| Field | Value |
|---|---|
| **Date** | 2026-02-17T21:20:57+09:00 → Updated 22:49+09:00 |
| **Status** | ✅ Accepted (revised) |
| **Decision** | Apply Gaussian blur to binary segmentation mask |
| **v1** | 5×5 kernel (initial implementation in `src/app/clone_engine.py`) |
| **v2** | 3×3 kernel (per web directive in `src/engines/clone_engine.py`) |
| **Rationale** | Softens edges for "ghostly" clone appearance. 3×3 is sufficient and faster. |

---

## ADR-007: CAP_DSHOW for Windows Camera Backend

| Field | Value |
|---|---|
| **Date** | 2026-02-17T21:18:05+09:00 |
| **Status** | ✅ Accepted |
| **Decision** | Use `cv2.CAP_DSHOW` (DirectShow) backend |
| **Context** | Project rule: "Always attempt CAP_DSHOW first for Windows compatibility." |
| **Rationale** | Most reliable on Windows 11. MSMF can have latency issues with Hello cameras. |
| **Consequence** | All `VideoCapture` calls pass `cv2.CAP_DSHOW` as second argument. |

---

## ADR-008: HOLD Mode for Jutsu Activation

| Field | Value |
|---|---|
| **Date** | 2026-02-17T21:20:57+09:00 |
| **Status** | ✅ Accepted |
| **Decision** | Clones appear while seal is held, disappear when released |
| **Rationale** | More interactive. Prevents false-positive toggles from fleeting detections. |
| **Implementation** | `jutsu_active = active_now` (direct assignment, not toggle) |

---

## ADR-009: --cli Flag for Diagnostic Mode

| Field | Value |
|---|---|
| **Date** | 2026-02-17T22:07:00+09:00 |
| **Status** | ✅ Accepted |
| **Decision** | Add `--cli` flag to `main.py` for headless diagnostics |
| **Context** | CRAFT Protocol Phase 6 requirement. |
| **Rationale** | Separates verification from GUI. Enables CI/CD and SSH testing. |
| **Implementation** | `argparse` → `run_cli_mode()` vs `run_gui_mode()` |

---

## ADR-010: Protobuf 3.20.3 (Pinned)

| Field | Value |
|---|---|
| **Date** | 2026-02-17T21:38:00+09:00 |
| **Status** | ✅ Accepted |
| **Decision** | Pin Protobuf to `3.20.3` |
| **Rationale** | Last stable 3.x release. 4.x has breaking changes. MediaPipe 0.10.9 needs `<4,>=3.11`. |

---

## ADR-011: FastAPI for Web Streaming (v2.0)

| Field | Value |
|---|---|
| **Date** | 2026-02-17T22:49:29+09:00 |
| **Status** | ✅ Accepted |
| **Decision** | Transition from local OpenCV window to FastAPI MJPEG streaming |
| **Context** | User directive to create a "Floating UI" web interface. Terminal-only output is limiting for demos and polish. |
| **Rationale** | FastAPI is lightweight, async-capable, and supports `StreamingResponse` for MJPEG. Allows rich HTML/CSS/JS UI overlays without adding heavy frontend dependencies. |
| **Alternatives** | Flask (heavier, sync-only), Streamlit (too opinionated), WebSocket raw (more complex) |
| **Stack** | FastAPI 0.129.0 + Uvicorn 0.41.0 + Jinja2 3.1.6 |
| **Consequence** | New entry point `run_web.py`. Camera processing moves to a background thread. |

---

## ADR-012: Glassmorphism Floating UI

| Field | Value |
|---|---|
| **Date** | 2026-02-17T22:49:29+09:00 |
| **Status** | ✅ Accepted |
| **Decision** | Use CSS glassmorphism (`backdrop-filter: blur`) for the control panel |
| **Context** | User referenced a "floating structure" and modern web design. |
| **Rationale** | Glassmorphism creates a premium, immersive feel without obscuring the video. The blurred panel sits over the dark background, letting animated glows show through. |
| **Implementation** | `backdrop-filter: blur(24px) saturate(150%)` on `#control-panel` |
| **Design Tokens** | Dark palette (`#0a0a1a`), accent cyan (`#00e5ff`), Outfit + JetBrains Mono fonts |

---

## ADR-013: Layered Alpha Compositing (v2 Clone Engine)

| Field | Value |
|---|---|
| **Date** | 2026-02-17T22:49:29+09:00 |
| **Status** | ✅ Accepted |
| **Decision** | Replace additive blending (v1) with layered alpha compositing (v2) |
| **Context** | v1 used `cv2.addWeighted` which caused brightness blowout in overlapping regions. |
| **Rationale** | Proper alpha: `output = output * (1 - mask) + clone * mask`. Produces clean, correctly-layered clones without washing out the background or the real user. |
| **Layer Order** | Layer 0: Background → Layer 1: Left+Right Clones (70% alpha) → Layer 2: Real User (100%) |
| **Consequence** | Real user is always on top. Clones are semi-transparent. No blowout. |

---

## ADR-014: Blue Chakra Tint (B:255, G:100, R:100)

| Field | Value |
|---|---|
| **Date** | 2026-02-17T22:49:29+09:00 |
| **Status** | ✅ Accepted |
| **Decision** | Apply BGR tint `(255, 100, 100)` to clones |
| **Context** | User directive: "blue color-tint (B:255, G:100, R:100)" |
| **Rationale** | Creates a distinctive "chakra" visual. Blue-dominant tint matches the Naruto lore (shadow clones emit blue chakra). Multiplicative tinting preserves detail. |
| **v1** | Simple `*= 1.5` on blue channel only (crude) |
| **v2** | Per-channel multiplication: B×1.0, G×0.39, R×0.39 (normalized) |

---

## ADR-015: Touch Threshold 0.05 (v2 Gesture Engine)

| Field | Value |
|---|---|
| **Date** | 2026-02-17T22:49:29+09:00 |
| **Status** | ✅ Accepted |
| **Decision** | Increase touch threshold from 0.04 (v1) to 0.05 (v2) |
| **Context** | User directive: "trigger when Index Tip (8) and Middle Tip (12) are within normalized distance of 0.05." |
| **Rationale** | More forgiving detection. 0.04 was occasionally too tight, requiring very precise finger crossing. 0.05 provides a better UX while remaining precise enough to avoid false positives. |

---

## ADR-016: Status Polling (250ms) over WebSocket

| Field | Value |
|---|---|
| **Date** | 2026-02-17T22:51:00+09:00 |
| **Status** | ✅ Accepted |
| **Decision** | Client polls `/status` every 250ms instead of using WebSocket |
| **Context** | The video feed uses MJPEG (HTTP streaming). Status data is small (JSON). |
| **Rationale** | Polling is simpler, avoids connection management complexity, and 250ms is fast enough for UI updates. WebSocket would be overkill for ~50 bytes of status JSON. |
| **Consequence** | `setInterval(pollStatus, 250)` in `app.js`. |
