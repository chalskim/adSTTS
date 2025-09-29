#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch MeloTTS to avoid Japanese imports and enable Korean speed control
"""

import sys
import os
from types import ModuleType

# Create a comprehensive mock for the Japanese module
class MockJapaneseModule(ModuleType):
    """Mock Japanese module to prevent import errors"""
    def __init__(self):
        super().__init__('japanese')
    
    def distribute_phone(self, *args, **kwargs):
        # Return empty list as fallback
        return []

# Monkey patch the Japanese import
sys.modules['melo.text.japanese'] = MockJapaneseModule()

# Set environment variables
os.environ['MELO_LANG'] = 'KR'
os.environ['LANGUAGE'] = 'ko'

def convert_korean_with_patched_melotts(input_file, output_file, speed=1.0):
    """Convert Korean text to speech with patched MeloTTS"""
    try:
        # Import MeloTTS after patching
        from melo.api import TTS
        print("✓ MeloTTS imported successfully (with patch)")
        
        # Check if input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Read text from file
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        if not text:
            raise ValueError("Input file is empty")
        
        print(f"Converting text with speed {speed}x...")
        print(f"Text: {text[:50]}...")
        
        # Initialize Korean TTS
        tts = TTS(language='KR')
        print("✓ Korean TTS model loaded")
        
        # Get speaker ID from the model (like the CLI does)
        try:
            speaker_ids = tts.hps.data.spk2id
            speaker = list(speaker_ids.keys())[0]  # Get first speaker
            speaker_id = speaker_ids[speaker]      # Get the numeric ID
            print(f"Available speakers: {list(speaker_ids.keys())}")
            print(f"Using speaker: {speaker} (ID: {speaker_id})")
        except:
            # Fallback to string speaker ID
            speaker = 'KR'
            speaker_id = 0
            print(f"Using fallback speaker: {speaker}")
        
        # Convert to speech using the numeric speaker ID
        tts.tts_to_file(text, speaker_id, output_file, speed=speed)
        print(f"✓ Audio saved to: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 patched_korean_tts.py <input_text_file> <output_audio_file> [speed]")
        print("Example: python3 patched_korean_tts.py sample_korean.txt output.wav 1.5")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    
    print("Patched Korean TTS Converter")
    print("=" * 30)
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"Speed: {speed}x")
    print("-" * 30)
    
    if convert_korean_with_patched_melotts(input_file, output_file, speed):
        print("\n✓ Conversion completed successfully!")
        file_size = os.path.getsize(output_file)
        print(f"Output file size: {file_size} bytes")
    else:
        print("\n✗ Conversion failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()