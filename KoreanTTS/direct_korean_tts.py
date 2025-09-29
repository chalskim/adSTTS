#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct Korean TTS script that avoids Japanese dependency issues
"""

import os
import sys

def main():
    # Try to import only what we need
    try:
        # Set environment variable to avoid Japanese imports
        os.environ['MELO_LANG'] = 'KR'
        
        # Import only the TTS class
        from melo.api import TTS
        
        print("MeloTTS imported successfully")
        
        # Check if sample file exists
        if not os.path.exists("sample_korean.txt"):
            print("Error: sample_korean.txt not found")
            return 1
            
        # Read the sample text
        with open("sample_korean.txt", "r", encoding="utf-8") as f:
            text = f.read().strip()
            
        print(f"Converting text: {text[:50]}...")
        
        # Initialize Korean TTS
        tts = TTS(language='KR')
        print("Korean TTS initialized")
        
        # Get speaker
        try:
            speakers = list(tts.hps.data.spk2id.keys())
            speaker = speakers[0]
            print(f"Using speaker: {speaker}")
        except:
            speaker = 'KR'
            print("Using default Korean speaker")
        
        # Generate audio
        output_file = "output_korean.wav"
        tts.tts_to_file(text, speaker, output_file)
        print(f"Audio saved to: {output_file}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())