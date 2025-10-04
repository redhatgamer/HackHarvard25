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
        """Create the floating pet window"""
        self.pet_window = tk.Toplevel(self.root)
        
        # Window properties
        pet_config = self.config.get("pet", {})
        size = pet_config.get("size", {"width": 100, "height": 100})
        
        self.pet_window.title("Pixie - Your AI Pet")
        self.pet_window.geometry(f"{size['width']}x{size['height']}")
        
        # Make window stay on top and semi-transparent
        ui_config = self.config.get("ui", {})
        if ui_config.get("always_on_top", True):
            self.pet_window.wm_attributes("-topmost", True)
        
        transparency = ui_config.get("transparency", 0.9)
        self.pet_window.wm_attributes("-alpha", transparency)
        
        # Remove window decorations for floating effect
        self.pet_window.overrideredirect(True)
        
        # Position window
        position = pet_config.get("position", {"x": -1, "y": -1})
        if position["x"] == -1 or position["y"] == -1:
            # Auto-position in bottom-right corner
            screen_width = self.pet_window.winfo_screenwidth()
            screen_height = self.pet_window.winfo_screenheight()
            x = screen_width - size["width"] - 50
            y = screen_height - size["height"] - 100
        else:
            x, y = position["x"], position["y"]
        
        self.pet_window.geometry(f"+{x}+{y}")
        
        # Create pet display
        await self._setup_pet_display()
        
        # Bind events
        self.pet_window.bind("<Button-1>", self._on_pet_click)
        self.pet_window.bind("<B1-Motion>", self._on_pet_drag)
        self.pet_window.bind("<Button-3>", self._on_pet_right_click)  # Right click menu
        
        self.logger.info("Pet window created")
    
    async def _setup_pet_display(self):
        """Setup the pet display with animations"""
        # For now, create a simple colored circle as the pet
        # In a full implementation, you'd load animated GIFs or sprites
        
        canvas = tk.Canvas(
            self.pet_window,
            width=80,
            height=80,
            bg='lightblue',
            highlightthickness=0
        )
        canvas.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Draw a simple pet face
        # Body (circle)
        canvas.create_oval(10, 10, 70, 70, fill='#FFB6C1', outline='#FF69B4', width=2)
        
        # Eyes
        canvas.create_oval(25, 25, 35, 35, fill='black')
        canvas.create_oval(45, 25, 55, 35, fill='black')
        
        # Eye sparkles
        canvas.create_oval(28, 28, 30, 30, fill='white')
        canvas.create_oval(48, 28, 50, 30, fill='white')
        
        # Nose
        canvas.create_polygon(40, 40, 35, 48, 45, 48, fill='#FF1493')
        
        # Mouth
        canvas.create_arc(30, 45, 50, 60, start=0, extent=180, fill='#FF69B4')
        
        # Add a speech bubble indicator when active
        self.speech_indicator = canvas.create_text(
            40, 5, text="💭", font=("Arial", 12), fill='blue'
        )
        canvas.itemconfig(self.speech_indicator, state='hidden')
        
        self.pet_canvas = canvas
    
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
        """Handle right click - show context menu"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Chat with Pixie", command=lambda: asyncio.create_task(self._open_chat_interface()))
        menu.add_command(label="Take Screenshot & Analyze", command=lambda: asyncio.create_task(self._analyze_current_screen()))
        menu.add_separator()
        menu.add_command(label="Settings", command=self._open_settings)
        menu.add_command(label="Exit", command=self._exit_application)
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    async def _open_chat_interface(self):
        """Open the chat interface window"""
        if self.chat_window and self.chat_window.winfo_exists():
            self.chat_window.lift()
            return
        
        self.chat_window = tk.Toplevel(self.root)
        self.chat_window.title("Chat with Pixie 🐱")
        self.chat_window.geometry("400x500")
        self.chat_window.wm_attributes("-topmost", True)
        
        # Chat display
        chat_frame = ttk.Frame(self.chat_window)
        chat_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Chat history
        self.chat_display = tk.Text(
            chat_frame,
            wrap='word',
            state='disabled',
            height=15
        )
        scrollbar = ttk.Scrollbar(chat_frame, orient="vertical", command=self.chat_display.yview)
        self.chat_display.configure(yscrollcommand=scrollbar.set)
        
        self.chat_display.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Input frame
        input_frame = ttk.Frame(self.chat_window)
        input_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.chat_input = tk.Text(input_frame, height=3, wrap='word')
        self.chat_input.pack(fill='x', pady=(0, 5))
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill='x')
        
        send_button = ttk.Button(
            button_frame,
            text="Send",
            command=lambda: asyncio.create_task(self._send_chat_message())
        )
        send_button.pack(side='right', padx=(5, 0))
        
        analyze_button = ttk.Button(
            button_frame,
            text="Analyze Screen",
            command=lambda: asyncio.create_task(self._analyze_current_screen())
        )
        analyze_button.pack(side='right')
        
        # Bind Enter key
        self.chat_input.bind("<Control-Return>", lambda e: asyncio.create_task(self._send_chat_message()))
        
        # Welcome message
        self._add_chat_message("Pixie", "Hi there! 🐾 I'm Pixie, your AI assistant! I can see what's on your screen and help you with whatever you're working on. What can I help you with today?")
        
        self.chat_input.focus_set()
    
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
            if hasattr(self, 'pet_canvas'):
                self.pet_canvas.itemconfig(self.speech_indicator, state='normal')
            
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
            if hasattr(self, 'pet_canvas'):
                self.pet_canvas.itemconfig(self.speech_indicator, state='hidden')
    
    def _add_chat_message(self, sender: str, message: str) -> str:
        """Add a message to the chat display"""
        if not hasattr(self, 'chat_display'):
            return ""
        
        self.chat_display.config(state='normal')
        
        # Create unique tag for this message
        import uuid
        message_id = str(uuid.uuid4())
        
        # Add sender and message
        self.chat_display.insert('end', f"{sender}: ", f"sender_{message_id}")
        self.chat_display.insert('end', f"{message}\n\n", f"message_{message_id}")
        
        # Style sender names
        if sender == "Pixie":
            self.chat_display.tag_config(f"sender_{message_id}", foreground="blue", font=("Arial", 10, "bold"))
        else:
            self.chat_display.tag_config(f"sender_{message_id}", foreground="green", font=("Arial", 10, "bold"))
        
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