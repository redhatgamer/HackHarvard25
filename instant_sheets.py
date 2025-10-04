"""
Super Simple Google Sheets Integration
No API, no credentials - just works!
"""

import csv
import os
from datetime import datetime
import webbrowser

class InstantSheetsLogger:
    """Log to CSV that can be directly imported to Google Sheets"""
    
    def __init__(self, filename="pixie_log.csv"):
        self.filename = filename
        self.setup_csv()
    
    def setup_csv(self):
        """Create CSV with headers if it doesn't exist"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Activity', 'Description', 'Duration', 'Notes'])
    
    def log_activity(self, activity_type, description, duration_minutes=0, notes=""):
        """Log activity to CSV"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(self.filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, 
                activity_type, 
                description, 
                f"{duration_minutes} min" if duration_minutes > 0 else "",
                notes or "Added by Pixie"
            ])
        
        return True
    
    def get_google_sheets_import_url(self):
        """Generate URL to import CSV directly to Google Sheets"""
        # This opens a new Google Sheet and prompts to import the CSV
        return "https://sheets.google.com/create"
    
    def show_import_instructions(self):
        """Show how to import the CSV to Google Sheets"""
        instructions = f"""
🚀 INSTANT GOOGLE SHEETS INTEGRATION:

1. 📂 Your data is saved in: {os.path.abspath(self.filename)}

2. 📊 Import to Google Sheets:
   - Go to: https://sheets.google.com
   - Click "Blank" to create new sheet
   - Click "File" → "Import" 
   - Upload: {self.filename}
   - Choose "Replace spreadsheet"
   - Click "Import data"

3. ✅ Done! Your Pixie data is now in Google Sheets!

💡 OR use this quick method:
   - Drag and drop {self.filename} into an open Google Sheet
   - It will import automatically!

🔄 Auto-sync: Every time Pixie logs new data, just re-import the file
   to update your Google Sheet with the latest information.
"""
        return instructions

# Demo the instant logger
def demo_instant_sheets():
    print("INSTANT GOOGLE SHEETS INTEGRATION")
    print("=" * 50)
    
    # Create logger
    logger = InstantSheetsLogger("demo_pixie_log.csv")
    
    # Add sample data
    sample_activities = [
        ("Code Review", "Fixed React JSX parsing error", 15, "Issue resolved"),
        ("Feature Development", "Added Google Sheets integration", 45, "Working great!"),
        ("Screen Analysis", "AI detected coding session", 2, "Automatic detection"),
        ("Bug Fix", "Resolved speech bubble sizing", 20, "Dynamic sizing works"),
        ("Planning", "Designed new pet features", 30, "Productive session")
    ]
    
    print("📝 Logging sample activities...")
    for activity, desc, duration, notes in sample_activities:
        logger.log_activity(activity, desc, duration, notes)
        print(f"   ✅ {activity}: {desc}")
    
    print(f"\n📂 Data saved to: {os.path.abspath(logger.filename)}")
    print(logger.show_import_instructions())
    
    # Show the CSV content
    print("\n📋 CSV Content Preview:")
    print("-" * 50)
    with open(logger.filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i < 6:  # Show first 6 lines
                print(f"   {line.strip()}")

if __name__ == "__main__":
    demo_instant_sheets()