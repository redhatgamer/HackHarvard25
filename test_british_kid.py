#!/usr/bin/env python3
"""
Test the enhanced British kid voice
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.natural_speech_manager import NaturalSpeechManager

def test_british_kid_voice():
    """Test the British kid voice with enhanced speech patterns"""
    print("🇬🇧👧 Testing Enhanced British Kid Voice...")
    
    # Create natural speech manager for British kid
    speech_manager = NaturalSpeechManager(
        use_gtts=True, 
        british_accent=True, 
        child_like=True
    )
    
    if not speech_manager.is_available():
        print("❌ British kid TTS is not available!")
        return False
    
    print("✅ British kid TTS is ready!")
    print(f"Voice info: {speech_manager.get_voice_info()}")
    
    # Test phrases that showcase British kid speech patterns
    test_phrases = [
        "Hello! I'm Pixie, your awesome virtual pet!",
        "That's really cool! I'm so excited to help you today!",
        "Okay, let's work on something fun together!",
        "Wow, this computer is amazing! Thanks for asking me!",
        "I'm very happy and I think this is great!",
        "Sure, I can help you with that weird problem!",
        "Hey there! Want to do something totally awesome?"
    ]
    
    print(f"\nTesting {len(test_phrases)} phrases with British kid patterns...")
    print("🔊 Listen for proper British kid vocabulary and enthusiasm!")
    
    for i, phrase in enumerate(test_phrases):
        enhanced_phrase = speech_manager._enhance_for_british_speech(phrase)
        print(f"\n📢 Original: {phrase}")
        print(f"🇬🇧 British Kid: {enhanced_phrase}")
        input("Press Enter to hear the British kid version...")
        
        result = speech_manager.speak_text(phrase, blocking=True)  # This will auto-enhance
        
        if not result:
            print("❌ Failed to speak this phrase")
            return False
    
    print("\n✅ British kid voice test completed!")
    print("\n🎭 The voice should now sound like:")
    print("- A proper British child (not American!)")
    print("- Enthusiastic and energetic")
    print("- Uses British kid vocabulary ('dead brilliant', 'proper ace', etc.)")
    print("- Natural British accent with child-like excitement")
    print("- Much more engaging and authentic!")
    
    return True

if __name__ == "__main__":
    test_british_kid_voice()