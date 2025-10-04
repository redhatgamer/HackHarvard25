"""
Speech Manager for Text-to-Speech functionality
"""

import pyttsx3
import threading
import logging
from typing import Optional, Dict, Any
import time

class SpeechManager:
    """Manages text-to-speech functionality for the desktop pet"""
    
    def __init__(self, child_like: bool = False, british_style: bool = False):
        self.logger = logging.getLogger(__name__)
        self.engine: Optional[pyttsx3.Engine] = None
        self.is_speaking = False
        self.speech_thread: Optional[threading.Thread] = None
        self.british_style = british_style
        self.child_like = child_like
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize the TTS engine with default settings"""
        try:
            self.engine = pyttsx3.init()
            
            # Configure voice settings
            voices = self.engine.getProperty('voices')
            
            # Try to find a female voice for Pixie
            female_voice = None
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower() or 'hazel' in voice.name.lower():
                    female_voice = voice
                    break
            
            if female_voice:
                self.engine.setProperty('voice', female_voice.id)
                self.logger.info(f"Selected voice: {female_voice.name}")
            
            # Set speech rate (words per minute)
            self.engine.setProperty('rate', 150)  # Slightly slower for clarity
            
            # Set volume (0.0 to 1.0)
            self.engine.setProperty('volume', 0.8)
            
            # Apply child-like settings if requested
            if self.child_like:
                self.set_child_like_voice(british_style=self.british_style)
            
            self.logger.info("TTS engine initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize TTS engine: {e}")
            self.engine = None
    
    def speak_text(self, text: str, blocking: bool = False) -> bool:
        """
        Convert text to speech
        
        Args:
            text: Text to speak
            blocking: If True, wait for speech to complete
            
        Returns:
            bool: True if speech was initiated successfully
        """
        if not self.engine or not text.strip():
            return False
        
        try:
            # Clean the text for better speech
            clean_text = self._clean_text_for_speech(text)
            
            if blocking:
                # Speak synchronously
                self.is_speaking = True
                self.engine.say(clean_text)
                self.engine.runAndWait()
                self.is_speaking = False
            else:
                # Speak asynchronously
                if self.is_speaking:
                    self.stop_speech()
                
                self.speech_thread = threading.Thread(
                    target=self._speak_async,
                    args=(clean_text,),
                    daemon=True
                )
                self.speech_thread.start()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in text-to-speech: {e}")
            self.is_speaking = False
            return False
    
    def _speak_async(self, text: str):
        """Speak text asynchronously in a separate thread"""
        try:
            self.is_speaking = True
            self.engine.say(text)
            self.engine.runAndWait()
            self.is_speaking = False
        except Exception as e:
            self.logger.error(f"Error in async speech: {e}")
            self.is_speaking = False
    
    def _clean_text_for_speech(self, text: str) -> str:
        """Clean text to make it more suitable for speech"""
        # Remove common markdown or formatting
        clean_text = text.replace('*', '').replace('_', '').replace('#', '')
        
        # Replace some symbols with words
        replacements = {
            '&': ' and ',
            '@': ' at ',
            '%': ' percent ',
            '$': ' dollars ',
            '+': ' plus ',
            '=': ' equals ',
            '<': ' less than ',
            '>': ' greater than ',
        }
        
        for symbol, word in replacements.items():
            clean_text = clean_text.replace(symbol, word)
        
        # Apply British pronunciation if enabled
        if self.british_style:
            clean_text = self.add_british_pronunciation_hints(clean_text)
        
        return clean_text.strip()
    
    def stop_speech(self):
        """Stop current speech"""
        if self.engine and self.is_speaking:
            try:
                self.engine.stop()
                self.is_speaking = False
            except Exception as e:
                self.logger.error(f"Error stopping speech: {e}")
    
    def set_voice_properties(self, rate: Optional[int] = None, 
                           volume: Optional[float] = None,
                           voice_id: Optional[str] = None):
        """
        Set voice properties
        
        Args:
            rate: Speech rate in words per minute
            volume: Volume level (0.0 to 1.0)
            voice_id: Voice ID to use
        """
        if not self.engine:
            return
        
        try:
            if rate is not None:
                self.engine.setProperty('rate', rate)
            
            if volume is not None:
                self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
            
            if voice_id is not None:
                voices = self.engine.getProperty('voices')
                for voice in voices:
                    if voice.id == voice_id:
                        self.engine.setProperty('voice', voice_id)
                        break
                        
        except Exception as e:
            self.logger.error(f"Error setting voice properties: {e}")
    
    def set_child_like_voice(self, british_style: bool = False):
        """
        Configure voice to sound more child-like
        
        Args:
            british_style: If True, attempt to use British pronunciation patterns
        """
        if not self.engine:
            return
        
        try:
            # Use Zira (female) voice which sounds younger
            voices = self.engine.getProperty('voices')
            zira_voice = None
            
            for voice in voices:
                if 'zira' in voice.name.lower():
                    zira_voice = voice
                    break
            
            if zira_voice:
                self.engine.setProperty('voice', zira_voice.id)
                self.logger.info(f"Set voice to: {zira_voice.name}")
            
            # Child-like speech characteristics:
            # 1. Faster speech rate (children speak quickly)
            self.engine.setProperty('rate', 180)  # Faster than adult speech
            
            # 2. Slightly higher volume (children are often louder)
            self.engine.setProperty('volume', 0.9)
            
            self.logger.info("Configured child-like voice settings")
            
        except Exception as e:
            self.logger.error(f"Error setting child-like voice: {e}")
    
    def add_british_pronunciation_hints(self, text: str) -> str:
        """
        Add pronunciation hints to make speech sound more British
        
        Args:
            text: Original text
            
        Returns:
            Text with British pronunciation hints
        """
        # British pronunciation replacements
        british_replacements = {
            # R-dropping (non-rhotic)
            'card': 'cahd',
            'car': 'cah',
            'far': 'fah',
            'hard': 'hahd',
            'start': 'staht',
            
            # Short 'a' sound
            'can\'t': 'caahn\'t',
            'dance': 'dahnce',
            'answer': 'ahnswer',
            'ask': 'ahsk',
            'fast': 'fahst',
            
            # Different vowel sounds
            'schedule': 'shedule',
            'privacy': 'priv-uh-see',
            'mobile': 'mo-bile',
            
            # T pronunciation
            'better': 'bet-ter',
            'water': 'wah-ter',
            'butter': 'but-ter',
            
            # British vocabulary
            'awesome': 'brilliant',
            'cool': 'brilliant',
            'great': 'lovely',
            'okay': 'right then',
            'hi': 'hullo',
            'hello': 'hullo',
        }
        
        modified_text = text
        for american, british in british_replacements.items():
            # Use word boundaries to avoid partial matches
            import re
            pattern = r'\b' + re.escape(american) + r'\b'
            modified_text = re.sub(pattern, british, modified_text, flags=re.IGNORECASE)
        
        return modified_text
    
    def get_available_voices(self) -> list:
        """Get list of available voices"""
        if not self.engine:
            return []
        
        try:
            voices = self.engine.getProperty('voices')
            return [{
                'id': voice.id,
                'name': voice.name,
                'language': getattr(voice, 'languages', ['Unknown'])[0] if hasattr(voice, 'languages') else 'Unknown'
            } for voice in voices]
        except Exception as e:
            self.logger.error(f"Error getting voices: {e}")
            return []
    
    def is_available(self) -> bool:
        """Check if TTS is available and working"""
        return self.engine is not None
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_speech()
        if self.speech_thread and self.speech_thread.is_alive():
            self.speech_thread.join(timeout=1.0)