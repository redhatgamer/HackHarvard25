"""
Google Sheets Setup Helper
Simple script to help set up Google Sheets integration
"""

import json
import os
from pathlib import Path

def setup_google_sheets_config():
    """Setup Google Sheets configuration"""
    
    print("🚀 Google Sheets Integration Setup")
    print("=" * 50)
    
    config_path = Path("config/settings.json")
    
    # Load existing config
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        print("❌ Config file not found!")
        return False
    
    print("\n📋 Setup Options:")
    print("1. 🔑 Set up Service Account (Recommended for automation)")
    print("2. 📄 Show setup instructions")
    print("3. ✅ Test connection")
    
    choice = input("\nChoose option (1-3): ").strip()
    
    if choice == "1":
        credentials_path = input("Enter path to your service account JSON file: ").strip()
        
        if os.path.exists(credentials_path):
            # Add to config
            if "integrations" not in config:
                config["integrations"] = {}
            
            config["integrations"]["google_sheets"] = {
                "enabled": True,
                "credentials_path": credentials_path
            }
            
            # Save config
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"✅ Configuration saved! Credentials path: {credentials_path}")
            print("🔄 Restart your pet to activate Google Sheets integration.")
            
        else:
            print("❌ Credentials file not found!")
            
    elif choice == "2":
        show_setup_instructions()
        
    elif choice == "3":
        test_connection()
    
    else:
        print("Invalid choice!")

def show_setup_instructions():
    """Show detailed setup instructions"""
    
    instructions = """
🛠️ Google Sheets API Setup Instructions:

1. 🌐 Go to Google Cloud Console:
   https://console.cloud.google.com/

2. 📁 Create or select a project:
   - Click "New Project" or select existing
   - Note the project ID

3. 🔌 Enable Google Sheets API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

4. 🔑 Create Service Account:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in details and create

5. 📁 Download Credentials:
   - Click on your service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Choose JSON format and download

6. 📊 Share your Google Sheet:
   - Open your Google Sheet
   - Click "Share"
   - Add the service account email (from JSON file)
   - Give "Editor" permissions

7. 🔗 Get Sheet ID:
   - From your sheet URL: https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit
   - Copy the SHEET_ID part

8. 🐾 Configure Pixie:
   - Run this setup script
   - Enter your credentials file path
   - Restart Pixie

✨ You're ready to go!
"""
    
    print(instructions)

def test_connection():
    """Test Google Sheets connection"""
    
    try:
        from src.integrations.google_sheets_manager import GoogleSheetsManager
        
        config_path = Path("config/settings.json")
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            sheets_config = config.get('integrations', {}).get('google_sheets', {})
            credentials_path = sheets_config.get('credentials_path')
            
            if credentials_path and os.path.exists(credentials_path):
                print("🔍 Testing connection...")
                
                manager = GoogleSheetsManager(credentials_path)
                if manager.is_connected():
                    print("✅ Google Sheets connection successful!")
                    
                    # Test creating a simple sheet
                    test_sheet_id = manager.create_sheet("Pixie Test Sheet", [
                        ["Pixie Test", "Status"],
                        ["Connection Test", "✅ Success!"],
                        ["Timestamp", str(datetime.now())]
                    ])
                    
                    if test_sheet_id:
                        sheet_url = manager.get_sheet_url(test_sheet_id)
                        print(f"🎉 Test sheet created: {sheet_url}")
                    
                else:
                    print("❌ Failed to connect to Google Sheets")
            else:
                print("❌ No credentials file configured")
        else:
            print("❌ Config file not found")
            
    except ImportError:
        print("❌ Google Sheets dependencies not installed")
        print("💡 Run: pip install google-api-python-client google-auth-oauthlib google-auth")
    except Exception as e:
        print(f"❌ Error testing connection: {e}")

if __name__ == "__main__":
    from datetime import datetime
    setup_google_sheets_config()