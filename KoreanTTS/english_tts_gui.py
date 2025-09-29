#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI for English TTS with Speed Control and Speaker Selection
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys

# Add the current directory to Python path to import our TTS modules
# This is especially important when running as a PyInstaller executable
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    current_dir = os.path.dirname(sys.executable)
else:
    # Running as script
    current_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(current_dir)

class EnglishTTSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("English TTS Converter")
        self.root.geometry("550x350")
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.speed = tk.DoubleVar(value=1.0)
        self.speaker = tk.StringVar(value="EN-US")
        self.is_converting = False
        
        # Available English speakers
        self.speakers = {
            "American English (EN-US)": "EN-US",
            "British English (EN-BR)": "EN-BR",
            "Indian English (EN-INDIA)": "EN_INDIA",
            "Australian English (EN-AU)": "EN-AU",
            "Default English (EN-Default)": "EN-Default"
        }
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="English TTS Converter", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Input file
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        ttk.Label(input_frame, text="Input File:").pack(anchor=tk.W)
        input_file_frame = ttk.Frame(input_frame)
        input_file_frame.pack(fill=tk.X, pady=5)
        ttk.Entry(input_file_frame, textvariable=self.input_file).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(input_file_frame, text="Browse", command=self.browse_input).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Output file
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.X, pady=5)
        ttk.Label(output_frame, text="Output File:").pack(anchor=tk.W)
        output_file_frame = ttk.Frame(output_frame)
        output_file_frame.pack(fill=tk.X, pady=5)
        ttk.Entry(output_file_frame, textvariable=self.output_file).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(output_file_frame, text="Browse", command=self.browse_output).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Speaker selection
        speaker_frame = ttk.Frame(main_frame)
        speaker_frame.pack(fill=tk.X, pady=(15, 5))
        ttk.Label(speaker_frame, text="Speaker:").pack(anchor=tk.W)
        self.speaker_combo = ttk.Combobox(
            speaker_frame, 
            textvariable=self.speaker, 
            values=list(self.speakers.keys()),
            state="readonly"
        )
        self.speaker_combo.set("American English (EN-US)")
        self.speaker_combo.pack(fill=tk.X, pady=5)
        
        # Speed control
        speed_frame = ttk.Frame(main_frame)
        speed_frame.pack(fill=tk.X, pady=(15, 5))
        ttk.Label(speed_frame, text="Speed:").pack(anchor=tk.W)
        speed_scale_frame = ttk.Frame(speed_frame)
        speed_scale_frame.pack(fill=tk.X, pady=5)
        self.speed_label = ttk.Label(speed_scale_frame, text="1.0x (Normal)")
        self.speed_label.pack(side=tk.LEFT)
        self.speed_scale = ttk.Scale(
            speed_scale_frame, 
            from_=0.5, 
            to=2.0, 
            orient=tk.HORIZONTAL, 
            variable=self.speed,
            command=self.update_speed_label
        )
        self.speed_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Speed buttons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=10)
        ttk.Button(buttons_frame, text="0.7x", command=lambda: self.set_speed(0.7)).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="1.0x", command=lambda: self.set_speed(1.0)).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="1.3x", command=lambda: self.set_speed(1.3)).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="1.5x", command=lambda: self.set_speed(1.5)).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="2.0x", command=lambda: self.set_speed(2.0)).pack(side=tk.LEFT, padx=2)
        
        # Convert button
        self.convert_button = ttk.Button(main_frame, text="Convert to Speech", command=self.start_conversion)
        self.convert_button.pack(pady=20)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Ready")
        self.status_label.pack()
        
    def update_speed_label(self, value):
        speed_value = float(value)
        if speed_value == 1.0:
            self.speed_label.config(text=f"{speed_value:.1f}x (Normal)")
        elif speed_value < 1.0:
            self.speed_label.config(text=f"{speed_value:.1f}x (Slower)")
        else:
            self.speed_label.config(text=f"{speed_value:.1f}x (Faster)")
            
    def set_speed(self, value):
        self.speed.set(value)
        self.update_speed_label(str(value))
        
    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="Select Input Text File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            # Set default output filename
            if not self.output_file.get():
                base_name = os.path.splitext(filename)[0]
                self.output_file.set(f"{base_name}.wav")
                
    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save Output WAV File",
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        if filename:
            self.output_file.set(filename)
            
    def start_conversion(self):
        if self.is_converting:
            return
            
        if not self.input_file.get():
            messagebox.showwarning("Warning", "Please select an input text file.")
            return
            
        if not self.output_file.get():
            messagebox.showwarning("Warning", "Please specify an output WAV file.")
            return
            
        self.is_converting = True
        self.convert_button.config(state='disabled', text="Converting...")
        self.status_label.config(text="Converting...")
        
        # Run conversion in separate thread
        thread = threading.Thread(target=self.convert_text_to_speech)
        thread.daemon = True
        thread.start()
        
    def convert_text_to_speech(self):
        try:
            # Read input text
            with open(self.input_file.get(), 'r', encoding='utf-8') as f:
                text = f.read().strip()
            
            if not text:
                self.root.after(0, self.conversion_error, "Input file is empty")
                return
                
            # Get selected speaker value
            speaker_key = self.speaker_combo.get()
            speaker_value = self.speakers.get(speaker_key, "EN-US")
            
            # Convert using English TTS
            success = self.convert_with_english_tts(text, speaker_value)
            
            if success:
                self.root.after(0, self.conversion_success)
            else:
                self.root.after(0, self.conversion_error, "Conversion failed")
                
        except Exception as e:
            self.root.after(0, self.conversion_error, str(e))
            
    def convert_with_english_tts(self, text, speaker):
        """Convert text using English TTS with speaker selection"""
        try:
            # Create a mock Japanese module to avoid import errors
            import sys
            from types import ModuleType
            
            class MockJapaneseModule(ModuleType):
                def __init__(self):
                    super().__init__('japanese')
                def distribute_phone(self, *args, **kwargs):
                    return []
            
            # Monkey patch the Japanese import
            sys.modules['melo.text.japanese'] = MockJapaneseModule()
            
            # Set environment variables for English TTS
            os.environ['MELO_LANG'] = 'EN'
            os.environ['LANGUAGE'] = 'en'
            
            # Import MeloTTS
            from melo.api import TTS
            
            # Initialize English TTS
            tts = TTS(language='EN')
            
            # Get speaker ID from the model
            try:
                # Access speaker IDs (suppressing linter warning)
                speaker_ids = tts.hps.data.spk2id  # type: ignore
                print(f"Available English speakers: {list(speaker_ids.keys())}")
                
                if speaker not in speaker_ids:
                    # Try to find a similar speaker
                    speaker_options = [s for s in speaker_ids.keys() if speaker.split('-')[0].upper() in s.upper()]
                    if speaker_options:
                        speaker = speaker_options[0]
                    else:
                        speaker = list(speaker_ids.keys())[0]  # Get first speaker as fallback
                    print(f"Speaker adjusted to: {speaker}")
                
                speaker_id = speaker_ids[speaker]      # Get the numeric ID
            except Exception as e:
                print(f"Speaker selection error: {e}")
                # Fallback to string speaker ID
                speaker_id = speaker
            
            # Convert to speech
            tts.tts_to_file(text, speaker_id, self.output_file.get(), speed=self.speed.get())
            print(f"Audio saved to: {self.output_file.get()} (using MeloTTS)")
            
            return True
            
        except Exception as e:
            # This will catch both ImportError and other MeloTTS errors
            print(f"MeloTTS not available or encountered an error: {e}")
            print("Falling back to gTTS for English...")
            try:
                from gtts import gTTS
                # For gTTS, we use 'en' for English regardless of specific variant
                slow = self.speed.get() < 1.0
                tts = gTTS(text=text, lang='en', slow=slow)
                tts.save(self.output_file.get())
                print(f"Audio saved to: {self.output_file.get()} (using gTTS)")
                return True
            except Exception as gTTS_error:
                print(f"gTTS error: {gTTS_error}")
                return False
            
    def conversion_success(self):
        self.is_converting = False
        self.convert_button.config(state='normal', text="Convert to Speech")
        self.status_label.config(text="Conversion completed!")
        messagebox.showinfo("Success", f"Audio saved to:\n{self.output_file.get()}")
        
    def conversion_error(self, error_message):
        self.is_converting = False
        self.convert_button.config(state='normal', text="Convert to Speech")
        self.status_label.config(text="Conversion failed")
        messagebox.showerror("Error", f"Conversion failed:\n{error_message}")

def main():
    root = tk.Tk()
    app = EnglishTTSGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()