# Spanish TTS

This directory contains the Spanish text-to-speech conversion scripts.

## Usage

```bash
python3 tts.py <input_text_file> <output_audio_file> [speed]
```

Example:
```bash
python3 tts.py ../input/sp0928.txt ../voice/sp0928.wav 1.0
```

## Files
- `spanish_tts.py`: Main Spanish TTS implementation
- `tts.py`: Wrapper script for easy execution