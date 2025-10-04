#!/usr/bin/env python3
"""
Test script for dark mode functionality
This script demonstrates the dark mode toggle without requiring the full pet assistant setup
"""

import tkinter as tk
import sys
import os
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from ui.theme_manager import StyleManager, get_style_manager
    from ui.modern_components import DarkModeToggle, ModernChatWindow
except ImportError as e:
    print(f"Could not import required modules: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)

class DarkModeDemo:
    """Demo application for testing dark mode functionality"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dark Mode Demo - Desktop Pet")
        self.root.geometry("600x500")
        
        # Initialize style manager
        self.style_manager = get_style_manager()
        self.theme = self.style_manager.get_theme()
        
        # Set up theme change callback
        self.style_manager.add_theme_change_callback(self.on_theme_change)
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Setup the demo UI"""
        # Main container
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        self.title_label = tk.Label(
            self.main_frame,
            text="🐱 Desktop Pet - Dark Mode Demo",
            font=('Segoe UI', 16, 'bold')
        )
        self.title_label.pack(pady=(0, 20))
        
        # Dark mode toggle
        toggle_frame = tk.Frame(self.main_frame)
        toggle_frame.pack(pady=10)
        
        self.dark_toggle = DarkModeToggle(
            toggle_frame,
            callback=self.on_dark_mode_toggle,
            initial_state=self.theme.is_dark_theme()
        )
        self.dark_toggle.pack()
        
        # Demo content area
        content_frame = tk.Frame(self.main_frame)
        content_frame.pack(fill='both', expand=True, pady=20)
        
        # Sample text area
        text_label = tk.Label(content_frame, text="Sample Text Area:", font=('Segoe UI', 12, 'bold'))
        text_label.pack(anchor='w', pady=(0, 5))
        
        self.text_area = tk.Text(
            content_frame,
            height=10,
            font=('Segoe UI', 10),
            wrap='word'
        )
        self.text_area.pack(fill='both', expand=True)
        
        # Sample content
        sample_text = """This is a demonstration of the dark mode functionality for the Desktop Pet AI Assistant.

🌟 Features:
• Toggle between light and dark themes
• Automatic color scheme switching
• Persistent theme settings
• Modern UI components
• Smooth transitions

Try clicking the dark mode toggle above to see the theme change in real-time!

The theme setting is automatically saved to the configuration file and will persist between sessions."""
        
        self.text_area.insert('1.0', sample_text)
        
        # Buttons frame
        button_frame = tk.Frame(content_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        self.primary_btn = tk.Button(
            button_frame,
            text="Primary Button",
            font=('Segoe UI', 10, 'bold'),
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.primary_btn.pack(side='left', padx=(0, 10))
        
        self.secondary_btn = tk.Button(
            button_frame,
            text="Secondary Button",
            font=('Segoe UI', 10, 'bold'),
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.secondary_btn.pack(side='left')
        
        # Test chat window button
        self.chat_btn = tk.Button(
            button_frame,
            text="Open Chat Window",
            font=('Segoe UI', 10),
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.open_chat_window
        )
        self.chat_btn.pack(side='right')
    
    def apply_theme(self):
        """Apply current theme to all UI elements"""
        # Get theme colors
        bg_color = self.theme.get_color("background")
        surface_color = self.theme.get_color("surface")
        text_color = self.theme.get_color("text_primary")
        primary_color = self.theme.get_color("primary")
        secondary_color = self.theme.get_color("secondary")
        border_color = self.theme.get_color("border")
        
        # Apply to main window and frames
        self.root.configure(bg=bg_color)
        self.main_frame.configure(bg=bg_color)
        
        # Apply to title
        self.title_label.configure(bg=bg_color, fg=text_color)
        
        # Apply to text area
        self.text_area.configure(
            bg=surface_color,
            fg=text_color,
            insertbackground=primary_color,
            selectbackground=self.theme.get_color("primary") + "40"  # Semi-transparent
        )
        
        # Apply to buttons
        self.primary_btn.configure(
            bg=primary_color,
            fg='white',
            activebackground=self.theme.get_color("primary_hover"),
            activeforeground='white'
        )
        
        self.secondary_btn.configure(
            bg=secondary_color,
            fg='white',
            activebackground=self.theme.get_color("secondary_hover"),
            activeforeground='white'
        )
        
        self.chat_btn.configure(
            bg=surface_color,
            fg=text_color,
            activebackground=border_color,
            activeforeground=text_color
        )
        
        # Update all child frames recursively
        self._update_frame_colors(self.main_frame, bg_color)
    
    def _update_frame_colors(self, frame, bg_color):
        """Recursively update frame background colors"""
        for child in frame.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=bg_color)
                self._update_frame_colors(child, bg_color)
            elif isinstance(child, tk.Label) and child != self.title_label:
                child.configure(bg=bg_color, fg=self.theme.get_color("text_primary"))
    
    def on_dark_mode_toggle(self, is_dark):
        """Handle dark mode toggle"""
        print(f"Dark mode {'enabled' if is_dark else 'disabled'}")
        # The StyleManager will handle the theme change and trigger our callback
    
    def on_theme_change(self, new_theme):
        """Handle theme change event"""
        self.theme = new_theme
        self.apply_theme()
        print(f"Theme changed to: {'Dark' if new_theme.is_dark_theme() else 'Light'}")
    
    def open_chat_window(self):
        """Open a demo chat window"""
        try:
            chat = ModernChatWindow(self.root, "Dark Mode Demo Chat")
            chat.add_message("System", "Welcome to the dark mode demo chat!")
            chat.add_message("User", "This chat window also supports dark mode!")
            chat.add_message("System", "Try toggling dark mode in the main window to see this chat update automatically.")
        except Exception as e:
            print(f"Error opening chat window: {e}")
    
    def run(self):
        """Start the demo application"""
        print("Starting Dark Mode Demo...")
        print("Use the toggle to switch between light and dark themes")
        self.root.mainloop()

if __name__ == "__main__":
    try:
        demo = DarkModeDemo()
        demo.run()
    except Exception as e:
        print(f"Error starting demo: {e}")
        import traceback
        traceback.print_exc()