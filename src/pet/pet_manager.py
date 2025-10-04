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
from PIL import Image, ImageTk

# Import modern UI components
try:
    from src.ui.modern_components import ModernPetWidget, ModernChatWindow, ModernContextMenu
except ImportError:
    # Fallback if modern components aren't available
    ModernPetWidget = None
    ModernChatWindow = None
    ModernContextMenu = None

class PetManager:
    """Main manager for the virtual pet assistant"""
    
    def __init__(self, gemini_client, screen_monitor, config):
        self.logger = logging.getLogger(__name__)
        self.gemini_client = gemini_client
        self.screen_monitor = screen_monitor
        self.config = config
        
        # UI components
        self.root = None
        self.pet_window = None
        self.chat_window = None
        self.is_running = False
        
        # State
        self.current_context = None
        self.chat_history = []
        
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
        size = pet_config.get("size", {"width": 120, "height": 120})  # Slightly larger for modern design
        
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
            
            # Connect events
            self.pet_widget.canvas.bind("<Button-1>", self._on_pet_click)
            self.pet_widget.canvas.bind("<B1-Motion>", self._on_pet_drag)
            
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
        
        # Bind events
        canvas.bind("<Button-1>", self._on_pet_click)
        canvas.bind("<B1-Motion>", self._on_pet_drag)
    
    def _on_pet_click(self, event):
        """Handle pet click - open chat interface"""
        asyncio.create_task(self._open_chat_interface())
    
    def _on_pet_drag(self, event):
        """Handle pet dragging"""
        x = self.pet_window.winfo_pointerx() - self.pet_window.winfo_rootx()
        y = self.pet_window.winfo_pointery() - self.pet_window.winfo_rooty()
        
        new_x = self.pet_window.winfo_pointerx() - x
        new_y = self.pet_window.winfo_pointery() - y
        
        self.pet_window.geometry(f"+{new_x}+{new_y}")
    
    def _on_pet_right_click(self, event):
        """Handle right click - show modern context menu"""
        if ModernContextMenu:
            # Use modern context menu
            menu_options = [
                ("💬 Chat with Pixie", lambda: asyncio.create_task(self._open_chat_interface())),
                ("📸 Take Screenshot & Analyze", lambda: asyncio.create_task(self._analyze_current_screen())),
                "---",  # Separator
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
            
            # If chat window is open, add the analysis
            if self.chat_window and self.chat_window.winfo_exists():
                self._add_chat_message("Pixie", f"📸 I can see your screen! Here's what I notice:\n\n{analysis}")
            else:
                # Show in a popup
                messagebox.showinfo("Screen Analysis", analysis)
            
        except Exception as e:
            self.logger.error(f"Error analyzing screen: {e}")
            error_msg = "I'm having trouble seeing your screen right now. Please try again! 🐱"
            
            if self.chat_window and self.chat_window.winfo_exists():
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