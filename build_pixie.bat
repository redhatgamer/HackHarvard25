@echo off
echo 🦎 Building Pixie Pet Executable...
echo ======================================

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Build the executable
echo Building executable...
pyinstaller --onefile --windowed --name=PixiePet --add-data "assets;assets" --add-data "config;config" --add-data "src;src" main.py

REM Check if build was successful
if exist "dist\PixiePet.exe" (
    echo ✅ Build successful!
    echo 📦 Executable created at: dist\PixiePet.exe
    echo.
    echo 💡 To distribute:
    echo    1. Copy the entire 'dist' folder
    echo    2. Make sure assets and config folders are included
    echo    3. Share with users!
) else (
    echo ❌ Build failed! Check the output above for errors.
)

pause