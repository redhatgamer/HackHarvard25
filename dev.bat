@echo off
REM Development Mode Launcher for Virtual Pet AI Assistant
REM This script provides live development with auto-reload

echo 🛠️  Starting Development Mode...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists, create if not
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
    
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo ⚡ Activating virtual environment...
call .venv\Scripts\activate

REM Install/update dependencies
echo 📦 Installing development dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found!
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo Created .env from template
        echo ⚠️  IMPORTANT: Please edit .env and add your Gemini API key!
    )
)

echo.
echo 🚀 Starting Development Server with Hot-Reload...
echo.
echo Features:
echo - 🔄 Automatic restart when files change
echo - 📝 Real-time development feedback  
echo - 🐱 Live pet testing
echo.
echo Press Ctrl+C to stop development mode
echo =====================================

REM Run the development server
python dev.py

if errorlevel 1 (
    echo.
    echo ❌ Development server exited with an error
    echo Check the console output above for details
)

echo.
echo 👋 Development mode stopped
pause