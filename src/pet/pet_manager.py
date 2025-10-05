"""
Pet Manager
Main orchestrator for the virtual pet assistant
"""

import asyncio
import logging
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Optional, Dict, Any
import threading
import sys
import time
import random
from pathlib import Path
from PIL import Image, ImageTk

# Import file management
try:
    from src.file.file_manager import FileManager
except ImportError:
    FileManager = None

# Import VS Code integration
try:
    from src.vscode.vscode_integration import VSCodeIntegration
except ImportError:
    VSCodeIntegration = None  # Not implemented yet

# Import modern UI components
try:
    from src.ui.modern_components import (ModernPetWidget, ModernChatWindow, 
                                        ModernContextMenu, CardboardContextMenu,
                                        ModernSpeechBubble, DarkModeToggle)
except ImportError:
    # Fallback if modern components aren't available
    ModernPetWidget = None
    ModernChatWindow = None
    ModernContextMenu = None
    CardboardContextMenu = None
    ModernSpeechBubble = None
    DarkModeToggle = None

# Import theme manager
try:
    from src.ui.theme_manager import get_style_manager, get_theme
except ImportError:
    get_style_manager = None
    get_theme = None

# Import speech managers
try:
    from src.ui.speech_manager import SpeechManager
except ImportError as e:
    SpeechManager = None

try:
    from src.ui.natural_speech_manager import NaturalSpeechManager
except ImportError as e:
    NaturalSpeechManager = None

# Import voice input manager
try:
    from src.ui.voice_input_manager import VoiceInputManager
except ImportError as e:
    VoiceInputManager = None

# Import Google Sheets manager
try:
    from src.integrations.google_sheets_manager import GoogleSheetsManager
except ImportError as e:
    GoogleSheetsManager = None

