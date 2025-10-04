# Voice Interaction Guide 🎤

## Quick Start

1. **Make sure your microphone is working** - Test it with the Windows Sound Recorder or another app
2. **Run the desktop pet** with voice enabled:
   ```bash
   run_with_voice.bat
   ```
   Or manually:
   ```bash
   & ".venv\Scripts\python.exe" main.py
   ```

## How to Use Voice Interaction

### 🎯 Two Ways to Ask Questions

**1. Continuous Listening (Always On)**
The pet listens continuously for questions. Just speak naturally and ask:

**2. Right-Click Voice Input (On-Demand)**
Right-click on the pet → Select "🎤 Ask Question (Voice)" → Speak your question

### 📝 Questions You Can Ask

**Tech Questions:**
- "What flavor of Linux do you recommend?"
- "How do I learn Python programming?"
- "Explain machine learning in simple terms"
- "What's the best text editor for coding?"
- "How does Git work?"

**General Questions:**
- "What's the weather like today?"
- "Tell me a programming joke"
- "How do I stay productive while coding?"

### 🎪 Activation Triggers
The pet will respond to speech that:
- Contains question words (what, how, why, when, where, etc.)
- Mentions the pet by name ("Pixie")
- Contains question marks
- Uses phrases like "recommend", "suggest", "help", "explain"

### 🔊 Response System
When you ask a question:
1. **Visual Feedback**: Speech bubble shows "🎤 Thinking..."
2. **AI Processing**: Gemini AI generates a helpful response
3. **Text Response**: Answer appears in speech bubble and chat
4. **Voice Response**: Pet speaks the answer using British child-like voice

### ⚙️ Configuration
Voice settings are in `config/settings.json`:

```json
{
  "speech": {
    "voice_input": {
      "enabled": true,
      "language": "en-US", 
      "energy_threshold": 300,
      "pause_threshold": 0.8,
      "phrase_time_limit": 5
    },
    "tts": {
      "enabled": true,
      "use_natural_voice": true,
      "british_accent": true
    }
  }
}
```

### 🐛 Troubleshooting

**Microphone Not Working:**
- Check Windows microphone permissions
- Test with: `& ".venv\Scripts\python.exe" test_voice_interaction.py`
- Adjust `energy_threshold` in config if too sensitive/insensitive

**No AI Response:**
- Make sure `GEMINI_API_KEY` is set in your environment
- Check internet connection
- Look at console output for error messages

**Speech Output Issues:**
- Make sure speakers/headphones are working
- Try toggling `use_natural_voice` to `false` in config
- Check Windows TTS settings

### 🎯 Example Conversation

```
You: "What flavor of Linux do you recommend?"
Pixie: "I'd recommend Ubuntu for beginners! It's user-friendly, has great community support, and tons of software available. If you're more advanced, consider Arch Linux or Fedora!"

You: "How do I learn Python?"
Pixie: "Start with interactive tutorials like Codecademy or Python.org's official tutorial! Practice with small projects, and try coding challenges on websites like HackerRank. The key is consistent practice!"
```

### 🔥 Pro Tips

1. **Speak Clearly**: The pet uses Google Speech Recognition, so clear speech works best
2. **Wait for Response**: Let the pet finish speaking before asking the next question
3. **Natural Language**: Ask questions like you would ask a human assistant
4. **Context Aware**: The pet can see your screen, so ask about what you're working on!
5. **Right-Click Method**: Use right-click voice input for better control over when you're asking questions
6. **5-Second Window**: When using right-click voice, you have 5 seconds to ask your question

Enjoy chatting with your AI desktop pet! 🐾✨