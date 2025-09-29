#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demonstration of Korean TTS functionality
"""

import os
import sys

def create_sample_text():
    """Create a sample Korean text file"""
    sample_text = """안녕하세요! 이것은 한국어 텍스트 음성 변환 데모입니다.
이 프로그램은 텍스트를 자연스러운 음성으로 변환해줍니다.
다양한 속도 설정이 가능하며, 고품질의 음성을 생성할 수 있습니다.
감사합니다!"""
    
    with open("sample_korean.txt", "w", encoding="utf-8") as f:
        f.write(sample_text)
    
    return sample_text

def demo_korean_tts():
    """Demonstrate Korean TTS functionality"""
    print("Korean TTS Demonstration")
    print("=" * 50)
    
    # Create sample text
    sample_text = create_sample_text()
    print("Created sample text file: sample_korean.txt")
    print("Text content:")
    print(sample_text)
    print()
    
    # Test different speeds
    speeds = [0.7, 1.0, 1.5]
    
    for speed in speeds:
        print(f"Testing speed {speed}x...")
        output_file = f"output_speed_{str(speed).replace('.', '_')}.wav"
        
        # Use the universal approach
        cmd = f"python3 tts.py korean sample_korean.txt {output_file} {speed}"
        print(f"Command: {cmd}")
        
        result = os.system(cmd)
        if result == 0:
            if os.path.exists(output_file):
                size = os.path.getsize(output_file)
                print(f"✓ Success! Output file: {output_file} ({size} bytes)")
            else:
                print(f"✓ Success! Output file: {output_file}")
        else:
            print(f"✗ Failed!")
        print()
    
    print("Demonstration completed!")
    print("\nTo listen to the generated audio files, you can use:")
    print("  - On macOS: afplay output_speed_1_0.wav")
    print("  - On Linux: aplay output_speed_1_0.wav")
    print("  - On Windows: start output_speed_1_0.wav")

if __name__ == "__main__":
    # Make sure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    demo_korean_tts()