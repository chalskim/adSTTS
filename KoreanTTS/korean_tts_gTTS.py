#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Korean TTS using gTTS (Google Text-to-Speech)
"""

import os
import sys
import argparse
from gtts import gTTS

def convert_korean_text_to_speech(input_file, output_file, speed=1.0):
    """
    Convert Korean text file to WAV audio file using gTTS
    
    Args:
        input_file (str): Path to the input text file
        output_file (str): Path to the output WAV file
        speed (float): Speech speed (gTTS only supports slow=True/False)
    """
    
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Read text from file
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    if not text:
        raise ValueError("Input file is empty")
    
    print(f"Converting text to speech: {text[:50]}...")
    
    # Create gTTS object for Korean
    # Note: gTTS doesn't have precise speed control, but slow=True makes it slower
    slow = speed < 1.0
    tts = gTTS(text=text, lang='ko', slow=slow)
    
    # Save to file
    tts.save(output_file)
    print(f"Audio saved to: {output_file}")
    print(f"Speed setting: {'slow' if slow else 'normal'} (approx. {speed}x)")

def main():
    parser = argparse.ArgumentParser(description="Convert Korean text file to speech (WAV) using gTTS")
    parser.add_argument("input", help="Input text file path")
    parser.add_argument("-o", "--output", help="Output WAV file path (default: input.wav)")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed (gTTS: <1.0 for slow, >=1.0 for normal)")
    
    args = parser.parse_args()
    
    # Set default output file name if not provided
    if not args.output:
        base_name = os.path.splitext(args.input)[0]
        args.output = f"{base_name}.wav"
    
    try:
        convert_korean_text_to_speech(args.input, args.output, args.speed)
        print("Conversion completed successfully!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()