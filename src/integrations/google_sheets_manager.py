"""
Google Sheets Manager
Handles integration with Google Sheets API for data manipulation
"""

import logging
from typing import List, Dict, Any, Optional, Union
import json
import os
from pathlib import Path
import time
from datetime import datetime
import asyncio

try:
    from google.oauth2.credentials import Credentials
    from google.oauth2 import service_account
    from google_auth_oauthlib.flow import Flow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

class GoogleSheetsManager:
    """Manages Google Sheets operations for the virtual pet"""
    
    def __init__(self, credentials_path: str = None):
        self.logger = logging.getLogger(__name__)
        self.service = None
        self.credentials = None
        self.current_sheet_id = None
        self.current_sheet_name = None
        
        if not GOOGLE_AVAILABLE:
            self.logger.warning("Google API libraries not available. Install with: pip install google-api-python-client google-auth-oauthlib google-auth")
            return
        
        # Try to initialize with credentials
        if credentials_path and os.path.exists(credentials_path):
            self._authenticate_with_service_account(credentials_path)
        else:
            self.logger.info("No credentials provided. Use setup_oauth() or setup_service_account() to authenticate.")
    
    def _authenticate_with_service_account(self, credentials_path: str):
        """Authenticate using service account credentials"""
        try:
            self.credentials = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            self.service = build('sheets', 'v4', credentials=self.credentials)
            self.logger.info("Successfully authenticated with Google Sheets using service account")
            return True
        except Exception as e:
            self.logger.error(f"Service account authentication failed: {e}")
            return False
    
    def setup_oauth(self, client_secrets_path: str, port: int = 8080):
        """Setup OAuth2 authentication (for personal use)"""
        if not GOOGLE_AVAILABLE:
            return False
        
        try:
            flow = Flow.from_client_secrets_file(
                client_secrets_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets'],
                redirect_uri=f'http://localhost:{port}'
            )
            
            # Get authorization URL
            auth_url, _ = flow.authorization_url(prompt='consent')
            
            self.logger.info(f"Please visit this URL to authorize the application: {auth_url}")
            
            # This is a simplified version - in practice you'd handle the callback
            # For now, we'll use service account approach which is easier for automation
            return False
            
        except Exception as e:
            self.logger.error(f"OAuth setup failed: {e}")
            return False
    
    def is_connected(self) -> bool:
        """Check if connected to Google Sheets"""
        return self.service is not None
    
    def create_sheet(self, title: str, initial_data: List[List[str]] = None) -> Optional[str]:
        """Create a new Google Sheet"""
        if not self.is_connected():
            self.logger.error("Not connected to Google Sheets")
            return None
        
        try:
            spreadsheet = {
                'properties': {
                    'title': title
                }
            }
            
            result = self.service.spreadsheets().create(body=spreadsheet).execute()
            sheet_id = result.get('spreadsheetId')
            
            self.current_sheet_id = sheet_id
            self.current_sheet_name = title
            
            # Add initial data if provided
            if initial_data:
                self.write_data('A1', initial_data)
            
            self.logger.info(f"Created new sheet: {title} (ID: {sheet_id})")
            return sheet_id
            
        except HttpError as e:
            self.logger.error(f"Failed to create sheet: {e}")
            return None
    
    def connect_to_sheet(self, sheet_id: str, sheet_name: str = None) -> bool:
        """Connect to an existing Google Sheet"""
        if not self.is_connected():
            return False
        
        try:
            # Test connection by getting sheet metadata
            result = self.service.spreadsheets().get(spreadsheetId=sheet_id).execute()
            
            self.current_sheet_id = sheet_id
            self.current_sheet_name = sheet_name or result.get('properties', {}).get('title', 'Unknown')
            
            self.logger.info(f"Connected to sheet: {self.current_sheet_name} (ID: {sheet_id})")
            return True
            
        except HttpError as e:
            self.logger.error(f"Failed to connect to sheet: {e}")
            return False
    
    def write_data(self, range_name: str, data: Union[List[List], List[str]], sheet_id: str = None) -> bool:
        """Write data to a specific range in the sheet"""
        if not self.is_connected():
            return False
        
        target_sheet_id = sheet_id or self.current_sheet_id
        if not target_sheet_id:
            self.logger.error("No sheet ID provided or connected")
            return False
        
        try:
            # Ensure data is in correct format
            if isinstance(data[0], str):
                data = [data]  # Single row
            
            body = {
                'values': data
            }
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=target_sheet_id,
                range=range_name,
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            
            self.logger.info(f"Updated {result.get('updatedCells', 0)} cells in range {range_name}")
            return True
            
        except HttpError as e:
            self.logger.error(f"Failed to write data: {e}")
            return False
    
    def append_row(self, data: List[str], sheet_name: str = "Sheet1", sheet_id: str = None) -> bool:
        """Append a row to the end of the sheet"""
        if not self.is_connected():
            return False
        
        target_sheet_id = sheet_id or self.current_sheet_id
        if not target_sheet_id:
            return False
        
        try:
            body = {
                'values': [data]
            }
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=target_sheet_id,
                range=f"{sheet_name}!A:Z",
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            
            self.logger.info(f"Appended row with {len(data)} values")
            return True
            
        except HttpError as e:
            self.logger.error(f"Failed to append row: {e}")
            return False
    
    def read_data(self, range_name: str, sheet_id: str = None) -> Optional[List[List[str]]]:
        """Read data from a specific range"""
        if not self.is_connected():
            return None
        
        target_sheet_id = sheet_id or self.current_sheet_id
        if not target_sheet_id:
            return None
        
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=target_sheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            self.logger.info(f"Read {len(values)} rows from {range_name}")
            return values
            
        except HttpError as e:
            self.logger.error(f"Failed to read data: {e}")
            return None
    
    def clear_range(self, range_name: str, sheet_id: str = None) -> bool:
        """Clear data from a specific range"""
        if not self.is_connected():
            return False
        
        target_sheet_id = sheet_id or self.current_sheet_id
        if not target_sheet_id:
            return False
        
        try:
            self.service.spreadsheets().values().clear(
                spreadsheetId=target_sheet_id,
                range=range_name,
                body={}
            ).execute()
            
            self.logger.info(f"Cleared range {range_name}")
            return True
            
        except HttpError as e:
            self.logger.error(f"Failed to clear range: {e}")
            return False
    
    def format_cells(self, range_name: str, format_options: Dict, sheet_id: str = None) -> bool:
        """Format cells in a specific range"""
        if not self.is_connected():
            return False
        
        target_sheet_id = sheet_id or self.current_sheet_id
        if not target_sheet_id:
            return False
        
        try:
            # This is a simplified formatting - can be expanded
            requests = [{
                'repeatCell': {
                    'range': self._parse_range(range_name),
                    'cell': {
                        'userEnteredFormat': format_options
                    },
                    'fields': 'userEnteredFormat'
                }
            }]
            
            body = {'requests': requests}
            
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=target_sheet_id,
                body=body
            ).execute()
            
            self.logger.info(f"Formatted range {range_name}")
            return True
            
        except HttpError as e:
            self.logger.error(f"Failed to format cells: {e}")
            return False
    
    def _parse_range(self, range_name: str) -> Dict:
        """Parse range name into sheet API format (simplified)"""
        # This is a basic implementation - would need more sophisticated parsing
        return {
            'sheetId': 0,  # Assuming first sheet for now
            'startRowIndex': 0,
            'endRowIndex': 10,
            'startColumnIndex': 0,
            'endColumnIndex': 5
        }
    
    def create_project_tracker(self, project_name: str) -> Optional[str]:
        """Create a pre-formatted project tracking sheet"""
        headers = [
            ['Project Tracker - ' + project_name, '', '', '', ''],
            ['', '', '', '', ''],
            ['Date', 'Task', 'Status', 'Hours', 'Notes'],
            [datetime.now().strftime('%Y-%m-%d'), 'Project Setup', 'In Progress', '1', 'Initial setup and configuration']
        ]
        
        sheet_id = self.create_sheet(f"{project_name} - Project Tracker", headers)
        
        if sheet_id:
            # Format headers
            self.format_cells('A1:E1', {
                'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 1.0},
                'textFormat': {'bold': True, 'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0}}
            })
            
            self.format_cells('A3:E3', {
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9},
                'textFormat': {'bold': True}
            })
        
        return sheet_id
    
    def log_coding_session(self, file_name: str, duration_minutes: int, description: str = "") -> bool:
        """Log a coding session to the current sheet"""
        if not self.current_sheet_id:
            return False
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        row_data = [timestamp, f"Coding: {file_name}", "Completed", str(duration_minutes/60), description]
        
        return self.append_row(row_data)
    
    def get_sheet_url(self, sheet_id: str = None) -> Optional[str]:
        """Get the web URL for the sheet"""
        target_sheet_id = sheet_id or self.current_sheet_id
        if target_sheet_id:
            return f"https://docs.google.com/spreadsheets/d/{target_sheet_id}/edit"
        return None
    
    @staticmethod
    def extract_sheet_id_from_url(url: str) -> Optional[str]:
        """Extract Sheet ID from Google Sheets URL"""
        import re
        
        # Pattern to match Google Sheets URLs
        patterns = [
            r'/spreadsheets/d/([a-zA-Z0-9-_]+)',  # Standard URL
            r'spreadsheets/d/([a-zA-Z0-9-_]+)',   # Without leading slash
            r'^([a-zA-Z0-9-_]{44})$',              # Just the ID (44 characters)
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def connect_with_url_or_id(self, url_or_id: str) -> tuple[bool, str]:
        """Connect using URL or Sheet ID, returns (success, message)"""
        # Extract sheet ID from URL if needed
        sheet_id = self.extract_sheet_id_from_url(url_or_id.strip())
        
        if not sheet_id:
            return False, "❌ Invalid Google Sheets URL or ID. Please check the format."
        
        # Check if we have authentication
        if not self.is_connected():
            return False, "🔑 Google Sheets API not authenticated. Please set up credentials first."
        
        # Try to connect
        success = self.connect_to_sheet(sheet_id)
        if success:
            return True, f"✅ Connected to Google Sheet successfully!"
        else:
            return False, "❌ Failed to connect. Check if the sheet exists and you have permission."

# Simple connection helper for easy setup
def create_simple_sheets_connection():
    """Create a simple sheets manager for quick testing"""
    # This will be enhanced once we have proper credentials setup
    return GoogleSheetsManager()