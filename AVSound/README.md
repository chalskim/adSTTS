# AVSound - YouTube Audio/Screen Recorder for macOS

AVSound is a macOS application that allows you to record audio and screen from YouTube videos or any other content on your Mac. It also supports direct audio extraction from YouTube URLs.

## Features

- Record system audio (including YouTube videos)
- Record screen with audio
- Download audio directly from YouTube URLs
- Simple graphical user interface
- Enhanced graphical user interface with better UX
- Command-line interface
- Export recordings in common formats
- Custom output directory selection
- Real-time status updates
- Easy to use for macOS users

## Prerequisites

- macOS 10.15 or later
- Python 3.6 or later (for development)
- Xcode command line tools (for building the executable)

## Installation

### For Development

1. Clone this repository
2. Install required packages:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Install additional tools:
   ```bash
   # Using Homebrew (recommended)
   brew install ffmpeg
   brew install yt-dlp
   
   # Or install via pip
   pip3 install yt-dlp
   ```

### For End Users (Executable)

Download the pre-built executable from the releases page and drag it to your Applications folder.

## Usage

### Quick Start

```bash
./run_avsound.sh
```

### Running from Source

```bash
# Original GUI version
python3 avsound.py

# Enhanced GUI version (based on CLI functionality)
python3 avsound_gui.py

# Command-line version
python3 avsound_cli.py

# Direct YouTube audio extraction
python3 youtube_audio_extractor.py
```

### Using the Executable

Double-click the AVSound.app file to launch the application.

## Building the Executable

To build the executable for distribution:

```bash
pip3 install py2app
python3 setup.py py2app
```

The executable will be created in the `dist` folder.

### Customizing the Icon

To create a custom icon for your app:

1. Create a 1024x1024 PNG image
2. Convert it to ICNS format (see [CREATE_ICON.md](file:///Users/zing1977gmail.com/src/STTtest/AVSound/CREATE_ICON.md) for detailed instructions)
3. Save it as `app_icon.icns` in the project root
4. Rebuild the application

## How It Works

AVSound uses the following technologies:

1. **Tkinter**: Python's standard GUI toolkit for the user interface
2. **ffmpeg**: For audio and screen capture
3. **yt-dlp**: For downloading and extracting audio from YouTube
4. **py2app**: Converts Python applications to macOS executables

## Learning Tkinter

This project includes examples and documentation for learning Tkinter:

- [tkinter_examples.py](file:///Users/zing1977gmail.com/src/STTtest/AVSound/tkinter_examples.py) - Practical examples of Tkinter usage
- [TKINTER_BASICS.md](file:///Users/zing1977gmail.com/src/STTtest/AVSound/TKINTER_BASICS.md) - Comprehensive guide to Tkinter basics

To run the Tkinter examples:
```bash
python3 tkinter_examples.py
```

## YouTube Audio Extraction

AVSound can extract audio directly from YouTube URLs:

1. **In the GUI**: Select "Download YouTube Audio" mode and enter the URL
2. **Command-line**: Use `python3 youtube_audio_extractor.py`
3. **CLI version**: Select option 3 in `python3 avsound_cli.py`

The audio is automatically converted to MP3 format with the highest quality available.

### Supported Formats

- **With ffmpeg**: MP3 (highest quality)
- **Without ffmpeg**: M4A (original format)

## Enhanced GUI Features (avsound_gui.py)

The enhanced GUI version includes:

- Better user interface with organized sections
- Real-time status updates in a scrollable text area
- Custom output directory selection
- Progress indication for long operations
- Improved error handling and user feedback
- All functionality from the CLI version in a GUI format

## Troubleshooting Tkinter Issues

If you encounter the error:
```
macOS 15 (1507) or later required, have instead 15 (1506)!
```

This is a known compatibility issue between Tkinter and certain macOS versions. Try these solutions:

1. **Update Python via Homebrew**:
   ```bash
   brew install python
   ```

2. **Use the command-line version**:
   ```bash
   python3 avsound_cli.py
   ```

3. **Install Python from python.org**:
   Visit https://www.python.org/downloads/macos/

Note: On some newer macOS versions, you may encounter compatibility issues with Tkinter.

## Limitations

- Due to macOS security restrictions, you may need to grant screen recording permissions
- System audio capture may require additional drivers on some macOS versions
- YouTube content is subject to copyright restrictions
- YouTube audio extraction depends on yt-dlp which may break if YouTube changes their API

## Troubleshooting

### Screen Recording Permissions

If screen recording doesn't work:

1. Go to System Preferences > Security & Privacy > Privacy
2. Select "Screen Recording" from the left sidebar
3. Check the box next to Terminal or your application

### Audio Recording Issues

If you're having trouble capturing system audio:

1. Install BlackHole virtual audio driver from https://github.com/ExistentialAudio/BlackHole
2. Create a multi-output device in Audio MIDI Setup
3. Select the multi-output device as your audio source

### YouTube Download Issues

If YouTube audio extraction fails:

1. Update yt-dlp: `pip3 install -U yt-dlp`
2. Install/update ffmpeg: `brew install ffmpeg`
3. Check if the video is available in your region
4. Some videos may have download restrictions

### Testing Your Setup

You can verify your setup by running:
```bash
python3 test_setup.py
```

## Example Usage

For more examples, run:
```bash
python3 example_usage.py
```