"""
Simple Google Sheets Integration - No API Setup Required
Uses Google Apps Script for direct sheet manipulation
"""

import webbrowser
import json
import time
from datetime import datetime
import requests
import urllib.parse

class SimpleGoogleSheets:
    """Simple Google Sheets integration using web methods"""
    
    def __init__(self):
        self.sheet_url = None
        self.sheet_id = None
        self.web_app_url = None
    
    def setup_simple_connection(self, sheet_url):
        """Setup connection with just a Google Sheets URL"""
        self.sheet_url = sheet_url
        self.sheet_id = self.extract_sheet_id(sheet_url)
        return self.sheet_id is not None
    
    def extract_sheet_id(self, url):
        """Extract Sheet ID from URL"""
        import re
        match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
        return match.group(1) if match else None
    
    def create_apps_script_code(self):
        """Generate Google Apps Script code for the user"""
        return '''
function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSheet();
  var data = JSON.parse(e.postData.contents);
  
  // Add row to sheet
  if (data.action === 'addRow') {
    sheet.appendRow(data.row);
    return ContentService.createTextOutput(JSON.stringify({success: true}));
  }
  
  // Get sheet data
  if (data.action === 'getData') {
    var values = sheet.getDataRange().getValues();
    return ContentService.createTextOutput(JSON.stringify({data: values}));
  }
  
  return ContentService.createTextOutput(JSON.stringify({success: false}));
}

function doGet(e) {
  return ContentService.createTextOutput("Pixie Sheets Integration Active!");
}
'''
    
    def generate_setup_instructions(self):
        """Generate step-by-step setup instructions"""
        return f"""
🎯 SIMPLE GOOGLE SHEETS SETUP (5 minutes):

1. 📊 Open your Google Sheet: {self.sheet_url or 'YOUR_SHEET_URL'}

2. 🔧 Add Google Apps Script:
   - Click "Extensions" → "Apps Script"
   - Delete existing code and paste this:

{self.create_apps_script_code()}

3. 🚀 Deploy the script:
   - Click "Deploy" → "New Deployment"
   - Choose "Web app" type
   - Set execute as "Me"
   - Set access to "Anyone"
   - Click "Deploy" and copy the URL

4. 🔗 Connect Pixie:
   - Right-click Pixie → Google Sheets → Enter Web App URL
   - Start logging data!

✨ That's it! No API keys, no credentials, just works!
"""

class WebSheetsManager:
    """Manager for web-based Google Sheets integration"""
    
    def __init__(self, web_app_url=None):
        self.web_app_url = web_app_url
        self.connected = False
    
    def connect(self, web_app_url):
        """Connect to Google Apps Script web app"""
        self.web_app_url = web_app_url.strip()
        try:
            # Test connection
            response = requests.get(self.web_app_url, timeout=5)
            if response.status_code == 200:
                self.connected = True
                return True, "✅ Connected to Google Sheet successfully!"
            else:
                return False, f"❌ Connection failed: HTTP {response.status_code}"
        except Exception as e:
            return False, f"❌ Connection error: {str(e)}"
    
    def add_row(self, row_data):
        """Add a row to the Google Sheet"""
        if not self.connected:
            return False, "Not connected to sheet"
        
        try:
            payload = {
                "action": "addRow",
                "row": row_data
            }
            
            response = requests.post(
                self.web_app_url,
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('success', False), "Row added successfully!"
            else:
                return False, f"Failed to add row: HTTP {response.status_code}"
                
        except Exception as e:
            return False, f"Error adding row: {str(e)}"
    
    def log_activity(self, activity_type, description, duration_minutes=0):
        """Log an activity to the sheet"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [timestamp, activity_type, description, f"{duration_minutes} min", "Added by Pixie 🐾"]
        return self.add_row(row)

def create_simple_sheet_template():
    """Create a template that user can copy to their Google Sheet"""
    template = [
        ["Pixie Activity Log", "", "", "", ""],
        ["", "", "", "", ""],
        ["Timestamp", "Activity Type", "Description", "Duration", "Notes"],
        ["2025-10-04 16:30", "Code Review", "Fixed React JSX error", "15 min", "Completed"],
        ["2025-10-04 16:35", "Integration", "Added Google Sheets support", "30 min", "In Progress"]
    ]
    
    print("📋 Copy this template to your Google Sheet:")
    print("=" * 50)
    for row in template:
        print("\t".join(str(cell) for cell in row))
    
    return template

def demo_simple_integration():
    """Demo the simple integration approach"""
    print("🚀 Simple Google Sheets Integration Demo")
    print("=" * 50)
    
    # Create template
    create_simple_sheet_template()
    
    print("\n💡 How it works:")
    print("1. Copy the template above to your Google Sheet")
    print("2. Add the Apps Script code (provided in setup)")
    print("3. Deploy as web app") 
    print("4. Pixie sends data directly to your sheet!")
    
    print("\n✅ Benefits:")
    print("• No API keys or credentials needed")
    print("• Works with any Google account") 
    print("• Real-time updates")
    print("• Simple 5-minute setup")
    
    print("\n🎯 What Pixie can log:")
    sample_logs = [
        ["Coding Session", "Working on React components", "45 min"],
        ["Bug Fix", "Resolved JSX parsing error", "10 min"],
        ["Feature Add", "Implemented Google Sheets integration", "60 min"],
        ["Screen Analysis", "AI detected productivity patterns", "2 min"],
        ["Break Time", "Coffee and planning next tasks", "15 min"]
    ]
    
    print("\nSample data Pixie would add:")
    for log in sample_logs:
        timestamp = datetime.now().strftime('%H:%M')
        print(f"  {timestamp} | {log[0]} | {log[1]} | {log[2]}")

if __name__ == "__main__":
    demo_simple_integration()