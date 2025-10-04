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
    VSCodeIntegration = None

# Import modern UI components
try:
    from src.ui.modern_components import (ModernPetWidget, ModernChatWindow, 
                                        ModernContextMenu, ModernSpeechBubble, 
                                        DarkModeToggle)
except ImportError:
    # Fallback if modern components aren't available
    ModernPetWidget = None
    ModernChatWindow = None
    ModernContextMenu = None
    ModernSpeechBubble = None
    DarkModeToggle = None

# Import theme manager
try:
    from src.ui.theme_manager import get_style_manager, get_theme
except ImportError:
    get_style_manager = None
    get_theme = None

class PetManager:
    """Main manager for the virtual pet assistant"""
    
    def __init__(self, gemini_client, screen_monitor, config):
        self.logger = logging.getLogger(__name__)
        self.gemini_client = gemini_client
        self.screen_monitor = screen_monitor
        self.config = config
        
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
        
        # State
        self.current_context = None
        self.chat_history = []
        self.conversation_messages = []  # Store conversation for speech bubbles
        
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
            
            # Start UI loop
            ui_task = asyncio.create_task(self._run_ui_loop())
            
            # Wait for either task to complete
            await asyncio.gather(monitor_task, ui_task, return_exceptions=True)
            
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
        """Enhanced simple display as fallback"""
        canvas = tk.Canvas(
            self.pet_window,
            width=size["width"] - 20,
            height=size["height"] - 20,
            bg='#000001',
            highlightthickness=0,
            bd=0
        )
        canvas.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Enable transparency
        self.pet_window.wm_attributes('-transparentcolor', '#000001')
        
        # Draw enhanced pet with gradient colors
        center_x, center_y = (size["width"] - 20) // 2, (size["height"] - 20) // 2
        radius = min(size["width"], size["height"]) // 3
        
        # Glow effect
        for i in range(5):
            glow_radius = radius + i * 3
            canvas.create_oval(
                center_x - glow_radius, center_y - glow_radius,
                center_x + glow_radius, center_y + glow_radius,
                fill='#FF69B4', outline='', stipple='gray25'
            )
        
        # Main body with modern colors
        canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill='#FFB6C1', outline='#FF69B4', width=3
        )
        
        # Enhanced eyes
        eye_size = 8
        left_eye_x, right_eye_x = center_x - 15, center_x + 15
        eye_y = center_y - 8
        
        # Eye whites
        canvas.create_oval(left_eye_x - eye_size, eye_y - 4, left_eye_x + eye_size, eye_y + 4, fill='white', outline='#ddd')
        canvas.create_oval(right_eye_x - eye_size, eye_y - 4, right_eye_x + eye_size, eye_y + 4, fill='white', outline='#ddd')
        
        # Pupils
        canvas.create_oval(left_eye_x - 3, eye_y - 3, left_eye_x + 3, eye_y + 3, fill='#333')
        canvas.create_oval(right_eye_x - 3, eye_y - 3, right_eye_x + 3, eye_y + 3, fill='#333')
        
        # Sparkles
        canvas.create_oval(left_eye_x - 1, eye_y - 2, left_eye_x + 1, eye_y, fill='white')
        canvas.create_oval(right_eye_x - 1, eye_y - 2, right_eye_x + 1, eye_y, fill='white')
        
        # Nose
        canvas.create_polygon(center_x - 3, center_y + 5, center_x + 3, center_y + 5, center_x, center_y - 2, fill='#FF1493', outline='#C71585')
        
        # Mouth
        canvas.create_arc(center_x - 12, center_y + 8, center_x + 12, center_y + 20, start=0, extent=180, outline='#FF1493', width=2, style='arc')
        
        self.pet_canvas = canvas
        
        # Bind events for dragging and clicking
        canvas.bind("<Button-1>", self._on_pet_press)
        canvas.bind("<B1-Motion>", self._on_pet_drag)
        canvas.bind("<ButtonRelease-1>", self._on_pet_release)
        canvas.bind("<Double-Button-1>", self._on_pet_double_click)
        canvas.bind("<Enter>", self._on_pet_hover_enter)
        canvas.bind("<Leave>", self._on_pet_hover_leave)
    
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
        self.speech_bubble.show_message(message, duration=4000, typing_effect=True)
        
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
    
    def _on_pet_right_click(self, event):
        """Handle right click - show modern context menu"""
        if ModernContextMenu:
            # Use modern context menu
            # Determine current theme for toggle text
            current_theme = self.style_manager.get_theme() if self.style_manager else None
            is_dark = current_theme.is_dark_theme() if current_theme else False
            theme_text = "☀️ Switch to Light Mode" if is_dark else "🌙 Switch to Dark Mode"
            
            menu_options = [
                ("💬 Open Full Chat Window", lambda: asyncio.create_task(self._open_chat_interface())),
                ("💭 Say Something", lambda: asyncio.create_task(self._show_pet_message())),
                ("📸 Take Screenshot & Analyze", lambda: asyncio.create_task(self._analyze_current_screen())),
                "---",  # Separator - VS Code
                ("🎯 Fix Current File", lambda: asyncio.create_task(self._fix_current_vscode_file())),
                "---",  # Separator - Code Generation
                ("🛠️ Generate Code", lambda: asyncio.create_task(self._show_code_generation_menu())),
                ("📝 Analyze Code", lambda: asyncio.create_task(self._analyze_code_interface())),
                ("🔧 Fix Code Errors", lambda: asyncio.create_task(self._fix_code_interface())),
                ("🧪 Generate Tests", lambda: asyncio.create_task(self._generate_tests_interface())),
                "---",  # Separator - Appearance
                ("🔍 Make Bigger", self._resize_bigger),
                ("🔎 Make Smaller", self._resize_smaller),
                ("📏 Reset Size", self._reset_pet_size),
                (theme_text, self._toggle_dark_mode),
                "---",  # Separator - Settings
                ("⚙️ Settings", self._open_settings),
                ("❌ Exit", self._exit_application)
            ]
            
            modern_menu = ModernContextMenu(self.root)
            modern_menu.show(event.x_root, event.y_root, menu_options)
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
            # Get response from AI
            response = await self.gemini_client.chat_response(
                message=message,
                context=self.current_context
            )
            
            # Replace thinking message with response
            self._replace_chat_message(thinking_id, "Pixie", response)
            
        except Exception as e:
            self.logger.error(f"Error getting AI response: {e}")
            self._replace_chat_message(thinking_id, "Pixie", "Sorry, I'm having trouble thinking right now. Could you try again? 🐱")
    
    async def _analyze_current_screen(self):
        """Analyze the current screen and provide suggestions"""
        try:
            # Show activity indicator
            self._show_activity_indicator(True)
            
            # Capture screenshot
            screenshot = self.screen_monitor.get_screenshot()
            context = self.screen_monitor.get_screen_context()
            
            # Get AI analysis
            analysis = await self.gemini_client.analyze_screen(
                screenshot=screenshot,
                context=context
            )
            
            # Show analysis in speech bubble if available, otherwise use chat/popup
            if self.speech_bubble:
                # Truncate analysis for speech bubble display
                short_analysis = analysis[:100] + "..." if len(analysis) > 100 else analysis
                self.speech_bubble.show_message(f"📸 {short_analysis}", duration=6000, typing_effect=True)
            elif self.chat_window and self.chat_window.winfo_exists():
                self._add_chat_message("Pixie", f"📸 I can see your screen! Here's what I notice:\n\n{analysis}")
            else:
                # Show in a popup as last resort
                messagebox.showinfo("Screen Analysis", analysis)
            
        except Exception as e:
            self.logger.error(f"Error analyzing screen: {e}")
            error_msg = "I'm having trouble seeing your screen right now. Please try again! 🐱"
            
            # Show error in speech bubble if available
            if self.speech_bubble:
                self.speech_bubble.show_message(error_msg, duration=4000, typing_effect=True)
            elif self.chat_window and self.chat_window.winfo_exists():
                self._add_chat_message("Pixie", error_msg)
            else:
                messagebox.showerror("Error", error_msg)
        
        finally:
            # Hide activity indicator
            self._show_activity_indicator(False)
    
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
            "timestamp": asyncio.get_event_loop().time()
        }
        
        self.logger.debug(f"Screen changed to: {window_info.get('title', 'Unknown')}")
    
    def _open_settings(self):
        """Open settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Pixie Settings")
        settings_window.geometry("300x200")
        settings_window.wm_attributes("-topmost", True)
        
        ttk.Label(settings_window, text="Settings coming soon! 🛠️").pack(expand=True)
        ttk.Button(settings_window, text="Close", command=settings_window.destroy).pack(pady=10)
    
    def _exit_application(self):
        """Exit the application"""
        if messagebox.askquestion("Exit", "Are you sure you want to close Pixie?") == 'yes':
            self.is_running = False
            self.screen_monitor.stop_monitoring()
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
        """Run the UI event loop"""
        while self.is_running and self.root and self.root.winfo_exists():
            try:
                self.root.update()
                await asyncio.sleep(0.01)  # Small delay to prevent excessive CPU usage
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
                await self._show_speech_bubble("I need a Gemini API key to generate code! 🔑", duration=3000)
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
                    await self._show_speech_bubble(f"Code generation failed: {result.get('error', 'Unknown error')} 😿", duration=4000)
                    
        except Exception as e:
            self.logger.error(f"Error in code generation: {e}")
            await self._show_speech_bubble("Something went wrong with code generation! 😿", duration=3000)
    
    async def _analyze_code_interface(self):
        """Show code analysis interface"""
        try:
            if not self.gemini_client:
                await self._show_speech_bubble("I need a Gemini API key to analyze code! 🔑", duration=3000)
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
                    await self._show_speech_bubble(f"Code analysis failed: {result.get('error', 'Unknown error')} 😿", duration=4000)
            else:
                await self._show_speech_bubble("I need some code to analyze! 🤔", duration=3000)
                
        except Exception as e:
            self.logger.error(f"Error in code analysis: {e}")
            await self._show_speech_bubble("Something went wrong with code analysis! 😿", duration=3000)
    
    async def _fix_code_interface(self):
        """Show code fixing interface"""
        try:
            if not self.gemini_client:
                await self._show_speech_bubble("I need a Gemini API key to fix code! 🔑", duration=3000)
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
                        await self._show_speech_bubble(f"Code fixing failed: {result.get('error', 'Unknown error')} 😿", duration=4000)
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
            window.title(f"Pixie - {title}")
            window.geometry("800x600")
            window.wm_attributes("-topmost", True)
            
            # Create notebook for tabs
            notebook = ttk.Notebook(window)
            notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
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
        """Fix the currently active file in VS Code"""
        try:
            if not self.vscode_integration:
                await self._show_speech_bubble("VS Code integration not available! 😿", duration=3000)
                return
            
            await self._show_speech_bubble("Fixing your current file... 🔧", duration=2000)
            
            result = await self.vscode_integration.apply_code_fix(self.gemini_client)
            
            if result.get('success'):
                if result.get('applied'):
                    message = f"✅ Fixed your file!\n\n{result.get('explanation', 'Code has been improved')}"
                    if result.get('backup_path'):
                        message += f"\n\nBackup saved: {Path(result['backup_path']).name}"
                    
                    await self._show_speech_bubble(message, duration=5000)
                else:
                    await self._show_speech_bubble(f"Found issues but couldn't apply fix: {result.get('edit_error', 'Unknown error')} 😿", duration=4000)
            else:
                await self._show_speech_bubble(f"Couldn't fix the file: {result.get('error', 'Unknown error')} 😿", duration=4000)
                
        except Exception as e:
            self.logger.error(f"Error fixing VS Code file: {e}")
            await self._show_speech_bubble("Something went wrong fixing your file! 😿", duration=3000)
    
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
    
    async def _show_speech_bubble(self, message: str, duration: int = 3000):
        """Show a speech bubble message near the pet"""
        try:
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