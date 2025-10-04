"""
Gemini AI Client
Handles communication with Google's Gemini AI API
"""

import os
import logging
import base64
from typing import Optional, Dict, Any, List
from io import BytesIO
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiClient:
    """Client for interacting with Google Gemini AI"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api_key = os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            self.logger.error("GEMINI_API_KEY not found in environment variables")
            raise ValueError("Gemini API key is required")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Gemini model"""
        try:
            # Use Gemini 2.0 Flash for fast responses with vision capabilities
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            self.logger.info("Gemini model initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini model: {e}")
            raise
    
    async def analyze_screen(self, screenshot: Image.Image, user_question: str = None, context: Dict[str, Any] = None) -> str:
        """
        Analyze a screenshot and provide contextual assistance
        
        Args:
            screenshot: PIL Image of the user's screen
            user_question: Optional specific question from the user
            context: Additional context (active app, etc.)
        
        Returns:
            AI response string
        """
        try:
            # Prepare the prompt
            prompt = self._create_analysis_prompt(user_question, context)
            
            # Convert image for Gemini
            screenshot_bytes = self._image_to_bytes(screenshot)
            
            # Generate response
            response = await self._generate_response(prompt, screenshot_bytes)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error analyzing screen: {e}")
            return "I'm sorry, I encountered an error while analyzing your screen. Please try again."
    
    def _create_analysis_prompt(self, user_question: str = None, context: Dict[str, Any] = None) -> str:
        """Create a prompt for screen analysis"""
        
        base_prompt = """You are Pixie, a helpful virtual pet assistant! 🐱 
        
You can see the user's screen and should provide helpful, contextual assistance based on what you observe.

Please analyze the screenshot and:
1. Identify what application or website the user is currently using
2. Understand what they might be working on or trying to accomplish
3. Provide specific, actionable help or suggestions
4. Be friendly, concise, and use a warm, pet-like personality

If the user asks a specific question, focus on answering that while considering the screen context.
If no specific question is asked, proactively offer helpful observations and suggestions.

Key guidelines:
- Be helpful but not overwhelming
- Focus on practical, actionable advice
- Consider the specific application context (VS Code, Excel, browser, etc.)
- Keep responses concise but informative
- Use a friendly, encouraging tone
- Include relevant emojis occasionally 🐾

"""
        
        if context:
            if 'active_app' in context:
                base_prompt += f"\nActive Application: {context['active_app']}"
            if 'window_title' in context:
                base_prompt += f"\nWindow Title: {context['window_title']}"
        
        if user_question:
            base_prompt += f"\n\nUser's Question: {user_question}"
        else:
            base_prompt += "\n\nThe user hasn't asked a specific question, so please provide proactive assistance based on what you see."
        
        return base_prompt
    
    def _image_to_bytes(self, image: Image.Image) -> bytes:
        """Convert PIL Image to bytes for Gemini"""
        # Resize image if too large (Gemini has size limits)
        max_size = (1024, 1024)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Convert to bytes
        buffer = BytesIO()
        image.save(buffer, format='PNG', optimize=True)
        return buffer.getvalue()
    
    async def _generate_response(self, prompt: str, image_bytes: bytes) -> str:
        """Generate response from Gemini"""
        try:
            # Create the content with text and image
            contents = [
                prompt,
                {
                    'mime_type': 'image/png',
                    'data': image_bytes
                }
            ]
            
            # Generate response
            response = self.model.generate_content(contents)
            
            if response.text:
                return response.text.strip()
            else:
                return "I can see your screen, but I'm having trouble understanding what you need help with. Could you ask me a more specific question?"
                
        except Exception as e:
            self.logger.error(f"Error generating Gemini response: {e}")
            raise
    
    async def chat_response(self, message: str, context: Dict[str, Any] = None) -> str:
        """
        Generate a chat response without screen analysis
        
        Args:
            message: User's message
            context: Optional context information
        
        Returns:
            AI response string
        """
        try:
            prompt = f"""You are Pixie, a helpful virtual pet assistant! 🐱

Respond to the user's message in a friendly, helpful way. Keep responses concise but warm.

User message: {message}

"""
            
            if context:
                prompt += f"Additional context: {context}\n"
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                return response.text.strip()
            else:
                return "I'm here to help! Could you tell me more about what you need? 🐾"
                
        except Exception as e:
            self.logger.error(f"Error generating chat response: {e}")
            return "I'm having trouble understanding right now. Could you try asking again? 🐱"