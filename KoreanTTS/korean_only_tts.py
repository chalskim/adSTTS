#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Korean-only TTS script that bypasses Japanese dependency issues
"""

import os
import sys

def convert_korean_with_melotts(input_file, output_file, speed=1.0):
    """Convert Korean text to speech using MeloTTS with workaround for Japanese issues"""
    try:
        # Set environment variables to minimize Japanese imports
        os.environ['MELO_LANG'] = 'KR'
        os.environ['LANGUAGE'] = 'ko'
        
        # Try to import only what we need
        from melo.api import TTS
        print("✓ MeloTTS imported successfully")
        
        # Check if input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Read text from file
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        if not text:
            raise ValueError("Input file is empty")
        
        print(f"Converting text: {text[:50]}...")
        print(f"Speed setting: {speed}x")
        
        # Initialize Korean TTS with explicit language
        tts = TTS(language='KR')
        print("✓ Korean TTS model loaded")
        
        # Use default Korean speaker
        speaker = 'KR'
        print(f"Using speaker: {speaker}")
        
        # Convert to speech with speed control
        tts.tts_to_file(text, speaker, output_file, speed=speed)
        print(f"✓ Audio saved to: {output_file}")
        
        return True
        
    except ImportError as e:
        print(f"Import error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 korean_only_tts.py <input_text_file> [output_audio_file] [--speed SPEED]")
        print("Example: python3 korean_only_tts.py sample_korean.txt output.wav --speed 1.5")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = "output_korean.wav"
    speed = 1.0
    
    # Parse arguments
    if len(sys.argv) > 2:
        for i, arg in enumerate(sys.argv[2:], 2):
            if arg == "--speed" and i + 1 < len(sys.argv):
                try:
                    speed = float(sys.argv[i + 1])
                except ValueError:
                    print("Invalid speed value. Using default 1.0")
                    speed = 1.0
                break
            elif not arg.startswith("--"):
                output_file = arg
    
    print(f"Korean TTS Conversion")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"Speed: {speed}x")
    print("-" * 30)
    
    if convert_korean_with_melotts(input_file, output_file, speed):
        print("\n✓ Conversion completed successfully!")
        file_size = os.path.getsize(output_file)
        print(f"Output file size: {file_size} bytes")
    else:
        print("\n✗ Conversion failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()