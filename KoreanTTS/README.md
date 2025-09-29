# Multilingual TTS System

This project provides text-to-speech conversion capabilities for multiple languages including Korean, Chinese, English, German, French, Japanese, and Spanish.

## Project Structure

The project is organized by language for better maintainability:

- `chinese/` - Chinese TTS implementation
- `english/` - English TTS implementation
- `german/` - German TTS implementation
- `french/` - French TTS implementation
- `japanese/` - Japanese TTS implementation
- `korean/` - Korean TTS implementation
- `spanish/` - Spanish TTS implementation
- `input/` - Input text files
- `voice/` - Generated audio files
- `doc/` - Documentation

## Usage

Each language directory contains its own TTS script. To convert text to speech:

```bash
# For Chinese
cd chinese && python3 tts.py ../input/ch0928.txt ../voice/ch0928.wav 1.0

# For English
cd english && python3 tts.py ../input/en0928.txt ../voice/en0928.wav 1.0 EN-US

# For German
cd german && python3 tts.py ../input/dc0928.txt ../voice/dc0928.wav 1.0

# For French
cd french && python3 tts.py ../input/fr0928.txt ../voice/fr0928.wav 1.0

# For Japanese
cd japanese && python3 tts.py ../input/jp0928.txt ../voice/jp0928.wav 1.0

# For Korean
cd korean && python3 tts.py ../input/kr0928.txt ../voice/kr0928.wav 1.0

# For Spanish
cd spanish && python3 tts.py ../input/sp0928.txt ../voice/sp0928.wav 1.0
```

Refer to each language directory's README.md for specific usage instructions.

## Features

- Converts text to natural-sounding speech
- Supports multiple languages
- Adjustable speech speed (0.5x to 2.0x)
- Simple command-line interface
- Graphical user interface (GUI) available
- Fallback to gTTS when MeloTTS is not available
- Windows executable available

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

### Option 1: Use Pre-built Windows Executable (Easiest)

1. Download the pre-built `korean_tts.exe` file
2. Create a text file with Korean content
3. Run from Command Prompt:
   ```
   korean_tts.exe input.txt output.wav 1.5
   ```

### Option 2: Run from Source

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

This will install:
- `melo-tts`: The main TTS library with Korean support
- `librosa`: For audio processing
- `soundfile`: For reading/writing audio files
- `numpy`: For numerical computations
- `gTTS`: Fallback TTS library

## Usage

### Basic usage with patched MeloTTS (recommended for proper speed control)

```bash
python patched_korean_tts.py input.txt output.wav 1.5
```

This will convert `input.txt` to `output.wav` with 1.5x speed.

### GUI usage (graphical interface)

```bash
python korean_tts_gui.py
```

This will open a graphical interface for easy text-to-speech conversion with speed control.

### Windows Executable Usage

```cmd
korean_tts.exe input.txt output.wav 1.5
```

### Specify different speeds

```bash
# Slow speech (0.7x speed)
python patched_korean_tts.py input.txt slow_output.wav 0.7

# Normal speech (1.0x speed)
python patched_korean_tts.py input.txt normal_output.wav 1.0

# Fast speech (1.5x speed)
python patched_korean_tts.py input.txt fast_output.wav 1.5

# Very fast speech (2.0x speed)
python patched_korean_tts.py input.txt very_fast_output.wav 2.0
```

### Universal approach (tries MeloTTS first, falls back to gTTS)

```bash
python universal_korean_tts.py input.txt
```

### Alternative approaches

1. **Using gTTS directly** (fallback option with approximate speed control):
   ```bash
   python korean_tts_gTTS.py input.txt --speed 0.8
   ```

2. **Using MeloTTS command-line tool** (if working):
   ```bash
   /Users/zing1977gmail.com/Library/Python/3.9/bin/melotts -f -l KR -s 1.2 input.txt output.wav
   ```

## Speed Control Details

The patched Korean TTS solution provides precise speed control:

- **0.5x**: Half speed (much slower)
- **0.7x**: Slower than normal
- **1.0x**: Normal speed (default)
- **1.3x**: Faster than normal
- **1.5x**: 1.5x speed (faster)
- **2.0x**: Double speed (much faster)

Note: For gTTS (fallback option), speed control is approximate:
- Speed < 1.0: Slower speech
- Speed >= 1.0: Normal speech

## Example with Korean text

Create a text file (e.g., `korean_sample.txt`) with Korean content:

```
안녕하세요. 저는 한국어를 구사할 수 있습니다. 이 프로그램은 텍스트를 음성으로 변환해줍니다.
```

Then convert it to speech:

```bash
python patched_korean_tts.py korean_sample.txt korean_output.wav 1.2
```

## Building Windows Executable

To build the Windows executable from source:

1. Install PyInstaller:
   ```bash
   pip install PyInstaller
   ```

2. Use the build script:
   ```bash
   build_windows_exe.bat
   ```

3. Two executables will be created in the `dist` folder:
   - `korean_tts_cli.exe` - Command-line interface
   - `korean_tts_gui.exe` - Graphical user interface

### Manual build options:

- Command-line version: `pyinstaller --onefile --console korean_tts_windows.py --name korean_tts_cli`
- GUI version: `pyinstaller --onefile --windowed korean_tts_gui.py --name korean_tts_gui`

## Supported Languages

While this tool is optimized for Korean, MeloTTS also supports:
- English (American, British, Indian, Australian, Default)
- Spanish
- French
- Chinese
- Japanese

### Language Codes
- Korean: `KR`
- English: `EN`
- Spanish: `ES`
- French: `FR`
- Chinese: `ZH`
- Japanese: `JP`

Note: This system provides native pronunciation for all supported languages:

- **Korean, Chinese, French, Spanish**: High-quality output using MeloTTS
- **English, Japanese**: Native pronunciation using gTTS (with MeloTTS fallback when available)

The system automatically uses the best available method for each language, ensuring native-like pronunciation rather than how a Korean speaker might read the text.

## Troubleshooting

### No module named 'melo'

Make sure you've installed the dependencies:

```bash
pip install -r requirements.txt
```

### Japanese dependency errors

If you encounter Japanese-related import errors, use the patched Korean TTS script:
```bash
python patched_korean_tts.py input.txt output.wav 1.0
```

### CUDA out of memory

If you encounter memory issues, try using CPU instead.

### Audio quality issues

- Ensure your input text file is saved in UTF-8 encoding
- For best results, avoid extremely long sentences without punctuation

## License

This project uses MeloTTS which is under MIT License.