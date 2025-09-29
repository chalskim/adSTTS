#!/bin/bash
# korean_tts.sh
# Script to run Korean TTS with proper environment setup

echo "Setting up environment for Korean TTS..."

# Set environment variables to avoid Japanese dependencies
export MELO_LANG=KR
export LANGUAGE=ko

echo "Running Korean TTS conversion..."

# Run the TTS conversion
python3 direct_korean_tts.py

if [ $? -eq 0 ]; then
    echo "Korean TTS conversion completed successfully!"
    echo "Output file: output_korean.wav"
else
    echo "Korean TTS conversion failed!"
    echo "Please check the error messages above."
fi