# Korean TTS

This directory contains the Korean text-to-speech conversion scripts.

## Usage

```bash
python3 tts.py <input_text_file> <output_audio_file> [speed]
```

Example:
```bash
python3 tts.py ../input/kr0928.txt ../voice/kr0928.wav 1.0
```

## Files
- `patched_korean_tts.py`: Main Korean TTS implementation with Japanese dependency patch
- `tts.py`: Wrapper script for easy execution