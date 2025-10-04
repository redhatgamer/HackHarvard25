"""
CSV Logger for Google Sheets Integration
Simple CSV export that can be directly imported to Google Sheets
"""

import csv
import os
from datetime import datetime
from pathlib import Path
import logging

class CSVSheetsLogger:
    """Simple CSV logger for Google Sheets integration"""
    
    def __init__(self, filename="pixie_activity_log.csv"):
        self.filename = filename
        self.logger = logging.getLogger(__name__)
        self.setup_csv()
    
    def setup_csv(self):
        """Create CSV with headers if it doesn't exist"""
        try:
            if not os.path.exists(self.filename):
                with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Timestamp', 'Activity Type', 'Description', 'Duration', 'File/Context', 'Notes'])
                self.logger.info(f"Created new CSV log file: {self.filename}")
        except Exception as e:
            self.logger.error(f"Failed to setup CSV: {e}")
    
    def log_activity(self, activity_type, description, duration_minutes=0, context="", notes="Added by Pixie"):
        """Log activity to CSV"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            duration_str = f"{duration_minutes} min" if duration_minutes > 0 else ""
            
            with open(self.filename, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    timestamp,
                    activity_type,
                    description,
                    duration_str,
                    context,
                    notes
                ])
            
            self.logger.info(f"Logged to CSV: {activity_type} - {description}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to log to CSV: {e}")
            return False
    
    def log_coding_session(self, file_name, action="Coding", duration_minutes=0):
        """Log a coding session"""
        return self.log_activity(
            "Coding Session",
            f"{action} in {file_name}",
            duration_minutes,
            file_name,
            "Automatic detection"
        )
    
    def log_screen_analysis(self, analysis_result, confidence=None):
        """Log screen analysis result"""
        description = analysis_result[:100] + "..." if len(analysis_result) > 100 else analysis_result
        notes = f"AI Analysis (Confidence: {confidence}%)" if confidence else "AI Analysis"
        
        return self.log_activity(
            "Screen Analysis",
            description,
            0,
            "Screen capture",
            notes
        )
    
    def log_error_fix(self, error_type, solution, file_name=""):
        """Log when an error is fixed"""
        return self.log_activity(
            "Bug Fix",
            f"Fixed {error_type}: {solution}",
            0,
            file_name,
            "Problem resolved"
        )
    
    def log_ai_interaction(self, user_question, ai_response):
        """Log AI chat interactions"""
        description = f"Q: {user_question[:50]}... A: {ai_response[:50]}..."
        return self.log_activity(
            "AI Chat",
            description,
            0,
            "Chat interaction",
            "Pixie conversation"
        )
    
    def get_file_path(self):
        """Get absolute path to the CSV file"""
        return os.path.abspath(self.filename)
    
    def get_import_instructions(self):
        """Get instructions for importing to Google Sheets"""
        return f"""
Google Sheets Import Instructions:

1. Go to https://sheets.google.com
2. Create a new blank sheet
3. Drag and drop this file into the sheet: {self.get_file_path()}
4. Choose "Replace spreadsheet" when prompted
5. Your Pixie activity log is now in Google Sheets!

Auto-update: Each time Pixie logs new activities, re-import the file to update your sheet.
"""
    
    def get_row_count(self):
        """Get number of rows in the CSV (excluding header)"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return sum(1 for line in f) - 1  # Subtract header row
        except:
            return 0