# Japanese TTS

This directory contains the Japanese text-to-speech conversion scripts.

## Usage

```bash
python3 tts.py <input_text_file> <output_audio_file> [speed]
```

Example:
```bash
python3 tts.py ../input/jp0928.txt ../voice/jp0928.wav 1.0
```

## Files
- `japanese_tts.py`: Main Japanese TTS implementation
- `tts.py`: Wrapper script for easy execution