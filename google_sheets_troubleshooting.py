"""
Google Sheets Connection Troubleshooting Guide
==================================================

🔍 DIAGNOSING CONNECTION ISSUES:

The main reasons Google Sheets connection fails:

1. ❌ NO API CREDENTIALS
   - Google Sheets requires API authentication
   - You can't connect with just a URL without credentials
   - Solution: Set up Google Cloud API credentials (see below)

2. ❌ INCORRECT URL FORMAT
   - URL should be: https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit
   - Sheet ID is exactly 44 characters long
   - Solution: Copy the full URL from your browser

3. ❌ PERMISSION ISSUES
   - The sheet must be shared with your service account email
   - Service account needs Editor permissions
   - Solution: Share the sheet properly

🚀 QUICK FIX OPTIONS:

Option 1: DEMO MODE (No credentials needed)
==========================================
Run this to test the functionality:

    python demo_google_sheets.py

This shows what Pixie can do without requiring API setup.

Option 2: PROPER API SETUP (Recommended)
========================================

Step 1: Get Google Cloud Credentials
   1. Go to: https://console.cloud.google.com/
   2. Create new project or select existing
   3. Enable "Google Sheets API"
   4. Create Service Account credentials
   5. Download JSON file

Step 2: Configure Pixie
   1. Run: python setup_google_sheets.py
   2. Enter path to your JSON credentials file
   3. Restart Pixie

Step 3: Share Your Sheet
   1. Open your Google Sheet
   2. Click "Share" button
   3. Add the service account email (from JSON file)
   4. Give "Editor" permissions

Step 4: Connect
   1. Right-click Pixie → Google Sheets → Connect to Sheet
   2. Paste your sheet URL or just the Sheet ID
   3. Should connect successfully!

Option 3: QUICK TEST (5 minutes)
================================

Want to test immediately? Here's the fastest way:

1. Create a simple test:
   - Right-click Pixie → Google Sheets → Setup Google Sheets
   - Follow the displayed guide
   - Use a test sheet first before your main one

2. Verify your URL format:
   Your URL should look like:
   https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit

   The Sheet ID is: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms

💡 HELPFUL TIPS:

• The error "not authenticated" = you need API credentials
• The error "invalid format" = check your URL
• The error "permission denied" = share the sheet properly
• Test with a new blank sheet first
• Make sure the sheet is not restricted to your organization only

🛠️ STILL HAVING ISSUES?

1. Check Pixie's logs: Right-click → Settings → View Logs
2. Try the setup script: python setup_google_sheets.py
3. Test the demo: python demo_google_sheets.py
4. Ask Pixie for help: Right-click → Chat with Pixie

The most common issue is missing API credentials. Google Sheets requires 
authentication for security - you can't connect with just a URL.
"""

if __name__ == "__main__":
    print(open(__file__).read().split('"""')[1])