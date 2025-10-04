# Project Structure

## Desktop Pet Application
```
main.py              # Main application entry point
requirements.txt     # Python dependencies
start.bat           # Easy startup script
config/             # Configuration files
  └── settings.json
assets/             # Pet images and resources
  └── pet/
src/                # Core application code
  ├── ai/           # AI/Gemini integration
  ├── pet/          # Pet management and behavior
  ├── screen/       # Screen monitoring
  ├── ui/           # User interface components
  ├── utils/        # Helper utilities
  └── file/         # File management
```

## React Web Interface
```
react-app/          # Complete React application
  ├── package.json  # Node dependencies
  ├── public/       # Static files
  └── src/          # React components
```

## Quick Commands
- **Start Desktop Pet:** `start.bat` or `python main.py`
- **Start Web App:** `cd react-app && npm start`
- **Install Dependencies:** `pip install -r requirements.txt`