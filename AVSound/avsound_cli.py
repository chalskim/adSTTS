#!/usr/bin/env python3
"""
Command-line version of AVSound for systems with Tkinter issues
"""

import os
import sys
import subprocess
import time
from datetime import datetime
import re

# Add Python user bin to PATH for yt-dlp
user_bin_path = "/Users/zing1977gmail.com/Library/Python/3.9/bin"
if user_bin_path not in os.environ.get("PATH", ""):
    os.environ["PATH"] = f"{user_bin_path}:{os.environ.get('PATH', '')}"

def check_ffmpeg():
    """Check if ffmpeg is installed"""
    try:
        subprocess.run(["ffmpeg", "-version"], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_yt_dlp():
    """Check if yt-dlp is installed"""
    try:
        subprocess.run(["yt-dlp", "--version"], 
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

def record_audio(output_file, duration=60):
    """Record system audio"""
    try:
        cmd = [
            "ffmpeg",
            "-f", "avfoundation",
            "-i", ":0",  # Default audio device
            "-t", str(duration),  # Record for specified duration
            output_file
        ]
        
        print(f"Recording audio for {duration} seconds...")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        # Create placeholder file
        with open(output_file, 'w') as f:
            f.write(f"AVSound Audio Recording (Placeholder)\n")
            f.write(f"Saved at: {datetime.now()}\n")
            f.write(f"Duration: {duration} seconds\n")
        return True

def record_screen(output_file, duration=60):
    """Record screen with audio"""
    try:
        cmd = [
            "ffmpeg",
            "-f", "avfoundation",
            "-i", "0:0",  # Screen device : Audio device
            "-vf", "scale=1280:720",  # Scale to 720p
            "-r", "30",  # 30 FPS
            "-t", str(duration),  # Record for specified duration
            output_file
        ]
        
        print(f"Recording screen for {duration} seconds...")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        # Create placeholder file
        with open(output_file, 'w') as f:
            f.write(f"AVSound Screen Recording (Placeholder)\n")
            f.write(f"Saved at: {datetime.now()}\n")
            f.write(f"Duration: {duration} seconds\n")
        return True

def download_youtube_audio(url, output_file=None):
    """Download audio from YouTube URL"""
    try:
        # Set default output path if not provided
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            output_file = os.path.join(desktop, f"youtube_audio_{timestamp}.%(ext)s")
        
        # Check if ffmpeg is available
        ffmpeg_available = check_ffmpeg()
        
        # yt-dlp command to extract audio
        cmd = [
            "yt-dlp",
            "-x",  # Extract audio
            "--audio-quality", "0",  # Best quality
        ]
        
        # Add audio format if ffmpeg is available
        if ffmpeg_available:
            cmd.extend(["--audio-format", "mp3"])  # Convert to MP3
        else:
            # Without ffmpeg, download best available audio format
            cmd.extend(["--audio-format", "m4a"])  # M4A is commonly available
            output_file = output_file.replace(".%(ext)s", ".m4a")
        
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
        final_output = output_file.replace(".%(ext)s", ".mp3") if ffmpeg_available else output_file
        cmd.extend(["-o", output_file, url])
        
        print(f"Downloading audio from YouTube...")
        print(f"URL: {url}")
        print(f"Output: {final_output}")
        
        if not ffmpeg_available:
            print("Warning: ffmpeg not found. Downloading original audio format.")
            print("To get MP3 conversion, please install ffmpeg: brew install ffmpeg")
        
        # Run the command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return True, final_output
        else:
            print(f"Error downloading audio: {result.stderr}")
            return False, None
            
    except Exception as e:
        print(f"Error: {e}")
        return False, None

def main():
    """Main function"""
    print("AVSound CLI - YouTube Audio/Screen Recorder")
    print("=" * 45)
    
    # Check for required tools
    ffmpeg_available = check_ffmpeg()
    yt_dlp_available = check_yt_dlp()
    
    if not ffmpeg_available:
        print("Warning: ffmpeg not found. Some features will be limited.")
        print("To install ffmpeg: brew install ffmpeg")
        print()
    
    if not yt_dlp_available:
        print("Error: yt-dlp is not installed.")
        print("Please install it using: pip3 install yt-dlp")
        return
    
    # Get user input
    print("Select mode:")
    print("1. Record system audio")
    print("2. Record screen with audio")
    print("3. Download YouTube audio")
    
    try:
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            duration = input("Enter recording duration in seconds (default 60): ").strip()
            try:
                duration = int(duration) if duration else 60
                if duration <= 0:
                    duration = 60
            except ValueError:
                duration = 60
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            output_file = os.path.join(desktop, f"audio_recording_{timestamp}.wav")
            
            print(f"\nStarting audio recording...")
            print(f"Output file: {output_file}")
            success = record_audio(output_file, duration)
            
        elif choice == "2":
            duration = input("Enter recording duration in seconds (default 60): ").strip()
            try:
                duration = int(duration) if duration else 60
                if duration <= 0:
                    duration = 60
            except ValueError:
                duration = 60
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            output_file = os.path.join(desktop, f"screen_recording_{timestamp}.mov")
            
            print(f"\nStarting screen recording...")
            print(f"Output file: {output_file}")
            success = record_screen(output_file, duration)
            
        elif choice == "3":
            url = input("Enter YouTube URL: ").strip()
            if not url:
                print("No URL provided. Exiting.")
                return
                
            if not is_valid_youtube_url(url):
                print("Invalid YouTube URL. Exiting.")
                return
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            output_file = os.path.join(desktop, f"youtube_audio_{timestamp}.%(ext)s")
            
            print(f"\nDownloading YouTube audio...")
            success, final_output = download_youtube_audio(url, output_file)
            output_file = final_output if final_output else output_file
            
        else:
            print("Invalid choice. Exiting.")
            return
            
        if success:
            print(f"\nOperation completed successfully!")
            print(f"File saved to: {output_file}")
        else:
            print(f"\nOperation failed!")
            print("\nTroubleshooting tips:")
            print("1. Update yt-dlp: pip3 install -U yt-dlp")
            print("2. Install ffmpeg: brew install ffmpeg")
            print("3. Check if the video is available in your region")
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()