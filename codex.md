Perfect. Below is a **one-shot CRAFT master prompt** you can paste into your IDE agent (Antigravity) to close every loose end in a single execution cycle.

This prompt assumes:

* OpenCV namespace collision has been identified
* You want a clean environment
* You want terminal-native execution
* You want permanent project documentation generated
* You want zero repetition of past mistakes

---

# 🚀 ANTIGRAVITY — ONE SHOT PROJECT STABILIZATION PROMPT

---

## 🧠 CRAFT MASTER PROMPT

````
You are operating inside the Antigravity Vision Agent project.

# C — CONTEXT

Project Name: Antigravity Vision Agent  
Core Stack: Python 3.x, MediaPipe, OpenCV (opencv-contrib-python)  
Environment: Local machine terminal (NOT sandboxed chat execution)  
IDE: VS Code integrated terminal  
Primary Goal: Stabilize environment + finalize native terminal execution  

Known Historical Failure:
- OpenCV namespace collision between:
  - opencv-python
  - opencv-contrib-python
  - opencv-python-headless
- Symptom: cv2 loads but lacks VideoCapture
- Root Cause: Simultaneous installation + mediapipe version forcing

We are executing a "Scorched Earth Stabilization Protocol" to permanently fix this.

This is a one-shot repair + documentation generation cycle.
No partial fixes. No iterative guessing.

---

# R — ROLE

You are a senior Python systems engineer specializing in:
- Virtual environment stabilization
- Computer vision stacks (MediaPipe + OpenCV)
- Dependency conflict resolution
- Reproducible project architecture
- CLI-native agent execution

You do not speculate.
You verify.
You enforce clean state before proceeding.

---

# A — ACTIONS (Execute Sequentially)

## 1️⃣ Environment Reset Protocol

1. Detect active Python interpreter.
2. Confirm virtual environment usage.
3. If no venv exists → create `.venv`
4. Activate `.venv`
5. Execute full OpenCV purge:

   pip uninstall -y opencv-python opencv-contrib-python opencv-python-headless

6. Confirm purge by running:
   python -c "import cv2"

   This MUST fail before continuing.

---

## 2️⃣ Controlled Reinstallation

Install in correct order:

1. pip install mediapipe
2. pip install opencv-contrib-python

Do NOT install opencv-python.
Do NOT install headless variant.

After install:
Run verification script:

```python
import cv2
cap = cv2.VideoCapture(0)
print("VideoCapture Exists:", hasattr(cv2, "VideoCapture"))
print("Camera Opened:", cap.isOpened())
cap.release()
````

If either check fails → abort and report environment instability.

---

## 3️⃣ Project Structure Enforcement

Ensure project tree:

Antigravity/
│
├── .venv/
├── main.py
├── requirements.txt
├── README.md
├── execution.md
├── troubleshoot.md
└── .idea/
└── project_metadata.xml

---

## 4️⃣ Generate Clean requirements.txt

It must contain ONLY:

mediapipe
opencv-contrib-python

No duplicates.
No headless.
No opencv-python.

---

## 5️⃣ Generate Documentation Files

### README.md

Include:

* Project purpose
* Stack explanation
* Why contrib version required
* Quick start instructions

### execution.md

Include:

* venv activation instructions
* how to run main.py
* CLI-only mode
* how to verify camera

### troubleshoot.md

Include:

* Exact namespace collision explanation
* How to detect it
* Full purge procedure
* Why mediapipe complicates installs
* How to avoid recurrence

---

## 6️⃣ Native Terminal Mode Enforcement

Modify main.py to:

* Accept `--cli` flag
* Avoid GUI dependencies when in CLI mode
* Log startup state
* Confirm camera access on boot
* Gracefully exit if camera unavailable

---

## 7️⃣ Final Verification Checklist

Output a verification report including:

* Python version
* Virtual environment path
* Installed OpenCV version
* Installed MediaPipe version
* VideoCapture test result
* Project file generation status

---

# F — FORMAT

Return structured output:

1. ENVIRONMENT REPORT
2. DEPENDENCY REPORT
3. FILE GENERATION REPORT
4. VERIFICATION STATUS
5. FINAL SYSTEM STATE

Use clear terminal-style formatting.
No filler explanation.
No conversational text.

---

# T — TARGET

Result:
A fully stabilized, reproducible, terminal-native Antigravity Vision Agent environment.

Zero OpenCV conflicts.
Zero namespace ambiguity.
Zero dependency drift.
Fully documented.
Ready for native execution.

If instability detected at any stage → halt and provide precise error state.
Do not attempt silent auto-correction.

Begin execution.

```

---

# 🔥 What This Does

This single prompt:

- Forces clean virtual environment discipline
- Eliminates OpenCV namespace collisions permanently
- Locks dependency stack
- Generates all documentation
- Enforces terminal-native operation
- Adds runtime verification
- Produces structured final report
- Prevents repeat of double-install mistake

---

If you'd like, I can now generate:

• A hardened `main.py` with CLI flag handling  
• A pinned version requirements file  
• A Docker fallback environment  
• A Makefile for one-command setup  
• Or a GitHub-ready production layout  

Just tell me the next level you want to push Antigravity to.
```
