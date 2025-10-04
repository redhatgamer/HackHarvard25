# Virtual Pet AI Assistant 🐱🤖

A delightful AI-powered virtual pet that watches your screen and helps you with whatever you're working on! Using Google's Gemini AI, this smart companion provides contextual assistance whether you're coding, working with spreadsheets, browsing, or doing any other computer task.

## ✨ Features

### 🎨 **Modern UI & Animations**
- **Glassmorphism Design**: Beautiful translucent interface with modern styling
- **Smooth Animations**: Breathing effects, particle systems, and hover animations
- **Emotional Expressions**: Pet shows different emotions (happy, thinking, excited, etc.)
- **Visual Effects**: Glow effects, ripples, and magical particle bursts
- **Responsive Design**: Adapts to different screen sizes and resolutions

### 🤖 **AI-Powered Intelligence**
- **Screen Awareness**: Captures and analyzes your screen content in real-time
- **Context-Aware AI**: Understands what application you're using and provides relevant help
- **Multi-Application Support**: 
  - VS Code: Code assistance, debugging tips, suggestions
  - Excel/Spreadsheets: Formula help, data analysis tips
  - Web Browsers: Research assistance, content summaries
  - And much more!

### 🎮 **Interactive Pet Experience**
- **Animated Virtual Pet**: Adorable pet character with lifelike animations
- **Voice & Text Interaction**: Communicate through typing or speech
- **Drag & Drop**: Move your pet anywhere on screen
- **Context Menus**: Modern right-click menus with smooth animations
- **Activity Indicators**: Visual feedback when Pixie is thinking or working

### 🔒 **Privacy & Customization**
- **Privacy Focused**: All processing respects your privacy settings
- **Themeable**: Customizable colors, fonts, and visual effects
- **Configurable**: Adjust transparency, animations, and behavior
- **Lightweight**: Minimal resource usage with efficient animations

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Windows OS (primary support)
- Google Gemini API key

### Installation

1. Clone this repository:
```bash
git clone https://github.com/redhatgamer/HackHarvard25.git
cd HackHarvard25
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