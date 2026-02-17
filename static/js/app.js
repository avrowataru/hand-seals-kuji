/**
 * Shadow Clone Jutsu — Client-side Controller
 * Polls the /status endpoint and updates the UI in real-time.
 */

// ============================================================
// State Polling
// ============================================================
const POLL_INTERVAL = 250; // ms

async function pollStatus() {
    try {
        const res = await fetch('/status');
        if (!res.ok) return;
        const data = await res.json();

        // Update Jutsu Indicator
        const indicator = document.getElementById('jutsu-indicator');
        const indicatorText = document.getElementById('indicator-text');
        const videoFeed = document.getElementById('video-feed');

        if (data.jutsu_active) {
            indicator.className = 'indicator-active';
            indicatorText.textContent = 'JUTSU ACTIVE';
            videoFeed.classList.add('jutsu-active');
        } else {
            indicator.className = 'indicator-inactive';
            indicatorText.textContent = 'STANDBY';
            videoFeed.classList.remove('jutsu-active');
        }

        // Update FPS
        const fpsValue = document.getElementById('fps-value');
        const statusFps = document.getElementById('status-fps');
        fpsValue.textContent = data.fps;
        statusFps.textContent = `${data.fps} fps`;

        // Update Status Panel
        const statusCamera = document.getElementById('status-camera');
        statusCamera.textContent = `●  Index ${data.camera_index} (${data.resolution})`;
        statusCamera.className = 'status-value ' + (data.running ? 'status-ok' : 'status-inactive');

        const statusJutsu = document.getElementById('status-jutsu');
        if (data.jutsu_active) {
            statusJutsu.textContent = '●  ACTIVE';
            statusJutsu.className = 'status-value status-active';
        } else {
            statusJutsu.textContent = '○  Inactive';
            statusJutsu.className = 'status-value status-inactive';
        }

        // Update debug button state
        const btnDebug = document.getElementById('btn-debug');
        if (data.debug_mode) {
            btnDebug.classList.add('active');
        } else {
            btnDebug.classList.remove('active');
        }

    } catch (err) {
        // Server might not be ready yet
        console.warn('Status poll failed:', err.message);
    }
}

// Start polling
setInterval(pollStatus, POLL_INTERVAL);
// Initial poll
pollStatus();

// ============================================================
// Controls
// ============================================================
async function toggleDebug() {
    try {
        await fetch('/toggle_debug', { method: 'POST' });
        pollStatus(); // Immediate refresh
    } catch (err) {
        console.error('Toggle debug failed:', err);
    }
}

function toggleFullscreen() {
    const videoContainer = document.getElementById('video-container');
    if (!document.fullscreenElement) {
        videoContainer.requestFullscreen().catch(err => {
            console.warn('Fullscreen failed:', err);
        });
    } else {
        document.exitFullscreen();
    }
}

// ============================================================
// Keyboard Shortcuts (for power users)
// ============================================================
document.addEventListener('keydown', (e) => {
    switch (e.key.toLowerCase()) {
        case 'd':
            toggleDebug();
            break;
        case 'f':
            toggleFullscreen();
            break;
    }
});

// ============================================================
// Startup Log
// ============================================================
console.log(
    '%c🥷 Shadow Clone Jutsu — Floating UI v2.0',
    'color: #00e5ff; font-size: 16px; font-weight: bold;'
);
console.log(
    '%cKeyboard: D = Debug | F = Fullscreen',
    'color: #9fa8da; font-size: 12px;'
);
