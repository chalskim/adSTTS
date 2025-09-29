#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Korean TTS functionality using gTTS as a fallback
"""

import os
import sys

def test_korean_tts():
    """Test Korean TTS using gTTS"""
    print("Testing Korean TTS functionality...")
    print("=" * 40)
    
    # Create a test file with Korean text
    test_text = "안녕하세요. 저는 한국어를 구사할 수 있습니다. 이 프로그램은 텍스트를 음성으로 변환해줍니다."
    test_file = "test_korean_input.txt"
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_text)
    
    print(f"Created test input file: {test_file}")
    print(f"Text: {test_text}")
    
    # Test gTTS version
    print("\n1. Testing gTTS version...")
    output_file = "test_korean_gtts.wav"
    cmd = f"python3 korean_tts_gTTS.py {test_file} -o {output_file} --speed 1.0"
    print(f"Command: {cmd}")
    
    result = os.system(cmd)
    if result == 0:
        print(f"✓ gTTS version successful! Output: {output_file}")
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(f"  File size: {size} bytes")
    else:
        print("✗ gTTS version failed!")
    
    # Test the universal approach
    print("\n2. Testing universal approach...")
    output_file2 = "test_korean_universal.wav"
    cmd = f"python3 tts.py korean {test_file} {output_file2} 1.0"
    print(f"Command: {cmd}")
    
    result = os.system(cmd)
    if result == 0:
        print(f"✓ Universal approach successful! Output: {output_file2}")
        if os.path.exists(output_file2):
            size = os.path.getsize(output_file2)
            print(f"  File size: {size} bytes")
    else:
        print("✗ Universal approach failed!")
    
    # Clean up test files
    print("\nCleaning up test files...")
    for file in [test_file, output_file, output_file2]:
        if os.path.exists(file):
            os.remove(file)
            print(f"Removed: {file}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    # Make sure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    test_korean_tts()