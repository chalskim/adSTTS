import whisper
import sys
import os
import torch
import numpy as np
import soundfile as sf
from typing import Union, Any


def transcribe_audio(file_path: str, model_size: str = "base") -> str:
    """
    Transcribe audio file using OpenAI Whisper
    
    Args:
        file_path (str): Path to the audio file
        model_size (str): Size of the Whisper model to use
    
    Returns:
        str: Transcribed text
    """
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")
    
    # Get file info
    file_info = sf.info(file_path)
    duration = file_info.duration
    
    # Get file size
    file_size = os.path.getsize(file_path)  # in bytes
    
    # Convert to MB for easier comparison
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"Audio file info - Duration: {duration/60:.1f} minutes, Size: {file_size_mb:.1f} MB")
    
    # For long files (>30 minutes) OR large files (>100 MB), process in chunks
    if duration > 1800 or file_size_mb > 100:  # 30 minutes OR 100 MB
        print(f"Large audio file detected. Processing in chunks...")
        return transcribe_long_audio(file_path, model_size)
    else:
        # Load the Whisper model
        print(f"Loading Whisper {model_size} model...")
        model = whisper.load_model(model_size)
        
        # Transcribe the audio directly
        print(f"Transcribing {file_path}...")
        result = model.transcribe(file_path)
        return str(result["text"])


def transcribe_long_audio(file_path: str, model_size: str = "base", chunk_duration: int = 600) -> str:
    """
    Transcribe long audio files by processing in chunks
    
    Args:
        file_path (str): Path to the audio file
        model_size (str): Size of the Whisper model to use
        chunk_duration (int): Duration of each chunk in seconds (default: 10 minutes)
    
    Returns:
        str: Transcribed text
    """
    print(f"Processing long audio file in {chunk_duration/60:.1f}-minute chunks...")
    
    # Load the Whisper model
    print(f"Loading Whisper {model_size} model...")
    model = whisper.load_model(model_size)
    
    # Load audio file
    audio_data, sample_rate = sf.read(file_path)
    
    # If stereo, convert to mono
    if len(audio_data.shape) > 1:
        audio_data = audio_data.mean(axis=1)
    
    # Calculate chunk size in samples
    chunk_size = int(chunk_duration * sample_rate)
    total_samples = len(audio_data)
    total_chunks = (total_samples + chunk_size - 1) // chunk_size  # Ceiling division
    
    transcriptions = []
    
    for i in range(total_chunks):
        start_sample = i * chunk_size
        end_sample = min((i + 1) * chunk_size, total_samples)
        
        # Extract chunk
        audio_chunk = audio_data[start_sample:end_sample]
        
        print(f"Processing chunk {i+1}/{total_chunks}...")
        
        try:
            # Transcribe chunk
            result = model.transcribe(audio_chunk, fp16=False)
            transcriptions.append(str(result["text"]))
            
            # Optional: Add a small delay to prevent overwhelming the system
            # time.sleep(0.1)
        except Exception as e:
            print(f"Error transcribing chunk {i+1}: {e}")
            transcriptions.append("")  # Add empty string to maintain order
    
    # Combine all transcriptions
    full_transcription = " ".join(transcriptions)
    return full_transcription


def save_transcription_to_output_folder(transcription: str, original_file_path: str) -> str:
    """
    Save transcription to an 'output' folder with the same base name as the original file
    
    Args:
        transcription (str): The transcribed text
        original_file_path (str): Path to the original audio file
    
    Returns:
        str: Path to the saved transcription file
    """
    # Create output directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # Generate output file path
    base_name = os.path.splitext(os.path.basename(original_file_path))[0]
    output_file = os.path.join(output_dir, f"{base_name}_transcription.txt")
    
    # Save transcription
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(transcription)
    
    return output_file


def main():
    # Check if audio file path is provided
    if len(sys.argv) < 2:
        print("Usage: python whisper_stt.py <audio_file_path> [model_size]")
        print("Example: python whisper_stt.py audio.mp3 base")
        print("\nAvailable model sizes: tiny, base, small, medium, large")
        return
    
    # Get file path and model size from command line arguments
    audio_file_path = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "base"
    
    try:
        # Transcribe the audio
        transcription: str = transcribe_audio(audio_file_path, model_size)
        
        # Print the result
        print("\nTranscription:")
        print("=" * 50)
        print(transcription)
        print("=" * 50)
        
        # Save to output folder
        output_file = save_transcription_to_output_folder(transcription, audio_file_path)
        print(f"\nTranscription saved to: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()