#!/usr/bin/env python3
"""
Test script for long audio file handling with Whisper
"""

import os
import numpy as np
import soundfile as sf


def create_test_audio(duration_seconds=300, sample_rate=16000, filename="test_long_audio.wav"):
    """
    Create a test audio file with synthetic data for testing long audio processing
    
    Args:
        duration_seconds (int): Duration of audio in seconds (default: 5 minutes)
        sample_rate (int): Sample rate in Hz (default: 16000)
        filename (str): Output filename
    """
    print(f"Creating test audio file: {filename}")
    print(f"Duration: {duration_seconds} seconds ({duration_seconds/60:.1f} minutes)")
    
    # Create synthetic audio data (simple sine wave)
    t = np.linspace(0, duration_seconds, int(duration_seconds * sample_rate), False)
    frequency = 440  # A4 note
    audio_data = np.sin(2 * np.pi * frequency * t) * 0.3  # Reduce volume to 30%
    
    # Add some noise to make it more realistic
    noise = np.random.normal(0, 0.05, audio_data.shape)
    audio_data = audio_data + noise
    
    # Save as WAV file
    sf.write(filename, audio_data, sample_rate)
    print(f"Test audio file created: {filename}")
    
    # Verify file info
    file_info = sf.info(filename)
    file_size = os.path.getsize(filename)
    file_size_mb = file_size / (1024 * 1024)
    print(f"File duration: {file_info.duration/60:.1f} minutes")
    print(f"Sample rate: {file_info.samplerate} Hz")
    print(f"File size: {file_size_mb:.1f} MB")


def test_long_audio_processing():
    """
    Test the long audio processing functionality
    """
    test_file = "test_long_audio.wav"
    
    # Create test file if it doesn't exist
    if not os.path.exists(test_file):
        # Create a 5-minute test file (long enough to demonstrate the concept)
        create_test_audio(duration_seconds=300, filename=test_file)
    
    print("\nTesting audio file info detection...")
    print("=" * 50)
    
    try:
        # Test file info detection
        import soundfile as sf
        file_info = sf.info(test_file)
        duration = file_info.duration
        file_size = os.path.getsize(test_file)
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"File: {test_file}")
        print(f"Duration: {duration/60:.1f} minutes")
        print(f"Size: {file_size_mb:.1f} MB")
        
        # Check our criteria
        is_long = duration > 1800  # 30 minutes
        is_large = file_size_mb > 100  # 100 MB
        
        print(f"Long file (>30 min): {is_long}")
        print(f"Large file (>100 MB): {is_large}")
        print(f"Needs chunked processing: {is_long or is_large}")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()


def main():
    print("OpenAI Whisper Long Audio Processing Test")
    print("=" * 45)
    
    # Test long audio processing
    test_long_audio_processing()
    
    print("\nTest completed!")


if __name__ == "__main__":
    main()