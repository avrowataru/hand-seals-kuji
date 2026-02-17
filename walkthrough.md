# Shadow Clone Jutsu Walkthrough

## Prerequisites
- Windows 11
- Webcam (Windows Hello capable preferred)
- NVIDIA GPU (RTX 4070) for best performance
- Conda environment `sha` active

## Installation
1.  Navigate to the project directory:
    ```powershell
    cd c:\Users\Rambo\Documents\source\shadowclone
    ```
2.  Activate the environment:
    ```powershell
    conda activate sha
    ```
3.  Install dependencies:
    ```powershell
    pip install -r requirements.txt
    ```

## Usage
1.  **Run the Camera Check** (Optional but recommended first):
    ```powershell
    python src/utils/camera_check.py
    ```
    This will probe your cameras and tell you which index is the RGB stream.

2.  **Start the Application**:
    ```powershell
    python main.py
    ```

3.  **Controls**:
    - **'q'**: Quit the application.
    - **'d'**: Toggle Debug Mode (shows landmarks and status).

## How to Perform the Jutsu
1.  Stand in front of the camera so your upper body is visible.
2.  Perform the **"Ram" Seal**:
    - Bring your **Index** and **Middle** fingers together (cross them or touch tips).
    - Can be done with one hand (crossing fingers) or two hands (touching tips).
3.  When detected, two "Shadow Clones" will appear on your left and right.
4.  Release the seal to make them vanish (or hold to keep them).

## Troubleshooting
- **Black Screen**: The wrong camera index might be selected. Check the output of [camera_check.py](file:///c:/Users/Rambo/Documents/source/shadowclone/src/utils/camera_check.py).
- **Low FPS**: Ensure your laptop is plugged in and using the Discrete GPU.
- **Clones look jagged**: The app uses a blur filter, but poor lighting can affect segmentation quality.
