# German TTS

This directory contains the German text-to-speech conversion scripts.

## Usage

```bash
python3 tts.py <input_text_file> <output_audio_file> [speed]
```

Example:
```bash
python3 tts.py ../input/dc0928.txt ../voice/dc0928.wav 1.0
```

## Files
- `german_tts.py`: Main German TTS implementation
- `tts.py`: Wrapper script for easy execution