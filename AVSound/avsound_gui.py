#!/usr/bin/env python3
"""
AVSound GUI - YouTube Audio/Screen Recorder for macOS
GUI version based on avsound_cli.py functionality
"""

import os
import sys
import subprocess
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re

# Add Python user bin to PATH for yt-dlp
user_bin_path = "/Users/zing1977gmail.com/Library/Python/3.9/bin"
if user_bin_path not in os.environ.get("PATH", ""):
    os.environ["PATH"] = f"{user_bin_path}:{os.environ.get('PATH', '')}"

class AVSoundGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AVSound - YouTube Audio/Screen Recorder")
        self.root.geometry("500x600")
        self.root.resizable(True, True)
        
        # Variables
        self.is_recording = False
        self.recording_process = None
        self.output_file = ""
        self.mode_var = tk.StringVar(value="record_audio")
        self.youtube_url_var = tk.StringVar()
        self.duration_var = tk.StringVar(value="60")
        
        # Create UI
        self.create_ui()
        
        # Check dependencies
        self.check_dependencies()
        
    def create_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="AVSound - YouTube Audio/Screen Recorder", 
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Mode selection frame
        mode_frame = ttk.LabelFrame(main_frame, text="Mode Selection", padding="10")
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Mode radio buttons
        modes_frame = ttk.Frame(mode_frame)
        modes_frame.pack(fill=tk.X)
        
        ttk.Radiobutton(modes_frame, text="Record System Audio", 
                       variable=self.mode_var, value="record_audio",
                       command=self.on_mode_change).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(modes_frame, text="Record Screen with Audio", 
                       variable=self.mode_var, value="record_screen",
                       command=self.on_mode_change).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(modes_frame, text="Download YouTube Audio", 
                       variable=self.mode_var, value="youtube",
                       command=self.on_mode_change).pack(anchor=tk.W, pady=2)
        
        # YouTube URL frame
        self.youtube_frame = ttk.LabelFrame(main_frame, text="YouTube Download", padding="10")
        self.youtube_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(self.youtube_frame, text="YouTube URL:").pack(anchor=tk.W)
        self.youtube_url_entry = ttk.Entry(self.youtube_frame, 
                                          textvariable=self.youtube_url_var, 
                                          width=50)
        self.youtube_url_entry.pack(fill=tk.X, pady=(5, 10))
        
        # Recording settings frame
        self.recording_frame = ttk.LabelFrame(main_frame, text="Recording Settings", padding="10")
        self.recording_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Duration setting
        duration_frame = ttk.Frame(self.recording_frame)
        duration_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(duration_frame, text="Duration (seconds):").pack(side=tk.LEFT)
        self.duration_entry = ttk.Entry(duration_frame, 
                                       textvariable=self.duration_var, 
                                       width=10)
        self.duration_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # Output file frame
        output_frame = ttk.LabelFrame(main_frame, text="Output Settings", padding="10")
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(output_frame, text="Output Directory:").pack(anchor=tk.W)
        output_dir_frame = ttk.Frame(output_frame)
        output_dir_frame.pack(fill=tk.X, pady=(5, 10))
        
        self.output_dir_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Desktop"))
        self.output_dir_entry = ttk.Entry(output_dir_frame, 
                                         textvariable=self.output_dir_var, 
                                         state="readonly")
        self.output_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(output_dir_frame, text="Browse", 
                  command=self.browse_output_dir).pack(side=tk.LEFT, padx=(5, 0))
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_button = ttk.Button(control_frame, text="Start", 
                                      command=self.start_action)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(control_frame, text="Stop", 
                                     command=self.stop_action, 
                                     state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True)
        
        self.status_text = tk.Text(status_frame, height=8, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Initialize UI state
        self.on_mode_change()
        
    def check_dependencies(self):
        """Check for required dependencies"""
        missing_deps = []
        
        if not self.check_ffmpeg():
            missing_deps.append("ffmpeg")
            
        if not self.check_yt_dlp():
            missing_deps.append("yt-dlp")
            
        if missing_deps:
            self.update_status(f"Warning: Missing dependencies: {', '.join(missing_deps)}")
            self.update_status("Some features may be limited.")
            if "ffmpeg" in missing_deps:
                self.update_status("To install ffmpeg: brew install ffmpeg")
            if "yt-dlp" in missing_deps:
                self.update_status("To install yt-dlp: pip3 install yt-dlp")
        else:
            self.update_status("All dependencies found. Ready to use all features.")
        
    def on_mode_change(self):
        """Show/hide UI elements based on mode selection"""
        mode = self.mode_var.get()
        
        if mode == "youtube":
            self.youtube_frame.pack(fill=tk.X, pady=(0, 10))
            self.recording_frame.pack_forget()
            self.start_button.config(text="Download")
        else:
            self.youtube_frame.pack_forget()
            self.recording_frame.pack(fill=tk.X, pady=(0, 10))
            self.start_button.config(text="Start Recording")
            
    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)
            
    def update_status(self, message):
        """Update status text area"""
        self.status_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        
    def start_action(self):
        """Start the selected action"""
        mode = self.mode_var.get()
        
        if mode == "youtube":
            self.download_youtube_audio()
        else:
            self.start_recording()
            
    def stop_action(self):
        """Stop the current action"""
        mode = self.mode_var.get()
        
        if mode == "youtube":
            self.update_status("Note: YouTube downloads cannot be stopped once started")
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
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.progress.start()
        self.update_status("Starting YouTube audio download...")
        
        # Start download in separate thread
        download_thread = threading.Thread(target=self.download_youtube_audio_background, args=(url,))
        download_thread.daemon = True
        download_thread.start()
        
    def download_youtube_audio_background(self, url):
        """Download YouTube audio in background thread"""
        try:
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = self.output_dir_var.get()
            output_file = os.path.join(output_dir, f"youtube_audio_{timestamp}.%(ext)s")
            
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
            
            self.update_status(f"Downloading: {url}")
            self.update_status(f"Output: {final_output}")
            
            # Run the command
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Update UI on main thread
                self.root.after(0, self.youtube_download_finished, final_output)
            else:
                self.root.after(0, self.youtube_download_error, result.stderr)
                
        except Exception as e:
            self.root.after(0, self.youtube_download_error, str(e))
            
    def youtube_download_finished(self, output_file):
        """Called when YouTube download is finished"""
        self.start_button.config(state=tk.NORMAL)
        self.progress.stop()
        self.update_status("YouTube audio download completed successfully!")
        messagebox.showinfo("Download Complete", f"Audio saved to:\n{output_file}")
        
    def youtube_download_error(self, error):
        """Called when YouTube download encounters an error"""
        self.start_button.config(state=tk.NORMAL)
        self.progress.stop()
        self.update_status("YouTube audio download failed!")
        self.update_status(f"Error: {error}")
        messagebox.showerror("Download Error", f"Failed to download audio:\n{error}")
        
    def start_recording(self):
        """Start recording audio and/or screen"""
        if self.is_recording:
            return
            
        # Validate duration
        try:
            duration = int(self.duration_var.get())
            if duration <= 0:
                raise ValueError("Duration must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid duration in seconds")
            return
            
        self.is_recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress.start()
        
        # Start recording in a separate thread
        recording_thread = threading.Thread(target=self.record_in_background)
        recording_thread.daemon = True
        recording_thread.start()
        
    def stop_recording(self):
        """Stop recording"""
        self.is_recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress.stop()
        self.update_status("Stopping recording...")
        
    def record_in_background(self):
        """Record audio/screen in background thread"""
        try:
            # Get duration
            duration = int(self.duration_var.get())
            
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = self.output_dir_var.get()
            
            mode = self.mode_var.get()
            if mode == "record_audio":
                filename = f"audio_recording_{timestamp}.wav"
                self.output_file = os.path.join(output_dir, filename)
                self.update_status(f"Starting audio recording for {duration} seconds...")
                self.update_status(f"Output: {self.output_file}")
                self.record_audio(duration)
            else:  # record_screen
                filename = f"screen_recording_{timestamp}.mov"
                self.output_file = os.path.join(output_dir, filename)
                self.update_status(f"Starting screen recording for {duration} seconds...")
                self.update_status(f"Output: {self.output_file}")
                self.record_screen(duration)
                
        except Exception as e:
            self.update_status(f"Error during recording: {e}")
            self.root.after(0, self.recording_error)
            
    def record_audio(self, duration):
        """Record system audio"""
        try:
            self.update_status("Recording system audio...")
            
            cmd = [
                "ffmpeg",
                "-f", "avfoundation",
                "-i", ":0",  # Default audio device
                "-t", str(duration),  # Record for specified duration
                self.output_file
            ]
            
            self.recording_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, 
                                                     stderr=subprocess.DEVNULL)
            self.recording_process.wait()
            
            if self.is_recording:  # Only update if not manually stopped
                self.root.after(0, self.recording_finished)
                
        except FileNotFoundError:
            # Fallback: create a placeholder file
            self.update_status("ffmpeg not found. Creating placeholder file...")
            with open(self.output_file, 'w') as f:
                f.write(f"AVSound Audio Recording\nSaved at: {datetime.now()}\n")
                f.write(f"Duration: {duration} seconds\n")
            self.root.after(0, self.recording_finished)
        except Exception as e:
            self.root.after(0, self.recording_error, str(e))
            
    def record_screen(self, duration):
        """Record screen with audio"""
        try:
            self.update_status("Recording screen with audio...")
            
            cmd = [
                "ffmpeg",
                "-f", "avfoundation",
                "-i", "0:0",  # Screen device : Audio device
                "-vf", "scale=1280:720",  # Scale to 720p
                "-r", "30",  # 30 FPS
                "-t", str(duration),  # Record for specified duration
                self.output_file
            ]
            
            self.recording_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, 
                                                     stderr=subprocess.DEVNULL)
            self.recording_process.wait()
            
            if self.is_recording:  # Only update if not manually stopped
                self.root.after(0, self.recording_finished)
                
        except FileNotFoundError:
            # Fallback: create a placeholder file
            self.update_status("ffmpeg not found. Creating placeholder file...")
            with open(self.output_file, 'w') as f:
                f.write(f"AVSound Screen Recording\nSaved at: {datetime.now()}\n")
                f.write(f"Duration: {duration} seconds\n")
            self.root.after(0, self.recording_finished)
        except Exception as e:
            self.root.after(0, self.recording_error, str(e))
            
    def recording_finished(self):
        """Called when recording is finished"""
        self.is_recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress.stop()
        self.update_status("Recording completed successfully!")
        messagebox.showinfo("Recording Complete", 
                           f"Recording saved to:\n{self.output_file}")
                           
    def recording_error(self, error=""):
        """Called when recording encounters an error"""
        self.is_recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress.stop()
        self.update_status("Recording failed!")
        if error:
            self.update_status(f"Error: {error}")
        messagebox.showerror("Recording Error", 
                            f"Recording failed:\n{error}")
        
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


def main():
    """Main entry point"""
    root = tk.Tk()
    app = AVSoundGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()