@echo off
echo Starting Dark Mode Demo for Desktop Pet...
echo.

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.7 or later
    pause
    exit /b 1
)

echo Running dark mode test...
python test_dark_mode.py

if errorlevel 1 (
    echo.
    echo Demo failed to start. Make sure all dependencies are available.
    pause
)