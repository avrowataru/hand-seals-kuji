# Error Log — Shadow Clone Jutsu

> **Complete record of every error encountered** during the development session.
> Updated: 2026-02-17T22:57:46+09:00

---

## Error Index

| # | Error | Severity | Time (JST) | Phase | Status |
|---|---|---|---|---|---|
| E-001 | venv command rejected by user | ⚪ Operational | 21:20 | 2 | ✅ Resolved |
| E-002 | `ModuleNotFoundError: No module named 'cv2'` | 🟡 Medium | 21:35 | 4 | ✅ Resolved |
| E-003 | `AttributeError: mp.solutions.hands` | 🔴 Critical | 21:35 | 4 | ✅ Resolved |
| E-004 | `AttributeError: cv2 has no __version__` | 🔴 Critical | 21:38 | 5 | ✅ Resolved |
| E-005 | `AttributeError: cv2 has no VideoCapture` | 🔴 Critical | 21:45 | 5 | ✅ Resolved |
| E-006 | `KeyboardInterrupt` on `cv2.waitKey` | ⚪ Expected | 21:48 | 5 | ✅ Normal |
| E-007 | Browser agent Playwright failure | 🟡 Environment | 22:54 | 9 | ⚠️ Bypassed |

---

## E-001: venv Command Rejected

| Field | Detail |
|---|---|
| **Time** | 2026-02-17T21:20:57+09:00 |
| **Phase** | 2 — User Refinements |
| **Severity** | ⚪ Operational |
| **Error** | Agent proposed `python -m venv venv` — user rejected |
| **Root Cause** | User already created conda env `sha` and preferred it |
| **Resolution** | Switched all commands to `conda activate sha` / explicit interpreter path |
| **Prevention** | Ask user for environment preference before creating |

---

## E-002: No module named 'cv2'

| Field | Detail |
|---|---|
| **Time** | 2026-02-17T21:35:00+09:00 |
| **Phase** | 4 — First Run |
| **Severity** | 🟡 Medium |
| **Command** | `python src/utils/camera_check.py` |
| **Error** | `ModuleNotFoundError: No module named 'cv2'` |
| **Root Cause** | Default `python` in PATH → base Conda env (3.13), not `sha` (3.11). Packages installed in `sha` but wrong interpreter invoked. |
| **Resolution** | Used explicit path: `c:\Users\Rambo\miniconda3\envs\sha\python.exe` |
| **Prevention** | Always use full interpreter path or verify `conda activate sha` |

---

## E-003: mp.solutions.hands AttributeError

| Field | Detail |
|---|---|
| **Time** | 2026-02-17T21:35:00+09:00 |
| **Phase** | 4 — First Run |
| **Severity** | 🔴 Critical |
| **Error** | `AttributeError: module 'mediapipe' has no attribute 'solutions'` |
| **Root Cause** | MediaPipe `0.10.32` from base env loaded instead of `sha`'s version. Import path leakage. |
| **Resolution** | Pinned `mediapipe==0.10.9`, installed via explicit interpreter |
| **Prevention** | Always pin MediaPipe. Always use explicit interpreter path. |

---

## E-004: cv2 has no attribute '__version__'

| Field | Detail |
|---|---|
| **Time** | 2026-02-17T21:38:00+09:00 |
| **Phase** | 5 — cv2 Collision |
| **Severity** | 🔴 Critical |
| **Error** | `AttributeError: module 'cv2' has no attribute '__version__'` |
| **Root Cause** | **Namespace collision.** Both `opencv-python` and `opencv-contrib-python` installed. They share the `cv2` namespace. Second install overwrote the `.pyd` binary, leaving a hollow module. |
| **Resolution** | Uninstalled `opencv-python`, kept `opencv-contrib-python` only |
| **Prevention** | Never install both. Safety headers in `requirements.txt`. |

### Collision Diagram
```
site-packages/
├── cv2/
│   ├── __init__.py         ← Points to wrong .pyd
│   └── cv2.pyd             ← Overwritten by second install → CORRUPT
├── opencv_python-4.13.0.92.dist-info/          ← STALE
└── opencv_contrib_python-4.13.0.92.dist-info/  ← ACTIVE
```

---

## E-005: cv2 has no attribute 'VideoCapture'

| Field | Detail |
|---|---|
| **Time** | 2026-02-17T21:45:00+09:00 |
| **Phase** | 5 — cv2 Collision |
| **Severity** | 🔴 Critical |
| **Error** | `module 'cv2' has no attribute 'VideoCapture'` |
| **Root Cause** | Same as E-004. After partial uninstall, residual files in `site-packages/cv2/` persisted. Module imported but was non-functional. |
| **Resolution** | **Scorched Earth Protocol:** |
| | 1. `pip uninstall -y opencv-python opencv-contrib-python opencv-python-headless` |
| | 2. `Remove-Item -Recurse -Force "$sitePackages\cv2"` |
| | 3. `Remove-Item -Recurse -Force "$sitePackages\opencv_python*"` |
| | 4. `Remove-Item -Recurse -Force "$sitePackages\opencv_contrib*"` |
| | 5. `pip install opencv-contrib-python==4.13.0.92` |
| **Prevention** | Always purge residual files after OpenCV uninstall. |

---

## E-006: KeyboardInterrupt on cv2.waitKey

| Field | Detail |
|---|---|
| **Time** | 2026-02-17T21:48:49+09:00 |
| **Phase** | 5 — Verification |
| **Severity** | ⚪ Expected |
| **Error** | `KeyboardInterrupt` at `key = cv2.waitKey(5) & 0xFF` |
| **Root Cause** | Agent sent terminate signal to stop background process after verification. Normal. |
| **Resolution** | N/A — expected behavior |

---

## E-007: Browser Agent Playwright Failure

| Field | Detail |
|---|---|
| **Time** | 2026-02-17T22:54:00+09:00 |
| **Phase** | 9 — Web Verification |
| **Severity** | 🟡 Environment |
| **Error** | `failed to create browser context: failed to install playwright: $HOME environment variable is not set` |
| **Root Cause** | Playwright browser was not installed in the agent sandbox. The `$HOME` environment variable is not set in the execution context. This is an IDE infrastructure limitation, not a project bug. |
| **Resolution** | Bypassed by verifying via HTTP requests instead: |
| | — `Invoke-RestMethod http://localhost:8000/status` → JSON confirmed |
| | — `read_url_content http://localhost:8000` → HTML confirmed with "影分身の術" |
| **Impact** | No visual screenshot of the Floating UI was captured. User can verify manually at `http://localhost:8000`. |
| **Prevention** | N/A — IDE infrastructure issue, not actionable. |

---

## Error Frequency by Category

| Category | Count | Resolution Rate |
|---|---|---|
| Namespace Collision (`cv2`) | 2 | 100% |
| Wrong Interpreter / Path | 2 | 100% |
| User Directive Override | 1 | 100% |
| Expected Behavior | 1 | N/A |
| IDE Infrastructure | 1 | Bypassed |
| **Total** | **7** | **100%** |

---

## Lessons Learned

1. **Always use explicit interpreter paths** on Windows with multiple Conda envs.
2. **Never install `opencv-python` and `opencv-contrib-python` together** — shared `cv2` namespace.
3. **Pin all critical versions** — MediaPipe and Protobuf are especially sensitive.
4. **Purge residual files** after OpenCV uninstall — `pip uninstall` alone is insufficient.
5. **Ask user for environment preference** before creating environments.
6. **Base Conda env can shadow `sha` env** — always verify which `python` is in PATH.
7. **HTTP verification** can substitute for browser-based verification when Playwright is unavailable.