class PetManager:
    """Main manager for the virtual pet assistant"""
    
    def __init__(self, gemini_client, screen_monitor, config):
        self.logger = logging.getLogger(__name__)
        self.gemini_client = gemini_client
        self.screen_monitor = screen_monitor
        self.config = config
        self.settings = config  # Alias for consistency with pet switching methods
        
        # Initialize file manager
        try:
            self.file_manager = FileManager() if FileManager else None
        except Exception as e:
            self.logger.warning(f"Could not initialize file manager: {e}")
            self.file_manager = None
        
        # Initialize VS Code integration
        try:
            self.vscode_integration = VSCodeIntegration(self.file_manager) if VSCodeIntegration else None
        except Exception as e:
            self.logger.warning(f"Could not initialize VS Code integration: {e}")
            self.vscode_integration = None
        
        # UI components
        self.root = None
        self.pet_window = None
        self.chat_window = None
        self.speech_bubble = None
        self.dark_mode_toggle = None
        self.is_running = False
        
        # Theme management
        self.style_manager = get_style_manager() if get_style_manager else None
        if self.style_manager:
            self.style_manager.add_theme_change_callback(self._on_theme_change)
        
        # Speech management
        tts_config = config.get('speech', {}).get('tts', {})
        if tts_config.get('enabled', True):
            
            # Try natural voice first (much better quality)
            if tts_config.get('use_natural_voice', True) and NaturalSpeechManager:
                try:
                    british_accent = tts_config.get('british_accent', True)
                    self.speech_manager = NaturalSpeechManager(
                        use_gtts=True,
                        british_accent=british_accent,
                        child_like=True  # Enable British kid voice
                    )
                    
                    if self.speech_manager.is_available():
                        voice_info = self.speech_manager.get_voice_info()
                        self.logger.info(f"Natural TTS initialized: {voice_info}")
                    else:
                        raise Exception("Natural TTS not available")
                        
                except Exception as e:
                    self.logger.warning(f"Natural TTS failed: {e}, falling back to basic TTS")
                    self.speech_manager = None
            
            # Fallback to basic TTS if natural voice failed
            if not self.speech_manager and SpeechManager:
                try:
                    self.speech_manager = SpeechManager(
                        child_like=True,
                        british_style=tts_config.get('british_accent', True)
                    )
                    
                    if self.speech_manager.is_available():
                        self.speech_manager.set_voice_properties(
                            rate=tts_config.get('fallback_rate', 180),
                            volume=tts_config.get('fallback_volume', 0.9)
                        )
                        self.logger.info("Basic TTS initialized (fallback)")
                    else:
                        self.speech_manager = None
                        
                except Exception as e:
                    self.logger.warning(f"Basic TTS failed: {e}")
                    self.speech_manager = None
            
            if not self.speech_manager:
                self.logger.warning("No TTS available")
        else:
            self.speech_manager = None
            self.logger.info("Text-to-speech disabled in configuration")
        
        # Voice input management
        voice_config = config.get('speech', {}).get('voice_input', {})
        if voice_config.get('enabled', True) and VoiceInputManager:
            try:
                self.voice_input_manager = VoiceInputManager(callback=self._on_voice_input)
                self.logger.info("Voice input manager initialized")
            except Exception as e:
                self.logger.warning(f"Voice input initialization failed: {e}")
                self.voice_input_manager = None
        else:
            self.voice_input_manager = None
            self.logger.info("Voice input disabled or not available")
        
        # State
        self.current_context = None
        self.chat_history = []
        self.conversation_messages = []  # Store conversation for speech bubbles
        
        # Enhanced conversation state
        self.conversation_history = []  # Recent conversation for context
        self.last_spontaneous_comment_time = 0
        
        # Google Sheets integration
        self.sheets_manager = None
        self.csv_logger = None
        
        sheets_config = config.get('integrations', {}).get('google_sheets', {})
        if sheets_config.get('enabled', False) and GoogleSheetsManager:
            try:
                credentials_path = sheets_config.get('credentials_path')
                self.sheets_manager = GoogleSheetsManager(credentials_path)
                self.logger.info("Google Sheets manager initialized")
            except Exception as e:
                self.logger.warning(f"Google Sheets initialization failed: {e}")
                self.sheets_manager = None
        
        # Always initialize simple CSV logger as backup/alternative
        try:
            from src.integrations.csv_logger import CSVSheetsLogger
            self.csv_logger = CSVSheetsLogger("pixie_activity_log.csv")
            self.logger.info("CSV logger initialized for Google Sheets import")
        except Exception as e:
            self.logger.warning(f"CSV logger initialization failed: {e}")
            self.csv_logger = None
        
        # Initialize performance monitoring
        try:
            from src.utils.performance_monitor import PerformanceMonitor
            perf_config = config.get("performance", {})
            self.performance_monitor = PerformanceMonitor(perf_config)
            if perf_config.get("enable_profiling", False):
                self.performance_monitor.start_monitoring()
            self.logger.info("Performance monitor initialized")
        except Exception as e:
            self.logger.warning(f"Performance monitor initialization failed: {e}")
            self.performance_monitor = None
        self.current_mood = "helpful"  # Pet's current mood
        self.personality_traits = ["helpful", "friendly", "curious"]
        
        # Memory management limits
        self.MAX_CONVERSATION_HISTORY = 50  # Limit conversation memory
        self.MAX_ACTIVITY_HISTORY = 20      # Limit activity tracking
        self.conversation_history = []       # Initialize conversation history
        
        # Memory-efficient activity tracking with limits
        self.activity_tracker = {
            "last_activity": None,
            "activity_start_time": None,
            "inactivity_count": 0,
            "recent_activities": []
        }
        
        # Drag state for smooth dragging
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.click_time = 0
        
        self.logger.info("Pet Manager initialized")
    
    async def run(self):
        """Start the pet assistant application"""
        self.is_running = True
        self.logger.info("Starting Pet Assistant...")
        
        try:
            # Initialize UI in main thread
            await self._initialize_ui()
            
            # Start screen monitoring in background
            monitor_task = asyncio.create_task(
                self.screen_monitor.start_monitoring(
                    callback=self._on_screen_change,
                    interval=self.config.get("screen", {}).get("capture_interval", 2.0)
                )
            )
            
            # Start spontaneous conversation system
            conversation_task = asyncio.create_task(self._start_spontaneous_conversations())
            
            # Start voice input if available
            if self.voice_input_manager:
                self.voice_input_manager.start_listening()
                self.logger.info("Voice input listening started")
            
            # Start UI loop
            ui_task = asyncio.create_task(self._run_ui_loop())
            
            # Wait for any task to complete
            await asyncio.gather(monitor_task, conversation_task, ui_task, return_exceptions=True)
            
        except Exception as e:
            self.logger.error(f"Error running pet manager: {e}")
            raise
        finally:
            self.is_running = False
    
    async def _initialize_ui(self):
        """Initialize the user interface"""
        # Create main window (hidden)
        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window
        
        # Create pet window
        await self._create_pet_window()
        
        self.logger.info("UI initialized")
    
    async def _create_pet_window(self):
        """Create the modern floating pet window"""
        self.pet_window = tk.Toplevel(self.root)
        
        # Window properties
        pet_config = self.config.get("pet", {})
        size = pet_config.get("size", {"width": 270, "height": 270})  # Default startup size
        
        self.pet_window.title("Pixie - Your AI Pet")
        self.pet_window.geometry(f"{size['width']}x{size['height']}")
        
        # Modern window styling
        ui_config = self.config.get("ui", {})
        if ui_config.get("always_on_top", True):
            self.pet_window.wm_attributes("-topmost", True)
        
        # Enhanced transparency for modern look
        transparency = ui_config.get("transparency", 0.95)
        self.pet_window.wm_attributes("-alpha", transparency)
        
        # Remove window decorations for floating effect
        self.pet_window.overrideredirect(True)
        
        # Set background for transparency
        self.pet_window.configure(bg='#000001')
        
        # Position window
        position = pet_config.get("position", {"x": -1, "y": -1})
        if position["x"] == -1 or position["y"] == -1:
            # Auto-position in bottom-right corner with padding for modern look
            screen_width = self.pet_window.winfo_screenwidth()
            screen_height = self.pet_window.winfo_screenheight()
            x = screen_width - size["width"] - 80
            y = screen_height - size["height"] - 120
        else:
            x, y = position["x"], position["y"]
        
        self.pet_window.geometry(f"+{x}+{y}")
        
        # Create modern pet display
        await self._setup_modern_pet_display()
        
        # Initialize speech bubble system
        if ModernSpeechBubble:
            self.speech_bubble = ModernSpeechBubble(
                self.pet_window, 
                pet_size=(size["width"], size["height"])
            )
            
            # Initialize conversation with some sample messages
            self._initialize_conversation_messages()
        
        # Bind window-level events for dragging
        self.pet_window.bind("<Button-3>", self._on_pet_right_click)
        
        self.logger.info("Modern pet window created")
    
    async def _setup_modern_pet_display(self):
        """Setup the modern pet display with animations and effects"""
        pet_config = self.config.get("pet", {})
        size = pet_config.get("size", {"width": 120, "height": 120})
        
        # Use modern pet widget if available, fallback to simple version
        if ModernPetWidget:
            self.pet_widget = ModernPetWidget(
                self.pet_window,
                size=(size["width"], size["height"]),
                pet_config=pet_config
            )
            
            # Connect drag and click events
            self.pet_widget.canvas.bind("<Button-1>", self._on_pet_press)
            self.pet_widget.canvas.bind("<B1-Motion>", self._on_pet_drag)
            self.pet_widget.canvas.bind("<ButtonRelease-1>", self._on_pet_release)
            self.pet_widget.canvas.bind("<Double-Button-1>", self._on_pet_double_click)
            self.pet_widget.canvas.bind("<Enter>", self._on_pet_hover_enter)
            self.pet_widget.canvas.bind("<Leave>", self._on_pet_hover_leave)
            
            # Store reference to canvas for activity indicator
            self.pet_canvas = self.pet_widget.canvas
        else:
            # Fallback to enhanced simple version
            self._setup_enhanced_simple_display(size)
    
    def _setup_enhanced_simple_display(self, size):
        """Enhanced simple display as fallback - now loads actual pet images"""
        self.canvas = tk.Canvas(
            self.pet_window,
            width=size["width"] - 20,
            height=size["height"] - 20,
            bg='#000001',
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Enable transparency
        self.pet_window.wm_attributes('-transparentcolor', '#000001')
        
        # Load and display the current pet image
        self._load_current_pet_image(size)
        
        # Store reference for compatibility
        self.pet_canvas = self.canvas
        
        # Bind events for dragging and clicking
        self.canvas.bind("<Button-1>", self._on_pet_press)
        self.canvas.bind("<B1-Motion>", self._on_pet_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_pet_release)
        self.canvas.bind("<Double-Button-1>", self._on_pet_double_click)
        self.canvas.bind("<Enter>", self._on_pet_hover_enter)
        self.canvas.bind("<Leave>", self._on_pet_hover_leave)
    
    def _load_current_pet_image(self, size):
        """Load the current pet image based on settings"""
        try:
            import os
            from PIL import Image, ImageTk
            
            # Get current pet info
            pet_info = self._get_current_pet_info()
            image_path = pet_info.get('image', 'react-app/public/ghost.png')
            
            # Check if image exists
            if not os.path.exists(image_path):
                self.logger.warning(f"Pet image not found: {image_path}, creating fallback")
                self._create_fallback_display(size)
                return
            
            # Load and resize image
            pil_image = Image.open(image_path)
            
            # Resize maintaining aspect ratio
            pil_image = pil_image.resize(
                (size["width"] - 40, size["height"] - 40), 
                Image.Resampling.LANCZOS
            )
            
            # Convert to PhotoImage
            self.pet_image = ImageTk.PhotoImage(pil_image)
            
            # Add image to canvas
            canvas_width = size["width"] - 20
            canvas_height = size["height"] - 20
            
            self.canvas.create_image(
                canvas_width // 2, 
                canvas_height // 2, 
                image=self.pet_image, 
                anchor="center",
                tags="pet"
            )
            
            self.logger.info(f"Loaded pet image: {image_path}")
            
        except Exception as e:
            self.logger.error(f"Error loading pet image: {e}")
            self._create_fallback_display(size)
    
    def _create_fallback_display(self, size):
        """Create fallback display when image loading fails"""
        center_x, center_y = (size["width"] - 20) // 2, (size["height"] - 20) // 2
        radius = min(size["width"], size["height"]) // 3
        
        # Glow effect
        for i in range(5):
            glow_radius = radius + i * 3
            self.canvas.create_oval(
                center_x - glow_radius, center_y - glow_radius,
                center_x + glow_radius, center_y + glow_radius,
                fill='#FF69B4', outline='', stipple='gray25'
            )
        
        # Main body with modern colors
        self.canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill='#FFB6C1', outline='#FF69B4', width=3
        )
        
        # Enhanced eyes
        eye_size = 8
        left_eye_x, right_eye_x = center_x - 15, center_x + 15
        eye_y = center_y - 8
        
        # Eye whites
        self.canvas.create_oval(left_eye_x - eye_size, eye_y - 4, left_eye_x + eye_size, eye_y + 4, fill='white', outline='#ddd')
        self.canvas.create_oval(right_eye_x - eye_size, eye_y - 4, right_eye_x + eye_size, eye_y + 4, fill='white', outline='#ddd')
        
        # Pupils
        self.canvas.create_oval(left_eye_x - 3, eye_y - 3, left_eye_x + 3, eye_y + 3, fill='#333')
        self.canvas.create_oval(right_eye_x - 3, eye_y - 3, right_eye_x + 3, eye_y + 3, fill='#333')
        
        # Sparkles
        self.canvas.create_oval(left_eye_x - 1, eye_y - 2, left_eye_x + 1, eye_y, fill='white')
        self.canvas.create_oval(right_eye_x - 1, eye_y - 2, right_eye_x + 1, eye_y, fill='white')
        
        # Nose
        self.canvas.create_polygon(center_x - 3, center_y + 5, center_x + 3, center_y + 5, center_x, center_y - 2, fill='#FF1493', outline='#C71585')
        
        # Mouth
        self.canvas.create_arc(center_x - 12, center_y + 8, center_x + 12, center_y + 20, start=0, extent=180, outline='#FF1493', width=2, style='arc')
    
    def _on_pet_press(self, event):
        """Handle mouse press on pet - start drag or prepare for click"""
        import time
        self.click_time = time.time()
        self.dragging = False
        
        # Store initial mouse position relative to window
        self.drag_start_x = event.x_root - self.pet_window.winfo_x()
        self.drag_start_y = event.y_root - self.pet_window.winfo_y()
        
        # Change cursor to indicate draggable
        self.pet_window.config(cursor="fleur")
    
    def _on_pet_drag(self, event):
        """Handle pet dragging - move the window"""
        import time
        
        # Start dragging immediately if mouse has moved (more responsive)
        if not self.dragging and time.time() - self.click_time > 0.05:
            self.dragging = True
            # Add slight transparency while dragging for visual feedback
            try:
                self.pet_window.wm_attributes("-alpha", 0.9)  # Less transparent for better visibility
            except:
                pass  # Alpha not supported on all systems
        
        if self.dragging:
            # Calculate new window position
            new_x = event.x_root - self.drag_start_x
            new_y = event.y_root - self.drag_start_y
            
            # Keep pet within screen bounds
            screen_width = self.pet_window.winfo_screenwidth()
            screen_height = self.pet_window.winfo_screenheight()
            pet_width = self.pet_window.winfo_width()
            pet_height = self.pet_window.winfo_height()
            
            # Constrain to screen bounds with small margin
            margin = 10
            new_x = max(-margin, min(new_x, screen_width - pet_width + margin))
            new_y = max(-margin, min(new_y, screen_height - pet_height + margin))
            
            # Move the window smoothly
            self.pet_window.geometry(f"+{new_x}+{new_y}")
    
    def _on_pet_release(self, event):
        """Handle mouse release - save position or handle click"""
        import time
        
        # Reset cursor
        self.pet_window.config(cursor="")
        
        # Restore full opacity
        try:
            self.pet_window.wm_attributes("-alpha", 1.0)
        except:
            pass
        
        if not self.dragging and time.time() - self.click_time < 0.3:
            # This was a click, not a drag - show speech bubble instead of chat
            asyncio.create_task(self._show_pet_message())
        elif self.dragging:
            # Save the new position immediately (hot-reload ignores position-only changes)
            self._save_pet_position()
        
        self.dragging = False
    
    def _initialize_conversation_messages(self):
        """Initialize conversation messages for the pet"""
        self.conversation_messages = [
            "Hi! I'm Pixie! 🐱✨",
            "I'm here to help you! 💫",
            "What are you working on? 🤔",
            "I can see your screen and help! 👀",
            "Click me again for more! 😊",
            "I love being your assistant! ❤️",
            "Let me know if you need help! 🚀",
            "I'm always watching over you! 👁️",
            "Your productivity buddy is here! 💪",
            "Ready for some AI magic? ✨",
            "Double-click me for screen analysis! 🔍",
            "Right-click for more options! 📋",
            "I can help with any questions! 🤓",
            "Your virtual companion at work! 💼",
            "I'm learning about your workflow! 📊"
        ]
        self.message_index = 0
    
    async def _show_pet_message(self):
        """Show a speech bubble message from the pet"""
        if not self.speech_bubble or not self.conversation_messages:
            return
        
        # Get next message in rotation
        message = self.conversation_messages[self.message_index]
        self.message_index = (self.message_index + 1) % len(self.conversation_messages)
        
        # Show the message with typing effect
        self.speech_bubble.show_message(message, typing_effect=True)
        
        # Log the interaction
        self.logger.info(f"Pet said: {message}")
    
    def _on_pet_double_click(self, event):
        """Handle double-click - quick screen analysis"""
        asyncio.create_task(self._analyze_current_screen())
    
    def _save_pet_position(self):
        """Save the current pet position to config"""
        try:
            current_x = self.pet_window.winfo_x()
            current_y = self.pet_window.winfo_y()
            
            # Update config in memory
            if "pet" not in self.config:
                self.config["pet"] = {}
            if "position" not in self.config["pet"]:
                self.config["pet"]["position"] = {}
            
            self.config["pet"]["position"]["x"] = current_x
            self.config["pet"]["position"]["y"] = current_y
            
            # Save to config file immediately (hot-reload will ignore position-only changes)
            from src.utils.config_manager import ConfigManager
            config_manager = ConfigManager()
            config_manager.save_config(self.config)
            
            self.logger.info(f"Pet position saved: ({current_x}, {current_y})")
            
        except Exception as e:
            self.logger.error(f"Failed to save pet position: {e}")
    
    def _on_pet_hover_enter(self, event):
        """Handle mouse entering pet area - show drag cursor"""
        self.pet_window.config(cursor="hand2")
    
    def _on_pet_hover_leave(self, event):
        """Handle mouse leaving pet area - reset cursor"""
        if not self.dragging:
            self.pet_window.config(cursor="")
    
    def _get_context_menu_class(self):
        """Get the appropriate context menu class based on theme"""
        ui_config = self.config.get("ui", {})
        theme_type = ui_config.get("theme", "modern_ui")
        
        # Use cardboard theme if available and selected, otherwise modern
        if theme_type == "cardboard" and CardboardContextMenu is not None:
            return CardboardContextMenu
        elif ModernContextMenu is not None:
            return ModernContextMenu
        else:
            return None
    
    def _on_pet_right_click(self, event):
        """Handle right click - show themed context menu"""
        ContextMenuClass = self._get_context_menu_class()
        
        if ContextMenuClass:
            # Determine current theme for toggle text
            current_theme = self.style_manager.get_theme() if self.style_manager else None
            is_dark = current_theme.is_dark_theme() if current_theme else False
            theme_text = "☀️ Switch to Light Mode" if is_dark else "🌙 Switch to Dark Mode"
            
            # Get current mood emoji
            mood_emoji = {
                "helpful": "🤝",
                "playful": "😸", 
                "curious": "🤔",
                "encouraging": "💪",
                "sleepy": "😴",
                "excited": "🎉"
            }.get(self.current_mood, "🐾")
            
            # Streamlined main menu - most common actions first
            menu_options = [
                ("💬 Chat with Pixie", lambda: asyncio.create_task(self._ask_pixie_something())),
                ("📸 Analyze Screen", lambda: asyncio.create_task(self._analyze_current_screen())),
                (" Fix Current File", lambda: asyncio.create_task(self._fix_current_vscode_file())),
                "---",  # Separator
                ("🛠️ Code Tools ►", lambda: self._show_code_tools_submenu(event)),
                ("📊 Google Sheets ►", lambda: self._show_sheets_submenu(event)),
                ("🎭 Pet Options ►", lambda: self._show_pet_options_submenu(event)),
                ("⚙️ Settings ►", lambda: self._show_settings_submenu(event)),
                "---",  # Separator
                ("❌ Exit", self._exit_application)
            ]
            
            context_menu = ContextMenuClass(self.root)
            context_menu.show(event.x_root, event.y_root, menu_options)
        else:
            # Fallback to standard menu with better styling
            menu = tk.Menu(self.root, tearoff=0, font=('Segoe UI', 10))
            menu.add_command(label="💬 Chat with Pixie", command=lambda: asyncio.create_task(self._open_chat_interface()))
            menu.add_command(label="📸 Take Screenshot & Analyze", command=lambda: asyncio.create_task(self._analyze_current_screen()))
            menu.add_separator()
            menu.add_command(label="🎯 Fix Current File", command=lambda: asyncio.create_task(self._fix_current_vscode_file()))
            menu.add_separator()
            menu.add_command(label="�️ Generate Code", command=lambda: asyncio.create_task(self._show_code_generation_menu()))
            menu.add_command(label="📝 Analyze Code", command=lambda: asyncio.create_task(self._analyze_code_interface()))
            menu.add_command(label="🔧 Fix Code Errors", command=lambda: asyncio.create_task(self._fix_code_interface()))
            menu.add_command(label="🧪 Generate Tests", command=lambda: asyncio.create_task(self._generate_tests_interface()))
            menu.add_separator()
            menu.add_command(label="�🔍 Make Bigger", command=self._resize_bigger)
            menu.add_command(label="🔎 Make Smaller", command=self._resize_smaller)
            menu.add_command(label="📏 Reset Size", command=self._reset_pet_size)
            menu.add_separator()
            menu.add_command(label="⚙️ Settings", command=self._open_settings)
            menu.add_command(label="❌ Exit", command=self._exit_application)
            
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

    def _show_code_tools_submenu(self, parent_event):
        """Show code tools submenu"""
        ContextMenuClass = self._get_context_menu_class()
        if ContextMenuClass:
            submenu_options = [
                ("🛠️ Generate Code", lambda: asyncio.create_task(self._show_code_generation_menu())),
                ("📝 Analyze Code", lambda: asyncio.create_task(self._analyze_code_interface())),
                ("🔧 Fix Code Errors", lambda: asyncio.create_task(self._fix_code_interface())),
                ("🧪 Generate Tests", lambda: asyncio.create_task(self._generate_tests_interface())),
                ("💬 Full Chat Window", lambda: asyncio.create_task(self._open_chat_interface()))
            ]
            submenu = ContextMenuClass(self.root)
            submenu.show(parent_event.x_root + 20, parent_event.y_root, submenu_options)

    def _show_pet_options_submenu(self, parent_event):
        """Show pet options submenu"""
        ContextMenuClass = self._get_context_menu_class()
        if ContextMenuClass:
            # Get current mood emoji
            mood_emoji = {
                "helpful": "🤝", "playful": "😸", "curious": "🤔",
                "encouraging": "💪", "sleepy": "😴", "excited": "🎉"
            }.get(self.current_mood, "🐾")
            
            submenu_options = [
                ("🎭 Change Mood", lambda: self._change_mood_menu()),
                (f"Current: {self.current_mood.title()} {mood_emoji}", lambda: None),
                "---",
                ("🎤 Voice Question", lambda: asyncio.create_task(self._ask_pixie_voice())),
                ("💬 Make Pet Talk", lambda: asyncio.create_task(self._make_spontaneous_comment())),
                "---",
                ("🔍 Make Bigger", self._resize_bigger),
                ("🔎 Make Smaller", self._resize_smaller),
                ("📏 Reset Size", self._reset_pet_size)
            ]
            submenu = ContextMenuClass(self.root)
            submenu.show(parent_event.x_root + 20, parent_event.y_root, submenu_options)

    def _show_settings_submenu(self, parent_event):
        """Show settings submenu"""
        ContextMenuClass = self._get_context_menu_class()
        if ContextMenuClass:
            # Determine current theme for toggle text
            current_theme = self.style_manager.get_theme() if self.style_manager else None
            is_dark = current_theme.is_dark_theme() if current_theme else False
            theme_text = "☀️ Light Mode" if is_dark else "🌙 Dark Mode"
            
            submenu_options = [
                (theme_text, self._toggle_dark_mode),
                ("⚙️ Open Settings", self._open_settings),
                "---",
                ("🎭 Change Pet ►", lambda: self._show_pet_selection_submenu(parent_event)),
                ("📋 View Logs", lambda: self._open_log_file()),
                ("🔄 Restart Pet", lambda: self._restart_application())
            ]
            submenu = ContextMenuClass(self.root)
            submenu.show(parent_event.x_root + 20, parent_event.y_root, submenu_options)

    def _show_pet_selection_submenu(self, parent_event):
        """Show pet selection submenu"""
        ContextMenuClass = self._get_context_menu_class()
        if ContextMenuClass:
            current_pet = self.settings.get('pet', {}).get('current_pet', 'ghost')
            
            submenu_options = [
                ("👻 Ghost Pixie" + (" ✓" if current_pet == "ghost" else ""), 
                 lambda: asyncio.create_task(self._change_pet("ghost"))),
                ("⏰ Time Keeper" + (" ✓" if current_pet == "clock" else ""), 
                 lambda: asyncio.create_task(self._change_pet("clock"))),
                ("🏠 Home Guardian" + (" ✓" if current_pet == "house" else ""), 
                 lambda: asyncio.create_task(self._change_pet("house")))
            ]
            submenu = ContextMenuClass(self.root)
            submenu.show(parent_event.x_root + 40, parent_event.y_root, submenu_options)

    def _show_sheets_submenu(self, parent_event):
        """Show Google Sheets submenu"""
        ContextMenuClass = self._get_context_menu_class()
        if ContextMenuClass:
            # Check if sheets manager is available
            sheets_available = self.sheets_manager and self.sheets_manager.is_connected()
            csv_available = self.csv_logger is not None
            
            if csv_available:
                row_count = self.csv_logger.get_row_count()
                status_text = f"📄 CSV Ready ({row_count} entries)"
            else:
                status_text = "✅ API Connected" if sheets_available else "⚠️ Not Connected"
            
            submenu_options = [
                (f"Status: {status_text}", lambda: None),
                "---",
                # Simple CSV options (always available)
                ("📄 Log to CSV (Simple)", lambda: asyncio.create_task(self._log_to_csv())),
                ("📋 Show CSV Instructions", lambda: self._show_csv_import_guide()),
                ("📁 Open CSV File", lambda: self._open_csv_file()),
                "---",
                # Advanced API options
                ("📊 Connect to Sheet (API)", lambda: asyncio.create_task(self._connect_to_sheet())),
                ("📝 Create Project Tracker", lambda: asyncio.create_task(self._create_project_sheet())),
                ("📈 Insert Screen Analysis", lambda: asyncio.create_task(self._analyze_screen_to_sheet())),
                "---",
                ("🔧 Setup Google Sheets", lambda: self._setup_google_sheets()),
                ("📖 View Sheet", lambda: self._open_current_sheet())
            ]
            submenu = ContextMenuClass(self.root)
            submenu.show(parent_event.x_root + 20, parent_event.y_root, submenu_options)
    
    def _show_activity_indicator(self, active: bool = True):
        """Show or hide activity indicator with modern styling"""
        if hasattr(self, 'pet_widget') and self.pet_widget:
            # Use modern pet widget method
            self.pet_widget.show_activity(active)
        elif hasattr(self, 'pet_canvas'):
            # Fallback method
            if active:
                # Create modern activity indicator
                if not hasattr(self, 'activity_indicator'):
                    center_x = self.pet_canvas.winfo_width() // 2
                    self.activity_indicator = self.pet_canvas.create_text(
                        center_x, 15, text="💭", font=("Segoe UI Emoji", 14),
                        fill='#4A90E2', tags="activity"
                    )
                self.pet_canvas.itemconfig(self.activity_indicator, state='normal')
            else:
                if hasattr(self, 'activity_indicator'):
                    self.pet_canvas.itemconfig(self.activity_indicator, state='hidden')
    
    async def _open_chat_interface(self):
        """Open the modern chat interface window"""
        if hasattr(self, 'modern_chat') and self.modern_chat.window and self.modern_chat.window.winfo_exists():
            self.modern_chat.window.lift()
            return
        
        # Use modern chat window if available
        if ModernChatWindow:
            self.modern_chat = ModernChatWindow(self.root, "Chat with Pixie 🐱")
            self.chat_window = self.modern_chat.window
            self.chat_display = self.modern_chat.chat_display
            self.chat_input = self.modern_chat.chat_input
            
            # Get buttons and connect events
            send_button, analyze_button = self.modern_chat._create_input_area()
            send_button.configure(command=lambda: asyncio.create_task(self._send_chat_message()))
            analyze_button.configure(command=lambda: asyncio.create_task(self._analyze_current_screen()))
            
            # Bind Enter key
            self.chat_input.bind("<Control-Return>", lambda e: asyncio.create_task(self._send_chat_message()))
            
            # Welcome message with modern styling
            self._add_modern_chat_message("Pixie", "Hi there! 🐾 I'm Pixie, your AI assistant! I can see what's on your screen and help you with whatever you're working on. What can I help you with today?")
            
        else:
            # Fallback to enhanced simple version
            await self._create_enhanced_simple_chat()
        
        self.chat_input.focus_set()
    
    async def _create_enhanced_simple_chat(self):
        """Enhanced simple chat as fallback"""
        self.chat_window = tk.Toplevel(self.root)
        self.chat_window.title("Chat with Pixie 🐱")
        self.chat_window.geometry("450x600")
        self.chat_window.wm_attributes("-topmost", True)
        self.chat_window.configure(bg='#f8f9fa')
        
        # Title bar
        title_frame = tk.Frame(self.chat_window, bg='#667eea', height=40)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, text="💬 Chat with Pixie",
            font=('Segoe UI', 12, 'bold'), bg='#667eea', fg='white'
        )
        title_label.pack(side='left', padx=15, pady=10)
        
        # Chat area
        chat_container = tk.Frame(self.chat_window, bg='#f8f9fa')
        chat_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.chat_display = tk.Text(
            chat_container, wrap='word', state='disabled',
            bg='white', fg='#2c3e50', font=('Segoe UI', 10),
            bd=0, padx=15, pady=15, relief='flat'
        )
        scrollbar = ttk.Scrollbar(chat_container, orient="vertical", command=self.chat_display.yview)
        self.chat_display.configure(yscrollcommand=scrollbar.set)
        
        self.chat_display.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Input area
        input_container = tk.Frame(self.chat_window, bg='#f8f9fa')
        input_container.pack(fill='x', padx=20, pady=(0, 20))
        
        input_frame = tk.Frame(input_container, bg='white', relief='flat', bd=1)
        input_frame.pack(fill='x', pady=(0, 10))
        
        self.chat_input = tk.Text(
            input_frame, height=3, wrap='word',
            bg='white', fg='#2c3e50', font=('Segoe UI', 10),
            bd=0, padx=15, pady=10, relief='flat'
        )
        self.chat_input.pack(fill='both', expand=True)
        
        # Buttons
        button_frame = tk.Frame(input_container, bg='#f8f9fa')
        button_frame.pack(fill='x')
        
        send_button = tk.Button(
            button_frame, text="Send Message",
            font=('Segoe UI', 10, 'bold'), bg='#667eea', fg='white',
            bd=0, padx=20, pady=8, relief='flat',
            command=lambda: asyncio.create_task(self._send_chat_message())
        )
        send_button.pack(side='right', padx=(10, 0))
        
        analyze_button = tk.Button(
            button_frame, text="📸 Analyze Screen",
            font=('Segoe UI', 10), bg='#48c78e', fg='white',
            bd=0, padx=20, pady=8, relief='flat',
            command=lambda: asyncio.create_task(self._analyze_current_screen())
        )
        analyze_button.pack(side='right')
        
        # Configure message styling
        self.chat_display.tag_configure("user_message", font=('Segoe UI', 10, 'bold'), foreground='#667eea')
        self.chat_display.tag_configure("pixie_message", font=('Segoe UI', 10, 'bold'), foreground='#48c78e')
        self.chat_display.tag_configure("message_content", font=('Segoe UI', 10), foreground='#2c3e50')
        
        # Welcome message
        self._add_modern_chat_message("Pixie", "Hi there! 🐾 I'm Pixie, your AI assistant! I can see what's on your screen and help you with whatever you're working on. What can I help you with today?")
    
    async def _send_chat_message(self):
        """Send a chat message to the AI"""
        message = self.chat_input.get(1.0, 'end-1c').strip()
        if not message:
            return
        
        # Clear input
        self.chat_input.delete(1.0, 'end')
        
        # Add user message to display
        self._add_chat_message("You", message)
        
        # Show thinking indicator
        thinking_id = self._add_chat_message("Pixie", "🤔 Thinking...")
        
        try:
            # Get enhanced response from AI with conversation context
            response = await self._enhanced_chat_response(message)
            
            # Replace thinking message with response
            self._replace_chat_message(thinking_id, "Pixie", response)
            
        except Exception as e:
            self.logger.error(f"Error getting AI response: {e}")
            self._replace_chat_message(thinking_id, "Pixie", "Sorry, I'm having trouble thinking right now. Could you try again? 🐱")
    
    async def _analyze_current_screen(self):
        """Advanced technical screen analysis with detailed insights"""
        try:
            # Show activity indicator
            self._show_activity_indicator(True)
            
            # Advanced screenshot capture with metadata
            screenshot = self.screen_monitor.get_screenshot()
            context = self.screen_monitor.get_screen_context()
            
            if not screenshot:
                await self._show_speech_bubble("❌ Screen capture failed. Check permissions!", duration=3000)
                return
            
            # Enhanced context gathering
            enhanced_context = await self._gather_enhanced_screen_context(context)
            
            await self._show_speech_bubble("🔍 Analyzing screen (AI + OCR + Context)...", duration=2000)
            
            # Multi-modal analysis
            analysis_results = await self._perform_advanced_screen_analysis(screenshot, enhanced_context)
            
            # Show detailed results in technical interface
            await self._show_technical_analysis_results(analysis_results)
            
        except Exception as e:
            self.logger.error(f"Error analyzing screen: {e}")
            error_msg = "I'm having trouble seeing your screen right now. Please try again! 🐱"
            
            # Show error in speech bubble if available
            if self.speech_bubble:
                self.speech_bubble.show_message(error_msg, typing_effect=True)
            elif self.chat_window and self.chat_window.winfo_exists():
                self._add_chat_message("Pixie", error_msg)
            else:
                messagebox.showerror("Error", error_msg)
        
        finally:
            # Hide activity indicator
            self._show_activity_indicator(False)
    
    async def _gather_enhanced_screen_context(self, base_context: Dict) -> Dict:
        """Gather comprehensive screen context for analysis"""
        enhanced_context = base_context.copy() if base_context else {}
        
        try:
            # Add system information
            import platform
            import psutil
            
            enhanced_context.update({
                'system_info': {
                    'os': platform.system(),
                    'version': platform.release(),
                    'python_version': platform.python_version()
                },
                'resource_usage': {
                    'memory_percent': psutil.virtual_memory().percent,
                    'cpu_percent': psutil.cpu_percent(),
                    'disk_usage': psutil.disk_usage('/').percent if platform.system() != 'Windows' else psutil.disk_usage('C:').percent
                },
                'timestamp': time.time()
            })
            
            # Add VS Code context if available
            if self.vscode_integration:
                try:
                    vscode_context = await self.vscode_integration.get_workspace_info()
                    enhanced_context['vscode'] = vscode_context
                except Exception as e:
                    self.logger.warning(f"Could not get VS Code context: {e}")
            
            # Add recent activity context
            enhanced_context['activity_history'] = self.activity_tracker.get('recent_activities', [])[-5:]
            enhanced_context['current_mood'] = self.current_mood
            
        except Exception as e:
            self.logger.error(f"Error gathering enhanced context: {e}")
        
        return enhanced_context
    
    async def _perform_advanced_screen_analysis(self, screenshot, enhanced_context: Dict) -> Dict:
        """Perform comprehensive screen analysis with AI and technical insights"""
        analysis_results = {
            'ai_analysis': None,
            'technical_insights': {},
            'suggestions': [],
            'detected_issues': [],
            'screenshot_metadata': {}
        }
        
        try:
            # Screenshot metadata
            if screenshot:
                analysis_results['screenshot_metadata'] = {
                    'size': f"{screenshot.width}x{screenshot.height}",
                    'mode': screenshot.mode if hasattr(screenshot, 'mode') else 'Unknown',
                    'timestamp': time.time()
                }
            
            # AI Analysis
            if self.gemini_client and screenshot:
                ai_prompt = f"""
                Analyze this screenshot with technical depth. Consider:
                
                Context: {enhanced_context}
                
                Please provide:
                1. What application/environment is visible
                2. Any errors, warnings, or issues visible
                3. Workflow optimization suggestions
                4. Code quality observations (if code is visible)
                5. Performance recommendations
                6. Security considerations
                
                Be specific and technical in your analysis.
                """
                
                analysis_results['ai_analysis'] = await self.gemini_client.analyze_screen(
                    screenshot=screenshot,
                    context=enhanced_context,
                    prompt=ai_prompt
                )
            
            # Technical insights based on context
            active_app = enhanced_context.get('active_app', '').lower()
            
            if 'code' in active_app or 'visual studio' in active_app:
                analysis_results['technical_insights']['environment'] = 'Development'
                analysis_results['suggestions'].append("💡 Consider using code analysis tools")
                analysis_results['suggestions'].append("🔍 Check for syntax highlighting errors")
            
            elif 'browser' in active_app or 'chrome' in active_app or 'firefox' in active_app:
                analysis_results['technical_insights']['environment'] = 'Web Browsing'
                analysis_results['suggestions'].append("🌐 Check browser developer tools (F12)")
                analysis_results['suggestions'].append("🔒 Verify SSL/HTTPS security")
            
            elif 'terminal' in active_app or 'cmd' in active_app or 'powershell' in active_app:
                analysis_results['technical_insights']['environment'] = 'Command Line'
                analysis_results['suggestions'].append("⚡ Consider using command history (↑)")
                analysis_results['suggestions'].append("📝 Document complex commands")
            
            # Resource usage insights
            resource_usage = enhanced_context.get('resource_usage', {})
            memory_percent = resource_usage.get('memory_percent', 0)
            cpu_percent = resource_usage.get('cpu_percent', 0)
            
            if memory_percent > 80:
                analysis_results['detected_issues'].append(f"⚠️ High memory usage: {memory_percent:.1f}%")
                analysis_results['suggestions'].append("💾 Close unused applications")
            
            if cpu_percent > 80:
                analysis_results['detected_issues'].append(f"⚠️ High CPU usage: {cpu_percent:.1f}%")
                analysis_results['suggestions'].append("⚡ Check task manager for resource-heavy processes")
            
        except Exception as e:
            self.logger.error(f"Error in advanced screen analysis: {e}")
            analysis_results['error'] = str(e)
        
        return analysis_results
    
    async def _show_technical_analysis_results(self, analysis_results: Dict):
        """Display comprehensive analysis results in technical format"""
        try:
            # Build technical report
            report_lines = [
                "🔍 ADVANCED SCREEN ANALYSIS",
                "=" * 35,
                ""
            ]
            
            # Screenshot metadata
            metadata = analysis_results.get('screenshot_metadata', {})
            if metadata:
                report_lines.extend([
                    "📸 Screenshot Info:",
                    f"  • Resolution: {metadata.get('size', 'Unknown')}",
                    f"  • Format: {metadata.get('mode', 'Unknown')}",
                    ""
                ])
            
            # Technical insights
            insights = analysis_results.get('technical_insights', {})
            if insights:
                report_lines.append("🔧 Technical Insights:")
                for key, value in insights.items():
                    report_lines.append(f"  • {key.title()}: {value}")
                report_lines.append("")
            
            # Detected issues
            issues = analysis_results.get('detected_issues', [])
            if issues:
                report_lines.append("⚠️ Detected Issues:")
                for issue in issues:
                    report_lines.append(f"  • {issue}")
                report_lines.append("")
            
            # Suggestions
            suggestions = analysis_results.get('suggestions', [])
            if suggestions:
                report_lines.append("💡 Optimization Suggestions:")
                for suggestion in suggestions[:5]:  # Limit to top 5
                    report_lines.append(f"  • {suggestion}")
                report_lines.append("")
            
            # AI Analysis summary
            ai_analysis = analysis_results.get('ai_analysis', '')
            if ai_analysis:
                # Truncate for speech bubble
                ai_summary = ai_analysis[:200] + "..." if len(ai_analysis) > 200 else ai_analysis
                report_lines.extend([
                    "🤖 AI Analysis:",
                    ai_summary,
                    ""
                ])
            
            # Create final report
            final_report = "\n".join(report_lines)
            
            # Show in speech bubble (truncated) and log full report
            speech_summary = final_report[:400] + "\n\n📊 Full report logged to console."
            await self._show_speech_bubble(speech_summary, duration=8000)
            
            # Log complete analysis
            self.logger.info(f"Complete Screen Analysis:\n{final_report}")
            
            if ai_analysis:
                self.logger.info(f"Full AI Analysis:\n{ai_analysis}")
            
        except Exception as e:
            self.logger.error(f"Error showing analysis results: {e}")
            await self._show_speech_bubble("❌ Analysis complete but display failed. Check logs.", duration=3000)
    
    def _add_modern_chat_message(self, sender: str, message: str) -> str:
        """Add a message with modern styling"""
        if hasattr(self, 'modern_chat') and self.modern_chat:
            # Use modern chat window method
            self.modern_chat.add_message(sender, message)
            return "modern_message"
        else:
            # Fallback to enhanced simple version
            return self._add_chat_message(sender, message)
    
    def _add_chat_message(self, sender: str, message: str) -> str:
        """Add a message to the chat display (enhanced version)"""
        if not hasattr(self, 'chat_display'):
            return ""
        
        self.chat_display.config(state='normal')
        
        # Create unique tag for this message
        import uuid
        message_id = str(uuid.uuid4())
        
        # Add sender with emoji and modern styling
        sender_icon = "🤖 " if sender == "Pixie" else "👤 "
        sender_tag = "pixie_message" if sender == "Pixie" else "user_message"
        
        self.chat_display.insert('end', f"{sender_icon}{sender}\n", sender_tag)
        self.chat_display.insert('end', f"{message}\n\n", "message_content")
        
        self.chat_display.config(state='disabled')
        self.chat_display.see('end')
        
        return message_id
    
    def _replace_chat_message(self, message_id: str, sender: str, new_message: str):
        """Replace a chat message (for updating thinking indicators)"""
        if not hasattr(self, 'chat_display'):
            return
        
        self.chat_display.config(state='normal')
        
        # Find and replace the message
        try:
            start_index = self.chat_display.tag_ranges(f"sender_{message_id}")[0]
            end_index = self.chat_display.tag_ranges(f"message_{message_id}")[1]
            
            self.chat_display.delete(start_index, end_index)
            self.chat_display.insert(start_index, f"{sender}: {new_message}\n\n")
            
        except (IndexError, tk.TclError):
            # If we can't find the message, just add a new one
            self._add_chat_message(sender, new_message)
        
        self.chat_display.config(state='disabled')
        self.chat_display.see('end')
    
    async def _on_screen_change(self, window_info: Dict[str, Any]):
        """Handle screen/window changes"""
        self.current_context = {
            "window_info": window_info,
            "app_type": self.screen_monitor.detect_application_type(window_info),
            "timestamp": asyncio.get_event_loop().time(),
            "active_app": window_info.get("app_name", "Unknown")
        }
        
        self.logger.debug(f"Screen changed to: {window_info.get('title', 'Unknown')}")
        
        # React to screen changes with enhanced conversation system
        if self.gemini_client:
            await self._react_to_screen_change(self.current_context)
    
    def _on_voice_input(self, text: str):
        """Handle voice input from the microphone"""
        self.logger.info(f"Voice input received: '{text}'")
        
        # Run the async response in a thread to avoid blocking
        def handle_voice_async():
            try:
                asyncio.run(self._process_voice_question(text))
            except Exception as e:
                self.logger.error(f"Error processing voice input: {e}")
        
        # Start processing in a separate thread
        voice_thread = threading.Thread(target=handle_voice_async, daemon=True)
        voice_thread.start()
    
    async def _process_voice_question(self, question: str):
        """Process a voice question and provide AI response"""
        try:
            # Add visual indicator that we're processing
            if self.speech_bubble:
                self.speech_bubble.show_message("🎤 Thinking...", duration=2000)
            
            # Get AI response
            response = await self.gemini_client.chat_response(
                message=question,
                context=self.current_context
            )
            
            if response:
                # Show response in speech bubble with dynamic duration
                if self.speech_bubble:
                    # Let the bubble calculate its own duration based on length
                    self.speech_bubble.show_message(f"💭 {response}")
                
                # Add to chat history
                self._add_chat_message("You", question)
                self._add_chat_message("Pixie", response)
                
                # Speak the response
                if self.speech_manager:
                    def speak_response():
                        try:
                            self.speech_manager.speak_text(response)
                        except Exception as e:
                            self.logger.error(f"Error speaking response: {e}")
                    
                    # Speak in a separate thread
                    speech_thread = threading.Thread(target=speak_response, daemon=True)
                    speech_thread.start()
                
                self.logger.info(f"AI response to voice: {response[:100]}...")
            else:
                error_msg = "Sorry, I couldn't understand that. Could you try again?"
                if self.speech_bubble:
                    self.speech_bubble.show_message(f"❓ {error_msg}")
                
                if self.speech_manager:
                    def speak_error():
                        try:
                            self.speech_manager.speak_text(error_msg)
                        except Exception as e:
                            self.logger.error(f"Error speaking error message: {e}")
                    
                    speech_thread = threading.Thread(target=speak_error, daemon=True)
                    speech_thread.start()
        
        except Exception as e:
            self.logger.error(f"Error processing voice question: {e}")
            error_msg = "Sorry, I had trouble processing that question."
            if self.speech_bubble:
                self.speech_bubble.show_message(f"❌ {error_msg}")
    
    def _open_settings(self):
        """Open settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Pixie Settings")
        settings_window.geometry("300x200")
        settings_window.wm_attributes("-topmost", True)
        
        ttk.Label(settings_window, text="Settings coming soon! 🛠️").pack(expand=True)
        ttk.Button(settings_window, text="Close", command=settings_window.destroy).pack(pady=10)

    def _open_log_file(self):
        """Open the log file in default text editor"""
        try:
            log_path = Path("logs") / f"pet_assistant_{time.strftime('%Y%m%d')}.log"
            if log_path.exists():
                import os
                os.startfile(str(log_path))  # Windows
            else:
                messagebox.showinfo("Log File", "No log file found for today.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open log file: {e}")

    def _restart_application(self):
        """Restart the application"""
        if messagebox.askquestion("Restart", "Restart Pixie? This will close and reopen the pet.") == 'yes':
            try:
                import subprocess
                import sys
                # Get the path to the current Python executable and script
                python_exe = sys.executable
                script_path = Path(__file__).parent.parent.parent / "main.py"
                
                # Start new process
                subprocess.Popen([python_exe, str(script_path)])
                
                # Close current instance
                self._exit_application()
            except Exception as e:
                messagebox.showerror("Restart Error", f"Could not restart application: {e}")
    
    def _exit_application(self):
        """Exit the application"""
        if messagebox.askquestion("Exit", "Are you sure you want to close Pixie?") == 'yes':
            self.is_running = False
            self.screen_monitor.stop_monitoring()
            
            # Cleanup speech manager
            if hasattr(self, 'speech_manager') and self.speech_manager:
                self.speech_manager.cleanup()
            
            # Cleanup voice input manager
            if hasattr(self, 'voice_input_manager') and self.voice_input_manager:
                self.voice_input_manager.stop_listening()
            
            if self.root:
                self.root.quit()
                self.root.destroy()
            sys.exit(0)
    
    def _resize_bigger(self):
        """Increase pet size through menu"""
        if self.pet_widget:
            self.pet_widget._resize_pet(delta=20)
    
    def _resize_smaller(self):
        """Decrease pet size through menu"""
        if self.pet_widget:
            self.pet_widget._resize_pet(delta=-20)
    
    def _reset_pet_size(self):
        """Reset pet to default size through menu"""
        if self.pet_widget:
            self.pet_widget._resize_pet(reset_to_default=True)
    
    async def _run_ui_loop(self):
        """Run the UI event loop with optimized frequency"""
        frame_time = 1/30  # 30 FPS instead of 100 FPS for better performance
        while self.is_running and self.root and self.root.winfo_exists():
            try:
                frame_start = time.time()
                self.root.update()
                
                # Adaptive sleep to maintain consistent frame rate
                elapsed = time.time() - frame_start
                sleep_time = max(0.001, frame_time - elapsed)  # Min 1ms sleep
                await asyncio.sleep(sleep_time)
            except tk.TclError:
                # Window was destroyed
                break
            except Exception as e:
                self.logger.error(f"Error in UI loop: {e}")
        
        self.is_running = False
    
    # ===== Code Generation Features =====
    
    async def _show_code_generation_menu(self):
        """Show code generation interface"""
        try:
            if not self.gemini_client:
                await self._show_speech_bubble("I need a Gemini API key to generate code! 🔑")
                return
            
            # Create a simple input dialog
            request = simpledialog.askstring(
                "Code Generation 🛠️",
                "What code would you like me to generate?\n\nExample: 'Create a Python function to sort a list of dictionaries by name'"
            )
            
            if request:
                await self._show_speech_bubble("Generating code... 🔧", duration=2000)
                
                # Detect language from context or ask user
                language = self._detect_current_language()
                if not language:
                    language = simpledialog.askstring(
                        "Programming Language",
                        "Which programming language? (python, javascript, java, etc.)"
                    ) or "python"
                
                # Generate code
                result = await self.gemini_client.generate_code(
                    request=request,
                    language=language,
                    context=self._get_current_file_context()
                )
                
                if result.get('success'):
                    await self._show_code_result_window(result, "Generated Code")
                else:
                    await self._show_speech_bubble(f"Code generation failed: {result.get('error', 'Unknown error')} 😿")
                    
        except Exception as e:
            self.logger.error(f"Error in code generation: {e}")
            await self._show_speech_bubble("Something went wrong with code generation! 😿")
    
    async def _analyze_code_interface(self):
        """Show code analysis interface"""
        try:
            if not self.gemini_client:
                await self._show_speech_bubble("I need a Gemini API key to analyze code! 🔑")
                return
            
            # Try to get code from clipboard or ask user
            code_input = self._get_clipboard_code()
            if not code_input:
                code_input = simpledialog.askstring(
                    "Code Analysis 📝",
                    "Paste the code you want me to analyze:",
                    initialvalue=""
                )
            
            if code_input and code_input.strip():
                await self._show_speech_bubble("Analyzing your code... 🔍", duration=2000)
                
                language = self._detect_language_from_code(code_input)
                task = simpledialog.askstring(
                    "Analysis Type",
                    "What type of analysis? (review, explain, optimize, debug)"
                ) or "review"
                
                result = await self.gemini_client.analyze_code(
                    code=code_input,
                    language=language,
                    task=task
                )
                
                if result.get('success'):
                    await self._show_analysis_result_window(result)
                else:
                    await self._show_speech_bubble(f"Code analysis failed: {result.get('error', 'Unknown error')} 😿")
            else:
                await self._show_speech_bubble("I need some code to analyze! 🤔")
                
        except Exception as e:
            self.logger.error(f"Error in code analysis: {e}")
            await self._show_speech_bubble("Something went wrong with code analysis! 😿")
    
    async def _fix_code_interface(self):
        """Show code fixing interface"""
        try:
            if not self.gemini_client:
                await self._show_speech_bubble("I need a Gemini API key to fix code! 🔑")
                return
            
            # Get problematic code
            code_input = self._get_clipboard_code() or simpledialog.askstring(
                "Code Fixing 🔧",
                "Paste the problematic code:"
            )
            
            if code_input and code_input.strip():
                error_msg = simpledialog.askstring(
                    "Error Description",
                    "What's the error or problem you're experiencing?"
                )
                
                if error_msg:
                    await self._show_speech_bubble("Fixing your code... 🛠️", duration=2000)
                    
                    language = self._detect_language_from_code(code_input)
                    
                    result = await self.gemini_client.fix_code_errors(
                        code=code_input,
                        error_message=error_msg,
                        language=language
                    )
                    
                    if result.get('success'):
                        await self._show_fix_result_window(result)
                    else:
                        await self._show_speech_bubble(f"Code fixing failed: {result.get('error', 'Unknown error')} 😿")
                else:
                    await self._show_speech_bubble("I need to know what's wrong to help fix it! 🤔", duration=3000)
            else:
                await self._show_speech_bubble("I need some code to fix! 🤔", duration=3000)
                
        except Exception as e:
            self.logger.error(f"Error in code fixing: {e}")
            await self._show_speech_bubble("Something went wrong with code fixing! 😿", duration=3000)
    
    async def _generate_tests_interface(self):
        """Show test generation interface"""
        try:
            if not self.gemini_client:
                await self._show_speech_bubble("I need a Gemini API key to generate tests! 🔑", duration=3000)
                return
            
            # Get code to test
            code_input = self._get_clipboard_code() or simpledialog.askstring(
                "Test Generation 🧪",
                "Paste the code you want me to write tests for:"
            )
            
            if code_input and code_input.strip():
                language = self._detect_language_from_code(code_input)
                test_framework = "unittest" if language == "python" else "jest"
                
                if language == "python":
                    test_framework = simpledialog.askstring(
                        "Test Framework",
                        "Which test framework? (unittest, pytest)"
                    ) or "unittest"
                
                await self._show_speech_bubble("Writing tests... 🧪", duration=2000)
                
                result = await self.gemini_client.generate_tests(
                    code=code_input,
                    language=language,
                    test_framework=test_framework
                )
                
                if result.get('success'):
                    await self._show_test_result_window(result)
                else:
                    await self._show_speech_bubble(f"Test generation failed: {result.get('error', 'Unknown error')} 😿", duration=4000)
            else:
                await self._show_speech_bubble("I need some code to write tests for! 🤔", duration=3000)
                
        except Exception as e:
            self.logger.error(f"Error in test generation: {e}")
            await self._show_speech_bubble("Something went wrong with test generation! 😿", duration=3000)
    
    # ===== Helper Methods =====
    
    def _detect_current_language(self) -> Optional[str]:
        """Try to detect current programming language from screen context"""
        try:
            if self.current_context and 'active_app' in self.current_context:
                app = self.current_context['active_app'].lower()
                title = self.current_context.get('window_title', '').lower()
                
                if 'code' in app or 'vscode' in app:
                    # Try to detect from file extension in title
                    if '.py' in title: return 'python'
                    elif '.js' in title: return 'javascript'
                    elif '.ts' in title: return 'typescript'
                    elif '.java' in title: return 'java'
                    elif '.cpp' in title or '.c' in title: return 'cpp'
                    elif '.cs' in title: return 'csharp'
                    elif '.go' in title: return 'go'
                    elif '.rs' in title: return 'rust'
                    elif '.php' in title: return 'php'
                
            return None
        except Exception:
            return None
    
    def _detect_language_from_code(self, code: str) -> str:
        """Detect programming language from code content"""
        code_lower = code.lower().strip()
        
        if 'def ' in code or 'import ' in code or 'print(' in code:
            return 'python'
        elif 'function ' in code or 'const ' in code or 'console.log' in code:
            return 'javascript'
        elif 'public class ' in code or 'System.out' in code:
            return 'java'
        elif '#include' in code or 'cout <<' in code:
            return 'cpp'
        elif 'using namespace' in code or 'Console.WriteLine' in code:
            return 'csharp'
        else:
            return 'python'  # Default fallback
    
    def _get_current_file_context(self) -> Dict[str, Any]:
        """Get context about current file being edited"""
        context = {}
        
        if self.current_context:
            context.update(self.current_context)
        
        if self.file_manager:
            try:
                project_info = self.file_manager.analyze_project_structure()
                if project_info.get('success'):
                    context['project_type'] = project_info['structure'].get('primary_language')
                    context['recent_files'] = self.file_manager.get_recent_files(5)
            except Exception as e:
                self.logger.warning(f"Could not get project context: {e}")
        
        return context
    
    def _get_clipboard_code(self) -> Optional[str]:
        """Try to get code from clipboard"""
        try:
            clipboard_content = self.root.clipboard_get()
            # Simple heuristic to check if clipboard contains code
            if any(keyword in clipboard_content for keyword in ['def ', 'function ', 'class ', '{', '}', ';']):
                return clipboard_content
        except Exception:
            pass
        return None
    
    # ===== Result Display Windows =====
    
    async def _show_code_result_window(self, result: Dict[str, Any], title: str):
        """Show generated code in a result window"""
        try:
            window = tk.Toplevel(self.root)
            window.title(f"📦 Pixie's Workshop - {title}")
            window.geometry("850x650")
            window.configure(bg='#D2B48C')
            window.wm_attributes("-topmost", True)
            
            # Create cardboard-styled main frame
            main_frame = tk.Frame(window, bg='#D2B48C', relief='raised', bd=3)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
            
            # Create notebook for tabs with cardboard styling
            notebook = ttk.Notebook(main_frame)
            notebook.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
            
            # Code tab
            code_frame = ttk.Frame(notebook)
            notebook.add(code_frame, text="Generated Code")
            
            # Code text area
            code_text = tk.Text(code_frame, wrap=tk.NONE, font=('Consolas', 11))
            code_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            code_text.insert(tk.END, result.get('code', ''))
            
            # Info tab
            info_frame = ttk.Frame(notebook)
            notebook.add(info_frame, text="Details")
            
            info_text = tk.Text(info_frame, wrap=tk.WORD, font=('Segoe UI', 10))
            info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            info_content = f"""📋 Explanation:
{result.get('explanation', 'No explanation provided')}

