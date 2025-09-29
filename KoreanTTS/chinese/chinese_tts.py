#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chinese TTS Converter using patched MeloTTS
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

# Set environment variables for Chinese TTS
os.environ['MELO_LANG'] = 'ZH'
os.environ['LANGUAGE'] = 'zh'

def convert_chinese_tts(input_file, output_file, speed=1.0):
    """Convert Chinese text to speech with speed control"""
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
        
        print(f"Converting Chinese text to speech...")
        print(f"Speed: {speed}x")
        
        # Initialize Chinese TTS
        tts = TTS(language='ZH')
        
        # Get speaker ID from the model
        try:
            # Access speaker IDs (suppressing linter warning)
            speaker_ids = tts.hps.data.spk2id  # type: ignore
            speaker = list(speaker_ids.keys())[0]  # Get first speaker
            speaker_id = speaker_ids[speaker]      # Get the numeric ID
        except:
            # Fallback to string speaker ID
            speaker = 'ZH'
            speaker_id = 0
        
        # Convert to speech
        tts.tts_to_file(text, speaker_id, output_file, speed=speed)
        print(f"Audio saved to: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"Error with MeloTTS: {e}")
        print("Falling back to gTTS for Chinese...")
        try:
            from gtts import gTTS
            # Read text from file
            with open(input_file, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            
            # Create gTTS object for Chinese
            # Note: gTTS doesn't have precise speed control, but slow=True makes it slower
            slow = speed < 1.0
            tts = gTTS(text=text, lang='zh', slow=slow)
            
            # Save to file
            tts.save(output_file)
            print(f"Audio saved to: {output_file} (using gTTS)")
            return True
        except Exception as gTTS_error:
            print(f"gTTS error: {gTTS_error}")
            return False

def main():
    # Handle command line arguments
    if len(sys.argv) < 3:
        print("Chinese TTS Converter")
        print("=" * 20)
        print("Usage: chinese_tts.py <input_text_file> <output_audio_file> [speed]")
        print("Example: chinese_tts.py chinese_test.txt output.wav 1.5")
        print("\nSpeed values:")
        print("  0.5 - Very slow")
        print("  1.0 - Normal (default)")
        print("  1.5 - Fast")
        print("  2.0 - Very fast")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    
    print("Chinese TTS Converter")
    print("=" * 20)
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"Speed: {speed}x")
    print("-" * 20)
    
    if convert_chinese_tts(input_file, output_file, speed):
        print("\nConversion completed successfully!")
        file_size = os.path.getsize(output_file)
        print(f"Output file size: {file_size:,} bytes")
    else:
        print("\nConversion failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()