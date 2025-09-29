#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple GUI for Korean TTS with Speed Control
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

class KoreanTTSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Korean TTS Converter")
        self.root.geometry("500x300")
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.speed = tk.DoubleVar(value=1.0)
        self.is_converting = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Korean TTS Converter", font=("Arial", 14, "bold"))
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
        
        # Speed control
        speed_frame = ttk.Frame(main_frame)
        speed_frame.pack(fill=tk.X, pady=(20, 5))
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
                
            # Try to use patched Korean TTS
            success = self.convert_with_patched_tts(text)
            
            if success:
                self.root.after(0, self.conversion_success)
            else:
                self.root.after(0, self.conversion_error, "Conversion failed")
                
        except Exception as e:
            self.root.after(0, self.conversion_error, str(e))
            
    def convert_with_patched_tts(self, text):
        """Convert text using patched MeloTTS"""
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
            
            # Set environment variables
            os.environ['MELO_LANG'] = 'KR'
            os.environ['LANGUAGE'] = 'ko'
            
            # Import MeloTTS
            from melo.api import TTS
            
            # Initialize Korean TTS
            tts = TTS(language='KR')
            
            # Get speaker - handle attribute access properly
            try:
                # Access speaker IDs (suppressing linter warning)
                speaker_ids = tts.hps.data.spk2id  # type: ignore
                speakers = list(speaker_ids.keys())
                speaker = speakers[0] if speakers else 'KR'
            except AttributeError:
                # Fallback if attribute structure is different
                try:
                    speakers = tts.speakers if hasattr(tts, 'speakers') else ['KR']
                    speaker = speakers[0] if speakers else 'KR'
                except:
                    speaker = 'KR'
            except:
                speaker = 'KR'
            
            # Convert to speech with speed control
            tts.tts_to_file(text, speaker, self.output_file.get(), speed=self.speed.get())
            return True
            
        except Exception as e:
            print(f"MeloTTS error: {e}")
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
    app = KoreanTTSGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()