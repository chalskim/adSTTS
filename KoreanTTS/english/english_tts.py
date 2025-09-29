#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
English TTS Converter using patched MeloTTS
Provides native English pronunciation with multiple speaker options
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

# Set environment variables for English TTS
os.environ['MELO_LANG'] = 'EN'
os.environ['LANGUAGE'] = 'en'

def convert_english_tts(input_file, output_file, speed=1.0, speaker='EN-US'):
    """Convert English text to speech with speed control and speaker selection"""
    # Read text from file first
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    if not text:
        raise ValueError("Input file is empty")
    
    # Try MeloTTS first
    try:
        # Import MeloTTS after patching
        from melo.api import TTS
        
        print(f"Converting English text to speech with native pronunciation...")
        print(f"Speed: {speed}x")
        print(f"Speaker: {speaker}")
        
        # Initialize English TTS
        tts = TTS(language='EN')
        
        # Get speaker ID from the model
        try:
            # Access speaker IDs (suppressing linter warning)
            speaker_ids = tts.hps.data.spk2id  # type: ignore
            print(f"Available English speakers: {list(speaker_ids.keys())}")
            
            if speaker not in speaker_ids:
                # Try to find a similar speaker
                speaker_options = [s for s in speaker_ids.keys() if speaker.split('-')[0].upper() in s.upper()]
                if speaker_options:
                    speaker = speaker_options[0]
                else:
                    speaker = list(speaker_ids.keys())[0]  # Get first speaker as fallback
                print(f"Speaker adjusted to: {speaker}")
            
            speaker_id = speaker_ids[speaker]      # Get the numeric ID
        except Exception as e:
            print(f"Speaker selection error: {e}")
            # Fallback to string speaker ID
            speaker_id = speaker
        
        # Convert to speech
        tts.tts_to_file(text, speaker_id, output_file, speed=speed)
        print(f"Audio saved to: {output_file} (using MeloTTS)")
        
        return True
        
    except Exception as e:
        # This will catch both ImportError and other MeloTTS errors
        print(f"MeloTTS not available or encountered an error: {e}")
        print("Falling back to gTTS for English...")
        try:
            from gtts import gTTS
            # For gTTS, we use 'en' for English regardless of specific variant
            slow = speed < 1.0
            tts = gTTS(text=text, lang='en', slow=slow)
            tts.save(output_file)
            print(f"Audio saved to: {output_file} (using gTTS)")
            return True
        except Exception as gTTS_error:
            print(f"gTTS error: {gTTS_error}")
            return False

def main():
    # Handle command line arguments
    if len(sys.argv) < 3:
        print("English TTS Converter")
        print("=" * 30)
        print("Usage: english_tts.py <input_text_file> <output_audio_file> [speed] [speaker]")
        print("Example: english_tts.py english_test.txt output.wav 1.5 EN-US")
        print("\nAvailable speakers (when using MeloTTS):")
        print("  EN-US      - American English")
        print("  EN-BR      - British English") 
        print("  EN_INDIA   - Indian English")
        print("  EN-AU      - Australian English")
        print("  EN-Default - Default English")
        print("\nSpeed values:")
        print("  0.5 - Very slow")
        print("  1.0 - Normal (default)")
        print("  1.5 - Fast")
        print("  2.0 - Very fast")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    speaker = sys.argv[4] if len(sys.argv) > 4 else 'EN-US'
    
    print("English TTS Converter")
    print("=" * 30)
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"Speed: {speed}x")
    print(f"Speaker: {speaker}")
    print("-" * 30)
    
    if convert_english_tts(input_file, output_file, speed, speaker):
        print("\n✓ Conversion completed successfully!")
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"Output file size: {file_size:,} bytes")
    else:
        print("\n✗ Conversion failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()