import whisper
import numpy as np
import queue
import collections
import sys
import time

class EnhancedRealTimeSTT:
    def __init__(self, model_size="base", use_vad=True, use_noise_reduction=False):
        """
        Enhanced real-time speech-to-text with noise reduction and voice activity detection
        
        Args:
            model_size (str): Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
            use_vad (bool): Whether to use WebRTC VAD for voice activity detection
            use_noise_reduction (bool): Whether to apply noise reduction (RNNoise-like)
        """
        # Load Whisper model
        print(f"Loading Whisper {model_size} model...")
        self.model = whisper.load_model(model_size)
        print("Model loaded successfully!")
        
        # Audio parameters
        self.sample_rate = 16000  # WebRTC VAD requires 8000, 16000, 32000, or 48000 Hz
        self.frame_duration = 30  # ms (10, 20, or 30 ms required by WebRTC VAD)
        self.frame_size = int(self.sample_rate * self.frame_duration / 1000)
        self.block_duration = 5  # seconds for transcription
        
        # VAD setup
        self.use_vad = use_vad
        if self.use_vad:
            import webrtcvad
            self.vad = webrtcvad.Vad(2)  # Aggressiveness mode 0-3 (3 most aggressive)
            self.ring_buffer = collections.deque(maxlen=30)  # For VAD decision smoothing
            self.triggered = False
            
        # Noise reduction
        self.use_noise_reduction = use_noise_reduction
        
        # Buffer for audio data
        self.audio_buffer = queue.Queue()
        self.transcription_buffer = []
        self.is_recording = False
        
    def reduce_noise_simple(self, audio_data):
        """
        Simple noise reduction using spectral gating (simplified RNNoise-like approach)
        This is a basic implementation - for production use, consider using the noisereduce library
        """
        if not self.use_noise_reduction:
            return audio_data
            
        # Convert to frequency domain
        fft_data = np.fft.rfft(audio_data)
        
        # Simple spectral gating
        magnitude = np.abs(fft_data)
        threshold = np.mean(magnitude) * 1.5  # Simple threshold
        
        # Apply gate
        mask = magnitude > threshold
        fft_data = fft_data * mask
        
        # Convert back to time domain
        filtered_audio = np.fft.irfft(fft_data)
        
        return filtered_audio.astype(np.float32)
    
    def is_speech(self, frame):
        """Check if audio frame contains speech using WebRTC VAD"""
        if not self.use_vad:
            return True
            
        # WebRTC VAD requires 16-bit PCM audio
        frame_pcm = (frame * 32767).astype(np.int16).tobytes()
        
        try:
            import webrtcvad
            return self.vad.is_speech(frame_pcm, self.sample_rate)
        except:
            return True  # If VAD fails, assume speech is present
    
    def audio_callback(self, indata, frames, time, status):
        """Callback function for audio input"""
        if status:
            print(f"Audio status: {status}")
            
        # Convert to float32
        audio_data = indata[:, 0].astype(np.float32)
        
        # Apply noise reduction if enabled
        if self.use_noise_reduction:
            audio_data = self.reduce_noise_simple(audio_data)
        
        # Process with VAD if enabled
        if self.use_vad:
            # Split into VAD frames
            for i in range(0, len(audio_data), self.frame_size):
                frame = audio_data[i:i + self.frame_size]
                if len(frame) == self.frame_size:  # Only process complete frames
                    is_speech = self.is_speech(frame)
                    self.ring_buffer.append((frame, is_speech))
                    
                    # VAD decision logic
                    if not self.triggered:
                        # Waiting for speech to start
                        num_voiced = len([f for f, speech in self.ring_buffer if speech])
                        if self.ring_buffer.maxlen and num_voiced > int(0.5 * self.ring_buffer.maxlen):
                            self.triggered = True
                            # Add buffered audio to transcription buffer
                            for f, s in self.ring_buffer:
                                self.transcription_buffer.extend(f)
                            self.ring_buffer.clear()
                    else:
                        # Speech in progress
                        self.transcription_buffer.extend(frame)
                        if not is_speech:
                            num_unvoiced = len([f for f, speech in self.ring_buffer if not speech])
                            if self.ring_buffer.maxlen and num_unvoiced > int(0.3 * self.ring_buffer.maxlen):
                                self.triggered = False
                                # Transcribe the accumulated speech
                                if len(self.transcription_buffer) > self.sample_rate:  # At least 1 second
                                    combined_audio = np.array(self.transcription_buffer)
                                    self.audio_buffer.put(combined_audio)
                                self.transcription_buffer = []
                                self.ring_buffer.clear()
        else:
            # No VAD - just accumulate audio
            self.audio_buffer.put(audio_data)
    
    def transcribe_buffer(self):
        """Transcribe accumulated audio data"""
        if not self.audio_buffer.empty():
            try:
                # Get audio data from queue
                audio_data = self.audio_buffer.get()
                
                # Transcribe
                result = self.model.transcribe(audio_data, fp16=False)
                text = result["text"]
                
                if isinstance(text, str) and text.strip():
                    print(f"Transcribed: {text}")
                    return text
                    
            except Exception as e:
                print(f"Transcription error: {e}")
        
        return ""
    
    def start_listening(self):
        """Start real-time listening and transcription"""
        # Import sounddevice here
        try:
            import sounddevice as sd
        except ImportError:
            print("Error: sounddevice module not found.")
            print("Please install it with: pip install sounddevice")
            return
            
        print("Starting enhanced real-time transcription...")
        if self.use_vad:
            print("Voice Activity Detection (VAD) is ENABLED")
        if self.use_noise_reduction:
            print("Noise reduction is ENABLED")
        print("Speak into your microphone (Press Ctrl+C to stop)")
        
        self.is_recording = True
        
        # Start audio stream
        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                callback=self.audio_callback,
                blocksize=self.frame_size  # Use VAD frame size
            ):
                # Transcription loop
                while self.is_recording:
                    # Transcribe buffered audio
                    self.transcribe_buffer()
                    time.sleep(0.05)  # Small delay to prevent excessive CPU usage
                    
        except KeyboardInterrupt:
            print("\nStopping enhanced real-time transcription...")
        except Exception as e:
            print(f"Error with audio input: {e}")
            print("Make sure you have a working microphone connected.")
        
        self.is_recording = False

def main():
    print("Enhanced OpenAI Whisper Real-Time Speech-to-Text")
    print("=" * 50)
    
    # Check if webrtcvad is available
    try:
        import webrtcvad
        WEBRTC_VAD_AVAILABLE = True
    except ImportError:
        WEBRTC_VAD_AVAILABLE = False
        print("Warning: webrtcvad not available. VAD will be disabled.")
    
    # Get options from user
    print("Available models: tiny, base, small, medium, large")
    model_input = input("Choose model size (default: base): ")
    model_size = model_input.strip() if model_input else "base"
    
    vad_choice = input("Enable Voice Activity Detection (VAD)? (y/n, default: y): ")
    use_vad = vad_choice.strip().lower() != 'n' and WEBRTC_VAD_AVAILABLE
    
    nr_choice = input("Enable noise reduction? (y/n, default: n): ")
    use_noise_reduction = nr_choice.strip().lower() == 'y'
    
    # Create and run enhanced real-time STT
    stt = EnhancedRealTimeSTT(
        model_size=model_size,
        use_vad=use_vad,
        use_noise_reduction=use_noise_reduction
    )
    stt.start_listening()
    
    print("Enhanced real-time STT session ended")

if __name__ == "__main__":
    main()