📁 Suggested Filename:
{result.get('filename_suggestion', 'code_file.txt')}

📦 Dependencies:
{', '.join(result.get('dependencies', [])) or 'None'}

💡 Usage Example:
{result.get('usage_example', 'No example provided')}
"""
            info_text.insert(tk.END, info_content)
            
            # Buttons frame
            button_frame = ttk.Frame(window)
            button_frame.pack(fill=tk.X, padx=10, pady=5)
            
            def save_code():
                if self.file_manager:
                    filename = result.get('filename_suggestion', 'generated_code.py')
                    save_result = self.file_manager.create_new_file(filename, result.get('code', ''))
                    if save_result.get('success'):
                        messagebox.showinfo("Success", f"Code saved to {save_result['path']}")
                    else:
                        messagebox.showerror("Error", f"Failed to save: {save_result.get('error')}")
                else:
                    messagebox.showerror("Error", "File manager not available")
            
            def copy_code():
                window.clipboard_clear()
                window.clipboard_append(result.get('code', ''))
                messagebox.showinfo("Copied", "Code copied to clipboard!")
            
            ttk.Button(button_frame, text="💾 Save File", command=save_code).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="📋 Copy Code", command=copy_code).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="❌ Close", command=window.destroy).pack(side=tk.RIGHT, padx=5)
            
        except Exception as e:
            self.logger.error(f"Error showing code result: {e}")
            await self._show_speech_bubble("Error displaying results! 😿", duration=3000)
    
    async def _show_analysis_result_window(self, result: Dict[str, Any]):
        """Show code analysis results"""
        try:
            window = tk.Toplevel(self.root)
            window.title("Pixie - Code Analysis")
            window.geometry("700x500")
            window.wm_attributes("-topmost", True)
            
            # Create scrollable text area
            text_frame = ttk.Frame(window)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Segoe UI', 10))
            scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Format analysis content
            content = f"""🔍 CODE ANALYSIS RESULTS

