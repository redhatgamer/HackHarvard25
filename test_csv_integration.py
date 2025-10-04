"""
Test CSV Integration with Google Sheets

This script demonstrates the simple 30-second Google Sheets integration 
using CSV export instead of complex API setup.
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.integrations.csv_logger import CSVSheetsLogger
import time

async def main():
    print("🔍 Testing CSV to Google Sheets Integration")
    print("=" * 50)
    
    # Initialize CSV logger
    csv_logger = CSVSheetsLogger()
    
    # Log some sample activities
    print("\n📝 Creating sample data...")
    
    activities = [
        ("Python Development", "Fixed JSX parsing errors", 45),
        ("UI Design", "Streamlined context menu", 30), 
        ("Bug Fixes", "Fixed speech bubble sizing", 25),
        ("Integration", "Added Google Sheets CSV export", 60),
        ("Testing", "Validated CSV workflow", 15)
    ]
    
    for activity, description, duration in activities:
        success = csv_logger.log_activity(activity, description, duration, "", "Demo")
        print(f"  ✅ Logged: {activity} - {description}")
        time.sleep(0.1)  # Small delay for realistic timing
    
    # Show file info
    print(f"\n📊 CSV File Location: {csv_logger.get_file_path()}")
    print(f"📈 Total Entries: {csv_logger.get_row_count()}")
    
    # Show import instructions
    print("\n" + "="*50)
    print("📋 GOOGLE SHEETS IMPORT INSTRUCTIONS")
    print("="*50)
    print(csv_logger.get_import_instructions())
    
    # Offer to open file location
    print("\n🔧 Would you like to open the CSV file location? (y/n): ", end="")
    response = input().lower().strip()
    
    if response == 'y':
        try:
            import os
            csv_path = csv_logger.get_file_path()
            os.system(f'explorer /select,"{csv_path}"')
            print("✅ Opened file location!")
        except Exception as e:
            print(f"❌ Error opening file: {e}")
    
    print("\n🎉 CSV Integration test complete!")
    print("💡 Now you can drag the CSV file into Google Sheets for instant import!")

if __name__ == "__main__":
    asyncio.run(main())