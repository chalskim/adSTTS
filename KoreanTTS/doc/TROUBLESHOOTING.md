# Troubleshooting Guide

This document helps resolve common issues with the Korean TTS Converter.

## Installation Issues

### "No module named melo.api"

**Problem**: When running the script, you get an error like:
```
ModuleNotFoundError: No module named 'melo.api'
```

**Solution**: 
1. Make sure you've installed the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Or run the setup script:
   - macOS/Linux: `./setup.sh`
   - Windows: `setup.bat`

### "Command 'pip' not found"

**Problem**: Your system doesn't recognize the pip command.

**Solution**:
1. Try using `pip3` instead of `pip`:
   ```bash
   pip3 install -r requirements.txt
   ```
2. If that doesn't work, you may need to install pip:
   - macOS: `brew install python`
   - Ubuntu/Debian: `sudo apt install python3-pip`
   - Windows: Reinstall Python and check "Add to PATH"

## Usage Issues

### "Input file not found"

**Problem**: The script can't find your text file.

**Solution**:
1. Check that the file path is correct
2. Use the full path or relative path from your current directory
3. Make sure the file exists:
   ```bash
   ls -la your_file.txt  # macOS/Linux
   dir your_file.txt     # Windows
   ```

### "UnicodeDecodeError"

**Problem**: Error when reading text file:
```
UnicodeDecodeError: 'utf-8' codec can't decode byte
```

**Solution**:
1. Make sure your text file is saved in UTF-8 encoding
2. Most text editors allow you to specify encoding when saving
3. In Notepad (Windows): File → Save As → Encoding: UTF-8
4. In VS Code: Bottom right corner shows encoding, click to change

### No audio output

**Problem**: Script runs without errors but no audio file is created.

**Solution**:
1. Check the output directory permissions
2. Make sure you have write permissions in the directory
3. Try specifying a full output path:
   ```bash
   python text_to_speech.py input.txt -o /tmp/output.wav
   ```

## Audio Quality Issues

### Poor audio quality

**Solution**:
1. Try different speakers (0-3 for Korean):
   ```bash
   python text_to_speech.py input.txt -s 1
   ```
2. Adjust speech speed:
   ```bash
   python text_to_speech.py input.txt --speed 0.9
   ```
3. Ensure your text has proper punctuation

### Audio file is too large

**Solution**:
1. Reduce the amount of text in your input file
2. The generated WAV files are uncompressed and can be large
3. Consider converting to MP3 for smaller file sizes (requires additional tools)

## Platform-Specific Issues

### macOS Security Issues

**Problem**: "Operation not permitted" when running scripts.

**Solution**:
1. Give Terminal full disk access in System Preferences
2. Or run with sudo (not recommended):
   ```bash
   sudo python text_to_speech.py input.txt
   ```

### Windows Audio Issues

**Problem**: Audio doesn't play correctly on Windows.

**Solution**:
1. Install additional audio libraries:
   ```bash
   pip install pyaudio
   ```
2. Make sure you have the latest audio drivers

## Testing

To test if everything is working correctly:

1. Run the test script:
   ```bash
   python test_tts.py
   ```

2. Try with the sample file:
   ```bash
   python text_to_speech.py sample_korean.txt
   ```

If you continue to have issues, please check:
1. Your Python version (3.7 or higher)
2. Your internet connection (for initial model downloads)
3. Available disk space (models can be large)
4. System resources (RAM, CPU)