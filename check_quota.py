"""
Quick Gemini API Quota Checker
Run this to see your current API status
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_gemini_quota():
    """Check if Gemini API is working and quota status"""
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        return False
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Try to list models to check API access
        print("🔍 Checking Gemini API access...")
        
        # Test with a simple request
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content("Just say 'API Working' - nothing else")
        
        if response.text:
            print("✅ Gemini API is working!")
            print(f"📝 Response: {response.text.strip()}")
            return True
        else:
            print("⚠️ API responded but no content returned")
            return False
            
    except Exception as e:
        error_msg = str(e)
        print("❌ Gemini API Error:")
        print(f"   {error_msg}")
        
        if "429" in error_msg or "quota" in error_msg.lower():
            print("\n🚫 QUOTA EXCEEDED!")
            print("   • You've reached your daily limit (50 requests)")
            print("   • Quota resets at midnight UTC")
            print("   • Pixie will use fallback responses until reset")
        elif "404" in error_msg:
            print("\n🔧 MODEL NOT FOUND!")
            print("   • The gemini-2.0-flash-exp model may not be available")
            print("   • Check available models in Google AI Studio")
        else:
            print("\n🛠️ OTHER API ISSUE!")
            print("   • Check your API key configuration")
            print("   • Verify internet connection")
            
        return False

if __name__ == "__main__":
    print("🦎 Pixie's Gemini API Quota Checker")
    print("=" * 40)
    check_gemini_quota()
    print("\n💡 Tip: Run this anytime to check your API status!")