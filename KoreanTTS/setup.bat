@echo off
REM setup.bat
REM Setup script for Korean TTS Converter (Windows)

echo Setting up Korean TTS Converter...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.7 or higher.
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed. Please install pip.
    exit /b 1
)

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo Setup completed successfully!
    echo.
    echo To test the Korean TTS converter:
    echo 1. Create a text file with Korean content
    echo 2. Run: python universal_korean_tts.py your_file.txt
    echo.
    echo Example:
    echo python universal_korean_tts.py sample_korean.txt
    echo.
    echo Alternative approaches:
    echo - MeloTTS only: python text_to_speech.py your_file.txt
    echo - gTTS only: python korean_tts_gTTS.py your_file.txt
) else (
    echo Setup failed. Please check the error messages above.
    exit /b 1
)