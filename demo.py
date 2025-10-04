#!/usr/bin/env python3
"""
Quick demo/test script for the Virtual Pet AI Assistant
Run this to test basic functionality without the full GUI
"""

import sys
import os
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.config_manager import ConfigManager
from src.utils.logger import setup_logging
from src.screen.screen_monitor import ScreenMonitor
from src.ai.gemini_client import GeminiClient

async def test_screen_capture():
    """Test screen capture functionality"""
    print("🖥️  Testing screen capture...")
    
    try:
        monitor = ScreenMonitor()
        
        # Get screenshot
        screenshot = monitor.get_screenshot()
        print(f"✅ Screenshot captured: {screenshot.size}")
        
        # Get window info
        window_info = monitor.get_active_window_info()
        print(f"✅ Active window: {window_info['title']}")
        
        # Get app type
        app_type = monitor.detect_application_type(window_info)
        print(f"✅ App type detected: {app_type}")
        
        return True
        
    except Exception as e:
        print(f"❌ Screen capture test failed: {e}")
        return False

async def test_config_manager():
    """Test configuration management"""
    print("⚙️  Testing configuration...")
    
    try:
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        pet_name = config_manager.get_setting("pet.name", config)
        print(f"✅ Pet name from config: {pet_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

async def test_gemini_client():
    """Test Gemini AI client (if API key is available)"""
    print("🤖 Testing Gemini AI client...")
    
    try:
        # Check if API key is available
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == 'your_gemini_api_key_here':
            print("⚠️  No valid Gemini API key found. Skipping AI test.")
            print("   Add your API key to .env file to test AI functionality")
            return True
        
        client = GeminiClient()
        
        # Test simple chat
        response = await client.chat_response("Hello! Can you introduce yourself?")
        print(f"✅ AI Response: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini client test failed: {e}")
        print("   Make sure you have a valid API key in .env file")
        return False

async def run_basic_demo():
    """Run a basic demonstration without GUI"""
    print("🐱 Virtual Pet AI Assistant - Basic Demo")
    print("=" * 50)
    
    setup_logging("INFO", False)  # Console logging only
    
    # Run tests
    tests = [
        ("Configuration Manager", test_config_manager),
        ("Screen Capture", test_screen_capture),
        ("Gemini AI Client", test_gemini_client)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        try:
            success = await test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! The system is ready to run.")
        print("💡 Run 'python main.py' to start the full application with GUI")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")
        print("💡 Run 'python setup.py' to fix common issues")
    
    return passed == len(results)

if __name__ == "__main__":
    try:
        success = asyncio.run(run_basic_demo())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Demo crashed: {e}")
        sys.exit(1)