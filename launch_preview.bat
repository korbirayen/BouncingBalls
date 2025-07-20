@echo off
echo 🎥 Starting Viral Video Factory Preview Launcher...
echo.
cd /d "%~dp0"
.venv\Scripts\python.exe video_preview_launcher.py
pause
