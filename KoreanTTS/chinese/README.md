# Chinese TTS

This directory contains the Chinese text-to-speech conversion scripts.

## Usage

```bash
python3 tts.py <input_text_file> <output_audio_file> [speed]
```

Example:
```bash
python3 tts.py ../input/ch0928.txt ../voice/ch0928.wav 1.0
```

## Files
- `chinese_tts.py`: Main Chinese TTS implementation
- `tts.py`: Wrapper script for easy execution