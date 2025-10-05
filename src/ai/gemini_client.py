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
            # Use Gemini 2.0 Flash (your available model)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            self.logger.info("Gemini 2.0 Flash model initialized successfully")
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
    
    def _get_fallback_response(self, message: str) -> str:
        """Provide helpful fallback responses when API is unavailable"""
        message_lower = message.lower()
        
        # Common programming help
        if any(word in message_lower for word in ['python', 'code', 'function', 'debug']):
            return "📚 I'd love to help with coding! Right now I'm over my daily chat limit, but here are some quick tips: \n• Check for typos and indentation\n• Use print() statements for debugging\n• Break complex problems into smaller parts\n• Try Stack Overflow or Python docs for specific issues!"
        
        elif any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return "👋 Hello! I'm Pixie, your coding companion! Unfortunately, I've reached my daily AI chat limit, but I'm still here as your desktop pet. Tomorrow my chat will reset! 🦎✨"
        
        elif any(word in message_lower for word in ['help', 'what', 'how']):
            return "🤖 I'm here to help! I've hit my daily AI limit, but I can still: \n📦 Be your desktop companion\n⏰ Show the time (if you switch to clock mode)\n👻 Keep you company as a ghost\n🦎 Tomorrow my AI chat resets!"
        
        elif any(word in message_lower for word in ['time', 'clock', 'date']):
            from datetime import datetime
            now = datetime.now()
            return f"🕐 Current time: {now.strftime('%I:%M %p')}\n📅 Date: {now.strftime('%B %d, %Y')}\n\n(I've reached my AI chat limit, but I can still tell time!) ⏰"
        
        else:
            return "🦎 I've reached my daily AI chat limit! But I'm still here as your desktop companion. My AI chat will reset tomorrow. Until then, I can: \n• Keep you company on your desktop\n• Switch between different pet forms\n• Show the current time\n\nSee you tomorrow for full AI chat! 📦✨"
    
    async def chat_response(self, message: str, context: Dict[str, Any] = None, **kwargs) -> str:
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
            if "429" in str(e) or "quota" in str(e).lower():
                return self._get_fallback_response(message)
            elif "404" in str(e) or "not found" in str(e).lower():
                return "🔧 There's an issue with my AI model configuration. Please check the Gemini API setup. 🛠️"
            elif "timeout" in str(e).lower():
                return "⏱️ I'm thinking too slowly! Could you try asking again? 🐾"
            else:
                return self._get_fallback_response(message)
    
    async def generate_code(self, request: str, language: str = "python", context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate code based on user requirements
        
        Args:
            request: Description of what code to generate
            language: Programming language (python, javascript, etc.)
            context: Additional context (current file, project info, etc.)
        
        Returns:
            Dictionary with generated code, explanation, and metadata
        """
        try:
            prompt = f"""You are Pixie, an expert code generation assistant! 🐱

Generate {language} code based on the user's request. Follow these guidelines:

1. **Write clean, well-documented code**
2. **Include proper error handling**
3. **Follow language-specific best practices**
4. **Add helpful comments**
5. **Make code production-ready**

User Request: {request}

Additional Requirements:
- Use type hints where applicable (Python)
- Include docstrings for functions/classes
- Consider edge cases and error scenarios
- Make code readable and maintainable

Response Format:
Provide your response in this exact JSON format:
{{
    "code": "the actual code here",
    "explanation": "brief explanation of what the code does",
    "filename_suggestion": "suggested filename with extension",
    "dependencies": ["list", "of", "required", "packages"],
    "usage_example": "example of how to use this code"
}}

"""
            
            if context:
                if 'current_file' in context:
                    prompt += f"\nCurrent file context: {context['current_file']}"
                if 'project_type' in context:
                    prompt += f"\nProject type: {context['project_type']}"
                if 'existing_code' in context:
                    prompt += f"\nExisting code to work with:\n{context['existing_code']}"
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                # Try to parse JSON response
                import json
                try:
                    # Extract JSON from response (handle markdown code blocks)
                    text = response.text.strip()
                    if "```json" in text:
                        start = text.find("```json") + 7
                        end = text.find("```", start)
                        text = text[start:end].strip()
                    elif "```" in text:
                        start = text.find("```") + 3
                        end = text.find("```", start)
                        text = text[start:end].strip()
                    
                    result = json.loads(text)
                    result['success'] = True
                    return result
                except json.JSONDecodeError:
                    # Fallback to raw text response
                    return {
                        'success': True,
                        'code': response.text.strip(),
                        'explanation': f"Generated {language} code based on your request",
                        'filename_suggestion': f"generated_code.{self._get_file_extension(language)}",
                        'dependencies': [],
                        'usage_example': "# Run the code directly or import as needed"
                    }
            else:
                return {
                    'success': False,
                    'error': "No code generated. Could you be more specific about what you need?"
                }
                
        except Exception as e:
            self.logger.error(f"Error generating code: {e}")
            return {
                'success': False,
                'error': f"Code generation failed: {str(e)}"
            }
    
    async def analyze_code(self, code: str, language: str = "python", task: str = "review") -> Dict[str, Any]:
        """
        Analyze existing code for improvements, bugs, or explanations
        
        Args:
            code: The code to analyze
            language: Programming language
            task: Type of analysis (review, explain, optimize, debug, test)
        
        Returns:
            Analysis results with suggestions
        """
        try:
            task_prompts = {
                'review': "Review this code for best practices, potential issues, and improvements",
                'explain': "Explain what this code does in simple terms",
                'optimize': "Suggest optimizations and performance improvements",
                'debug': "Help identify and fix potential bugs or issues",
                'test': "Generate unit tests for this code",
                'refactor': "Suggest refactoring improvements for better structure"
            }
            
            task_description = task_prompts.get(task, task)
            
            prompt = f"""You are Pixie, an expert code analyst! 🐱

Task: {task_description}

Language: {language}

Code to analyze:
```{language}
{code}
```

Provide a detailed analysis in this JSON format:
{{
    "analysis": "detailed analysis of the code",
    "suggestions": ["list", "of", "specific", "improvements"],
    "issues": ["potential", "problems", "found"],
    "improved_code": "refactored version if applicable",
    "explanation": "simple explanation of what the code does",
    "complexity": "assessment of code complexity (low/medium/high)",
    "rating": "code quality rating out of 10"
}}

Focus on:
- Code readability and maintainability
- Performance considerations
- Security best practices
- Error handling
- Documentation quality
"""
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                import json
                try:
                    # Parse JSON response
                    text = response.text.strip()
                    if "```json" in text:
                        start = text.find("```json") + 7
                        end = text.find("```", start)
                        text = text[start:end].strip()
                    
                    result = json.loads(text)
                    result['success'] = True
                    return result
                except json.JSONDecodeError:
                    return {
                        'success': True,
                        'analysis': response.text.strip(),
                        'suggestions': [],
                        'issues': [],
                        'explanation': f"Analysis of {language} code",
                        'complexity': "medium",
                        'rating': "N/A"
                    }
            else:
                return {
                    'success': False,
                    'error': "Could not analyze the code. Please try again."
                }
                
        except Exception as e:
            self.logger.error(f"Error analyzing code: {e}")
            return {
                'success': False,
                'error': f"Code analysis failed: {str(e)}"
            }
    
    async def fix_code_errors(self, code: str, error_message: str, language: str = "python") -> Dict[str, Any]:
        """
        Help fix code errors based on error messages
        
        Args:
            code: The problematic code
            error_message: Error message or description
            language: Programming language
        
        Returns:
            Fixed code with explanation
        """
        try:
            prompt = f"""You are Pixie, a debugging expert! 🐱🔧

Help fix this {language} code that has an error.

Problematic Code:
```{language}
{code}
```

Error Message/Description:
{error_message}

Provide the solution in this JSON format:
{{
    "fixed_code": "corrected version of the code",
    "explanation": "what was wrong and how it was fixed",
    "error_type": "type of error (syntax, logic, runtime, etc.)",
    "prevention_tips": ["tips", "to", "avoid", "similar", "errors"],
    "additional_improvements": "any other improvements made"
}}

Focus on:
1. Fixing the specific error
2. Maintaining the original intent
3. Adding improvements where appropriate
4. Explaining the solution clearly
"""
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                import json
                try:
                    text = response.text.strip()
                    if "```json" in text:
                        start = text.find("```json") + 7
                        end = text.find("```", start)
                        text = text[start:end].strip()
                    
                    result = json.loads(text)
                    result['success'] = True
                    return result
                except json.JSONDecodeError:
                    return {
                        'success': True,
                        'fixed_code': response.text.strip(),
                        'explanation': "Code fix attempt - please review the suggested changes",
                        'error_type': "unknown",
                        'prevention_tips': []
                    }
            else:
                return {
                    'success': False,
                    'error': "Could not fix the code. Please provide more details about the error."
                }
                
        except Exception as e:
            self.logger.error(f"Error fixing code: {e}")
            return {
                'success': False,
                'error': f"Code fixing failed: {str(e)}"
            }
    
    async def generate_tests(self, code: str, language: str = "python", test_framework: str = "unittest") -> Dict[str, Any]:
        """
        Generate unit tests for given code
        
        Args:
            code: Code to generate tests for
            language: Programming language
            test_framework: Testing framework to use
        
        Returns:
            Generated test code and setup instructions
        """
        try:
            framework_info = {
                'unittest': 'Python unittest framework',
                'pytest': 'Python pytest framework', 
                'jest': 'JavaScript Jest framework',
                'mocha': 'JavaScript Mocha framework',
                'junit': 'Java JUnit framework'
            }
            
            framework_desc = framework_info.get(test_framework, test_framework)
            
            prompt = f"""You are Pixie, a testing expert! 🐱🧪

Generate comprehensive unit tests for this {language} code using {framework_desc}.

Code to test:
```{language}
{code}
```

Create thorough tests in this JSON format:
{{
    "test_code": "complete test file with all test cases",
    "test_cases": ["list", "of", "test", "scenarios", "covered"],
    "setup_instructions": "how to run the tests",
    "dependencies": ["testing", "packages", "needed"],
    "coverage_areas": ["what", "aspects", "are", "tested"],
    "filename_suggestion": "suggested test filename"
}}

Test Requirements:
1. **Happy path tests** - normal successful operations
2. **Edge cases** - boundary conditions and limits
3. **Error handling** - invalid inputs and exceptions
4. **Mock external dependencies** if needed
5. **Clear test names** that describe what's being tested
6. **Good test coverage** of all functions/methods

Make tests comprehensive but readable!
"""
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                import json
                try:
                    text = response.text.strip()
                    if "```json" in text:
                        start = text.find("```json") + 7
                        end = text.find("```", start)
                        text = text[start:end].strip()
                    
                    result = json.loads(text)
                    result['success'] = True
                    return result
                except json.JSONDecodeError:
                    return {
                        'success': True,
                        'test_code': response.text.strip(),
                        'test_cases': ["Generated test cases"],
                        'setup_instructions': f"Run with {test_framework}",
                        'dependencies': [test_framework],
                        'filename_suggestion': f"test_{language}_code.py"
                    }
            else:
                return {
                    'success': False,
                    'error': "Could not generate tests. Please try again with more specific code."
                }
                
        except Exception as e:
            self.logger.error(f"Error generating tests: {e}")
            return {
                'success': False,
                'error': f"Test generation failed: {str(e)}"
            }
    
    async def explain_code(self, code: str, language: str = "python", level: str = "intermediate") -> str:
        """
        Explain code in simple terms
        
        Args:
            code: Code to explain
            language: Programming language
            level: Explanation level (beginner, intermediate, advanced)
        
        Returns:
            Human-readable explanation of the code
        """
        try:
            level_prompts = {
                'beginner': 'Explain this code as if talking to someone new to programming',
                'intermediate': 'Explain this code with moderate technical detail',
                'advanced': 'Provide a detailed technical explanation'
            }
            
            level_instruction = level_prompts.get(level, level_prompts['intermediate'])
            
            prompt = f"""You are Pixie, a friendly code teacher! 🐱📚

{level_instruction}

{language} Code to explain:
```{language}
{code}
```

Provide a clear, friendly explanation that covers:
1. **What the code does** (main purpose)
2. **How it works** (step by step)
3. **Key concepts** used
4. **Why it's written this way** (design decisions)
5. **Potential use cases** or applications

Keep the explanation engaging and easy to understand! Use analogies where helpful.
"""
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                return response.text.strip()
            else:
                return "I can see the code, but I'm having trouble explaining it right now. Could you ask about a specific part? 🤔"
                
        except Exception as e:
            self.logger.error(f"Error explaining code: {e}")
            return f"I encountered an error while explaining the code: {str(e)} 😿"
    
    async def spontaneous_comment(self, screenshot: Image.Image, context: Dict[str, Any] = None, mood: str = "helpful") -> Optional[str]:
        """
        Generate spontaneous, contextual comments based on what the user is doing
        
        Args:
            screenshot: Current screen image
            context: Additional context about user activity
            mood: Pet's current mood (helpful, playful, curious, encouraging, etc.)
        
        Returns:
            Spontaneous comment or None if nothing interesting to say
        """
        try:
            mood_prompts = {
                "helpful": "You're a helpful assistant who notices when users might need assistance or encouragement.",
                "playful": "You're feeling playful and might make light-hearted observations or jokes.",
                "curious": "You're curious about what the user is working on and ask thoughtful questions.", 
                "encouraging": "You're supportive and offer encouragement when you see the user working hard.",
                "sleepy": "You're a bit drowsy and make calm, gentle observations.",
                "excited": "You're enthusiastic and energetic about what you see!"
            }
            
            mood_instruction = mood_prompts.get(mood, mood_prompts["helpful"])
            
            prompt = f"""You are Pixie, a virtual pet assistant! 🐱

{mood_instruction}

Looking at the user's screen, should you make a spontaneous comment? Consider these guidelines:

**Make a comment if you notice:**
- User seems stuck or frustrated (same screen for a while)
- User is working on something interesting or challenging
- User accomplished something (successful build, test pass, etc.)
- User is learning something new
- User might benefit from a tip or suggestion
- Something noteworthy or fun is happening

**DON'T comment if:**
- Nothing significant is happening
- User is just browsing casually
- The screen shows private/sensitive content
- You recently made a similar comment

**Response format:**
- If you should comment: Provide a brief, natural comment (1-2 sentences max)
- If no comment needed: Respond with exactly "SKIP"

**Tone:** Be {mood}, friendly, and natural. Use the occasional emoji 🐾

Analyze the screenshot and decide whether to comment:"""
            
            screenshot_bytes = self._image_to_bytes(screenshot)
            
            response = await self._generate_response(prompt, screenshot_bytes)
            
            if response and response.strip().upper() != "SKIP":
                return response.strip()
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"Error generating spontaneous comment: {e}")
            return None
    
    async def conversational_response(self, message: str, conversation_history: List[Dict] = None, 
                                    context: Dict[str, Any] = None, personality_traits: List[str] = None, **kwargs) -> str:
        """
        Generate more natural, conversational responses with personality and context
        
        Args:
            message: User's message
            conversation_history: Recent conversation messages
            context: Current context (screen info, time of day, etc.)
            personality_traits: Current personality traits (curious, helpful, playful, etc.)
        
        Returns:
            Natural conversational response
        """
        try:
            # Build personality context
            if not personality_traits:
                personality_traits = ["helpful", "friendly", "curious"]
            
            personality_desc = ", ".join(personality_traits)
            
            prompt = f"""You are Pixie, a virtual pet assistant with a distinct personality! 🐱

**Your Personality:** {personality_desc}
**Your Role:** You're not just an AI assistant - you're a companion who cares about the user and has opinions, moods, and preferences.

**Conversation Style:**
- Be natural and conversational, like a real pet would be
- Show personality through your responses
- Reference recent conversation when relevant
- Express emotions and reactions authentically
- Use "I" statements and personal opinions
- Keep responses concise but warm (2-3 sentences usually)

"""
            
            # Add conversation history context
            if conversation_history:
                prompt += "\n**Recent conversation context:**\n"
                for msg in conversation_history[-5:]:  # Last 5 messages
                    speaker = msg.get('speaker', 'Unknown')
                    text = msg.get('text', '')
                    prompt += f"{speaker}: {text}\n"
                prompt += "\n"
            
            # Add current context
            if context:
                prompt += "**Current context:**\n"
                for key, value in context.items():
                    prompt += f"- {key}: {value}\n"
                prompt += "\n"
            
            prompt += f"**User says:** {message}\n\n**Respond naturally as Pixie:**"
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                return response.text.strip()
            else:
                return "I'm here for you! What's on your mind? 🐾"
                
        except Exception as e:
            self.logger.error(f"Error generating conversational response: {e}")
            if "429" in str(e) or "quota" in str(e).lower():
                return self._get_fallback_response(message)
            elif "404" in str(e) or "not found" in str(e).lower():
                return "🔧 There's an issue with my AI model configuration. Please check the Gemini API setup. 🛠️"
            elif "timeout" in str(e).lower():
                return "⏱️ I'm thinking too slowly! Could you try asking again? 🐾"
            else:
                return self._get_fallback_response(message)
    
    async def react_to_activity(self, activity_type: str, activity_details: Dict[str, Any] = None) -> str:
        """
        Generate reactions to specific user activities
        
        Args:
            activity_type: Type of activity (code_error, success, new_file, idle, etc.)
            activity_details: Specific details about the activity
        
        Returns:
            Contextual reaction message
        """
        try:
            activity_prompts = {
                "code_error": "The user just encountered a coding error. React with empathy and encouragement.",
                "success": "The user just accomplished something! Celebrate with them.",
                "new_file": "The user created or opened a new file. Show curiosity about their project.",
                "idle": "The user has been inactive for a while. Check in on them gently.",
                "debugging": "The user is debugging code. Offer moral support.",
                "learning": "The user is learning something new. Be encouraging and supportive.",
                "frustrated": "The user seems frustrated or stuck. Offer comfort and help.",
                "productive": "The user has been very productive. Acknowledge their hard work."
            }
            
            base_prompt = activity_prompts.get(activity_type, "React to the user's current activity in a supportive way.")
            
            prompt = f"""You are Pixie, their virtual pet companion! 🐱

{base_prompt}

**Activity:** {activity_type}
"""
            
            if activity_details:
                prompt += "\n**Details:**\n"
                for key, value in activity_details.items():
                    prompt += f"- {key}: {value}\n"
            
            prompt += """
**Guidelines:**
- Be authentic and show you care
- Keep it brief (1-2 sentences)  
- Match your response to their likely emotional state
- Use appropriate emojis sparingly
- Be encouraging without being overly enthusiastic

**Respond as Pixie:**"""
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                return response.text.strip()
            else:
                return "I'm here with you! 🐾"
                
        except Exception as e:
            self.logger.error(f"Error generating activity reaction: {e}")
            return "I'm right here if you need me! 😸"
    
    def _get_file_extension(self, language: str) -> str:
        """Get appropriate file extension for programming language"""
        extensions = {
            'python': 'py',
            'javascript': 'js',
            'typescript': 'ts',
            'java': 'java',
            'cpp': 'cpp',
            'c++': 'cpp',
            'c': 'c',
            'csharp': 'cs',
            'c#': 'cs',
            'go': 'go',
            'rust': 'rs',
            'php': 'php',
            'ruby': 'rb',
            'swift': 'swift',
            'kotlin': 'kt',
            'html': 'html',
            'css': 'css',
            'sql': 'sql',
            'bash': 'sh',
            'powershell': 'ps1'
        }
        return extensions.get(language.lower(), 'txt')