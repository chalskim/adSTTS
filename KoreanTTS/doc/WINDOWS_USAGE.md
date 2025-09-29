# Korean TTS Converter for Windows

This guide explains how to use the Korean TTS Converter on Windows systems.

## New: Graphical User Interface Available

In addition to the command-line interface, a graphical user interface (GUI) version is now available for easier use.

## Prerequisites

1. Windows 7 or higher (64-bit recommended)
2. Python 3.7 or higher installed
3. Internet connection for initial setup

## Installation Options

### Option 1: Use Pre-built Executable (Recommended)

Two executables are available:

1. **Command-line version** (`korean_tts_cli.exe`):
   - Create a text file with Korean content
   - Run the converter from Command Prompt:
     ```
     korean_tts_cli.exe input.txt output.wav 1.5
     ```

2. **Graphical interface version** (`korean_tts_gui.exe`):
   - Simply double-click the executable to open the GUI
   - Use the file browser to select input/output files
   - Adjust speed with the slider or preset buttons

### Option 2: Build from Source

1. **Install Dependencies**:
   - Double-click `install_dependencies.bat`
   - Or manually run in Command Prompt:
     ```
     pip install melo-tts librosa soundfile numpy
     ```

2. **Build Executables**:
   - Double-click `build_windows_exe.bat`
   - Or manually run in Command Prompt:
     ```
     pip install PyInstaller
     pyinstaller --onefile --console korean_tts_windows.py --name korean_tts_cli
     pyinstaller --onefile --windowed korean_tts_gui.py --name korean_tts_gui
     pyinstaller --onefile --windowed english_tts_gui.py --name english_tts_gui
     ```

## Usage

### Command-line Version
```
korean_tts_cli.exe input.txt output.wav 1.5
```

### Korean GUI Version
Simply double-click `korean_tts_gui.exe` and use the graphical interface.

### English GUI Version
Simply double-click `english_tts_gui.exe` and use the graphical interface with speaker selection.

### Speed Values
- `0.5` - Very slow
- `0.7` - Slower than normal
- `1.0` - Normal speed (default)
- `1.3` - Faster than normal
- `1.5` - Fast
- `2.0` - Very fast

## Example

1. Create a text file named `korean_sample.txt` with content:
   ```
   안녕하세요. 저는 한국어 텍스트를 음성으로 변환하는 프로그램입니다.
   ```

2. Convert to speech:
   ```
   korean_tts.exe korean_sample.txt korean_output.wav 1.2
   ```

3. Play the generated `korean_output.wav` file with any media player

## Troubleshooting

### Error: "Python is not installed"
- Download and install Python from https://python.org
- Make sure to check "Add Python to PATH" during installation

### Error: "Missing dependencies"
- Run `install_dependencies.bat` as administrator
- Or manually install with: `pip install melo-tts librosa soundfile numpy`

### Error: "No module named 'melo'"
- Make sure you've installed the dependencies correctly
- Try: `pip install melo-tts`

## File Information

- `korean_tts_windows.py` - Source code for the command-line converter
- `korean_tts_gui.py` - Source code for the Korean graphical interface
- `english_tts_gui.py` - Source code for the English graphical interface with speaker selection
- `build_windows_exe.bat` - Script to build Windows executables
- `install_dependencies.bat` - Script to install dependencies
- `korean_tts.spec` - PyInstaller configuration file

## License

This software uses MeloTTS which is under MIT License.