📊 Overall Rating: {result.get('rating', 'N/A')}/10
📈 Complexity: {result.get('complexity', 'Unknown')}

📝 Analysis:
{result.get('analysis', 'No analysis provided')}

💡 Suggestions for Improvement:
"""
            for i, suggestion in enumerate(result.get('suggestions', []), 1):
                content += f"{i}. {suggestion}\n"
            
            if result.get('issues'):
                content += f"\n⚠️ Potential Issues:\n"
                for i, issue in enumerate(result.get('issues', []), 1):
                    content += f"{i}. {issue}\n"
            
            if result.get('improved_code'):
                content += f"\n✨ Improved Code:\n{result.get('improved_code')}"
            
            text_widget.insert(tk.END, content)
            text_widget.config(state=tk.DISABLED)
            
            # Close button
            ttk.Button(window, text="❌ Close", command=window.destroy).pack(pady=10)
            
        except Exception as e:
            self.logger.error(f"Error showing analysis result: {e}")
            await self._show_speech_bubble("Error displaying analysis! 😿", duration=3000)
    
    async def _show_fix_result_window(self, result: Dict[str, Any]):
        """Show code fixing results"""
        try:
            window = tk.Toplevel(self.root)
            window.title("Pixie - Code Fix")
            window.geometry("800x600")
            window.wm_attributes("-topmost", True)
            
            # Create notebook for before/after comparison
            notebook = ttk.Notebook(window)
            notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Fixed code tab
            code_frame = ttk.Frame(notebook)
            notebook.add(code_frame, text="Fixed Code")
            
            code_text = tk.Text(code_frame, wrap=tk.NONE, font=('Consolas', 11))
            code_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            code_text.insert(tk.END, result.get('fixed_code', ''))
            
            # Explanation tab
            exp_frame = ttk.Frame(notebook)
            notebook.add(exp_frame, text="Explanation")
            
            exp_text = tk.Text(exp_frame, wrap=tk.WORD, font=('Segoe UI', 10))
            exp_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            exp_content = f"""🔧 What was wrong:
{result.get('explanation', 'No explanation provided')}

