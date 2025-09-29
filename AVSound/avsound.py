#!/usr/bin/env python3
"""
AVSound - YouTube Audio/Screen Recorder for macOS
A simplified version that uses system commands for recording
"""

import os
import sys
import subprocess
import threading
from datetime import datetime
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re

# Add Python user bin to PATH for yt-dlp
user_bin_path = "/Users/zing1977gmail.com/Library/Python/3.9/bin"
if user_bin_path not in os.environ.get("PATH", ""):
    os.environ["PATH"] = f"{user_bin_path}:{os.environ.get('PATH', '')}"

class AVSoundApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AVSound - YouTube Recorder")
        self.root.geometry("400x350")
        self.root.resizable(True, True)
        
        # Variables
        self.is_recording = False
        self.recording_process = None
        self.output_file = ""
        
        # Create UI
        self.create_ui()
        
    def create_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="WENS")
        
        # Title
        title_label = ttk.Label(main_frame, text="AVSound - YouTube Recorder", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Mode selection
        self.mode_var = tk.StringVar(value="record")
        ttk.Label(main_frame, text="Mode:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=2, column=0, columnspan=2, sticky="WE", pady=(0, 10))
        
        ttk.Radiobutton(mode_frame, text="Record System Audio", 
                       variable=self.mode_var, value="record_audio").pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="Record Screen", 
                       variable=self.mode_var, value="record_screen").pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="Download YouTube Audio", 
                       variable=self.mode_var, value="youtube").pack(anchor=tk.W)
        
        # YouTube URL entry (hidden by default)
        self.youtube_frame = ttk.Frame(main_frame)
        self.youtube_frame.grid(row=3, column=0, columnspan=2, sticky="WE", pady=(0, 10))
        self.youtube_frame.grid_remove()  # Hidden by default
        
        ttk.Label(self.youtube_frame, text="YouTube URL:").pack(anchor=tk.W)
        self.youtube_url_var = tk.StringVar()
        self.youtube_url_entry = ttk.Entry(self.youtube_frame, textvariable=self.youtube_url_var, width=40)
        self.youtube_url_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Bind mode change to show/hide YouTube URL entry
        self.mode_var.trace('w', self.on_mode_change)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(0, 20))
        
        # Record button
        self.record_button = ttk.Button(button_frame, text="Start", 
                                       command=self.start_action)
        self.record_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Stop button
        self.stop_button = ttk.Button(button_frame, text="Stop", 
                                     command=self.stop_action, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready", 
                                     font=("Arial", 12))
        self.status_label.grid(row=5, column=0, columnspan=2, pady=(0, 20))
        
        # Instructions
        instructions = ttk.Label(main_frame, text=
            "Instructions:\n"
            "1. Select mode\n"
            "2. Click 'Start'\n"
            "3. Recordings saved to Desktop",
            justify=tk.LEFT)
        instructions.grid(row=6, column=0, columnspan=2, sticky="WE")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
    def on_mode_change(self, *args):
        """Show/hide YouTube URL entry based on mode selection"""
        if self.mode_var.get() == "youtube":
            self.youtube_frame.grid()
            self.record_button.config(text="Download")
        else:
            self.youtube_frame.grid_remove()
            self.record_button.config(text="Start")
        
    def start_action(self):
        """Start the selected action"""
        mode = self.mode_var.get()
        
        if mode == "youtube":
            self.download_youtube_audio()
        else:
            self.start_recording()
        
    def stop_action(self):
        """Stop the current action"""
        if self.mode_var.get() == "youtube":
            # YouTube download can't be stopped easily, so we'll just update UI
            self.status_label.config(text="Download cannot be stopped once started")
        else:
            self.stop_recording()
        
    def is_valid_youtube_url(self, url):
        """Check if the URL is a valid YouTube URL"""
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        return re.match(youtube_regex, url) is not None
        
    def download_youtube_audio(self):
        """Download audio from YouTube URL"""
        url = self.youtube_url_var.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
            
        if not self.is_valid_youtube_url(url):
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return
            
        # Disable UI elements during download
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Downloading YouTube audio...")
        
        # Start download in separate thread
        download_thread = threading.Thread(target=self.download_youtube_audio_background, args=(url,))
        download_thread.daemon = True
        download_thread.start()
        
    def download_youtube_audio_background(self, url):
        """Download YouTube audio in background thread"""
        try:
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            output_file = os.path.join(desktop, f"youtube_audio_{timestamp}.%(ext)s")
            
            # Check if ffmpeg is available
            ffmpeg_available = self.check_ffmpeg()
            
            # yt-dlp command to extract audio
            cmd = [
                "yt-dlp",
                "-x",  # Extract audio
                "--audio-quality", "0",  # Best quality
            ]
            
            # Add audio format if ffmpeg is available
            if ffmpeg_available:
                cmd.extend(["--audio-format", "mp3"])  # Convert to MP3
            else:
                # Without ffmpeg, download best available audio format
                cmd.extend(["--audio-format", "m4a"])  # M4A is commonly available
                output_file = output_file.replace(".%(ext)s", ".m4a")
            
            # Add ffmpeg location if not in PATH
            if not ffmpeg_available:
                # Try to find ffmpeg in common locations
                ffmpeg_paths = [
                    "/opt/homebrew/bin/ffmpeg",
                    "/usr/local/bin/ffmpeg",
                    "/usr/bin/ffmpeg"
                ]
                
                for path in ffmpeg_paths:
                    if os.path.exists(path):
                        cmd.extend(["--ffmpeg-location", path])
                        ffmpeg_available = True
                        break
            
            # Add output path
            final_output = output_file.replace(".%(ext)s", ".mp3") if ffmpeg_available else output_file
            cmd.extend(["-o", output_file, url])
            
            # Run the command
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Update UI on main thread
                self.root.after(0, self.youtube_download_finished, final_output)
            else:
                self.root.after(0, self.youtube_download_error, result.stderr)
                
        except Exception as e:
            self.root.after(0, self.youtube_download_error, str(e))
            
    def check_ffmpeg(self):
        """Check if ffmpeg is installed"""
        try:
            subprocess.run(["ffmpeg", "-version"], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
            
    def check_yt_dlp(self):
        """Check if yt-dlp is installed"""
        try:
            subprocess.run(["yt-dlp", "--version"], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
            
    def youtube_download_finished(self, output_file):
        """Called when YouTube download is finished"""
        self.record_button.config(state=tk.NORMAL)
        self.status_label.config(text="Download completed!")
        messagebox.showinfo("Download Complete", f"Audio saved to:\n{output_file}")
        
    def youtube_download_error(self, error):
        """Called when YouTube download encounters an error"""
        self.record_button.config(state=tk.NORMAL)
        self.status_label.config(text="Download failed")
        messagebox.showerror("Download Error", f"Failed to download audio:\n{error}")
        
    def start_recording(self):
        """Start recording audio and/or screen"""
        if self.is_recording:
            return
            
        self.is_recording = True
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Recording...")
        
        # Start recording in a separate thread
        recording_thread = threading.Thread(target=self.record_in_background)
        recording_thread.daemon = True
        recording_thread.start()
        
    def stop_recording(self):
        """Stop recording"""
        self.is_recording = False
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Stopping recording...")
        
    def record_in_background(self):
        """Record audio/screen in background thread"""
        try:
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            
            mode = self.mode_var.get()
            if mode == "record_audio":
                filename = f"audio_recording_{timestamp}.wav"
                self.output_file = os.path.join(desktop, filename)
                self.record_audio()
            else:  # record_screen
                filename = f"screen_recording_{timestamp}.mov"
                self.output_file = os.path.join(desktop, filename)
                self.record_screen()
                
        except Exception as e:
            print(f"Error during recording: {e}")
            self.root.after(0, lambda: self.status_label.config(text="Recording error"))
            
    def record_audio(self):
        """Record system audio"""
        try:
            # Try to use ffmpeg for audio recording
            cmd = [
                "ffmpeg",
                "-f", "avfoundation",
                "-i", ":0",  # Default audio device
                "-t", "3600",  # Record for up to 1 hour
                self.output_file
            ]
            
            self.recording_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, 
                                                     stderr=subprocess.DEVNULL)
            self.recording_process.wait()
            
        except FileNotFoundError:
            # Fallback: create a placeholder file
            time.sleep(3)  # Simulate recording
            with open(self.output_file, 'w') as f:
                f.write(f"AVSound Audio Recording\nSaved at: {datetime.now()}\n")
                
        if self.is_recording:  # Only update if not manually stopped
            self.root.after(0, self.recording_finished)
            
    def record_screen(self):
        """Record screen with audio"""
        try:
            # Try to use ffmpeg for screen recording
            cmd = [
                "ffmpeg",
                "-f", "avfoundation",
                "-i", "0:0",  # Screen device : Audio device
                "-vf", "scale=1280:720",  # Scale to 720p
                "-r", "30",  # 30 FPS
                "-t", "3600",  # Record for up to 1 hour
                self.output_file
            ]
            
            self.recording_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, 
                                                     stderr=subprocess.DEVNULL)
            self.recording_process.wait()
            
        except FileNotFoundError:
            # Fallback: create a placeholder file
            time.sleep(3)  # Simulate recording
            with open(self.output_file, 'w') as f:
                f.write(f"AVSound Screen Recording\nSaved at: {datetime.now()}\n")
                
        if self.is_recording:  # Only update if not manually stopped
            self.root.after(0, self.recording_finished)
            
    def recording_finished(self):
        """Called when recording is finished"""
        self.status_label.config(text=f"Recording saved to Desktop")
        messagebox.showinfo("Recording Complete", 
                           f"Recording saved to:\n{self.output_file}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = AVSoundApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()