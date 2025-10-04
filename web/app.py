# Web Interface for Virtual Pet AI Assistant

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from src.ai.gemini_client import GeminiClient
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("Warning: AI client not available. Running in demo mode.")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    """Main web interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chatting with the AI"""
    try:
        data = request.json
        message = data.get('message', '')
        
        if not AI_AVAILABLE:
            # Demo responses when AI is not available
            demo_responses = [
                f"🤖 I heard you say: '{message}' - This is demo mode since the AI client isn't configured yet!",
                "🐱 That's interesting! In the full version, I'd analyze your screen and give contextual help.",
                "✨ I'm your virtual pet assistant! I can help with coding, Excel, and much more when fully configured.",
                "🚀 To enable full AI features, please configure your Gemini API key in the .env file!"
            ]
            import random
            response = random.choice(demo_responses)
        else:
            # Use actual AI when available
            gemini = GeminiClient()
            response = gemini.generate_response(
                prompt=f"User message: {message}",
                context="Web interface chat"
            )
        
        return jsonify({
            'success': True,
            'response': response
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/status')
def status():
    """API endpoint for checking system status"""
    return jsonify({
        'status': 'online',
        'features': [
            'AI Chat',
            'Screen Analysis',
            'Context Awareness',
            'Multi-App Support'
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)