@echo off
echo Starting Desktop Pet with Voice Interaction...
echo ================================================
echo.
echo Make sure you have a microphone attached and working!
echo.
echo You can now ask your pet questions like:
echo - "What flavor of Linux do you recommend?"
echo - "How do I learn Python?"
echo - "Explain machine learning"
echo - "What's the best text editor?"
echo.
echo Press Ctrl+C to stop the pet
echo.
pause
echo.
echo Starting pet...
cd /d "%~dp0"
".venv\Scripts\python.exe" main.py
pause