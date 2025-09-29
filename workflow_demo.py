#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete workflow demonstration: Whisper transcription -> Korean TTS
"""

import os
import sys
import subprocess

def demo_workflow():
    """Demonstrate the complete workflow from Whisper to Korean TTS"""
    print("Complete Workflow Demo: Whisper -> Korean TTS")
    print("=" * 50)
    
    # Step 1: Show available Whisper transcriptions
    whisper_output_dir = "OpenAI Whisper/output"
    if os.path.exists(whisper_output_dir):
        txt_files = [f for f in os.listdir(whisper_output_dir) if f.endswith('.txt')]
        if txt_files:
            print("Available Whisper transcriptions:")
            for i, f in enumerate(txt_files, 1):
                print(f"  {i}. {f}")
            
            # Use the first transcription file for demo
            transcription_file = os.path.join(whisper_output_dir, txt_files[0])
            print(f"\nUsing transcription: {txt_files[0]}")
            
            # Show first few lines of the transcription
            with open(transcription_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                print(f"\nTranscription content (first 100 chars):")
                print(f"  {content[:100]}...")
        else:
            print("No transcription files found in Whisper output directory")
            return
    else:
        print("Whisper output directory not found")
        return
    
    # Step 2: Convert transcription to Korean speech
    print("\n" + "-" * 30)
    print("Step 2: Converting to Korean speech")
    
    # Create output filename
    base_name = os.path.splitext(os.path.basename(transcription_file))[0]
    output_audio = f"KoreanTTS/voice/{base_name}.wav"
    
    # Ensure voice directory exists
    os.makedirs("KoreanTTS/voice", exist_ok=True)
    
    # Convert using Korean TTS (need to run from the adSTTS directory)
    cmd = f"cd KoreanTTS && python3 tts.py korean '../{transcription_file}' '{base_name}.wav' 1.0"
    print(f"Command: {cmd}")
    
    result = os.system(cmd)
    if result == 0:
        if os.path.exists(f"KoreanTTS/voice/{base_name}.wav"):
            size = os.path.getsize(f"KoreanTTS/voice/{base_name}.wav")
            print(f"✓ Success! Audio saved to: {output_audio} ({size} bytes)")
        else:
            print(f"✓ Success! Audio saved to: {output_audio}")
    else:
        print("✗ Failed to convert text to speech!")
        return
    
    print("\n" + "=" * 50)
    print("Workflow completed successfully!")
    print("\nTo listen to the generated audio file, you can use:")
    print(f"  afplay {output_audio}  # On macOS")
    print(f"  aplay {output_audio}   # On Linux")
    print(f"  start {output_audio}   # On Windows")

if __name__ == "__main__":
    # Make sure we're in the right directory (adSTTS root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    demo_workflow()