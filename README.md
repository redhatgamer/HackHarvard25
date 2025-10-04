# Virtual Pet AI Assistant 🐱🤖

A delightful AI-powered virtual pet that sits on your desktop and helps you with whatever you're working on! Using Google's Gemini AI, this smart companion provides contextual assistance and keeps you company while you work.

## ✨ Features

### 🎨 **Modern Pet Interface**
- **Animated Virtual Pet**: Adorable pet character with smooth animations
- **Drag & Drop**: Move your pet anywhere on screen
- **Interactive Experience**: Click and interact with your pet
- **Visual Effects**: Beautiful animations and visual feedback

### 🤖 **AI-Powered Intelligence**  
- **Screen Awareness**: Captures and analyzes your screen content
- **Context-Aware Help**: Understands what you're working on and provides relevant assistance
- **Smart Conversations**: Powered by Google's Gemini AI for natural interactions

### � **Web Interface**
- **React-based Website**: Beautiful web interface for your pet
- **Responsive Design**: Works on all screen sizes
- **Modern UI**: Clean, intuitive user experience

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js (for React app)
- Google Gemini API key

### Quick Start

1. **Desktop Pet Setup:**
   - Install Python dependencies: `pip install -r requirements.txt`
   - Set up your Gemini API key in `config/settings.json`
   - Run: `start.bat` or `python main.py`

2. **Web Interface Setup:**
   ```bash
   cd react-app
   npm install
   npm start
   ```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
Create a `.env` file and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
python main.py
```

## 🎮 Usage

1. **Launch the Pet**: Run the application and your virtual pet will appear on screen
2. **Interact**: Click on the pet or use the hotkey (Ctrl+Alt+P) to start a conversation
3. **Get Help**: Ask questions about what you're working on, and the pet will analyze your screen and provide contextual assistance
4. **Customize**: Configure pet appearance, behavior, and AI personality in settings

## 🧠 How It Works

The virtual pet uses several technologies:
- **Screen Capture**: Takes screenshots to understand your current context
- **Computer Vision**: Identifies active applications and UI elements
- **Gemini AI**: Processes screen content and generates helpful responses
- **Natural Language Processing**: Understands your questions and provides human-like responses

## 🛠️ Configuration

Edit `config/settings.json` to customize:
- Pet appearance and animations
- AI response personality
- Screen capture frequency
- Supported applications
- Privacy settings

## 🔒 Privacy & Security

- Screenshots are processed locally when possible
- Only necessary screen content is sent to AI services
- No data is stored permanently without consent
- Easy privacy controls and opt-out options

## 📁 Project Structure

```
HackHarvard25/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── .env                   # Environment variables
├── src/
│   ├── pet/               # Virtual pet UI and animations
│   ├── ai/                # AI integration (Gemini)
│   ├── screen/            # Screen capture and analysis
│   ├── apps/              # Application-specific helpers
│   └── utils/             # Utility functions
├── assets/                # Pet sprites, sounds, etc.
├── config/                # Configuration files
└── tests/                # Unit tests
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powering the intelligence
- The open-source community for amazing libraries
- HackHarvard 2025 for the inspiration!