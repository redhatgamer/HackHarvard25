#!/usr/bin/env python3
"""
Test script to try the new British child-like voice
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.speech_manager import SpeechManager

def test_british_child_voice():
    """Test the British child-like voice"""
    print("Testing British child-like voice...")
    
    # Create speech manager with British child settings
    speech_manager = SpeechManager(child_like=True, british_style=True)
    
    if not speech_manager.is_available():
        print("❌ TTS is not available!")
        return False
    
    print("✅ British child-like TTS is ready!")
    
    # Test different phrases that showcase British pronunciation
    test_phrases = [
        "Hullo there! I'm Pixie, your brilliant virtual pet!",
        "That's absolutely lovely! I can't wait to help you!",
        "Right then, let's get started with something fantastic!",
        "I say, this is rather exciting, isn't it?",
        "Blimey! You're asking me to dance? That's brilliant!",
        "I'm feeling quite cheerful today! How about you?",
        "Would you like me to answer some questions? I'd love to help!"
    ]
    
    for i, phrase in enumerate(test_phrases):
        print(f"\n🔊 Testing phrase {i+1}: {phrase}")
        input("Press Enter to hear this phrase...")
        
        result = speech_manager.speak_text(phrase, blocking=True)
        
        if not result:
            print("❌ Failed to speak this phrase")
            return False
    
    print("\n✅ British child voice test completed!")
    print("\nHow did it sound? The voice should be:")
    print("- Faster speech rate (child-like)")
    print("- Higher pitch (Zira voice)")
    print("- British pronunciation (hullo, brilliant, etc.)")
    
    return True

if __name__ == "__main__":
    test_british_child_voice()