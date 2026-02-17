"""
Shadow Clone Jutsu — Web Application Launcher
===============================================
Starts the FastAPI server with uvicorn.

Usage:
    python run_web.py              # http://localhost:8000
    python run_web.py --port 9000  # http://localhost:9000
"""

import argparse
import uvicorn


def main():
    parser = argparse.ArgumentParser(description="Shadow Clone Jutsu Web Server")
    parser.add_argument('--host', default='0.0.0.0', help='Bind address (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='Port (default: 8000)')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload for development')
    args = parser.parse_args()

    print("=" * 60)
    print("  🥷 SHADOW CLONE JUTSU — Web Mode")
    print(f"  Open: http://localhost:{args.port}")
    print("=" * 60)

    uvicorn.run(
        "src.web_server:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )


if __name__ == "__main__":
    main()
