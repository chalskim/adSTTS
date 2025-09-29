import noisereduce as nr
import soundfile as sf
import numpy as np
from scipy.io.wavfile import write
import os

def reduce_noise_file(input_file, output_file=None, noise_sample_duration=0.5):
    """
    Reduce noise in an audio file using the noisereduce library
    
    Args:
        input_file (str): Path to the input audio file
        output_file (str): Path to the output denoised file (optional)
        noise_sample_duration (float): Duration of noise sample to use for noise profiling (seconds)
    
    Returns:
        str: Path to the denoised audio file
    """
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Load audio file
    print(f"Loading audio file: {input_file}")
    audio_data, sample_rate = sf.read(input_file)
    
    # Convert to mono if stereo
    if len(audio_data.shape) > 1:
        audio_data = np.mean(audio_data, axis=1)
    
    print(f"Audio loaded - Sample rate: {sample_rate} Hz, Duration: {len(audio_data)/sample_rate:.2f} seconds")
    
    # Get noise sample from the beginning of the file
    noise_sample = audio_data[:int(noise_sample_duration * sample_rate)]
    
    # Apply noise reduction
    print("Applying noise reduction...")
    reduced_noise = nr.reduce_noise(
        y=audio_data,
        sr=sample_rate,
        noise_profile=noise_sample,
        verbose=True
    )
    
    # Generate output file name if not provided
    if output_file is None:
        name, ext = os.path.splitext(input_file)
        output_file = f"{name}_denoised{ext}"
    
    # Save denoised audio
    print(f"Saving denoised audio to: {output_file}")
    sf.write(output_file, reduced_noise, sample_rate)
    
    print("Noise reduction completed successfully!")
    return output_file

def main():
    """Main function to demonstrate file-based noise reduction"""
    print("File-based Noise Reduction with noisereduce")
    print("=" * 45)
    
    # Get input file from user
    input_file = input("Enter path to audio file: ").strip()
    
    if not input_file:
        print("No input file provided.")
        return
    
    try:
        # Apply noise reduction
        output_file = reduce_noise_file(input_file)
        print(f"\nDenoised file saved as: {output_file}")
        print("You can now use this file with whisper_stt.py for better transcription accuracy.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()