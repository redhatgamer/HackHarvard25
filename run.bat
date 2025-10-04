@echo off
REM Windows Batch Script to Launch Virtual Pet AI Assistant

echo 🐱 Starting Virtual Pet AI Assistant...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv" (
    echo 📦 Virtual environment not found. Creating one...
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

REM Install dependencies if requirements.txt exists and is newer
if exist "requirements.txt" (
    echo 📦 Checking dependencies...
    pip install -r requirements.txt
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found!
    echo Creating .env from template...
    
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo.
        echo ⚠️  IMPORTANT: Please edit .env and add your Gemini API key!
        echo Get your API key from: https://makersuite.google.com/app/apikey
        echo.
        pause
    ) else (
        echo ❌ .env.example not found. Please create .env manually.
        pause
        exit /b 1
    )
)

REM Run the application
echo 🚀 Launching Pixie...
python main.py

if errorlevel 1 (
    echo.
    echo ❌ Application exited with an error
    echo Check the logs in the logs/ directory for more information
    pause
)

echo.
echo 👋 Pixie has stopped. Goodbye!
pause