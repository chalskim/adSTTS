#!/bin/bash
# setup.sh
# Setup script for Korean TTS Converter

echo "Setting up Korean TTS Converter..."

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "pip is not installed. Please install pip."
    exit 1
fi

# Install required packages
echo "Installing required packages..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "Setup completed successfully!"
    echo ""
    echo "To test the Korean TTS converter:"
    echo "1. Create a text file with Korean content"
    echo "2. Run: python3 universal_korean_tts.py your_file.txt"
    echo ""
    echo "Example:"
    echo "python3 universal_korean_tts.py sample_korean.txt"
    echo ""
    echo "Alternative approaches:"
    echo "- MeloTTS only: python3 text_to_speech.py your_file.txt"
    echo "- gTTS only: python3 korean_tts_gTTS.py your_file.txt"
else
    echo "Setup failed. Please check the error messages above."
    exit 1
fi