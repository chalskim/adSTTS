@echo off
REM install_dependencies.bat
REM Script to install Korean TTS dependencies on Windows

echo Korean TTS Dependency Installer
echo ===============================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

echo Installing Korean TTS dependencies...
pip install melo-tts librosa soundfile numpy

if %errorlevel% equ 0 (
    echo.
    echo Dependencies installed successfully!
    echo.
    echo You can now build the Windows executable by running:
    echo   build_windows_exe.bat
    echo.
    echo Or run the Korean TTS converter directly with:
    echo   python korean_tts_windows.py input.txt output.wav 1.5
) else (
    echo.
    echo Error: Failed to install dependencies
    echo You may need to run this script as administrator
)

pause