#!/usr/bin/env python3
"""
Example usage of AVSound application
"""

def show_usage_examples():
    """Show example usage of AVSound"""
    
    print("AVSound - YouTube Audio/Screen Recorder")
    print("=" * 40)
    
    print("\n1. Quick Start:")
    print("   ./run_avsound.sh")
    
    print("\n2. Manual Setup:")
    print("   pip3 install -r requirements.txt")
    print("   python3 avsound.py           # Original GUI version")
    print("   python3 avsound_gui.py       # Enhanced GUI version")
    print("   python3 avsound_cli.py       # Command-line version")
    print("   python3 youtube_audio_extractor.py  # Direct YouTube audio extraction")
    
    print("\n3. Building macOS Executable:")
    print("   pip3 install py2app")
    print("   python3 setup.py py2app")
    print("   # Executable will be in dist/AVSound.app")
    
    print("\n4. Testing Setup:")
    print("   python3 test_setup.py")
    
    print("\nFeatures:")
    print("- Record system audio (including YouTube videos)")
    print("- Record screen with audio")
    print("- Download audio directly from YouTube URLs")
    print("- Simple graphical interface")
    print("- Enhanced graphical interface with better UX")
    print("- Command-line interface (for systems with Tkinter issues)")
    print("- Saves recordings to custom directories")
    print("- Audio only mode available")
    
    print("\nRequirements:")
    print("- macOS 10.15 or later")
    print("- Python 3.6 or later")
    print("- ffmpeg (for recording and YouTube extraction)")
    print("- yt-dlp (for YouTube audio extraction)")
    print("- Xcode command line tools (for building executable)")
    
    print("\nNote:")
    print("Due to macOS security restrictions, you may need to grant")
    print("screen recording and microphone permissions to the application.")
    print("You can do this in System Preferences > Security & Privacy.")
    
    print("\nIf you encounter Tkinter compatibility issues:")
    print("- Use the command-line version: python3 avsound_cli.py")
    print("- Update Python via Homebrew: brew install python")
    print("- Or install Python from https://www.python.org/downloads/macos/")
    
    print("\nYouTube Audio Extraction:")
    print("- GUI: Select 'Download YouTube Audio' mode")
    print("- CLI: Use python3 youtube_audio_extractor.py")
    print("- CLI version: Select option 3 in avsound_cli.py")

if __name__ == "__main__":
    show_usage_examples()