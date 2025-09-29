#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for Korean TTS Windows executable
"""

import os
import sys
import subprocess

def check_python():
    """Check if Python is installed"""
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        print(f"✓ Python installed: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"✗ Python not found: {e}")
        return False

def install_pyinstaller():
    """Install PyInstaller"""
    try:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "PyInstaller"],
                      check=True, capture_output=True)
        print("✓ PyInstaller installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install PyInstaller: {e}")
        return False

def build_executable():
    """Build Windows executable"""
    try:
        print("Building Windows executable...")
        subprocess.run([sys.executable, "-m", "PyInstaller", "--onefile", 
                       "--console", "korean_tts_windows.py"],
                      check=True, capture_output=True)
        print("✓ Windows executable built successfully")
        print("Executable location: dist/korean_tts.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to build executable: {e}")
        return False

def main():
    print("Korean TTS Windows Executable Setup")
    print("=" * 40)
    
    # Check Python installation
    if not check_python():
        print("Please install Python 3.7 or higher")
        return False
    
    # Install PyInstaller
    if not install_pyinstaller():
        print("Failed to install PyInstaller")
        return False
    
    # Build executable
    if not build_executable():
        print("Failed to build executable")
        return False
    
    print("\n" + "=" * 40)
    print("Setup completed successfully!")
    print("Windows executable is ready in the 'dist' folder")
    print("\nTo use the Korean TTS converter:")
    print("  dist/korean_tts.exe input.txt output.wav 1.5")
    
    return True

if __name__ == "__main__":
    main()