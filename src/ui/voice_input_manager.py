"""
Voice Input Manager for Speech Recognition
Handles microphone input and converts speech to text
"""

import speech_recognition as sr
import threading
import logging
import time
from typing import Optional, Callable
import asyncio


class VoiceInputManager:
    """Manages speech recognition from microphone input"""
    
    def __init__(self, callback: Optional[Callable[[str], None]] = None):
        """
        Initialize the voice input manager
        
        Args:
            callback: Function to call when speech is recognized
        """
        self.logger = logging.getLogger(__name__)
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.is_listening = False
        self.listen_thread: Optional[threading.Thread] = None
        self.callback = callback
        
        # Configure recognition settings
        self.recognizer.energy_threshold = 300  # Adjust for ambient noise
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        self.recognizer.dynamic_energy_ratio = 1.5
        self.recognizer.pause_threshold = 0.8  # Seconds of silence before considering speech ended
        self.recognizer.operation_timeout = None  # No timeout
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5
        
        self._initialize_microphone()
    
    def _initialize_microphone(self):
        """Initialize the microphone"""
        try:
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            self.logger.info("Adjusting for ambient noise... Please be quiet for a moment.")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            self.logger.info(f"Microphone initialized. Energy threshold: {self.recognizer.energy_threshold}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize microphone: {e}")
            raise
    
    def start_listening(self):
        """Start continuous listening for voice input"""
        if self.is_listening:
            self.logger.warning("Already listening")
            return
        
        if not self.microphone:
            self.logger.error("Microphone not initialized")
            return
        
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._listen_continuously, daemon=True)
        self.listen_thread.start()
        self.logger.info("Started continuous voice listening")
    
    def stop_listening(self):
        """Stop continuous listening"""
        if not self.is_listening:
            return
        
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        
        self.logger.info("Stopped voice listening")
    
    def _listen_continuously(self):
        """Continuously listen for speech input"""
        while self.is_listening:
            try:
                # Listen for audio with timeout
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Recognize speech in a separate thread to avoid blocking
                recognition_thread = threading.Thread(
                    target=self._process_audio,
                    args=(audio,),
                    daemon=True
                )
                recognition_thread.start()
                
            except sr.WaitTimeoutError:
                # Timeout is expected during continuous listening
                pass
            except Exception as e:
                if self.is_listening:  # Only log if we're still supposed to be listening
                    self.logger.warning(f"Error during listening: {e}")
                time.sleep(0.1)
    
    def _process_audio(self, audio):
        """Process recognized audio in a separate thread"""
        try:
            # Use Google Speech Recognition
            text = self.recognizer.recognize_google(audio, language='en-US')
            
            if text.strip():
                self.logger.info(f"Recognized speech: '{text}'")
                
                # Check if this looks like a question for the pet
                if self._is_pet_question(text):
                    if self.callback:
                        self.callback(text)
                
        except sr.UnknownValueError:
            # Speech not recognized - this is normal, don't log
            pass
        except sr.RequestError as e:
            self.logger.error(f"Speech recognition service error: {e}")
        except Exception as e:
            self.logger.error(f"Error processing audio: {e}")
    
    def _is_pet_question(self, text: str) -> bool:
        """
        Determine if the recognized text is a question for the pet
        
        Args:
            text: Recognized speech text
            
        Returns:
            True if this appears to be a question for the pet
        """
        text_lower = text.lower().strip()
        
        # Check for direct pet addressing
        pet_names = ['pixie', 'pet', 'assistant']
        for name in pet_names:
            if name in text_lower:
                return True
        
        # Check for question patterns
        question_starters = [
            'what', 'how', 'why', 'when', 'where', 'who', 'which',
            'can you', 'could you', 'would you', 'do you',
            'tell me', 'explain', 'recommend', 'suggest'
        ]
        
        for starter in question_starters:
            if text_lower.startswith(starter):
                return True
        
        # Check for question marks or question-like patterns
        if '?' in text or any(word in text_lower for word in ['recommend', 'suggest', 'help', 'advice']):
            return True
        
        return False
    
    def listen_once(self) -> Optional[str]:
        """
        Listen for a single speech input
        
        Returns:
            Recognized text or None if no speech recognized
        """
        if not self.microphone:
            self.logger.error("Microphone not initialized")
            return None
        
        try:
            self.logger.info("Listening for speech...")
            
            with self.microphone as source:
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio, language='en-US')
            self.logger.info(f"Recognized: '{text}'")
            return text.strip()
            
        except sr.WaitTimeoutError:
            self.logger.info("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            self.logger.info("Could not understand the audio")
            return None
        except sr.RequestError as e:
            self.logger.error(f"Speech recognition service error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error during speech recognition: {e}")
            return None
    
    def set_callback(self, callback: Callable[[str], None]):
        """Set the callback function for recognized speech"""
        self.callback = callback
    
    def test_microphone(self) -> bool:
        """
        Test if the microphone is working
        
        Returns:
            True if microphone test successful
        """
        try:
            if not self.microphone:
                self.logger.error("Microphone not initialized")
                return False
            
            self.logger.info("Testing microphone... Say something!")
            
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            text = self.recognizer.recognize_google(audio)
            self.logger.info(f"Microphone test successful. Heard: '{text}'")
            return True
            
        except Exception as e:
            self.logger.error(f"Microphone test failed: {e}")
            return False