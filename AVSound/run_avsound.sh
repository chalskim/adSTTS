#!/bin/bash

# AVSound - YouTube Audio/Screen Recorder for macOS
# Setup and run script

echo "============================"

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Error: This script is designed for macOS only."
    exit 1
fi

echo "Detected macOS system"

# Add Python user bin to PATH
export PATH="/Users/zing1977gmail.com/Library/Python/3.9/bin:$PATH"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3 from https://www.python.org/downloads/macos/"
    exit 1
fi

echo "Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 not found, trying to install..."
    python3 -m ensurepip --upgrade
fi

# Install required packages
echo "Installing required packages..."
pip3 install -r requirements.txt

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg not found"
    echo "To install ffmpeg, you can use Homebrew:"
    echo "  brew install ffmpeg"
    echo ""
    echo "Or download it from https://evermeet.cx/ffmpeg/"
    echo ""
fi

# Check if yt-dlp is installed
if ! command -v yt-dlp &> /dev/null; then
    echo "yt-dlp not found, installing..."
    pip3 install yt-dlp
fi

# Ask user which version to run
echo "Which version would you like to run?"
echo "1. Original GUI (avsound.py)"
echo "2. New Enhanced GUI (avsound_gui.py)"
echo "3. Command Line Interface (avsound_cli.py)"
echo "4. YouTube Audio Extractor (youtube_audio_extractor.py)"
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo "Starting Original GUI version..."
        python3 avsound.py
        ;;
    2)
        echo "Starting Enhanced GUI version..."
        python3 avsound_gui.py
        ;;
    3)
        echo "Starting Command Line Interface..."
        python3 avsound_cli.py
        ;;
    4)
        echo "Starting YouTube Audio Extractor..."
        python3 youtube_audio_extractor.py
        ;;
    *)
        echo "Invalid choice. Starting Original GUI version..."
        python3 avsound.py
        ;;
esac

echo "AVSound has been started."
echo "If you encounter any issues, please check the README.md file for troubleshooting tips."