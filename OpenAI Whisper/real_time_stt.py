import whisper
import numpy as np
import queue
import threading
import time

class RealTimeSTT:
    def __init__(self, model_size="base"):
        """
        Initialize real-time speech-to-text using sounddevice
        
        Args:
            model_size (str): Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
        """
        # Load Whisper model
        print(f"Loading Whisper {model_size} model...")
        self.model = whisper.load_model(model_size)
        print("Model loaded successfully!")
        
        # Audio parameters
        self.sample_rate = 16000
        self.block_duration = 5  # seconds
        self.block_size = self.block_duration * self.sample_rate
        
        # Buffer for audio data
        self.audio_buffer = queue.Queue()
        self.is_recording = False
        
    def audio_callback(self, indata, frames, time, status):
        """Callback function for audio input"""
        if status:
            print(f"Audio status: {status}")
        # Convert to float32 and add to buffer
        audio_data = indata[:, 0].astype(np.float32)
        self.audio_buffer.put(audio_data.copy())
    
    def transcribe_buffer(self):
        """Transcribe accumulated audio data"""
        audio_data_list = []
        
        # Collect all available audio chunks
        while not self.audio_buffer.empty():
            audio_data_list.append(self.audio_buffer.get())
        
        if audio_data_list:
            # Concatenate all audio data
            combined_audio = np.concatenate(audio_data_list)
            
            # Only transcribe if we have enough audio
            if len(combined_audio) > self.sample_rate:  # At least 1 second
                try:
                    # Transcribe
                    result = self.model.transcribe(combined_audio, fp16=False)
                    text = result["text"]
                    
                    if isinstance(text, str) and text.strip():
                        print(f"Transcribed: {text}")
                        return text
                except Exception as e:
                    print(f"Transcription error: {e}")
        
        return ""
    
    def start_listening(self):
        """Start real-time listening and transcription"""
        print("Starting real-time transcription...")
        print("Speak into your microphone (Press Ctrl+C to stop)")
        
        self.is_recording = True
        
        # Import sounddevice here to handle ImportError gracefully
        try:
            import sounddevice as sd
        except ImportError:
            print("Error: sounddevice module not found.")
            print("Please install it with: pip install sounddevice")
            return
        
        # Start audio stream
        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                callback=self.audio_callback,
                blocksize=self.block_size
            ):
                # Transcription loop
                while self.is_recording:
                    # Transcribe buffered audio every few seconds
                    self.transcribe_buffer()
                    time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                    
        except KeyboardInterrupt:
            print("\nStopping real-time transcription...")
        except Exception as e:
            print(f"Error with audio input: {e}")
            print("Make sure you have a working microphone connected.")
        
        self.is_recording = False

def main():
    print("OpenAI Whisper Real-Time Speech-to-Text")
    print("=" * 40)
    
    # Get model size from user
    print("Available models: tiny, base, small, medium, large")
    model_input = input("Choose model size (default: base): ")
    model_size = model_input.strip() if model_input else "base"
    
    # Create and run real-time STT
    stt = RealTimeSTT(model_size=model_size)
    stt.start_listening()
    
    print("Real-time STT session ended")

if __name__ == "__main__":
    main()