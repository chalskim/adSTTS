"""
Setup script for AVSound application
This script creates a macOS executable using py2app
"""

import os
from setuptools import setup

APP = ['avsound.py']
DATA_FILES = []

# Check if icon file exists, if not use None
icon_file = 'app_icon.icns'
if not os.path.exists(icon_file):
    icon_file = None

OPTIONS = {
    'argv_emulation': True,
    'iconfile': icon_file,
    'packages': ['tkinter'],
    'plist': {
        'CFBundleName': 'AVSound',
        'CFBundleDisplayName': 'AVSound',
        'CFBundleGetInfoString': 'YouTube Audio/Screen Recorder',
        'CFBundleIdentifier': 'com.example.AVSound',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright (c) 2025, AVSound Team',
        'NSMicrophoneUsageDescription': 'This app needs access to microphone for audio recording.',
        'NSScreenCaptureUsageDescription': 'This app needs access to screen recording to capture YouTube videos.',
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)