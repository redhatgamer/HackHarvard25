"""
Voice Test for Hiro Demo
Quick diagnostic to get voice input working for your presentation
"""

import speech_recognition as sr
import pyttsx3
import pyaudio
import sys

def test_microphone_access():
    """Test if microphone is accessible"""
    print("🎤 Testing Microphone Access...")
    print("=" * 40)
    
    try:
        # Test PyAudio
        p = pyaudio.PyAudio()
        print("✅ PyAudio initialized successfully")
        
        # List audio devices
        print(f"📊 Found {p.get_device_count()} audio devices:")
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:  # Input device
                print(f"   🎙️ {i}: {info['name']} (Input)")
        
        p.terminate()
        return True
        
    except Exception as e:
        print(f"❌ PyAudio error: {e}")
        return False

def test_speech_recognition():
    """Test speech recognition"""
    print(f"\n🗣️ Testing Speech Recognition...")
    print("=" * 40)
    
    try:
        r = sr.Recognizer()
        
        # Test microphone
        with sr.Microphone() as source:
            print("✅ Microphone connected")
            print("🔊 Adjusting for ambient noise... (2 seconds)")
            r.adjust_for_ambient_noise(source, duration=2)
            print(f"📊 Energy threshold set to: {r.energy_threshold}")
        
        return True
        
    except sr.RequestError as e:
        print(f"❌ Speech Recognition API error: {e}")
        return False
    except Exception as e:
        print(f"❌ Speech Recognition error: {e}")
        return False

def test_text_to_speech():
    """Test text-to-speech"""
    print(f"\n🔊 Testing Text-to-Speech...")
    print("=" * 40)
    
    try:
        # Test pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        print(f"✅ TTS Engine initialized")
        print(f"🎭 Available voices: {len(voices)}")
        for i, voice in enumerate(voices[:3]):  # Show first 3
            print(f"   {i+1}. {voice.name}")
        
        print("🔊 Testing speech output...")
        engine.say("Hello! This is Hiro testing text to speech.")
        engine.runAndWait()
        
        engine.stop()
        return True
        
    except Exception as e:
        print(f"❌ Text-to-Speech error: {e}")
        return False

def quick_voice_test():
    """Quick interactive voice test"""
    print(f"\n🎯 Quick Voice Test (for demo)")
    print("=" * 40)
    
    try:
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            print("🎤 SAY SOMETHING NOW (you have 5 seconds):")
            print("   Try: 'Hello Hiro'")
            
            # Listen for 5 seconds
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            
        print("🤖 Processing your speech...")
        
        # Try to recognize
        text = r.recognize_google(audio)
        print(f"✅ HEARD: '{text}'")
        
        # Respond with TTS
        engine = pyttsx3.init()
        response = f"I heard you say: {text}"
        print(f"🔊 RESPONDING: '{response}'")
        engine.say(response)
        engine.runAndWait()
        engine.stop()
        
        return True
        
    except sr.WaitTimeoutError:
        print("⏰ No speech detected in 5 seconds")
        return False
    except sr.UnknownValueError:
        print("❓ Could not understand audio")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def diagnose_voice_issues():
    """Diagnose common voice issues"""
    print(f"\n🔧 Voice Issue Diagnosis:")
    print("=" * 40)
    
    issues_and_fixes = [
        {
            "issue": "🎤 Microphone not detected",
            "fixes": [
                "Check Windows microphone permissions",
                "Go to Settings > Privacy > Microphone",
                "Allow apps to access microphone",
                "Test microphone in Windows Sound settings"
            ]
        },
        {
            "issue": "🌐 Internet connection required",
            "fixes": [
                "Speech Recognition uses Google API",
                "Ensure stable internet connection",
                "Check firewall/antivirus blocking"
            ]
        },
        {
            "issue": "🔊 Audio drivers",
            "fixes": [
                "Update audio drivers",
                "Restart audio services",
                "Try different microphone/headset"
            ]
        }
    ]
    
    for item in issues_and_fixes:
        print(f"\n{item['issue']}:")
        for fix in item['fixes']:
            print(f"   • {fix}")

def main():
    """Run complete voice diagnostic"""
    print("🎤 Hiro Voice System Diagnostic")
    print("🎯 Getting Voice Ready for Hackathon Demo")
    print("=" * 50)
    
    # Run tests
    mic_ok = test_microphone_access()
    sr_ok = test_speech_recognition()
    tts_ok = test_text_to_speech()
    
    print(f"\n📊 Test Results:")
    print("=" * 30)
    print(f"🎤 Microphone: {'✅ Working' if mic_ok else '❌ Failed'}")
    print(f"🗣️ Speech Recognition: {'✅ Working' if sr_ok else '❌ Failed'}")
    print(f"🔊 Text-to-Speech: {'✅ Working' if tts_ok else '❌ Failed'}")
    
    if all([mic_ok, sr_ok, tts_ok]):
        print(f"\n🎉 All systems working! Ready for voice demo!")
        
        # Try quick test
        print(f"\n🎯 Want to try a quick voice test? (y/n)")
        response = input().lower()
        if response == 'y':
            quick_voice_test()
    else:
        print(f"\n⚠️ Some issues detected...")
        diagnose_voice_issues()

if __name__ == "__main__":
    main()