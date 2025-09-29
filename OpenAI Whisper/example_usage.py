#!/usr/bin/env python3
"""
Example script demonstrating how to use the Whisper STT system
"""

import whisper
import sys
import os

def main():
    # Example 1: Basic usage with default model
    print("OpenAI Whisper Speech-to-Text Example")
    print("=" * 40)
    
    # Create a simple example
    audio_file = "example.wav"
    
    if not os.path.exists(audio_file):
        print(f"Audio file '{audio_file}' not found.")
        print("Please provide your own audio file or create a sample file.")
        return
    
    print(f"Transcribing audio file: {audio_file}")
    
    # Load the model (using base model for balance of speed and accuracy)
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    
    # Transcribe the audio
    print("Transcribing...")
    result = model.transcribe(audio_file)
    
    # Display results
    print("\nTranscription Results:")
    print("-" * 20)
    print(f"Detected language: {result['language']}")
    print(f"Transcribed text: {result['text']}")
    
    # Save to file
    output_file = f"{os.path.splitext(audio_file)[0]}_transcription.txt"
    with open(output_file, "w") as f:
        f.write(str(result["text"]))
    
    print(f"\nTranscription saved to: {output_file}")
    
    # Example 2: Advanced usage with options
    print("\n\nAdvanced Example with Options:")
    print("-" * 30)
    
    # Transcribe with additional options
    result_detailed = model.transcribe(
        audio_file,
        verbose=True,  # Print progress
        task="transcribe",  # or "translate" to translate to English
        language="en"  # Specify language (optional, auto-detected by default)
    )
    
    print(f"\nDetailed transcription: {result_detailed['text']}")

if __name__ == "__main__":
    main()