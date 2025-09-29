#!/bin/bash
# melo_korean_tts.sh
# Script to run MeloTTS for Korean with proper PATH

# Add Python bin to PATH
export PATH="/Users/zing1977gmail.com/Library/Python/3.9/bin:$PATH"

# Set environment variables to minimize Japanese imports
export MELO_LANG=KR
export LANGUAGE=ko

echo "Running MeloTTS for Korean TTS with speed control"
echo "Input file: $1"
echo "Output file: $2"
echo "Speed: $3"

# Run MeloTTS with Korean language and speed control
melo --file --language KR --speed $3 $1 $2