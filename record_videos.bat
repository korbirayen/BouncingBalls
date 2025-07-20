@echo off
echo 📹 Starting Video Recording Helper...
echo.
cd /d "%~dp0"
.venv\Scripts\python.exe record_helper.py
pause
