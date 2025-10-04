#!/usr/bin/env python3
"""
Test the new natural British voice using Google TTS
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.natural_speech_manager import NaturalSpeechManager

def test_natural_british_voice():
    """Test the natural British voice"""
    print("🇬🇧 Testing Natural British Voice with Google TTS...")
    
    # Create natural speech manager
    speech_manager = NaturalSpeechManager(use_gtts=True, british_accent=True)
    
    if not speech_manager.is_available():
        print("❌ Natural TTS is not available!")
        return False
    
    print("✅ Natural British TTS is ready!")
    print(f"Voice info: {speech_manager.get_voice_info()}")
    
    # Test phrases that will showcase natural British pronunciation
    test_phrases = [
        "Hiya! I'm Pixie, your brilliant virtual pet assistant!",
        "That's absolutely smashing! I can't wait to help you today!",
        "Right then, let's get started with something proper ace!",
        "Blimey, this is rather exciting, isn't it? I'm dead chuffed!",
        "Crikey! You want me to dance? That's brilliant, mate!",
        "I'm feeling proper cheerful today! How are you getting on?",
        "Ta very much for asking! I'd love to help you with that!"
    ]
    
    print(f"\nTesting {len(test_phrases)} phrases with natural British accent...")
    print("🔊 Listen for the natural British pronunciation!")
    
    for i, phrase in enumerate(test_phrases):
        print(f"\n📢 Phrase {i+1}: {phrase}")
        input("Press Enter to hear this phrase with natural voice...")
        
        result = speech_manager.speak_text(phrase, blocking=True)
        
        if not result:
            print("❌ Failed to speak this phrase")
            return False
    
    print("\n✅ Natural British voice test completed!")
    print("\n🎭 The voice should now sound:")
    print("- Like a real British person (not robotic!)")
    print("- Natural child-like enthusiasm")
    print("- Proper British accent and vocabulary")
    print("- Much more engaging and lively")
    
    return True

if __name__ == "__main__":
    test_natural_british_voice()