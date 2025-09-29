#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multilingual TTS Converter
This script allows you to convert text to speech in multiple languages.
"""

import sys
import os

def show_usage():
    print("Multilingual TTS Converter")
    print("=" * 30)
    print("Usage: python3 tts.py <language> <input_file> <output_file> [speed] [speaker]")
    print()
    print("Languages supported:")
    print("  chinese  - Chinese text-to-speech")
    print("  english  - English text-to-speech")
    print("  french   - French text-to-speech")
    print("  german   - German text-to-speech")
    print("  japanese - Japanese text-to-speech")
    print("  korean   - Korean text-to-speech")
    print("  spanish  - Spanish text-to-speech")
    print()
    print("Examples:")
    print("  python3 tts.py korean input/kr0928.txt voice/kr0928.wav 1.0")
    print("  python3 tts.py english input/en0928.txt voice/en0928.wav 1.0 EN-US")
    print("  python3 tts.py chinese input/ch0928.txt voice/ch0928.wav 1.2")

def main():
    if len(sys.argv) < 4:
        show_usage()
        sys.exit(1)
    
    language = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    speed = sys.argv[4] if len(sys.argv) > 4 else "1.0"
    speaker = sys.argv[5] if len(sys.argv) > 5 else ""
    
    # Validate language
    supported_languages = ["chinese", "english", "french", "german", "japanese", "korean", "spanish"]
    if language not in supported_languages:
        print(f"Error: Unsupported language '{language}'")
        print(f"Supported languages: {', '.join(supported_languages)}")
        sys.exit(1)
    
    # Validate input file
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Build command
    if language == "english" and speaker:
        cmd = f"cd {language} && python3 tts.py ../{input_file} ../{output_file} {speed} {speaker}"
    else:
        cmd = f"cd {language} && python3 tts.py ../{input_file} ../{output_file} {speed}"
    
    print(f"Converting {language} text to speech...")
    print(f"Command: {cmd}")
    
    # Execute command
    result = os.system(cmd)
    
    if result == 0:
        print(f"\n✓ Conversion completed successfully!")
        print(f"Audio saved to: {output_file}")
    else:
        print(f"\n✗ Conversion failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()