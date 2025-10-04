"""
Google Sheets Demo Mode
Works without API credentials to show functionality
"""

class DemoSheetsManager:
    """Demo version that simulates Google Sheets operations"""
    
    def __init__(self):
        self.current_sheet_id = None
        self.current_sheet_name = None
        self.demo_data = []
        self.connected = False
    
    def is_connected(self):
        return self.connected
    
    def connect_with_url_or_id(self, url_or_id):
        """Demo connection that always succeeds"""
        # Extract sheet ID for demo
        sheet_id = self.extract_sheet_id_from_url(url_or_id)
        if sheet_id:
            self.current_sheet_id = sheet_id
            self.current_sheet_name = "Demo Sheet"
            self.connected = True
            return True, "✅ Connected to Demo Mode! (No actual Google Sheet connection)"
        else:
            return False, "❌ Invalid URL format. Please check and try again."
    
    @staticmethod 
    def extract_sheet_id_from_url(url):
        """Extract Sheet ID from URL"""
        import re
        patterns = [
            r'/spreadsheets/d/([a-zA-Z0-9-_]+)',
            r'spreadsheets/d/([a-zA-Z0-9-_]+)', 
            r'^([a-zA-Z0-9-_]{44})$',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def append_row(self, data):
        """Demo append - just stores in memory"""
        self.demo_data.append(data)
        return True
    
    def create_project_tracker(self, project_name):
        """Demo project creation"""
        self.demo_data = [
            [f"Project Tracker - {project_name}"],
            [""],
            ["Date", "Task", "Status", "Hours", "Notes"],
            ["2025-10-04", "Initial Setup", "Completed", "1", "Created demo tracker"]
        ]
        return "demo_sheet_id"
    
    def get_sheet_url(self, sheet_id=None):
        """Demo URL"""
        return f"https://docs.google.com/spreadsheets/d/{self.current_sheet_id or 'demo'}/edit"
    
    def get_demo_data(self):
        """Return stored demo data"""
        return self.demo_data