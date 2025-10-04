@echo off
echo Starting Virtual Pet with Text-to-Speech...
echo.
echo Make sure your speakers are on to hear Pixie speak! 🔊
echo.
cd /d "%~dp0"
".venv\Scripts\python.exe" main.py
echo.
echo Pet application has closed.
pause