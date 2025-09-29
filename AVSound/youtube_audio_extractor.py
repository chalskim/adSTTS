#!/usr/bin/env python3
"""
YouTube Audio Extractor
Download audio directly from YouTube URLs
"""

import os
import sys
import subprocess
from datetime import datetime
import re

def check_yt_dlp():
    """Check if yt-dlp is installed"""
    try:
        subprocess.run(["yt-dlp", "--version"], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_ffmpeg():
    """Check if ffmpeg is installed"""
    try:
        subprocess.run(["ffmpeg", "-version"], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def is_valid_youtube_url(url):
    """Check if the URL is a valid YouTube URL"""
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return re.match(youtube_regex, url) is not None

def download_youtube_audio(url, output_path=None):
    """Download audio from YouTube URL"""
    try:
        # Set default output path if not provided
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            output_path = os.path.join(desktop, f"youtube_audio_{timestamp}.mp3")
        
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Check if ffmpeg is available
        ffmpeg_available = check_ffmpeg()
        
        # yt-dlp command to extract audio
        cmd = [
            "yt-dlp",
            "-x",  # Extract audio
            "--audio-format", "mp3",  # Convert to MP3
            "--audio-quality", "0",  # Best quality
        ]
        
        # Add ffmpeg location if not in PATH
        if not ffmpeg_available:
            # Try to find ffmpeg in common locations
            ffmpeg_paths = [
                "/opt/homebrew/bin/ffmpeg",
                "/usr/local/bin/ffmpeg",
                "/usr/bin/ffmpeg"
            ]
            
            for path in ffmpeg_paths:
                if os.path.exists(path):
                    cmd.extend(["--ffmpeg-location", path])
                    ffmpeg_available = True
                    break
        
        # Add output path
        cmd.extend(["-o", output_path, url])
        
        print(f"Downloading audio from YouTube...")
        print(f"URL: {url}")
        print(f"Output: {output_path}")
        
        if not ffmpeg_available:
            print("Warning: ffmpeg not found. Downloading original audio format without conversion.")
            print("To get MP3 conversion, please install ffmpeg:")
            print("  brew install ffmpeg")
            # Remove audio format conversion flags if ffmpeg not available
            cmd = [c for c in cmd if c not in ["--audio-format", "mp3", "--audio-quality", "0"]]
        
        # Run the command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Download completed successfully!")
            return True
        else:
            print(f"Error downloading audio: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Main function"""
    print("YouTube Audio Extractor")
    print("=" * 30)
    
    # Check for yt-dlp
    if not check_yt_dlp():
        print("Error: yt-dlp is not installed.")
        print("Please install it using: pip3 install yt-dlp")
        return
    
    # Check for ffmpeg
    ffmpeg_available = check_ffmpeg()
    if not ffmpeg_available:
        print("Warning: ffmpeg is not installed or not in PATH.")
        print("This may result in:")
        print("  - Audio not converted to MP3 format")
        print("  - Lower quality audio extraction")
        print("To install ffmpeg: brew install ffmpeg")
        print()
    
    # Get YouTube URL from user
    url = input("Enter YouTube URL: ").strip()
    
    if not url:
        print("No URL provided. Exiting.")
        return
    
    if not is_valid_youtube_url(url):
        print("Invalid YouTube URL. Please enter a valid YouTube link.")
        return
    
    # Optional: Get custom output path
    custom_output = input("Enter output file path (or press Enter for default): ").strip()
    output_path = custom_output if custom_output else None
    
    # Download the audio
    success = download_youtube_audio(url, output_path)
    
    if success:
        print("\nAudio extraction completed!")
        if output_path:
            print(f"File saved to: {output_path}")
        else:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            print(f"File saved to Desktop")
    else:
        print("\nAudio extraction failed!")
        print("\nTroubleshooting tips:")
        print("1. Update yt-dlp: pip3 install -U yt-dlp")
        print("2. Install ffmpeg: brew install ffmpeg")
        print("3. Check if the video is available in your region")
        print("4. Some videos may have download restrictions")

if __name__ == "__main__":
    main()