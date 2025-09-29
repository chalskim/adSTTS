# English TTS

This directory contains the English text-to-speech conversion scripts.

## Usage

```bash
python3 tts.py <input_text_file> <output_audio_file> [speed] [speaker]
```

Example:
```bash
python3 tts.py ../input/en0928.txt ../voice/en0928.wav 1.0 EN-US
```

## Files
- `english_tts.py`: Main English TTS implementation
- `tts.py`: Wrapper script for easy execution