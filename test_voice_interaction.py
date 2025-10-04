#!/usr/bin/env python3
"""
Test Voice Input with Desktop Pet
Simple test to verify voice input and Gemini AI integration
"""

import os
import sys
import asyncio
import logging

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.voice_input_manager import VoiceInputManager
from src.ai.gemini_client import GeminiClient
from src.ui.speech_manager import SpeechManager

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

async def test_voice_interaction():
    """Test voice input with AI response"""
    print("🎤 Voice Input Test with Desktop Pet AI")
    print("=" * 50)
    
    try:
        # Initialize components
        print("Initializing AI client...")
        gemini_client = GeminiClient()
        
        print("Initializing speech output...")
        speech_manager = SpeechManager(child_like=True, british_style=True)
        
        def process_voice_input(text: str):
            """Process voice input and get AI response"""
            print(f"\n🎤 You said: '{text}'")
            
            # Run async response in new event loop
            def handle_async():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    response = loop.run_until_complete(
                        gemini_client.chat_response(message=text)
                    )
                    
                    if response:
                        print(f"🤖 Pixie responds: '{response}'")
                        
                        # Speak the response
                        if speech_manager and speech_manager.is_available():
                            speech_manager.speak_text(response)
                        else:
                            print("⚠️ Speech output not available")
                    else:
                        print("❌ No response from AI")
                        
                except Exception as e:
                    print(f"❌ Error processing response: {e}")
                finally:
                    loop.close()
            
            import threading
            response_thread = threading.Thread(target=handle_async, daemon=True)
            response_thread.start()
        
        print("Initializing voice input...")
        voice_input = VoiceInputManager(callback=process_voice_input)
        
        # Test microphone
        print("\n🔍 Testing microphone...")
        if voice_input.test_microphone():
            print("✅ Microphone test successful!")
        else:
            print("❌ Microphone test failed!")
            return
        
        # Start listening
        print("\n🎧 Starting voice listening...")
        print("💬 Try asking questions like:")
        print("   - 'What flavor of Linux do you recommend?'")
        print("   - 'How do I learn Python?'")
        print("   - 'What's the weather like?'")
        print("\n🛑 Press Ctrl+C to stop")
        
        voice_input.start_listening()
        
        # Keep running until interrupted
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping voice input...")
            voice_input.stop_listening()
            
            if speech_manager:
                speech_manager.cleanup()
            
            print("✅ Voice test completed!")
    
    except Exception as e:
        logger.error(f"Error in voice test: {e}")
        print(f"❌ Test failed: {e}")

def main():
    """Main test function"""
    try:
        asyncio.run(test_voice_interaction())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())