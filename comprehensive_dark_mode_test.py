#!/usr/bin/env python3
"""
Comprehensive Dark Mode Test for Desktop Pet
Tests all UI components with dark mode functionality
"""

import tkinter as tk
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from ui.theme_manager import get_style_manager, get_theme
    from ui.modern_components import (ModernContextMenu, ModernChatWindow, 
                                    ModernSpeechBubble, DarkModeToggle)
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

class ComprehensiveDarkModeTest:
    """Comprehensive test for all dark mode components"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌙 Comprehensive Dark Mode Test")
        self.root.geometry("800x600")
        
        # Get style manager
        self.style_manager = get_style_manager()
        self.theme = self.style_manager.get_theme()
        
        # Set up theme callback
        self.style_manager.add_theme_change_callback(self.on_theme_change)
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Setup comprehensive test UI"""
        # Main container
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        self.title_label = tk.Label(
            self.main_frame,
            text="🌙 Desktop Pet - Dark Mode Test Suite",
            font=('Segoe UI', 18, 'bold')
        )
        self.title_label.pack(pady=(0, 20))
        
        # Control panel
        control_frame = tk.Frame(self.main_frame)
        control_frame.pack(fill='x', pady=(0, 20))
        
        # Dark mode toggle
        toggle_frame = tk.Frame(control_frame)
        toggle_frame.pack(side='left')
        
        self.dark_toggle = DarkModeToggle(
            toggle_frame,
            callback=self.on_dark_mode_toggle,
            initial_state=self.theme.is_dark_theme()
        )
        self.dark_toggle.pack()
        
        # Test buttons
        button_frame = tk.Frame(control_frame)
        button_frame.pack(side='right')
        
        self.context_menu_btn = tk.Button(
            button_frame,
            text="Test Context Menu",
            command=self.test_context_menu,
            font=('Segoe UI', 10),
            relief='flat',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        self.context_menu_btn.pack(side='left', padx=(0, 10))
        
        self.chat_btn = tk.Button(
            button_frame,
            text="Test Chat Window",
            command=self.test_chat_window,
            font=('Segoe UI', 10),
            relief='flat',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        self.chat_btn.pack(side='left', padx=(0, 10))
        
        self.speech_btn = tk.Button(
            button_frame,
            text="Test Speech Bubble",
            command=self.test_speech_bubble,
            font=('Segoe UI', 10),
            relief='flat',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        self.speech_btn.pack(side='left')
        
        # Theme info panel
        info_frame = tk.LabelFrame(self.main_frame, text="Theme Information", font=('Segoe UI', 12, 'bold'))
        info_frame.pack(fill='x', pady=(0, 20))
        
        self.theme_info_text = tk.Text(
            info_frame,
            height=8,
            font=('Consolas', 9),
            wrap='word'
        )
        self.theme_info_text.pack(fill='x', padx=10, pady=10)
        
        # Sample content area
        content_frame = tk.LabelFrame(self.main_frame, text="Sample Content", font=('Segoe UI', 12, 'bold'))
        content_frame.pack(fill='both', expand=True)
        
        # Sample text area
        self.sample_text = tk.Text(
            content_frame,
            font=('Segoe UI', 11),
            wrap='word'
        )
        self.sample_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add sample content
        sample_content = """🎨 Dark Mode Test Content

This text area demonstrates how the dark mode affects different UI elements:

• Background colors adapt automatically
• Text colors provide proper contrast  
• Button styles update with theme
• Context menus use theme colors
• Speech bubbles match the theme
• Chat windows are fully themed

🌟 Features Testing:
✅ Theme toggle functionality
✅ Color scheme switching
✅ Component theme awareness
✅ Persistent settings
✅ Real-time updates

🔧 Technical Details:
The theme system uses a centralized StyleManager that:
- Loads theme preferences from config
- Provides color access methods
- Handles theme change callbacks
- Saves preferences automatically

Try toggling dark mode and testing all the components!"""\n        \n        self.sample_text.insert('1.0', sample_content)\n        \n        # Status bar\n        self.status_bar = tk.Label(\n            self.root,\n            text=\"Ready - Toggle dark mode to test all components\",\n            font=('Segoe UI', 9),\n            relief='sunken',\n            bd=1\n        )\n        self.status_bar.pack(side='bottom', fill='x')\n    \n    def apply_theme(self):\n        \"\"\"Apply current theme to all components\"\"\"\n        # Get theme colors\n        bg_color = self.theme.get_color(\"background\")\n        surface_color = self.theme.get_color(\"surface\")\n        text_color = self.theme.get_color(\"text_primary\")\n        primary_color = self.theme.get_color(\"primary\")\n        secondary_color = self.theme.get_color(\"secondary\")\n        border_color = self.theme.get_color(\"border\")\n        \n        # Apply to main elements\n        self.root.configure(bg=bg_color)\n        self.main_frame.configure(bg=bg_color)\n        self.title_label.configure(bg=bg_color, fg=text_color)\n        \n        # Apply to buttons\n        self.context_menu_btn.configure(\n            bg=primary_color,\n            fg='white',\n            activebackground=self.theme.get_color(\"primary_hover\")\n        )\n        \n        self.chat_btn.configure(\n            bg=secondary_color,\n            fg='white',\n            activebackground=self.theme.get_color(\"secondary_hover\")\n        )\n        \n        self.speech_btn.configure(\n            bg=self.theme.get_color(\"accent\"),\n            fg='white',\n            activebackground=self.theme.get_color(\"accent_hover\")\n        )\n        \n        # Apply to text areas\n        self.theme_info_text.configure(\n            bg=surface_color,\n            fg=text_color,\n            insertbackground=primary_color\n        )\n        \n        self.sample_text.configure(\n            bg=surface_color,\n            fg=text_color,\n            insertbackground=primary_color\n        )\n        \n        # Apply to status bar\n        self.status_bar.configure(bg=bg_color, fg=text_color)\n        \n        # Update theme info\n        self.update_theme_info()\n        \n        # Update all child frames\n        self._update_frame_colors(self.main_frame, bg_color)\n        \n        print(f\"Applied {'dark' if self.theme.is_dark_theme() else 'light'} theme\")\n    \n    def _update_frame_colors(self, frame, bg_color):\n        \"\"\"Recursively update frame colors\"\"\"\n        for child in frame.winfo_children():\n            if isinstance(child, tk.Frame) or isinstance(child, tk.LabelFrame):\n                try:\n                    child.configure(bg=bg_color)\n                    if isinstance(child, tk.LabelFrame):\n                        child.configure(fg=self.theme.get_color(\"text_primary\"))\n                    self._update_frame_colors(child, bg_color)\n                except tk.TclError:\n                    pass\n    \n    def update_theme_info(self):\n        \"\"\"Update theme information display\"\"\"\n        self.theme_info_text.delete('1.0', 'end')\n        \n        theme_mode = \"Dark Mode\" if self.theme.is_dark_theme() else \"Light Mode\"\n        info = f\"\"\"Current Theme: {theme_mode}\n\nColor Palette:\n• Primary: {self.theme.get_color('primary')}\n• Secondary: {self.theme.get_color('secondary')}\n• Background: {self.theme.get_color('background')}\n• Surface: {self.theme.get_color('surface')}\n• Text: {self.theme.get_color('text_primary')}\n• Border: {self.theme.get_color('border')}\n\nTheme Features:\n• Automatic color adaptation\n• Component callback system\n• Persistent preferences\n• Real-time switching\"\"\"\n        \n        self.theme_info_text.insert('1.0', info)\n    \n    def on_dark_mode_toggle(self, is_dark):\n        \"\"\"Handle dark mode toggle\"\"\"\n        status = \"Dark mode enabled\" if is_dark else \"Light mode enabled\"\n        self.status_bar.configure(text=status)\n        print(f\"Theme toggled: {status}\")\n    \n    def on_theme_change(self, new_theme):\n        \"\"\"Handle theme change callback\"\"\"\n        self.theme = new_theme\n        self.apply_theme()\n        \n        status = f\"Theme changed to {'Dark' if new_theme.is_dark_theme() else 'Light'} mode\"\n        self.status_bar.configure(text=status)\n    \n    def test_context_menu(self):\n        \"\"\"Test the context menu with current theme\"\"\"\n        try:\n            menu_options = [\n                (\"🌙 Sample Menu Item 1\", lambda: print(\"Menu item 1 clicked\")),\n                (\"⭐ Sample Menu Item 2\", lambda: print(\"Menu item 2 clicked\")),\n                \"---\",\n                (\"🎨 Toggle Theme Demo\", lambda: self.style_manager.toggle_dark_mode()),\n                (\"📝 Another Item\", lambda: print(\"Another item clicked\")),\n                \"---\",\n                (\"❌ Close Menu\", lambda: print(\"Menu closed\"))\n            ]\n            \n            context_menu = ModernContextMenu(self.root)\n            \n            # Show menu at button position\n            x = self.root.winfo_rootx() + 100\n            y = self.root.winfo_rooty() + 150\n            context_menu.show(x, y, menu_options)\n            \n            self.status_bar.configure(text=\"Context menu opened - Check theme colors!\")\n            \n        except Exception as e:\n            print(f\"Error testing context menu: {e}\")\n            self.status_bar.configure(text=f\"Context menu error: {e}\")\n    \n    def test_chat_window(self):\n        \"\"\"Test the chat window with current theme\"\"\"\n        try:\n            chat = ModernChatWindow(self.root, \"Dark Mode Test Chat 💬\")\n            \n            # Add sample messages\n            chat.add_message(\"System\", \"Welcome to the dark mode test chat!\")\n            chat.add_message(\"User\", \"This chat window should use the current theme colors.\")\n            chat.add_message(\"Pixie\", \"Hi! I'm testing the dark mode functionality. Try toggling the theme in the main window!\")\n            chat.add_message(\"System\", f\"Current theme: {'Dark' if self.theme.is_dark_theme() else 'Light'} mode\")\n            \n            self.status_bar.configure(text=\"Chat window opened with theme colors\")\n            \n        except Exception as e:\n            print(f\"Error testing chat window: {e}\")\n            self.status_bar.configure(text=f\"Chat window error: {e}\")\n    \n    def test_speech_bubble(self):\n        \"\"\"Test the speech bubble with current theme\"\"\"\n        try:\n            bubble = ModernSpeechBubble(self.root, (200, 100))\n            \n            theme_name = \"dark\" if self.theme.is_dark_theme() else \"light\"\n            message = f\"🌟 This speech bubble is using the {theme_name} theme! The colors should match the current theme settings.\"\n            \n            bubble.show_message(message, duration=5000)\n            \n            self.status_bar.configure(text=\"Speech bubble displayed with theme colors\")\n            \n        except Exception as e:\n            print(f\"Error testing speech bubble: {e}\")\n            self.status_bar.configure(text=f\"Speech bubble error: {e}\")\n    \n    def run(self):\n        \"\"\"Run the comprehensive test\"\"\"\n        print(\"🌙 Starting Comprehensive Dark Mode Test...\")\n        print(f\"Initial theme: {'Dark' if self.theme.is_dark_theme() else 'Light'}\")\n        print(\"\\nInstructions:\")\n        print(\"1. Toggle dark mode using the switch\")\n        print(\"2. Test each component with both themes\")\n        print(\"3. Verify colors update properly\")\n        print(\"4. Check that settings persist\")\n        print(\"\\nComponents to test:\")\n        print(\"✓ Dark mode toggle switch\")\n        print(\"✓ Context menu (right-click simulation)\")\n        print(\"✓ Chat window with themed messages\")\n        print(\"✓ Speech bubble with theme colors\")\n        print(\"✓ Text areas and buttons\")\n        \n        self.status_bar.configure(text=\"Comprehensive dark mode test ready!\")\n        self.root.mainloop()\n\nif __name__ == \"__main__\":\n    try:\n        test = ComprehensiveDarkModeTest()\n        test.run()\n    except Exception as e:\n        print(f\"Test failed: {e}\")\n        import traceback\n        traceback.print_exc()