"""
Enhanced Speech Manager with Google TTS for natural British voices
"""

import pyttsx3
import threading
import logging
import tempfile
import os
import io
from typing import Optional, Dict, Any
import time

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    gTTS = None

try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    pygame = None

class NaturalSpeechManager:
    """Enhanced speech manager with natural British voices using Google TTS"""
    
    def __init__(self, use_gtts: bool = True, british_accent: bool = True, child_like: bool = True):
        self.logger = logging.getLogger(__name__)
        self.use_gtts = use_gtts and GTTS_AVAILABLE and PYGAME_AVAILABLE
        self.british_accent = british_accent
        self.child_like = child_like
        self.is_speaking = False
        
        # Fallback to pyttsx3 if gTTS not available
        self.pyttsx_engine = None
        
        # gTTS settings for British kid
        if self.use_gtts:
            # Use British English accent codes
            self.tts_lang = 'en'  # English
            self.tld = 'co.uk' if british_accent else 'com'  # British (.co.uk) or American (.com)
            
            # Child-like settings - use faster speech (slow=False) which sounds more energetic/youthful
            self.slow_speech = False  # Faster = more child-like energy
            
            self.logger.info(f"Using Google TTS - British {'Kid' if child_like else 'Adult'} Voice")
        else:
            self._init_pyttsx()
            self.logger.warning("Google TTS not available, using fallback pyttsx3")
    
    def _init_pyttsx(self):
        """Initialize pyttsx3 as fallback"""
        try:
            self.pyttsx_engine = pyttsx3.init()
            
            # Configure for British-like settings
            voices = self.pyttsx_engine.getProperty('voices')
            
            # Prefer Zira (female) for more youthful sound
            for voice in voices:
                if 'zira' in voice.name.lower():
                    self.pyttsx_engine.setProperty('voice', voice.id)
                    break
            
            # Child-like settings
            self.pyttsx_engine.setProperty('rate', 180)
            self.pyttsx_engine.setProperty('volume', 0.9)
            
        except Exception as e:
            self.logger.error(f"Failed to initialize pyttsx3: {e}")
            self.pyttsx_engine = None
    
    def speak_text(self, text: str, blocking: bool = False) -> bool:
        """
        Speak text with natural British voice
        
        Args:
            text: Text to speak
            blocking: If True, wait for speech to complete
            
        Returns:
            bool: True if speech was initiated successfully
        """
        if not text.strip():
            return False
        
        try:
            if self.use_gtts:
                return self._speak_with_gtts(text, blocking)
            else:
                return self._speak_with_pyttsx(text, blocking)
                
        except Exception as e:
            self.logger.error(f"Error in speech: {e}")
            return False
    
    def _speak_with_gtts(self, text: str, blocking: bool = False) -> bool:
        """Speak using Google TTS for natural British accent"""
        try:
            if self.is_speaking and not blocking:
                self.stop_speech()
            
            # Enhance text for British speech
            british_text = self._enhance_for_british_speech(text)
            
            if blocking:
                self._gtts_speak_sync(british_text)
            else:
                thread = threading.Thread(
                    target=self._gtts_speak_sync,
                    args=(british_text,),
                    daemon=True
                )
                thread.start()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error with Google TTS: {e}")
            return self._speak_with_pyttsx(text, blocking)  # Fallback
    
    def _gtts_speak_sync(self, text: str):
        """Synchronously generate and play speech with gTTS"""
        try:
            self.is_speaking = True
            
            # Create gTTS object with British kid settings
            # Use slow=False for energetic child-like speed
            tts = gTTS(
                text=text,
                lang=self.tts_lang,
                tld=self.tld,
                slow=self.slow_speech  # Fast speech for child-like energy
            )
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tmp_path = tmp_file.name
                tts.write_to_fp(tmp_file)
            
            # Play the audio
            if PYGAME_AVAILABLE:
                pygame.mixer.music.load(tmp_path)
                pygame.mixer.music.play()
                
                # Wait for playback to complete
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
            
            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except:
                pass
                
        except Exception as e:
            self.logger.error(f"Error in gTTS playback: {e}")
        finally:
            self.is_speaking = False
    
    def _speak_with_pyttsx(self, text: str, blocking: bool = False) -> bool:
        """Fallback to pyttsx3"""
        if not self.pyttsx_engine:
            return False
        
        try:
            # Enhance text for British pronunciation
            british_text = self._enhance_for_british_speech(text)
            
            if blocking:
                self.is_speaking = True
                self.pyttsx_engine.say(british_text)
                self.pyttsx_engine.runAndWait()
                self.is_speaking = False
            else:
                if self.is_speaking:
                    self.stop_speech()
                
                thread = threading.Thread(
                    target=self._pyttsx_speak_async,
                    args=(british_text,),
                    daemon=True
                )
                thread.start()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error with pyttsx3: {e}")
            return False
    
    def _pyttsx_speak_async(self, text: str):
        """Async pyttsx3 speech"""
        try:
            self.is_speaking = True
            self.pyttsx_engine.say(text)
            self.pyttsx_engine.runAndWait()
        except Exception as e:
            self.logger.error(f"Error in async pyttsx3 speech: {e}")
        finally:
            self.is_speaking = False
    
    def _enhance_for_british_speech(self, text: str) -> str:
        """Enhance text for British pronunciation and child-like speech patterns"""
        
        # Clean text first
        clean_text = text.replace('*', '').replace('_', '').replace('#', '')
        
        # British kid vocabulary and expressions
        british_kid_replacements = {
            # Basic American -> British kid
            'awesome': 'dead brilliant',
            'cool': 'proper ace',
            'great': 'dead good',
            'amazing': 'absolutely smashing',
            'fantastic': 'dead brilliant',
            'wonderful': 'lovely',
            'excellent': 'top notch',
            'perfect': 'spot on',
            
            # Greetings & responses (kid-like)
            'okay': 'righto',
            'ok': 'righto', 
            'hi': 'hiya',
            'hello': 'hiya there',
            'hey': 'oi oi',
            'hey there': 'hiya mate',
            'thanks': 'cheers mate',
            'thank you': 'ta loads',
            'you\'re welcome': 'no worries mate',
            'sure': 'dead cert',
            'yes': 'yeah mate',
            'no': 'nah mate',
            
            # Emotions (British kid style)
            'excited': 'dead chuffed',
            'happy': 'chuffed to bits',
            'sad': 'proper gutted',
            'angry': 'well cross',
            'surprised': 'gobsmacked',
            'confused': 'proper muddled',
            'tired': 'dead knackered',
            'hungry': 'dead peckish',
            'thirsty': 'gasping',
            
            # Actions (British kid)
            'quickly': 'dead quick',
            'slowly': 'dead slow',
            'carefully': 'dead careful like',
            'immediately': 'right now',
            'later': 'in a bit',
            'soon': 'dead soon',
            
            # British items kids know
            'candy': 'sweets',
            'cookies': 'biscuits', 
            'soda': 'fizzy drink',
            'french fries': 'chips',
            'chips': 'crisps',
            'soccer': 'footy',
            'vacation': 'hols',
            'bathroom': 'loo',
            'elevator': 'lift',
            'apartment': 'flat',
            'garbage': 'rubbish',
            'flashlight': 'torch',
            'sweater': 'jumper',
            
            # Intensifiers (British kid style)
            'very': 'dead',
            'really': 'proper',
            'quite': 'dead',
            'so': 'well',
            'totally': 'dead',
            'completely': 'proper',
            
            # Kid expressions
            'weird': 'dead weird',
            'strange': 'proper odd',
            'funny': 'dead funny',
            'silly': 'daft',
            'stupid': 'barmy',
            'crazy': 'mental',
            'loud': 'dead loud',
            'quiet': 'dead quiet',
            
            # Enthusiasm 
            'wow': 'blimey',
            'whoa': 'crikey',
            'oh my': 'blimey me',
            'gosh': 'crikey',
            'jeez': 'blimey',
            'darn': 'bloomin\' heck',
            'shoot': 'blooming heck',
        }
        
        # Apply British kid vocabulary (sort by length to avoid partial replacements)
        import re
        sorted_replacements = sorted(british_kid_replacements.items(), key=lambda x: len(x[0]), reverse=True)
        
        for american, british_kid in sorted_replacements:
            pattern = r'\b' + re.escape(american) + r'\b'
            clean_text = re.sub(pattern, british_kid, clean_text, flags=re.IGNORECASE)
        
        # Add British child-like speech patterns
        if self.british_accent:
            # Add kid-like sentence starters (randomly)
            import random
            kid_starters = [
                'Right then, ',
                'Blimey, ',
                'Crikey, ',
                'I say, ',
                'Cor, ',
                'Well, ',
                'Righto, '
            ]
            
            # Add enthusiastic endings for statements
            kid_endings = [
                ', innit!',
                ', mate!', 
                ', which is dead good!',
                ', and that\'s brilliant!',
                ', proper ace that is!',
                ', dead chuffed about that!'
            ]
            
            # Sometimes add starter (30% chance for variety)
            if random.random() < 0.3 and len(clean_text) > 15:
                starter = random.choice(kid_starters)
                if not any(clean_text.startswith(s.strip()) for s in kid_starters):
                    clean_text = starter + clean_text
            
            # Sometimes add enthusiastic ending (40% chance)
            if random.random() < 0.4 and len(clean_text) > 10:
                if clean_text.endswith('.') or clean_text.endswith('!'):
                    ending = random.choice(kid_endings)
                    clean_text = clean_text[:-1] + ending
            
            # Add typical British kid phrases for certain contexts
            if 'help' in clean_text.lower() and 'you' in clean_text.lower():
                clean_text = clean_text.replace('help you', 'give you a hand, mate')
            
            if 'computer' in clean_text.lower():
                clean_text = clean_text.replace('computer', 'this dead clever computer')
                
            if 'work' in clean_text.lower():
                clean_text = clean_text.replace('work', 'sort this out')
        
        return clean_text
    
    def stop_speech(self):
        """Stop current speech"""
        try:
            if PYGAME_AVAILABLE and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            
            if self.pyttsx_engine:
                self.pyttsx_engine.stop()
                
        except Exception as e:
            self.logger.error(f"Error stopping speech: {e}")
        finally:
            self.is_speaking = False
    
    def is_available(self) -> bool:
        """Check if speech is available"""
        return self.use_gtts or (self.pyttsx_engine is not None)
    
    def get_voice_info(self) -> str:
        """Get information about current voice"""
        if self.use_gtts:
            accent = "British" if self.british_accent else "American"
            return f"Google TTS - {accent} English (Natural)"
        elif self.pyttsx_engine:
            return "Microsoft TTS - Enhanced British"
        else:
            return "No TTS available"
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_speech()
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.quit()
            except:
                pass