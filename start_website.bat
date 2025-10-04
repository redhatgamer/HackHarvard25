@echo off
echo ================================================
echo    Virtual Pet AI Assistant - Website Launcher
echo ================================================
echo.
echo Choose an option:
echo 1. Start Static Website (GitHub Pages preview)
echo 2. Start Interactive Web App (Flask)
echo 3. Both websites
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto static
if "%choice%"=="2" goto flask
if "%choice%"=="3" goto both
if "%choice%"=="4" goto exit

:static
echo.
echo Starting static website on http://localhost:8000
echo Press Ctrl+C to stop
cd "%~dp0docs"
python -m http.server 8000
goto end

:flask
echo.
echo Starting Flask web app on http://localhost:5000
echo Press Ctrl+C to stop
cd "%~dp0"
".venv\Scripts\python.exe" "web\app.py"
goto end

:both
echo.
echo Starting both websites...
echo Static site: http://localhost:8000
echo Flask app: http://localhost:5000
echo.
start "Static Website" cmd /c "cd /d %~dp0docs && python -m http.server 8000"
start "Flask App" cmd /c "cd /d %~dp0 && .venv\Scripts\python.exe web\app.py"
echo Both websites are starting in separate windows...
goto end

:exit
echo Goodbye!
goto end

:end
pause