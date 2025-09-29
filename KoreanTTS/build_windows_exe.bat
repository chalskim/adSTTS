@echo off
REM build_windows_exe.bat
REM Script to build Korean TTS Windows executable

echo Korean TTS Windows Executable Builder
echo ====================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install PyInstaller
    if %errorlevel% neq 0 (
        echo Error: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

REM Install required dependencies
echo Installing required dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install required dependencies
    pause
    exit /b 1
)

REM Build the command-line executable
echo Building Windows command-line executable...
pyinstaller --onefile --console korean_tts_windows.py --name korean_tts_cli
if %errorlevel% neq 0 (
    echo Error: Failed to build command-line executable
    pause
    exit /b 1
)

REM Build the Korean GUI executable
echo Building Windows Korean GUI executable...
pyinstaller --onefile --windowed korean_tts_gui.py --name korean_tts_gui
if %errorlevel% neq 0 (
    echo Error: Failed to build Korean GUI executable
    pause
    exit /b 1
)

REM Build the English GUI executable
echo Building Windows English GUI executable...
pyinstaller --onefile --windowed english_tts_gui.py --name english_tts_gui
if %errorlevel% neq 0 (
    echo Error: Failed to build English GUI executable
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo The executables are located in the 'dist' folder:
echo   - korean_tts_cli.exe     (Command-line version)
echo   - korean_tts_gui.exe     (Korean GUI version)
echo   - english_tts_gui.exe    (English GUI version)
echo.
echo To use the TTS converters:
echo   Command-line: korean_tts_cli.exe input.txt output.wav 1.5
echo   Korean GUI:   Double-click korean_tts_gui.exe
echo   English GUI:  Double-click english_tts_gui.exe
echo.
echo Example:
echo   korean_tts_cli.exe sample_korean.txt korean_speech.wav 1.2
echo.
pause