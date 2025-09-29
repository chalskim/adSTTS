#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete setup and test script for Korean TTS Converter
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{description}")
    print("-" * len(description))
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(e.stderr)
        return False

def main():
    print("Korean TTS Converter - Complete Setup and Test")
    print("=" * 50)
    
    # Check if we're in the right directory
    required_files = ["requirements.txt", "text_to_speech.py"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"Error: Required file '{file}' not found.")
            print("Please run this script from the project directory.")
            sys.exit(1)
    
    # Step 1: Install dependencies
    print("\nStep 1: Installing dependencies")
    if not run_command("pip install -r requirements.txt", "Installing Python packages"):
        print("Failed to install dependencies. Exiting.")
        sys.exit(1)
    
    # Step 2: Create example files
    print("\nStep 2: Creating example files")
    if not run_command("python3 example_usage.py", "Creating example text files"):
        print("Failed to create example files. Continuing anyway...")
    
    # Step 3: Test installation
    print("\nStep 3: Testing installation")
    if not run_command("python3 test_tts.py", "Testing Korean TTS functionality"):
        print("TTS test failed. You may need to troubleshoot the installation.")
        sys.exit(1)
    
    # Step 4: Demonstrate usage
    print("\nStep 4: Demonstrating usage")
    run_command("python3 example_usage.py", "Showing usage examples")
    
    print("\n" + "=" * 50)
    print("Setup and testing completed successfully!")
    print("\nYou can now use the Korean TTS converter:")
    print("  python3 text_to_speech.py your_text_file.txt")
    print("\nFor more options, see the README.md file.")

if __name__ == "__main__":
    main()