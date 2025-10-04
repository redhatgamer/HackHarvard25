#!/usr/bin/env python3
"""
Test script to verify TTS functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.speech_manager import SpeechManager

def test_speech():
    """Test the speech functionality"""
    print("Testing TTS functionality...")
    
    # Create speech manager
    speech_manager = SpeechManager()
    
    if not speech_manager.is_available():
        print("❌ TTS is not available!")
        return False
    
    print("✅ TTS is available!")
    print(f"Selected voice: {speech_manager.engine.getProperty('voice')}")
    
    # Test speech
    print("🔊 Speaking test message...")
    result = speech_manager.speak_text("Hello! This is Pixie, your virtual pet assistant. The speech functionality is working correctly!", blocking=True)
    
    if result:
        print("✅ Speech test completed successfully!")
        return True
    else:
        print("❌ Speech test failed!")
        return False

if __name__ == "__main__":
    test_speech()