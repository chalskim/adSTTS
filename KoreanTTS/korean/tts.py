#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Korean TTS Converter
"""

import sys
import os

# Add the parent directory to the path so we can import the main TTS script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from korean.patched_korean_tts import main

if __name__ == "__main__":
    main()