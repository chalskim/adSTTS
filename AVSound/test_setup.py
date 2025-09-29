#!/usr/bin/env python3
"""
Test script to verify AVSound setup
"""

import sys
import os
import subprocess

def check_python_version():
    """Check if Python 3.6+ is installed"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print(f"Error: Python 3.6+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"Python version OK: {version.major}.{version.minor}")
    return True

def check_package(package_name):
    """Check if a Python package is installed"""
    try:
        __import__(package_name)
        print(f"Package {package_name}: OK")
        return True
    except ImportError:
        print(f"Package {package_name}: MISSING")
        return False

def check_command(command):
    """Check if a system command is available"""
    try:
        subprocess.run([command, "--version"], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL)
        print(f"Command {command}: OK")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"Command {command}: MISSING")
        return False

def main():
    print("AVSound Setup Verification")
    print("=" * 30)
    
    # Check Python version
    if not check_python_version():
        return False
    
    print()
    
    # Check Python packages
    required_packages = [
        "tkinter",
    ]
    
    all_good = True
    for package in required_packages:
        if not check_package(package):
            all_good = False
    
    print()
    
    # Check system commands
    required_commands = [
        "ffmpeg",
    ]
    
    for command in required_commands:
        if not check_command(command):
            all_good = False
    
    print()
    
    if all_good:
        print("All checks passed! You're ready to use AVSound.")
        print("Run './run_avsound.sh' to start the application.")
        return True
    else:
        print("Some requirements are missing. Please check the README.md for installation instructions.")
        return False

if __name__ == "__main__":
    main()