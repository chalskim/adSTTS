#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Korean TTS Converter - Windows Executable Version
Converts Korean text files to WAV audio with speed control
"""

import sys
import os
from types import ModuleType

# Create a comprehensive mock for the Japanese module to avoid import errors
class MockJapaneseModule(ModuleType):
    """Mock Japanese module to prevent import errors"""
    def __init__(self):
        super().__init__('japanese')
    
    def distribute_phone(self, *args, **kwargs):
        # Return empty list as fallback
        return []

# Monkey patch the Japanese import to avoid dependency issues
sys.modules['melo.text.japanese'] = MockJapaneseModule()

# Set environment variables for Korean TTS
os.environ['MELO_LANG'] = 'KR'
os.environ['LANGUAGE'] = 'ko'

def convert_korean_tts(input_file, output_file, speed=1.0):
    """Convert Korean text to speech with speed control"""
    try:
        # Import MeloTTS after patching
        from melo.api import TTS
        
        # Check if input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Read text from file
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        if not text:
            raise ValueError("Input file is empty")
        
        print(f"Converting Korean text to speech...")
        print(f"Speed: {speed}x")
        
        # Initialize Korean TTS
        tts = TTS(language='KR')
        
        # Get speaker ID from the model
        try:
            speaker_ids = tts.hps.data.spk2id
            speaker = list(speaker_ids.keys())[0]  # Get first speaker
            speaker_id = speaker_ids[speaker]      # Get the numeric ID
        except:
            # Fallback to string speaker ID
            speaker = 'KR'
            speaker_id = 0
        
        # Convert to speech
        tts.tts_to_file(text, speaker_id, output_file, speed=speed)
        print(f"Audio saved to: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    # Handle command line arguments
    if len(sys.argv) < 3:
        print("Korean TTS Converter")
        print("=" * 20)
        print("Usage: korean_tts.exe <input_text_file> <output_audio_file> [speed]")
        print("Example: korean_tts.exe sample.txt output.wav 1.5")
        print("\nSpeed values:")
        print("  0.5 - Very slow")
        print("  1.0 - Normal (default)")
        print("  1.5 - Fast")
        print("  2.0 - Very fast")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    
    print("Korean TTS Converter")
    print("=" * 20)
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"Speed: {speed}x")
    print("-" * 20)
    
    if convert_korean_tts(input_file, output_file, speed):
        print("\nConversion completed successfully!")
        file_size = os.path.getsize(output_file)
        print(f"Output file size: {file_size:,} bytes")
    else:
        print("\nConversion failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()