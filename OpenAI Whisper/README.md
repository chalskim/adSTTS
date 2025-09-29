# OpenAI Whisper Speech-to-Text Converter

This project uses OpenAI's Whisper model to convert speech in audio files to text, with optional noise reduction capabilities.

## Prerequisites

- Python 3.x
- pip (Python package installer)
- ffmpeg (for audio processing)
- PortAudio (for real-time audio capture)

## Installation

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Install system dependencies:
   - On macOS with Homebrew: 
     ```
     brew install ffmpeg portaudio
     ```
   - On Ubuntu/Debian: 
     ```
     sudo apt update && sudo apt install ffmpeg portaudio19-dev python3-pyaudio
     ```
   - On Windows: 
     Download from https://www.gyan.dev/ffmpeg/builds/ and install PyAudio with:
     ```
     pip install PyAudio
     ```

## Usage

### File-based Transcription
Run the script with the path to your audio file:
```
python whisper_stt.py <audio_file_path> [model_size]
```

### Automatic Large File Handling
Files are automatically processed in chunks if they meet either criterion:
- Longer than 30 minutes, OR
- Larger than 100 MB

This prevents memory issues with large files. See [longVDO.md](longVDO.md) for details.

### Output Directory
Transcriptions are automatically saved to an `output` folder with the same base name as the input file.

### File-based Noise Reduction
Reduce noise in audio files before transcription for better accuracy:
```
python file_noise_reduction.py
```

### Parameters:
- `audio_file_path`: Path to the audio file you want to transcribe
- `model_size` (optional): Size of the Whisper model to use. Options are:
  - `tiny` - Fastest, least accurate
  - `base` - Good balance of speed and accuracy (default)
  - `small` - More accurate, slower
  - `medium` - Accurate, slower
  - `large` - Most accurate, slowest

### Example:
```
python3 whisper_stt.py my_audio.mp3
python3 whisper_stt.py my_audio.mp3 large
```

### Real-time Transcription (Experimental)
For real-time speech-to-text from your microphone:
```
python3 real_time_stt.py
```

### Enhanced Real-time Transcription with Noise Reduction
For real-time speech-to-text with RNNoise-like noise reduction and WebRTC VAD:
```
python3 real_time_stt_enhanced.py
```

Note: Real-time transcription requires additional system dependencies (PortAudio) and may have installation challenges on some systems.

The transcribed text will be printed to the console and saved to the `output` folder with a filename matching the audio file but with `_transcription.txt` appended.

## Supported Audio Formats

Whisper supports various audio formats including:
- MP3
- WAV
- M4A
- FLAC
- And more

## Models

Different models offer trade-offs between speed and accuracy:
- `tiny`: ~32x speed, ~1GB VRAM
- `base`: ~16x speed, ~1GB VRAM
- `small`: ~6x speed, ~2GB VRAM
- `medium`: ~2x speed, ~5GB VRAM
- `large`: 1x speed, ~10GB VRAM

The default model is `base` which provides a good balance for most use cases.

## Noise Reduction Features

### File-based Noise Reduction
- Uses the `noisereduce` library for advanced spectral noise reduction
- Particularly effective for pre-recorded audio files with consistent background noise
- Can significantly improve transcription accuracy

### Real-time Noise Reduction
- RNNoise-like spectral gating for real-time noise reduction
- WebRTC Voice Activity Detection (VAD) to reduce processing of non-speech audio
- Configurable noise reduction and VAD settings

## Large Audio File Processing

For audio files that are either:
- Longer than 30 minutes, OR
- Larger than 100 MB

The system automatically processes them in chunks to:
- Prevent memory exhaustion
- Provide progress feedback
- Maintain system responsiveness

See [longVDO.md](longVDO.md) for technical details on how chunked processing works.

## Output Organization

All transcriptions are saved in an `output` folder in the same directory as the script:
- The output folder is automatically created if it doesn't exist
- Files are named with the same base name as the input file plus `_transcription.txt`
- Example: `my_audio.mp3` → `output/my_audio_transcription.txt`

For best results, experiment with both approaches depending on your use case:
- Use file-based noise reduction for pre-recorded audio with consistent noise
- Use real-time noise reduction for live microphone input