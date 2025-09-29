#!/usr/bin/env python3
"""
Test script for Whisper STT functionality
"""

import whisper
import os
import numpy as np
import soundfile as sf

def test_whisper_installation():
    """Test if Whisper is installed and working correctly"""
    try:
        # Try to load the tiny model (fastest for testing)
        print("Loading tiny Whisper model...")
        model = whisper.load_model("tiny")
        print("✓ Model loaded successfully")
        
        # Testing transcription capability with our example file
        print("Testing transcription capability...")
        
        # Check if example.wav exists, if not create it
        if not os.path.exists("example.wav"):
            print("Creating example.wav file...")
            sample_rate = 16000
            duration = 3.0
            silent_audio = np.zeros(int(sample_rate * duration))
            sf.write("example.wav", silent_audio, sample_rate)
        
        # Try to transcribe the example audio
        result = model.transcribe("example.wav")
        
        print("✓ Transcription test completed")
        print("Whisper installation is working correctly!")
        print(f"Transcribed text: {result['text']}")
        return True
        
    except ImportError as e:
        print(f"⚠ Missing dependency: {e}")
        print("Please install missing packages: pip install soundfile numpy")
        return False
    except Exception as e:
        print(f"✗ Error testing Whisper installation: {e}")
        if "ffmpeg" in str(e).lower():
            print("\nThis error is likely due to missing ffmpeg.")
            print("Please install ffmpeg:")
            print("- On macOS with Homebrew: brew install ffmpeg")
            print("- On Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg")
            print("- On Windows: Download from https://www.gyan.dev/ffmpeg/builds/")
        return False

if __name__ == "__main__":
    print("Testing OpenAI Whisper Installation")
    print("=" * 40)
    success = test_whisper_installation()
    
    if success:
        print("\nYou're ready to use Whisper for speech-to-text conversion!")
        print("Run: python whisper_stt.py <audio_file_path>")
    else:
        print("\nThere was an issue with the installation.")
        print("Please check the error message above.")