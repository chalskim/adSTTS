#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Korean Text-to-Speech Converter
Converts text files to WAV audio files using MeloTTS
"""

import os
import sys
import argparse

# Try to import MeloTTS
try:
    from melo.api import TTS
    MELO_TTS_AVAILABLE = True
except ImportError as e:
    print(f"Import error: {e}")
    # Try alternative import approach
    try:
        # Suppress Japanese-related imports that cause issues
        import os
        os.environ['MELO_LANG'] = 'KR'
        from melo.api import TTS
        MELO_TTS_AVAILABLE = True
    except ImportError:
        MELO_TTS_AVAILABLE = False
        TTS = None

import soundfile as sf
import librosa

def check_dependencies():
    """Check if all required dependencies are available"""
    if not MELO_TTS_AVAILABLE:
        print("Error: MeloTTS is not installed or not accessible.")
        print("Please install it by running: pip install melo-tts")
        print("Or run the setup script: ./setup.sh")
        return False
    return True

def convert_text_to_speech(input_file, output_file, language='KR', speaker_id=0, speed=1.0):
    """
    Convert text file to WAV audio file using MeloTTS
    
    Args:
        input_file (str): Path to the input text file
        output_file (str): Path to the output WAV file
        language (str): Language code ('KR' for Korean, 'EN' for English, etc.)
        speaker_id (int): Speaker ID (0-3 for Korean)
        speed (float): Speed of speech (0.5-2.0)
    """
    
    # Check if dependencies are available
    if not check_dependencies():
        raise ImportError("Required dependencies not available")
    
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Read text from file
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    if not text:
        raise ValueError("Input file is empty")
    
    # Initialize TTS model
    print(f"Initializing MeloTTS for {language}...")
    try:
        model = TTS(language=language.upper())
    except Exception as e:
        print(f"Error initializing TTS model: {e}")
        # Try with Korean specifically
        if language.upper() == 'KR':
            model = TTS(language='KR')
        else:
            raise e
    
    # Get speaker names
    try:
        speaker_names = model.hps.data.spk2id
        print(f"Available speakers: {list(speaker_names.keys())}")
    except AttributeError:
        # Fallback for accessing speaker information
        speaker_names = {'KR': 0}
        print("Using default Korean speaker")
    
    # Select speaker
    if language.upper() == 'KR':
        # For Korean, use speaker ID 0-3
        try:
            speaker_ids = list(speaker_names.values())
            if speaker_id >= len(speaker_ids):
                speaker_id = 0
            speaker = list(speaker_names.keys())[speaker_id]
        except:
            speaker = 'KR'
    else:
        try:
            speaker = list(speaker_names.keys())[0]
        except:
            speaker = 'EN-US'
    
    print(f"Using speaker: {speaker}")
    print(f"Speech speed: {speed}x")
    
    # Convert text to speech
    print("Converting text to speech...")
    try:
        audio = model.tts_to_file(text, speaker, output_file, speed=speed)
        print(f"Audio saved to: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error during TTS conversion: {e}")
        # Try with default parameters
        model.tts_to_file(text, speaker, output_file)
        print(f"Audio saved to: {output_file}")
        return output_file

def main():
    # Check dependencies early
    if not check_dependencies():
        sys.exit(1)
        
    parser = argparse.ArgumentParser(description="Convert text file to Korean speech (WAV)")
    parser.add_argument("input", help="Input text file path")
    parser.add_argument("-o", "--output", help="Output WAV file path (default: input.wav)")
    parser.add_argument("-l", "--language", default="KR", help="Language code (KR for Korean, EN for English)")
    parser.add_argument("-s", "--speaker", type=int, default=0, help="Speaker ID (0-3 for Korean)")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed (0.5-2.0)")
    
    args = parser.parse_args()
    
    # Set default output file name if not provided
    if not args.output:
        base_name = os.path.splitext(args.input)[0]
        args.output = f"{base_name}.wav"
    
    try:
        convert_text_to_speech(
            args.input, 
            args.output, 
            args.language, 
            args.speaker, 
            args.speed
        )
        print("Conversion completed successfully!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()