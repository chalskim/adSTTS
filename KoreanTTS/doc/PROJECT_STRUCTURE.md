# Project Structure

This document explains the files in the Korean TTS Converter project.

## Language-Specific Directories

The project is now organized by language for better maintainability:

### [chinese/](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/chinese)
- **[chinese_tts.py](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/chinese/chinese_tts.py)** - Chinese TTS converter with speed control using MeloTTS
- **tts.py** - Wrapper script for easy execution
- **README.md** - Usage instructions for Chinese TTS

### [english/](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/english)
- **[english_tts.py](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/english/english_tts.py)** - English TTS converter with native pronunciation using gTTS and speaker selection
- **[english_tts_gui.py](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/english/english_tts_gui.py)** - English TTS GUI with speaker selection and speed control
- **tts.py** - Wrapper script for easy execution
- **README.md** - Usage instructions for English TTS

### [german/](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/german)
- **[german_tts.py](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/german/german_tts.py)** - German TTS converter with native pronunciation using gTTS
- **tts.py** - Wrapper script for easy execution
- **README.md** - Usage instructions for German TTS

### [french/](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/french)
- **[french_tts.py](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/french/french_tts.py)** - French TTS converter with native pronunciation using gTTS
- **tts.py** - Wrapper script for easy execution
- **README.md** - Usage instructions for French TTS

### [japanese/](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/japanese)
- **[japanese_tts.py](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/japanese/japanese_tts.py)** - Japanese TTS converter with native pronunciation using gTTS
- **tts.py** - Wrapper script for easy execution
- **README.md** - Usage instructions for Japanese TTS

### [korean/](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/korean)
- **[patched_korean_tts.py](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/korean/patched_korean_tts.py)** - Patched version that works around Japanese dependency issues
- **tts.py** - Wrapper script for easy execution
- **README.md** - Usage instructions for Korean TTS

### [spanish/](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/spanish)
- **[spanish_tts.py](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/spanish/spanish_tts.py)** - Spanish TTS converter with native pronunciation using gTTS
- **tts.py** - Wrapper script for easy execution
- **README.md** - Usage instructions for Spanish TTS

## Main Files

1. **[text_to_speech.py](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/text_to_speech.py)** - The main script that converts text files to WAV audio files using MeloTTS
2. **[universal_korean_tts.py](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/universal_korean_tts.py)** - Universal script that tries MeloTTS first and falls back to gTTS
3. **[korean_tts_gTTS.py](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/korean_tts_gTTS.py)** - Script that uses gTTS directly for Korean TTS
4. **[korean_tts_windows.py](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/korean_tts_windows.py)** - Windows-optimized script for building executable
5. **[korean_tts_gui.py](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/korean_tts_gui.py)** - Graphical user interface for easy TTS conversion
6. **[requirements.txt](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/requirements.txt)** - Lists all required Python packages
7. **[sample_korean.txt](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/sample_korean.txt)** - Sample Korean text for testing

## Setup Scripts

1. **[setup.sh](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/setup.sh)** - Setup script for macOS/Linux
2. **[setup.bat](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/setup.bat)** - Setup script for Windows
3. **[setup_and_test.py](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/setup_and_test.py)** - Automated setup and test script
4. **[install_dependencies.bat](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/install_dependencies.bat)** - Windows dependency installer
5. **[build_windows_exe.bat](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/build_windows_exe.bat)** - Windows executable builder
6. **[setup_windows_exe.py](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/setup_windows_exe.py)** - Python setup script for Windows executable

## Input and Output

1. **[input/](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/input)** - Directory containing input text files organized by language
2. **[voice/](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/voice)** - Directory for generated audio files (as per project guidelines)

## Documentation

1. **[README.md](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/README.md)** - Main project documentation with updated structure
2. **[TROUBLESHOOTING.md](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/TROUBLESHOOTING.md)** - Troubleshooting guide for common issues
3. **[PROJECT_STRUCTURE.md](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/PROJECT_STRUCTURE.md)** - This document
4. **[WINDOWS_USAGE.md](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/WINDOWS_USAGE.md)** - Windows-specific usage guide

## PyInstaller Files

1. **[korean_tts.spec](file:///Users/zing1977gmail.com/src/TTStest/KoreanTTS/korean_tts.spec)** - PyInstaller configuration file

## How to Use

1. Run the setup script for your operating system:
   - macOS/Linux: `./setup.sh`
   - Windows: `setup.bat`
   - Or run: `python setup_and_test.py`

2. For language-specific usage, navigate to the language directory:
   ```bash
   cd chinese && python3 tts.py ../input/ch0928.txt ../voice/ch0928.wav 1.0
   ```

3. For Windows executable:
   - Run: `python setup_windows_exe.py`
   - Or use batch files: `install_dependencies.bat` and `build_windows_exe.bat`

4. Use the universal script for best results:
   ```bash
   python universal_korean_tts.py input.txt --speed 1.2
   ```

5. For Windows executable:
   ```cmd
   dist/korean_tts.exe input.txt output.wav 1.5
   ```