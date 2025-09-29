#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Japanese TTS Converter
Uses gTTS for native Japanese pronunciation as the primary method
"""

import sys
import os

def convert_japanese_tts(input_file, output_file, speed=1.0):
    """Convert Japanese text to speech with native pronunciation using gTTS"""
    # Read text from file first
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    if not text:
        raise ValueError("Input file is empty")
    
    try:
        print(f"Converting Japanese text to speech with native pronunciation...")
        print(f"Speed: {speed}x")
        
        # Use gTTS for Japanese as it provides the most natural pronunciation
        from gtts import gTTS
        
        # For Japanese, we use 'ja' language code
        # Note: gTTS doesn't have precise speed control, but slow=True makes it slower
        slow = speed < 1.0
        tts = gTTS(text=text, lang='ja', slow=slow)
        
        # Convert to speech
        tts.save(output_file)
        print(f"Audio saved to: {output_file} (using gTTS for native Japanese pronunciation)")
        
        return True
        
    except ImportError as e:
        print(f"gTTS not available: {e}")
        print("Please install gTTS: pip install gTTS")
        return False
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    # Handle command line arguments
    if len(sys.argv) < 3:
        print("Japanese TTS Converter")
        print("=" * 30)
        print("Usage: japanese_tts.py <input_text_file> <output_audio_file> [speed]")
        print("Example: japanese_tts.py japanese_test.txt output.wav 1.5")
        print("\nNote: This script uses gTTS for the most natural Japanese pronunciation")
        print("\nSpeed values:")
        print("  0.5 - Very slow")
        print("  1.0 - Normal (default)")
        print("  1.5 - Fast")
        print("  2.0 - Very fast")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    
    print("Japanese TTS Converter")
    print("=" * 30)
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"Speed: {speed}x")
    print("-" * 30)
    
    if convert_japanese_tts(input_file, output_file, speed):
        print("\n✓ Conversion completed successfully!")
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"Output file size: {file_size:,} bytes")
    else:
        print("\n✗ Conversion failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()