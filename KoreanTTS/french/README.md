# French TTS

This directory contains the French text-to-speech conversion scripts.

## Usage

```bash
python3 tts.py <input_text_file> <output_audio_file> [speed]
```

Example:
```bash
python3 tts.py ../input/fr0928.txt ../voice/fr0928.wav 1.0
```

## Files
- `french_tts.py`: Main French TTS implementation
- `tts.py`: Wrapper script for easy execution