🔍 Error Type: {result.get('error_type', 'Unknown')}

💡 Prevention Tips:
"""
            for i, tip in enumerate(result.get('prevention_tips', []), 1):
                exp_content += f"{i}. {tip}\n"
            
            if result.get('additional_improvements'):
                exp_content += f"\n✨ Additional Improvements:\n{result.get('additional_improvements')}"
            
            exp_text.insert(tk.END, exp_content)
            exp_text.config(state=tk.DISABLED)
            
            # Button frame
            button_frame = ttk.Frame(window)
            button_frame.pack(fill=tk.X, padx=10, pady=5)
            
            def copy_fixed_code():
                window.clipboard_clear()
                window.clipboard_append(result.get('fixed_code', ''))
                messagebox.showinfo("Copied", "Fixed code copied to clipboard!")
            
            ttk.Button(button_frame, text="📋 Copy Fixed Code", command=copy_fixed_code).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="❌ Close", command=window.destroy).pack(side=tk.RIGHT, padx=5)
            
        except Exception as e:
            self.logger.error(f"Error showing fix result: {e}")
            await self._show_speech_bubble("Error displaying fix results! 😿", duration=3000)
    
    async def _show_test_result_window(self, result: Dict[str, Any]):
        """Show generated test results"""
        try:
            window = tk.Toplevel(self.root)
            window.title("Pixie - Generated Tests")
            window.geometry("800x600")
            window.wm_attributes("-topmost", True)
            
            # Create notebook
            notebook = ttk.Notebook(window)
            notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Test code tab
            test_frame = ttk.Frame(notebook)
            notebook.add(test_frame, text="Test Code")
            
            test_text = tk.Text(test_frame, wrap=tk.NONE, font=('Consolas', 11))
            test_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            test_text.insert(tk.END, result.get('test_code', ''))
            
            # Instructions tab
            inst_frame = ttk.Frame(notebook)
            notebook.add(inst_frame, text="Instructions")
            
            inst_text = tk.Text(inst_frame, wrap=tk.WORD, font=('Segoe UI', 10))
            inst_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            inst_content = f"""🧪 Test Cases Covered:
"""
            for i, case in enumerate(result.get('test_cases', []), 1):
                inst_content += f"{i}. {case}\n"
            
            inst_content += f"""

🚀 How to Run Tests:
{result.get('setup_instructions', 'No instructions provided')}

📦 Dependencies Needed:
{', '.join(result.get('dependencies', [])) or 'None'}

📁 Suggested Filename:
{result.get('filename_suggestion', 'test_code.py')}

📊 Coverage Areas:
"""
            for area in result.get('coverage_areas', []):
                inst_content += f"• {area}\n"
            
            inst_text.insert(tk.END, inst_content)
            inst_text.config(state=tk.DISABLED)
            
            # Button frame
            button_frame = ttk.Frame(window)
            button_frame.pack(fill=tk.X, padx=10, pady=5)
            
            def save_tests():
                if self.file_manager:
                    filename = result.get('filename_suggestion', 'test_generated.py')
                    save_result = self.file_manager.create_new_file(filename, result.get('test_code', ''))
                    if save_result.get('success'):
                        messagebox.showinfo("Success", f"Tests saved to {save_result['path']}")
                    else:
                        messagebox.showerror("Error", f"Failed to save: {save_result.get('error')}")
                else:
                    messagebox.showerror("Error", "File manager not available")
            
            def copy_tests():
                window.clipboard_clear()
                window.clipboard_append(result.get('test_code', ''))
                messagebox.showinfo("Copied", "Test code copied to clipboard!")
            
            ttk.Button(button_frame, text="💾 Save Tests", command=save_tests).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="📋 Copy Tests", command=copy_tests).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="❌ Close", command=window.destroy).pack(side=tk.RIGHT, padx=5)
            
        except Exception as e:
            self.logger.error(f"Error showing test result: {e}")
            await self._show_speech_bubble("Error displaying test results! 😿", duration=3000)
    
    # ===== VS Code Integration Methods =====
    
    async def _fix_current_vscode_file(self):
        """Advanced VS Code file analysis and fixing with technical insights"""
        try:
            if not self.vscode_integration:
                await self._show_speech_bubble("❌ VS Code integration unavailable. Install VS Code extension!", duration=3000)
                return
            
            # Multi-step technical process
            await self._show_speech_bubble("🔍 Scanning active file for issues...", duration=1500)
            
            # Get detailed file analysis
            file_info = await self._get_detailed_file_info()
            if not file_info:
                await self._show_speech_bubble("❌ No active file detected in VS Code", duration=3000)
                return
            
            await self._show_speech_bubble(f"📄 Analyzing {file_info['language']} file ({file_info['lines']} lines)...", duration=2000)
            
            # Advanced code analysis
            analysis_result = await self._perform_advanced_code_analysis(file_info)
            
            # Show technical fix interface
            fix_applied = await self._show_technical_fix_interface(analysis_result)
            
            if fix_applied:
                await self._show_speech_bubble("✅ Code fixes applied successfully!", duration=3000)
            else:
                await self._show_speech_bubble("ℹ️ Analysis complete. Check results panel.", duration=3000)
                
        except Exception as e:
            self.logger.error(f"Error in advanced file fix: {e}")
            await self._show_speech_bubble("❌ File analysis failed. Check VS Code connection.", duration=3000)
    
    async def _get_detailed_file_info(self) -> Dict:
        """Get detailed information about the current VS Code file"""
        try:
            if not self.vscode_integration:
                return None
            
            # Get basic file info from VS Code integration
            file_info = {
                'path': None,
                'language': 'unknown',
                'lines': 0,
                'size': 0,
                'encoding': 'utf-8',
                'errors': [],
                'warnings': []
            }
            
            # Try to get active file details
            try:
                active_file = await self.vscode_integration.get_active_file_info()
                if active_file:
                    file_info.update(active_file)
            except Exception as e:
                self.logger.warning(f"Could not get VS Code file info: {e}")
            
            return file_info if file_info['path'] else None
            
        except Exception as e:
            self.logger.error(f"Error getting file info: {e}")
            return None
    
    async def _perform_advanced_code_analysis(self, file_info: Dict) -> Dict:
        """Perform comprehensive code analysis"""
        analysis = {
            'syntax_errors': [],
            'style_issues': [],
            'security_vulnerabilities': [],
            'performance_issues': [],
            'best_practices': [],
            'complexity_metrics': {},
            'suggested_fixes': []
        }
        
        try:
            if not self.gemini_client:
                analysis['error'] = "AI analysis unavailable - no Gemini client"
                return analysis
            
            # Get file content for analysis
            file_content = await self._get_file_content(file_info['path'])
            if not file_content:
                analysis['error'] = "Could not read file content"
                return analysis
            
            # Language-specific analysis
            language = file_info.get('language', '').lower()
            
            # AI-powered code analysis
            ai_analysis = await self.gemini_client.analyze_code(
                code=file_content,
                language=language,
                analysis_type='comprehensive',
                context={
                    'file_path': file_info['path'],
                    'file_size': file_info['size'],
                    'line_count': file_info['lines']
                }
            )
            
            # Parse AI analysis into structured format
            analysis = self._parse_ai_code_analysis(ai_analysis, analysis)
            
            # Add language-specific checks
            if language in ['python', 'javascript', 'typescript', 'java', 'cpp']:
                analysis = await self._add_language_specific_analysis(file_content, language, analysis)
            
        except Exception as e:
            self.logger.error(f"Error in code analysis: {e}")
            analysis['error'] = str(e)
        
        return analysis
    
    def _parse_ai_code_analysis(self, ai_response: str, base_analysis: Dict) -> Dict:
        """Parse AI analysis response into structured format"""
        try:
            # Simple parsing - in production, you'd use more sophisticated NLP
            lines = ai_response.lower().split('\n')
            
            for line in lines:
                if 'syntax error' in line or 'error:' in line:
                    base_analysis['syntax_errors'].append(line.strip())
                elif 'warning' in line or 'style' in line:
                    base_analysis['style_issues'].append(line.strip())
                elif 'security' in line or 'vulnerability' in line:
                    base_analysis['security_vulnerabilities'].append(line.strip())
                elif 'performance' in line or 'optimization' in line:
                    base_analysis['performance_issues'].append(line.strip())
                elif 'best practice' in line or 'recommend' in line:
                    base_analysis['best_practices'].append(line.strip())
                elif 'fix:' in line or 'solution:' in line:
                    base_analysis['suggested_fixes'].append(line.strip())
            
            return base_analysis
            
        except Exception as e:
            self.logger.warning(f"Error parsing AI analysis: {e}")
            return base_analysis
    
    async def _add_language_specific_analysis(self, code: str, language: str, analysis: Dict) -> Dict:
        """Add language-specific static analysis"""
        try:
            # Python-specific checks
            if language == 'python':
                # Check for common Python issues
                if 'import *' in code:
                    analysis['style_issues'].append("Avoid wildcard imports (import *)")
                if 'except:' in code and 'except Exception:' not in code:
                    analysis['best_practices'].append("Use specific exception handling")
                
                # Check for security issues
                if 'eval(' in code or 'exec(' in code:
                    analysis['security_vulnerabilities'].append("Avoid eval() and exec() - security risk")
            
            # JavaScript/TypeScript checks
            elif language in ['javascript', 'typescript']:
                if '==' in code and '===' not in code:
                    analysis['style_issues'].append("Use strict equality (===) instead of ==")
                if 'var ' in code:
                    analysis['best_practices'].append("Use 'let' or 'const' instead of 'var'")
            
            # Add complexity metrics
            analysis['complexity_metrics'] = {
                'lines_of_code': len(code.split('\n')),
                'function_count': code.count('def ') + code.count('function '),
                'class_count': code.count('class '),
                'comment_ratio': (code.count('#') + code.count('//') + code.count('/*')) / max(len(code.split('\n')), 1)
            }
            
        except Exception as e:
            self.logger.warning(f"Error in language-specific analysis: {e}")
        
        return analysis
    
    async def _get_file_content(self, file_path: str) -> str:
        """Get file content for analysis"""
        try:
            if self.vscode_integration and hasattr(self.vscode_integration, 'get_file_content'):
                return await self.vscode_integration.get_file_content(file_path)
            else:
                # Fallback: read file directly
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            self.logger.error(f"Error reading file content: {e}")
            return ""
    
    async def _show_technical_fix_interface(self, analysis_result: Dict) -> bool:
        """Show technical interface for code fixes"""
        try:
            # Create a comprehensive report
            report_lines = [
                "🔧 CODE ANALYSIS REPORT",
                "=" * 30,
                ""
            ]
            
            # Add metrics
            metrics = analysis_result.get('complexity_metrics', {})
            if metrics:
                report_lines.extend([
                    "📊 Code Metrics:",
                    f"  • Lines: {metrics.get('lines_of_code', 'N/A')}",
                    f"  • Functions: {metrics.get('function_count', 'N/A')}",
                    f"  • Classes: {metrics.get('class_count', 'N/A')}",
                    f"  • Comment Ratio: {metrics.get('comment_ratio', 0):.2f}",
                    ""
                ])
            
            # Add issues
            syntax_errors = analysis_result.get('syntax_errors', [])
            if syntax_errors:
                report_lines.append("❌ Syntax Errors:")
                for error in syntax_errors[:3]:
                    report_lines.append(f"  • {error}")
                report_lines.append("")
            
            security_issues = analysis_result.get('security_vulnerabilities', [])
            if security_issues:
                report_lines.append("�️ Security Issues:")
                for issue in security_issues[:3]:
                    report_lines.append(f"  • {issue}")
                report_lines.append("")
            
            # Add suggestions
            fixes = analysis_result.get('suggested_fixes', [])
            if fixes:
                report_lines.append("🔧 Suggested Fixes:")
                for fix in fixes[:3]:
                    report_lines.append(f"  • {fix}")
            
            # Show comprehensive report
            full_report = "\n".join(report_lines)
            await self._show_speech_bubble(full_report[:500] + "...", duration=10000)
            
            # Log detailed report
            self.logger.info(f"Code Analysis Report:\n{full_report}")
            
            # Return True if fixes were suggested
            return len(fixes) > 0 or len(syntax_errors) > 0
            
        except Exception as e:
            self.logger.error(f"Error showing technical fix interface: {e}")
            return False
    
    async def _analyze_current_vscode_file(self):
        """Analyze the currently active file in VS Code"""
        try:
            if not self.vscode_integration:
                await self._show_speech_bubble("VS Code integration not available! 😿", duration=3000)
                return
            
            await self._show_speech_bubble("Analyzing your current file... 🔍", duration=2000)
            
            result = await self.vscode_integration.suggest_improvements_for_current_file(self.gemini_client)
            
            if result.get('success'):
                await self._show_analysis_result_window(result)
            else:
                await self._show_speech_bubble(f"Couldn't analyze your file: {result.get('error', 'Unknown error')} 😿", duration=4000)
                
        except Exception as e:
            self.logger.error(f"Error analyzing VS Code file: {e}")
            await self._show_speech_bubble("Something went wrong analyzing your file! 😿", duration=3000)
    
    async def _generate_tests_for_current_file(self):
        """Generate tests for the currently active file in VS Code"""
        try:
            if not self.vscode_integration:
                await self._show_speech_bubble("VS Code integration not available! 😿", duration=3000)
                return
            
            await self._show_speech_bubble("Creating tests for your file... 🧪", duration=2000)
            
            result = await self.vscode_integration.create_companion_file(self.gemini_client, 'test')
            
            if result.get('success'):
                message = "✅ Tests created!"
                if result.get('companion_file'):
                    message += f"\n\nSaved as: {Path(result['companion_file']).name}"
                await self._show_speech_bubble(message, duration=4000)
                await self._show_test_result_window(result)
            else:
                await self._show_speech_bubble(f"Couldn't create tests: {result.get('error', 'Unknown error')} 😿", duration=4000)
                
        except Exception as e:
            self.logger.error(f"Error generating tests for VS Code file: {e}")
            await self._show_speech_bubble("Something went wrong creating tests! 😿", duration=3000)
    
    async def _show_speech_bubble(self, message: str, duration: int = None, speak: bool = True):
        """Show a speech bubble message near the pet and optionally speak it"""
        try:
            # Show visual speech bubble with automatic duration calculation
            if hasattr(self, 'speech_bubble') and self.speech_bubble:
                self.speech_bubble.show_message(message, duration)
            elif ModernSpeechBubble and self.root:
                # Create temporary speech bubble
                bubble = ModernSpeechBubble(self.root)
                pet_x = self.pet_window.winfo_x() if self.pet_window else 100
                pet_y = self.pet_window.winfo_y() if self.pet_window else 100
                bubble.show_message(message, duration, pet_x + 50, pet_y - 50)
            else:
                # Fallback to simple messagebox
                self.root.after(100, lambda: messagebox.showinfo("Pixie", message))
            
            # Speak the message if TTS is available and speak is True
            if speak and hasattr(self, 'speech_manager') and self.speech_manager and self.speech_manager.is_available():
                self.speech_manager.speak_text(message, blocking=False)
                self.logger.info(f"Pixie says (with voice): {message}")
            else:
                self.logger.info(f"Pixie says: {message}")
                
        except Exception as e:
            self.logger.error(f"Error showing speech bubble: {e}")
            # Ultimate fallback - just log the message
            self.logger.info(f"Pixie says: {message}")
    
    def _toggle_dark_mode(self):
        """Toggle between dark and light mode"""
        try:
            if self.style_manager:
                is_dark = self.style_manager.toggle_dark_mode()
                theme_name = "Dark Mode" if is_dark else "Light Mode"
                asyncio.create_task(self._show_speech_bubble(f"Switched to {theme_name}! ✨", duration=2000))
            else:
                asyncio.create_task(self._show_speech_bubble("Theme switching not available 😿", duration=2000))
        except Exception as e:
            self.logger.error(f"Error toggling dark mode: {e}")
    
    def _on_theme_change(self, new_theme):
        """Handle theme change event"""
        try:
            # Update all UI components to use new theme
            if self.chat_window and hasattr(self.chat_window, 'window'):
                self._apply_theme_to_chat_window(new_theme)
            
            if self.pet_window:
                self._apply_theme_to_pet_window(new_theme)
            
            # Update any other UI elements that need theme updates
            self.logger.info(f"Applied {'dark' if new_theme.is_dark_theme() else 'light'} theme to UI")
            
        except Exception as e:
            self.logger.error(f"Error applying theme change: {e}")
    
    def _apply_theme_to_chat_window(self, theme):
        """Apply theme colors to chat window"""
        try:
            if not (self.chat_window and hasattr(self.chat_window, 'window')):
                return
                
            bg_color = theme.get_color("background")
            surface_color = theme.get_color("surface")
            text_color = theme.get_color("text_primary")
            
            # Update window background
            self.chat_window.window.configure(bg=bg_color)
            
            # Update chat display
            if hasattr(self.chat_window, 'chat_display'):
                self.chat_window.chat_display.configure(
                    bg=surface_color,
                    fg=text_color,
                    insertbackground=theme.get_color("primary")
                )
            
            # Update input area
            if hasattr(self.chat_window, 'chat_input'):
                self.chat_window.chat_input.configure(
                    bg=surface_color,
                    fg=text_color,
                    insertbackground=theme.get_color("primary")
                )
                
        except Exception as e:
            self.logger.error(f"Error applying theme to chat window: {e}")
    
    def _apply_theme_to_pet_window(self, theme):
        """Apply theme colors to pet window"""
        try:
            if not self.pet_window:
                return
                
            # The pet window uses transparency, so we mainly need to update
            # any text or overlay elements to match the theme
            # The pet graphics themselves can adapt based on theme colors
            
            if hasattr(self, 'pet_widget') and self.pet_widget:
                # Let the pet widget handle its own theme updates
                # This could be expanded to change pet colors based on theme
                pass
                
        except Exception as e:
            self.logger.error(f"Error applying theme to pet window: {e}")
    
    async def _start_spontaneous_conversations(self):
        """Start the spontaneous conversation system with adaptive timing"""
        import time
        import random
        
        # Adaptive sleep intervals based on activity
        base_interval = 60  # Base check interval: 60 seconds
        
        while self.is_running:
            try:
                # Adaptive sleep based on user activity
                if self.activity_tracker.get("inactivity_count", 0) > 5:
                    sleep_time = base_interval * 2  # Less frequent when idle
                else:
                    sleep_time = base_interval
                
                await asyncio.sleep(sleep_time)
                current_time = time.time()
                
                # Decide if we should make a spontaneous comment
                should_comment = False
                
                # Check various conditions for spontaneous speech
                if current_time - self.last_spontaneous_comment_time > 300:  # 5 minutes since last comment
                    # Been a while, maybe check in
                    if self.activity_tracker["inactivity_count"] > 3:
                        should_comment = True
                        self.current_mood = "curious"
                    elif random.random() < 0.3:  # 30% chance for random comment
                        should_comment = True
                        
                elif self.activity_tracker.get("last_activity") == "error" and current_time - self.activity_tracker.get("activity_start_time", 0) > 60:
                    # User has been dealing with errors for a while
                    should_comment = True
                    self.current_mood = "encouraging"
                
                if should_comment and self.gemini_client:
                    await self._make_spontaneous_comment()
                
            except Exception as e:
                self.logger.error(f"Error in spontaneous conversation: {e}")
    
    async def _make_spontaneous_comment(self):
        """Generate and show a spontaneous comment"""
        try:
            import time
            
            # Get current screenshot for context
            screenshot = self.screen_monitor.get_screenshot()
            if not screenshot:
                return
            
            # Prepare context
            context = {
                "time_since_last_comment": int(time.time() - self.last_spontaneous_comment_time),
                "current_mood": self.current_mood,
                "recent_activity": self.activity_tracker.get("last_activity", "unknown"),
                "inactivity_count": self.activity_tracker["inactivity_count"]
            }
            
            # Generate spontaneous comment
            comment = await self.gemini_client.spontaneous_comment(
                screenshot, 
                context=context,
                mood=self.current_mood
            )
            
            if comment:
                await self._show_speech_bubble(comment, duration=4000)
                self.last_spontaneous_comment_time = time.time()
                
                # Add to conversation history
                self._add_to_conversation_history("Pixie", comment)
                
                # Randomly change mood after speaking
                if random.random() < 0.4:  # 40% chance to change mood
                    self._update_mood()
                    
        except Exception as e:
            self.logger.error(f"Error making spontaneous comment: {e}")
    
    def _add_to_conversation_history(self, speaker: str, message: str):
        """Add message to conversation history with optimized memory management"""
        # Ensure conversation_history exists
        if not hasattr(self, 'conversation_history'):
            self.conversation_history = []
        
        # Truncate long messages to save memory
        truncated_message = message[:500] if len(message) > 500 else message
        
        self.conversation_history.append({
            "speaker": speaker,
            "text": truncated_message,
            "timestamp": time.time()
        })
        
        # Maintain memory limit - use configured limit
        if len(self.conversation_history) > self.MAX_CONVERSATION_HISTORY:
            self.conversation_history = self.conversation_history[-self.MAX_CONVERSATION_HISTORY:]
    
    def _update_mood(self):
        """Update pet's mood based on context"""
        import random
        
        moods = ["helpful", "playful", "curious", "encouraging", "sleepy", "excited"]
        
        # Weight moods based on current activity
        if self.activity_tracker.get("last_activity") == "error":
            # More likely to be encouraging if user has errors
            weights = [20, 10, 15, 40, 5, 10]
        elif self.activity_tracker["inactivity_count"] > 2:
            # More likely to be curious if user is inactive
            weights = [15, 20, 40, 15, 5, 5]
        else:
            # Default weights
            weights = [25, 20, 20, 15, 10, 10]
        
        self.current_mood = random.choices(moods, weights=weights)[0]
        self.logger.debug(f"Pet mood changed to: {self.current_mood}")
    
    async def _track_user_activity(self, context: Dict[str, Any]):
        """Track user activity for better conversation context"""
        import time
        
        current_time = time.time()
        
        # Determine activity type from context
        activity_type = "general"
        if context:
            if "error" in str(context).lower():
                activity_type = "error"
            elif "success" in str(context).lower() or "completed" in str(context).lower():
                activity_type = "success"
            elif context.get("active_app") == "Visual Studio Code":
                activity_type = "coding"
            elif "idle" in str(context).lower():
                activity_type = "idle"
        
        # Update activity tracking
        if self.activity_tracker["last_activity"] != activity_type:
            self.activity_tracker["last_activity"] = activity_type
            self.activity_tracker["activity_start_time"] = current_time
            
            # Add to recent activities with memory management
            context_summary = str(context)[:200] if context else None  # Limit context size
            self.activity_tracker["recent_activities"].append({
                "type": activity_type,
                "context": context_summary,
                "start_time": current_time
            })
            
            # Maintain memory limits - use configured limit
            if len(self.activity_tracker["recent_activities"]) > self.MAX_ACTIVITY_HISTORY:
                self.activity_tracker["recent_activities"] = self.activity_tracker["recent_activities"][-self.MAX_ACTIVITY_HISTORY:]
        
        # Track inactivity
        if activity_type == "idle":
            self.activity_tracker["inactivity_count"] += 1
        else:
            self.activity_tracker["inactivity_count"] = 0
    
    async def _enhanced_chat_response(self, message: str) -> str:
        """Generate enhanced chat response with conversation context"""
        try:
            if not self.gemini_client:
                return "I'm not feeling very talkative right now 😸"
            
            # Prepare context for better responses
            context = {
                "current_mood": self.current_mood,
                "personality": ", ".join(self.personality_traits),
                "recent_activity": self.activity_tracker.get("last_activity", "unknown")
            }
            
            # Use enhanced conversational response
            response = await self.gemini_client.conversational_response(
                message,
                conversation_history=self.conversation_history,
                context=context,
                personality_traits=self.personality_traits
            )
            
            # Add both user message and response to history
            self._add_to_conversation_history("User", message)
            self._add_to_conversation_history("Pixie", response)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error in enhanced chat response: {e}")
            return "I'm having trouble thinking right now. Try talking to me again! 🐱"
    
    async def _react_to_screen_change(self, context: Dict[str, Any]):
        """React to screen changes with appropriate responses"""
        try:
            # Track the activity
            await self._track_user_activity(context)
            
            # Determine if we should react
            activity = self.activity_tracker.get("last_activity")
            
            reaction_triggers = {
                "error": 0.7,     # 70% chance to react to errors
                "success": 0.8,   # 80% chance to celebrate success  
                "coding": 0.2,    # 20% chance to comment on coding
                "idle": 0.1       # 10% chance to check on idle user
            }
            
            import random
            if activity in reaction_triggers and random.random() < reaction_triggers[activity]:
                reaction = await self.gemini_client.react_to_activity(
                    activity, 
                    activity_details={
                        "duration": time.time() - self.activity_tracker.get("activity_start_time", time.time()),
                        "context": context
                    }
                )
                
                if reaction:
                    await self._show_speech_bubble(reaction, duration=3500)
                    self._add_to_conversation_history("Pixie", reaction)
            
        except Exception as e:
            self.logger.error(f"Error reacting to screen change: {e}")
    
    async def _ask_pixie_something(self):
        """Advanced technical chat interface with context awareness"""
        try:
            # Show technical chat interface instead of simple dialog
            await self._show_advanced_chat_interface()
            
        except Exception as e:
            self.logger.error(f"Error in advanced chat: {e}")
            await self._show_speech_bubble("❌ Chat interface error. Check logs.", duration=3000)
    
    async def _show_advanced_chat_interface(self):
        """Show advanced technical chat interface with context awareness"""
        try:
            # Create advanced chat window with cardboard theme
            chat_window = tk.Toplevel(self.root)
            chat_window.title("📦 Pixie Cardboard Workshop")
            chat_window.geometry("650x550")
            chat_window.resizable(True, True)
            
            # Cardboard window styling
            chat_window.configure(bg='#D2B48C')
            chat_window.attributes('-topmost', True)
            chat_window.after(100, lambda: chat_window.attributes('-topmost', False))
            
            # Create main cardboard frame with texture
            main_frame = tk.Frame(chat_window, bg='#D2B48C', relief='raised', bd=3)
            main_frame.pack(fill='both', expand=True, padx=8, pady=8)
            
            # Add cardboard texture border
            texture_frame = tk.Frame(main_frame, bg='#C19A6B', relief='sunken', bd=2)
            texture_frame.pack(fill='both', expand=True, padx=3, pady=3)
            
            # Cardboard context panel (top)
            context_frame = tk.LabelFrame(texture_frame, text="� System Status", 
                                        bg='#DEB887', fg='#8B4513', font=('Courier New', 10, 'bold'),
                                        relief='raised', bd=2)
            context_frame.pack(fill='x', pady=(5, 10), padx=5)
            
            # Get current context
            current_context = await self._get_current_technical_context()
            
            # Cardboard-style context display
            context_text = tk.Text(context_frame, height=4, bg='#F5DEB3', fg='#5D4037', 
                                 font=('Courier New', 9), wrap='word', relief='sunken', bd=2)
            context_text.pack(fill='x', padx=6, pady=6)
            
            # Insert context information
            context_info = [
                f"System: {current_context.get('system', 'Unknown')}",
                f"Active App: {current_context.get('active_app', 'Unknown')}",
                f"Current Task: {current_context.get('current_task', 'General')}",
                f"Files Open: {current_context.get('open_files', 0)}"
            ]
            context_text.insert('1.0', '\n'.join(context_info))
            context_text.config(state='disabled')
            
            # Cardboard chat display (middle)
            chat_frame = tk.LabelFrame(texture_frame, text="� Workshop Conversation", 
                                     bg='#DEB887', fg='#8B4513', font=('Courier New', 10, 'bold'),
                                     relief='raised', bd=2)
            chat_frame.pack(fill='both', expand=True, pady=(0, 10), padx=5)
            
            # Cardboard chat display with rustic styling
            chat_display = tk.Text(chat_frame, bg='#FFF8DC', fg='#654321', 
                                 font=('Courier New', 10), wrap='word', state='disabled',
                                 relief='sunken', bd=2)
            
            # Cardboard scrollbar
            scrollbar = tk.Scrollbar(chat_frame, command=chat_display.yview,
                                   bg='#D2B48C', troughcolor='#C19A6B', 
                                   activebackground='#DEB887')
            chat_display.configure(yscrollcommand=scrollbar.set)
            
            chat_display.pack(side='left', fill='both', expand=True, padx=(6, 0), pady=6)
            scrollbar.pack(side='right', fill='y', pady=6)
            
            # Configure cardboard text tags
            chat_display.tag_configure('user', foreground='#8B4513', font=('Courier New', 10, 'bold'))
            chat_display.tag_configure('assistant', foreground='#A0522D', font=('Courier New', 10, 'bold'))
            chat_display.tag_configure('code', background='#F4A460', foreground='#654321', font=('Courier New', 9), relief='raised')
            chat_display.tag_configure('error', foreground='#B22222', font=('Courier New', 10, 'bold'))
            chat_display.tag_configure('success', foreground='#228B22', font=('Courier New', 10, 'bold'))
            
            # Cardboard input panel (bottom)
            input_frame = tk.LabelFrame(texture_frame, text="✍️ WRITE YOUR MESSAGE ON CARDBOARD ↓", 
                                      bg='#DEB887', fg='#8B4513', font=('Courier New', 11, 'bold'),
                                      relief='raised', bd=3)
            input_frame.pack(fill='x', pady=(5, 5), padx=5)
            
            # Cardboard instruction label
            instruction_label = tk.Label(input_frame, 
                                       text="� Write your workshop question below and press 'Send Message' or Ctrl+Enter",
                                       bg='#DEB887', fg='#A0522D', font=('Courier New', 9, 'bold'))
            instruction_label.pack(pady=(6, 4))
            
            # Cardboard input area
            input_text = tk.Text(input_frame, height=4, bg='#FFEFD5', fg='#654321', 
                               font=('Courier New', 11), wrap='word', relief='sunken', bd=3,
                               insertbackground='#8B4513', selectbackground='#DEB887')
            input_text.pack(fill='x', padx=10, pady=(0, 8))
            
            # Cardboard placeholder text
            placeholder_text = "Example: How do I craft better Python code in my workshop?"
            input_text.insert('1.0', placeholder_text)
            input_text.configure(fg='#A0522D')  # Brown placeholder text
            
            # Placeholder text handling
            def on_focus_in(event):
                if input_text.get('1.0', 'end-1c') == placeholder_text:
                    input_text.delete('1.0', 'end')
                    input_text.configure(fg='#654321')  # Dark brown text when typing
            
            def on_focus_out(event):
                if input_text.get('1.0', 'end-1c').strip() == '':
                    input_text.insert('1.0', placeholder_text)
                    input_text.configure(fg='#A0522D')  # Sienna placeholder
            
            input_text.bind('<FocusIn>', on_focus_in)
            input_text.bind('<FocusOut>', on_focus_out)
            
            # Button frame
            button_frame = tk.Frame(input_frame, bg='#DEB887')
            button_frame.pack(fill='x', padx=8, pady=6)
            
            # Cardboard quick action buttons
            quick_actions = [
                ("🔍 Workshop Status", lambda: self._quick_analyze_context(chat_display)),
                ("� Fix My Tools", lambda: self._quick_debug_help(chat_display)),
                ("� Code Recipes", lambda: self._quick_code_examples(chat_display)),
                ("⚙️ Speed Tips", lambda: self._quick_performance_tips(chat_display))
            ]
            
            for i, (text, command) in enumerate(quick_actions):
                btn = tk.Button(button_frame, text=text, command=command,
                              bg='#F4A460', fg='#654321', font=('Courier New', 8, 'bold'),
                              relief='raised', bd=2, padx=8, pady=3, cursor='hand2',
                              activebackground='#DEB887', activeforeground='#8B4513')
                btn.pack(side='left', padx=3)
                
                # Add cardboard hover effects
                def on_btn_hover(e, button=btn):
                    button.configure(relief='raised', bd=3, bg='#DEB887')
                def on_btn_leave(e, button=btn):
                    button.configure(relief='raised', bd=2, bg='#F4A460')
                
                btn.bind('<Enter>', on_btn_hover)
                btn.bind('<Leave>', on_btn_leave)
            
            # Enhanced send functionality
            async def send_technical_message():
                query = input_text.get('1.0', 'end-1c').strip()
                # Check if it's placeholder text
                if query and query != placeholder_text:
                    # Cardboard visual feedback
                    send_btn.configure(text="� Crafting...", state='disabled', bg='#BC9A6A')
                    chat_window.update()
                    
                    await self._process_technical_query(query, chat_display, current_context)
                    input_text.delete('1.0', 'end')
                    
                    # Re-enable cardboard button
                    send_btn.configure(text="� Send Message", state='normal', bg='#CD853F')
                    
                    # Add cardboard placeholder back
                    input_text.insert('1.0', placeholder_text)
                    input_text.configure(fg='#A0522D')
                else:
                    # Flash cardboard input area if empty
                    original_bg = input_text.cget('bg')
                    input_text.configure(bg='#F0E68C')  # Khaki flash
                    chat_window.after(200, lambda: input_text.configure(bg=original_bg))
            
            # Cardboard send button
            send_btn = tk.Button(button_frame, text="� Send Message",
                               command=lambda: asyncio.create_task(send_technical_message()),
                               bg='#CD853F', fg='#654321', font=('Courier New', 12, 'bold'),
                               relief='raised', bd=4, padx=18, pady=6, cursor='hand2',
                               activebackground='#DEB887', activeforeground='#8B4513')
            send_btn.pack(side='right', padx=(12, 8))
            
            # Cardboard send button hover effects
            def on_send_hover(event):
                send_btn.configure(bg='#DEB887', relief='raised', bd=5)
            
            def on_send_leave(event):
                send_btn.configure(bg='#CD853F', relief='raised', bd=4)
            
            send_btn.bind('<Enter>', on_send_hover)
            send_btn.bind('<Leave>', on_send_leave)
            
            # Enhanced key bindings
            def on_enter(event):
                if event.state & 0x4:  # Ctrl+Enter
                    asyncio.create_task(send_technical_message())
                    return 'break'
            
            def on_regular_enter(event):
                # Allow regular Enter for new lines, but show hint
                current_text = input_text.get('1.0', 'end-1c')
                if current_text.count('\n') == 0:  # First line
                    # Show hint in status
                    instruction_label.configure(text="💡 Press Ctrl+Enter to send, or use the Send Message button")
                    chat_window.after(3000, lambda: instruction_label.configure(
                        text="� Write your workshop question below and press 'Send Message' or Ctrl+Enter"))
            
            input_text.bind('<Control-Return>', on_enter)
            input_text.bind('<Return>', on_regular_enter)
            
            # Initial welcome message with usage instructions
            welcome_message = """📦 Welcome to Pixie's Cardboard Workshop!

I can craft solutions for:
• Code analysis & debugging
• Performance optimization  
• Architecture blueprints
• Best practices & security

� HOW TO USE THE WORKSHOP:
1. Click in the cardboard text box at the bottom
2. Write your technical question
3. Press 'Send Message' button or Ctrl+Enter
4. Use quick tools for common tasks

Example workshop requests:
• "How do I craft better Python functions?"
• "What's causing my workshop to slow down?"
• "Show me async/await blueprints"

Let's build something great! """
            
            self._add_technical_message(chat_display, 'assistant', welcome_message)
            
            # Focus on input and clear placeholder when ready
            def focus_input():
                input_text.focus_set()
                # Clear placeholder and position cursor
                if input_text.get('1.0', 'end-1c') == placeholder_text:
                    input_text.delete('1.0', 'end')
                    input_text.configure(fg='#000000')
            
            # Focus after window is fully loaded
            chat_window.after(100, focus_input)
            
        except Exception as e:
            self.logger.error(f"Error creating advanced chat interface: {e}")
            # Fallback to simple dialog
            question = simpledialog.askstring(
                "Pixie's Workshop (Simple)",
                "Cardboard workshop unavailable. What would you like to craft? �",
                parent=self.root
            )
            
            if question:
                response = await self._enhanced_chat_response(question)
                await self._show_speech_bubble(f"Q: {question}\n\nA: {response[:200]}...", duration=6000)
    
    async def _get_current_technical_context(self) -> Dict:
        """Get comprehensive technical context"""
        context = {}
        
        try:
            # System information
            import platform
            import psutil
            
            context['system'] = f"{platform.system()} {platform.release()}"
            context['python_version'] = platform.python_version()
            
            # Resource usage
            context['memory_usage'] = f"{psutil.virtual_memory().percent:.1f}%"
            context['cpu_usage'] = f"{psutil.cpu_percent():.1f}%"
            
            # Active application
            screen_context = self.screen_monitor.get_screen_context() if self.screen_monitor else {}
            context['active_app'] = screen_context.get('active_app', 'Unknown')
            
            # VS Code integration
            if self.vscode_integration:
                try:
                    vscode_info = await self.vscode_integration.get_workspace_info()
                    context.update(vscode_info)
                except:
                    context['vscode_status'] = 'Not connected'
            
            # Recent activity
            context['current_task'] = self.activity_tracker.get('last_activity', 'Unknown')
            context['mood'] = self.current_mood
            
        except Exception as e:
            self.logger.warning(f"Error getting technical context: {e}")
            context['error'] = 'Context gathering failed'
        
        return context
    
    def _add_technical_message(self, chat_display, sender: str, message: str):
        """Add message to technical chat with formatting"""
        try:
            chat_display.config(state='normal')
            
            # Add timestamp
            import datetime
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            
            # Add sender and message
            if sender == 'user':
                chat_display.insert('end', f"[{timestamp}] You: ", 'user')
            else:
                chat_display.insert('end', f"[{timestamp}] Pixie: ", 'assistant')
            
            # Add message with code highlighting
            lines = message.split('\n')
            for line in lines:
                if line.strip().startswith('```') or '`' in line:
                    chat_display.insert('end', line + '\n', 'code')
                elif 'error' in line.lower() or 'failed' in line.lower():
                    chat_display.insert('end', line + '\n', 'error')
                elif 'success' in line.lower() or 'completed' in line.lower():
                    chat_display.insert('end', line + '\n', 'success')
                else:
                    chat_display.insert('end', line + '\n')
            
            chat_display.insert('end', '\n')
            chat_display.config(state='disabled')
            chat_display.see('end')
            
        except Exception as e:
            self.logger.error(f"Error adding technical message: {e}")
    
    async def _process_technical_query(self, query: str, chat_display, context: Dict):
        """Process technical query with enhanced AI analysis"""
        try:
            # Add user message
            self._add_technical_message(chat_display, 'user', query)
            
            # Show processing indicator
            self._add_technical_message(chat_display, 'assistant', '🤖 Processing technical query...')
            
            # Enhanced query processing with context
            if not self.gemini_client:
                response = "AI client unavailable. Please configure Gemini API key."
            else:
                # Add technical context to query
                enhanced_query = f"""Technical Context:
{context}

User Query: {query}

Please provide a technical response with:
1. Direct answer
2. Code examples (if applicable)
3. Best practices
4. Potential issues to watch for"""
                
                response = await self.gemini_client.chat_response(
                    message=enhanced_query,
                    context=context
                )
            
            # Add AI response
            self._add_technical_message(chat_display, 'assistant', response)
            
            # Add to conversation history
            self._add_to_conversation_history("User", query)
            self._add_to_conversation_history("Pixie", response)
            
        except Exception as e:
            self.logger.error(f"Error processing technical query: {e}")
            self._add_technical_message(chat_display, 'assistant', 
                                      f"❌ Error processing query: {str(e)}")
    
    async def _quick_analyze_context(self, chat_display):
        """Quick context analysis"""
        context = await self._get_current_technical_context()
        analysis = f"""🔍 CONTEXT ANALYSIS:

System: {context.get('system', 'Unknown')}
Memory: {context.get('memory_usage', 'Unknown')}
CPU: {context.get('cpu_usage', 'Unknown')}
Active App: {context.get('active_app', 'Unknown')}
Current Task: {context.get('current_task', 'Unknown')}

Recommendations:
• Monitor resource usage
• Optimize current workflow
• Save work frequently"""
        
        self._add_technical_message(chat_display, 'assistant', analysis)
    
    async def _quick_debug_help(self, chat_display):
        """Quick debugging assistance"""
        debug_help = """🔧 DEBUG ASSISTANCE:

1. Check console/terminal for error messages
2. Verify file paths and permissions
3. Test with minimal input
4. Add logging/print statements
5. Check network connectivity (if applicable)

Common debugging commands:
• Python: python -m pdb script.py
• Node.js: node --inspect script.js
• Browser: F12 Developer Tools
• VS Code: Set breakpoints (F9)"""
        
        self._add_technical_message(chat_display, 'assistant', debug_help)
    
    async def _quick_code_examples(self, chat_display):
        """Show quick code examples"""
        examples = """📚 CODE EXAMPLES:

Python Error Handling:
```python
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    return None
```

JavaScript Async/Await:
```javascript
async function fetchData() {
    try {
        const response = await fetch('/api/data');
        return await response.json();
    } catch (error) {
        console.error('Fetch failed:', error);
    }
}
```

Need specific examples? Ask me!"""
        
        self._add_technical_message(chat_display, 'assistant', examples)
    
    async def _quick_performance_tips(self, chat_display):
        """Show performance optimization tips"""
        tips = """🚀 PERFORMANCE TIPS:

General:
• Profile before optimizing
• Cache frequently used data
• Minimize I/O operations
• Use appropriate data structures

Python Specific:
• Use list comprehensions
• Avoid global variables
• Use generators for large datasets
• Profile with cProfile

JavaScript Specific:
• Debounce event handlers
• Use requestAnimationFrame
• Minimize DOM manipulation
• Lazy load resources

Database:
• Add proper indexes
• Optimize queries
• Use connection pooling"""
        
        self._add_technical_message(chat_display, 'assistant', tips)
    
    async def _ask_pixie_voice(self):
        """Use voice input to ask Pixie a question"""
        try:
            if not self.voice_input_manager:
                await self._show_speech_bubble("Voice input is not available! 🎤❌", duration=3000)
                return
            
            # Show instruction bubble
            await self._show_speech_bubble("🎤 Listening... Ask me anything! (5 seconds)", duration=5000)
            
            # Listen for single input
            question = self.voice_input_manager.listen_once()
            
            if question:
                self.logger.info(f"Voice question from menu: '{question}'")
                
                # Show processing
                await self._show_speech_bubble("🎤 Thinking about your question...", duration=2000)
                
                # Get AI response using the existing chat response method
                response = await self._enhanced_chat_response(question)
                
                if response:
                    # Show response in speech bubble
                    await self._show_speech_bubble(f"You asked: {question}\n\n💭 {response}", duration=8000)
                    
                    # Add to chat history
                    self._add_chat_message("You (Voice)", question)
                    self._add_chat_message("Pixie", response)
                    
                    # Speak the response
                    if self.speech_manager and hasattr(self.speech_manager, 'speak_text'):
                        def speak_response():
                            try:
                                self.speech_manager.speak_text(response)
                            except Exception as e:
                                self.logger.error(f"Error speaking response: {e}")
                        
                        # Speak in a separate thread
                        import threading
                        speech_thread = threading.Thread(target=speak_response, daemon=True)
                        speech_thread.start()
                    
                    self.logger.info(f"Voice response completed for: {question[:50]}...")
                else:
                    error_msg = "Sorry, I couldn't process that question right now."
                    await self._show_speech_bubble(f"❓ {error_msg}", duration=3000)
            else:
                # No speech detected
                await self._show_speech_bubble("🎤 I didn't hear anything. Try again! 👂", duration=3000)
                
        except Exception as e:
            self.logger.error(f"Error in voice question: {e}")
            await self._show_speech_bubble("Sorry, I had trouble with voice input! 🎤❌", duration=3000)
    
    def _change_mood_menu(self):
        """Show mood selection menu"""
        try:
            mood_window = tk.Toplevel(self.root)
            mood_window.title("Change Pixie's Mood")
            mood_window.geometry("300x400")
            mood_window.wm_attributes("-topmost", True)
            
            # Apply theme
            if self.style_manager:
                theme = self.style_manager.get_theme()
                mood_window.configure(bg=theme.get_color("background"))
            
            tk.Label(
                mood_window, 
                text="Choose Pixie's Mood 🎭",
                font=('Segoe UI', 14, 'bold')
            ).pack(pady=20)
            
            moods = [
                ("🤝 Helpful", "helpful"),
                ("😸 Playful", "playful"),
                ("🤔 Curious", "curious"),
                ("💪 Encouraging", "encouraging"),
                ("😴 Sleepy", "sleepy"),
                ("🎉 Excited", "excited")
            ]
            
            for mood_text, mood_value in moods:
                btn = tk.Button(
                    mood_window,
                    text=mood_text,
                    font=('Segoe UI', 12),
                    relief='flat',
                    bd=0,
                    padx=20,
                    pady=10,
                    command=lambda m=mood_value: self._set_mood_and_close(m, mood_window)
                )
                btn.pack(pady=5, padx=20, fill='x')
                
                # Apply theme to button
                if self.style_manager:
                    theme = self.style_manager.get_theme()
                    if mood_value == self.current_mood:
                        btn.configure(bg=theme.get_color("primary"), fg="white")
                    else:
                        btn.configure(bg=theme.get_color("surface"), fg=theme.get_color("text_primary"))
            
            tk.Button(
                mood_window,
                text="Cancel",
                command=mood_window.destroy,
                font=('Segoe UI', 10)
            ).pack(pady=20)
            
        except Exception as e:
            self.logger.error(f"Error showing mood menu: {e}")
    
    def _set_mood_and_close(self, mood: str, window: tk.Toplevel):
        """Set pet mood and close the window"""
        self.current_mood = mood
        window.destroy()
        asyncio.create_task(self._show_speech_bubble(
            f"My mood is now {mood}! {self._get_mood_emoji()} Thanks for caring about how I feel!",
            duration=3000
        ))
    
    def _get_mood_emoji(self) -> str:
        """Get emoji for current mood"""
        return {
            "helpful": "🤝",
            "playful": "😸", 
            "curious": "🤔",
            "encouraging": "💪",
            "sleepy": "😴",
            "excited": "🎉"
        }.get(self.current_mood, "🐾")
    
    # Google Sheets Integration Methods
    
    async def _connect_to_sheet(self):
        """Connect to an existing Google Sheet"""
        if not GoogleSheetsManager:
            await self._show_speech_bubble("Google Sheets integration not available! Install required packages. 📦")
            return
        
        try:
            # Simple dialog to get sheet URL or ID
            if hasattr(self, 'root') and self.root:
                from tkinter import simpledialog
                url_or_id = simpledialog.askstring(
                    "Connect to Google Sheet",
                    "Enter your Google Sheet URL or ID:\n\n" +
                    "Full URL: https://docs.google.com/spreadsheets/d/[ID]/edit\n" +
                    "Or just the Sheet ID (44 characters long)",
                    parent=self.root
                )
                
                if url_or_id:
                    if not self.sheets_manager:
                        self.sheets_manager = GoogleSheetsManager()
                    
                    # Use the improved connection method
                    success, message = self.sheets_manager.connect_with_url_or_id(url_or_id)
                    await self._show_speech_bubble(message)
                    
                    if success:
                        self.logger.info(f"Connected to sheet: {self.sheets_manager.get_sheet_url()}")
                    else:
                        # Provide specific troubleshooting guidance
                        if "not authenticated" in message.lower():
                            await self._show_speech_bubble("💡 To connect to Google Sheets, you need API credentials. Right-click → Google Sheets → Setup Google Sheets for help!")
                        elif "invalid" in message.lower():
                            await self._show_speech_bubble("💡 Make sure to copy the full URL from your Google Sheet's address bar, or just the 44-character Sheet ID.")
                else:
                    await self._show_speech_bubble("No URL or ID provided. 🤔")
        except Exception as e:
            self.logger.error(f"Error connecting to sheet: {e}")
            await self._show_speech_bubble(f"❌ Error connecting to Google Sheet: {str(e)}")
    
    async def _create_project_sheet(self):
        """Create a new project tracking sheet"""
        if not GoogleSheetsManager:
            await self._show_speech_bubble("Google Sheets integration not available! 📦")
            return
        
        try:
            if hasattr(self, 'root') and self.root:
                from tkinter import simpledialog
                project_name = simpledialog.askstring(
                    "Create Project Sheet",
                    "Enter project name:",
                    parent=self.root
                )
                
                if project_name:
                    if not self.sheets_manager:
                        self.sheets_manager = GoogleSheetsManager()
                    
                    await self._show_speech_bubble("Creating project tracker... 📝", duration=2000)
                    
                    sheet_id = self.sheets_manager.create_project_tracker(project_name)
                    if sheet_id:
                        sheet_url = self.sheets_manager.get_sheet_url(sheet_id)
                        await self._show_speech_bubble(f"✅ Created project tracker for '{project_name}'! Ready to track your progress. 🎯")
                        
                        # Optionally open the sheet in browser
                        if sheet_url:
                            import webbrowser
                            webbrowser.open(sheet_url)
                    else:
                        await self._show_speech_bubble("❌ Failed to create project sheet. Check your Google Sheets setup. 🔧")
        except Exception as e:
            self.logger.error(f"Error creating project sheet: {e}")
            await self._show_speech_bubble("❌ Error creating project sheet! 😿")
    
    async def _log_to_sheet(self):
        """Log current activity to the connected sheet"""
        if not self.sheets_manager or not self.sheets_manager.current_sheet_id:
            await self._show_speech_bubble("No Google Sheet connected! Connect to a sheet first. 📊")
            return
        
        try:
            # Get current context or ask user what to log
            if hasattr(self, 'root') and self.root:
                from tkinter import simpledialog
                activity = simpledialog.askstring(
                    "Log Activity",
                    "What activity would you like to log?",
                    initialvalue="Working on code",
                    parent=self.root
                )
                
                if activity:
                    # Log with timestamp
                    timestamp = time.strftime('%Y-%m-%d %H:%M')
                    row_data = [timestamp, activity, "Completed", "1", f"Logged by Pixie 🐾"]
                    
                    if self.sheets_manager.append_row(row_data):
                        await self._show_speech_bubble(f"✅ Logged '{activity}' to your sheet! 📝")
                    else:
                        await self._show_speech_bubble("❌ Failed to log activity. Check your sheet connection. 🔗")
        except Exception as e:
            self.logger.error(f"Error logging to sheet: {e}")
            await self._show_speech_bubble("❌ Error logging activity! 😿")
    
    async def _analyze_screen_to_sheet(self):
        """Analyze current screen and insert results into sheet"""
        if not self.sheets_manager or not self.sheets_manager.current_sheet_id:
            await self._show_speech_bubble("No Google Sheet connected! Connect to a sheet first. 📊")
            return
        
        try:
            await self._show_speech_bubble("Analyzing screen and logging to sheet... 🔍", duration=2000)
            
            # Get screen analysis
            if hasattr(self, 'gemini_client') and self.gemini_client:
                context = self._capture_context()
                if context and context.get('screenshot'):
                    # Analyze screen
                    result = await self.gemini_client.analyze_screen_async(
                        screenshot=context['screenshot'],
                        context=context
                    )
                    
                    if result.get('success') and result.get('analysis'):
                        analysis = result['analysis'][:200] + "..." if len(result['analysis']) > 200 else result['analysis']
                        
                        # Log analysis to sheet
                        timestamp = time.strftime('%Y-%m-%d %H:%M')
                        row_data = [timestamp, "Screen Analysis", "Completed", "0.1", analysis]
                        
                        if self.sheets_manager.append_row(row_data):
                            await self._show_speech_bubble(f"✅ Screen analysis logged to sheet! 📊")
                        else:
                            await self._show_speech_bubble("❌ Failed to log analysis. Check sheet connection. 🔗")
                    else:
                        await self._show_speech_bubble("❌ Failed to analyze screen. 🤖")
                else:
                    await self._show_speech_bubble("❌ Could not capture screen for analysis. 📸")
            else:
                await self._show_speech_bubble("❌ AI analysis not available. 🤖")
                
        except Exception as e:
            self.logger.error(f"Error analyzing screen to sheet: {e}")
            await self._show_speech_bubble("❌ Error analyzing screen! 😿")
    
    def _setup_google_sheets(self):
        """Open Google Sheets setup guide"""
        try:
            setup_message = """Google Sheets Setup Guide:

1. Go to Google Cloud Console (console.cloud.google.com)
2. Create a new project or select existing one
3. Enable the Google Sheets API
4. Create credentials (Service Account)
5. Download the JSON credentials file
6. Add the path to config/settings.json under:
   "integrations": {
     "google_sheets": {
       "enabled": true,
       "credentials_path": "path/to/your/credentials.json"
     }
   }

Need help? Ask Pixie! 🐾"""

            messagebox.showinfo("Google Sheets Setup", setup_message)
            
        except Exception as e:
            self.logger.error(f"Error showing setup: {e}")
    
    def _open_current_sheet(self):
        """Open the current sheet in web browser"""
        if self.sheets_manager and self.sheets_manager.current_sheet_id:
            try:
                import webbrowser
                sheet_url = self.sheets_manager.get_sheet_url()
                if sheet_url:
                    webbrowser.open(sheet_url)
                    self.logger.info(f"Opened sheet in browser: {sheet_url}")
                else:
                    messagebox.showinfo("No Sheet", "No Google Sheet is currently connected.")
            except Exception as e:
                self.logger.error(f"Error opening sheet: {e}")
        else:
            messagebox.showinfo("No Sheet", "No Google Sheet is currently connected.")
    
    # Simple CSV Integration Methods
    
    async def _log_to_csv(self):
        """Log current activity to CSV file"""
        if not self.csv_logger:
            await self._show_speech_bubble("CSV logger not available!")
            return
        
        try:
            if hasattr(self, 'root') and self.root:
                from tkinter import simpledialog
                activity = simpledialog.askstring(
                    "Log to CSV",
                    "What activity would you like to log?",
                    initialvalue="Working on project",
                    parent=self.root
                )
                
                if activity:
                    success = self.csv_logger.log_activity("Manual Entry", activity, 0, "", "User logged")
                    if success:
                        row_count = self.csv_logger.get_row_count()
                        await self._show_speech_bubble(f"✅ Logged to CSV! Total entries: {row_count}")
                        self.logger.info(f"Manual activity logged to CSV: {activity}")
                    else:
                        await self._show_speech_bubble("❌ Failed to log to CSV file")
                else:
                    await self._show_speech_bubble("No activity entered")
        except Exception as e:
            self.logger.error(f"Error logging to CSV: {e}")
            await self._show_speech_bubble("❌ Error logging to CSV!")
    
    def _show_csv_import_guide(self):
        """Show instructions for importing CSV to Google Sheets"""
        if not self.csv_logger:
            messagebox.showinfo("CSV Logger", "CSV logger not available.")
            return
        
        try:
            instructions = self.csv_logger.get_import_instructions()
            messagebox.showinfo("Google Sheets Import Guide", instructions)
        except Exception as e:
            self.logger.error(f"Error showing CSV guide: {e}")
    
    def _open_csv_file(self):
        """Open the CSV file location"""
        if not self.csv_logger:
            messagebox.showinfo("CSV Logger", "CSV logger not available.")
            return
        
        try:
            import os
            csv_path = self.csv_logger.get_file_path()
            
            if os.path.exists(csv_path):
                # Open file location in Windows Explorer
                os.system(f'explorer /select,"{csv_path}"')
                self.logger.info(f"Opened CSV file location: {csv_path}")
            else:
                messagebox.showinfo("CSV File", f"CSV file not found at: {csv_path}")
        except Exception as e:
            self.logger.error(f"Error opening CSV file: {e}")
            messagebox.showerror("Error", f"Could not open CSV file: {e}")
    
    def auto_log_coding_activity(self, file_name, activity_type="File Edit"):
        """Automatically log coding activity to CSV"""
        if self.csv_logger:
            try:
                self.csv_logger.log_coding_session(file_name, activity_type, 0)
                self.logger.info(f"Auto-logged coding activity: {file_name}")
            except Exception as e:
                self.logger.error(f"Failed to auto-log activity: {e}")
    
    # Pet Switching Methods
    
    async def _change_pet(self, pet_type):
        """Change the current pet to a different one"""
        try:
            # Get available pets from settings
            available_pets = self.settings.get('pet', {}).get('available_pets', {})
            
            if pet_type not in available_pets:
                await self._show_speech_bubble(f"❌ Pet type '{pet_type}' not available!")
                return
            
            # Don't change if it's already the current pet
            current_pet = self.settings.get('pet', {}).get('current_pet', 'ghost')
            if current_pet == pet_type:
                pet_name = available_pets[pet_type].get('name', pet_type.title())
                await self._show_speech_bubble(f"✨ I'm already {pet_name}! 😊")
                return
            
            # Update current pet in settings
            pet_config = available_pets[pet_type]
            self.settings['pet']['current_pet'] = pet_type
            
            # Save settings
            from src.utils.config_manager import ConfigManager
            config_manager = ConfigManager()
            config_manager.save_config(self.config)
            
            # Reload settings to ensure consistency
            self.config = config_manager.load_config()
            self.settings = self.config
            
            # Update pet image
            await self._update_pet_image(pet_config)
            
            # Show confirmation with pet's personality
            pet_name = pet_config.get('name', pet_type.title())
            personality = pet_config.get('personality', 'helpful')
            await self._show_speech_bubble(f"✨ I'm now {pet_name}! I'm {personality} 🎭")
            
            # Log the change
            if self.csv_logger:
                self.csv_logger.log_activity(
                    "Pet Change", 
                    f"Changed to {pet_name} ({pet_type})", 
                    0, 
                    "Settings", 
                    f"Now {personality}"
                )
            
            self.logger.info(f"Pet changed to {pet_type} ({pet_name})")
            
        except Exception as e:
            self.logger.error(f"Error changing pet: {e}")
            await self._show_speech_bubble("❌ Failed to change pet!")
    
    async def _update_pet_image(self, pet_config):
        """Update the pet's visual appearance"""
        try:
            import os
            from PIL import Image, ImageTk
            
            # Get image path
            image_path = pet_config.get('image', 'react-app/public/ghost.png')
            
            # Check if image exists
            if not os.path.exists(image_path):
                self.logger.warning(f"Pet image not found: {image_path}")
                # Try to use default ghost image
                image_path = 'react-app/public/ghost.png'
                if not os.path.exists(image_path):
                    return
            
            # Load and resize image
            pil_image = Image.open(image_path)
            pet_size = self.settings.get('pet', {}).get('size', {'width': 270, 'height': 270})
            
            # Resize maintaining aspect ratio
            pil_image = pil_image.resize(
                (pet_size['width'], pet_size['height']), 
                Image.Resampling.LANCZOS
            )
            
            # Convert to PhotoImage
            self.pet_image = ImageTk.PhotoImage(pil_image)
            
            # Update the pet image display
            image_updated = False
            
            # Check if using ModernPetWidget first (preferred method)
            if hasattr(self, 'pet_widget') and self.pet_widget and hasattr(self.pet_widget, 'update_pet_image'):
                try:
                    success = self.pet_widget.update_pet_image(image_path)
                    if success:
                        image_updated = True
                        self.logger.info(f"Updated ModernPetWidget image: {image_path}")
                    else:
                        self.logger.warning(f"ModernPetWidget failed to update image: {image_path}")
                except Exception as e:
                    self.logger.error(f"Error updating ModernPetWidget image: {e}")
            
            # Fallback to manual canvas update if ModernPetWidget failed or not available
            if not image_updated:
                canvas_to_update = None
                
                # Check available canvas options
                if hasattr(self, 'pet_widget') and self.pet_widget and hasattr(self.pet_widget, 'canvas'):
                    canvas_to_update = self.pet_widget.canvas
                elif hasattr(self, 'canvas') and self.canvas:
                    canvas_to_update = self.canvas
                elif hasattr(self, 'pet_canvas') and self.pet_canvas:
                    canvas_to_update = self.pet_canvas
                
                if canvas_to_update and hasattr(self, 'root') and self.root:
                    # Clear canvas
                    canvas_to_update.delete("all")
                    
                    # Get canvas dimensions
                    try:
                        canvas_width = canvas_to_update.winfo_width() or pet_size['width']
                        canvas_height = canvas_to_update.winfo_height() or pet_size['height']
                    except:
                        canvas_width = pet_size['width']
                        canvas_height = pet_size['height']
                    
                    # Add new image
                    canvas_to_update.create_image(
                        canvas_width // 2, 
                        canvas_height // 2, 
                        image=self.pet_image, 
                        anchor="center",
                        tags="pet"
                    )
                    
                    # Update canvas background to transparent
                    try:
                        canvas_to_update.configure(bg='', highlightthickness=0)
                    except:
                        pass
                    
                    image_updated = True
                    self.logger.info(f"Updated canvas image manually: {image_path}")
            
            if not image_updated:
                self.logger.warning("Failed to update pet image - no suitable display method found")
                
            # Force a display update
            if hasattr(self, 'root') and self.root:
                self.root.update_idletasks()
                
            self.logger.info(f"Updated pet image: {image_path}")
            
        except Exception as e:
            self.logger.error(f"Error updating pet image: {e}")
            # Print full error for debugging
            import traceback
            self.logger.error(f"Full error traceback: {traceback.format_exc()}")
    
    def _get_current_pet_info(self):
        """Get information about the current pet"""
        try:
            current_pet_type = self.settings.get('pet', {}).get('current_pet', 'ghost')
            available_pets = self.settings.get('pet', {}).get('available_pets', {})
            
            if current_pet_type in available_pets:
                return available_pets[current_pet_type]
            else:
                # Return default ghost pet
                return {
                    'name': 'Ghost Pixie',
                    'image': 'react-app/public/ghost.png',
                    'personality': 'mysterious and helpful'
                }
        except Exception as e:
            self.logger.error(f"Error getting current pet info: {e}")
            return {'name': 'Pixie', 'image': 'react-app/public/ghost.png', 'personality': 'helpful'}
