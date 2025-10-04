#!/usr/bin/env python3
"""
Simple Dark Mode Test
"""

import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

import tkinter as tk
from ui.theme_manager import get_style_manager
from ui.modern_components import ModernContextMenu

def test_dark_mode():
    print("Testing dark mode functionality...")
    
    # Create root window
    root = tk.Tk()
    root.title("Dark Mode Test")
    root.geometry("500x400")
    
    # Get theme manager
    sm = get_style_manager()
    theme = sm.get_theme()
    
    # Show current theme info
    is_dark = theme.is_dark_theme()
    print(f"Current mode: {'Dark' if is_dark else 'Light'}")
    print(f"Background color: {theme.get_color('background')}")
    print(f"Text color: {theme.get_color('text_primary')}")
    print(f"Surface color: {theme.get_color('surface')}")
    
    # Apply theme to window
    bg_color = theme.get_color("background")
    text_color = theme.get_color("text_primary")
    surface_color = theme.get_color("surface")
    primary_color = theme.get_color("primary")
    
    root.configure(bg=bg_color)
    
    # Create UI elements
    title = tk.Label(
        root,
        text=f"🌙 Dark Mode Test - {'Dark' if is_dark else 'Light'} Theme",
        font=('Arial', 16, 'bold'),
        bg=bg_color,
        fg=text_color
    )
    title.pack(pady=30)
    
    # Info text
    info = tk.Text(
        root,
        height=10,
        bg=surface_color,
        fg=text_color,
        font=('Arial', 11),
        insertbackground=primary_color
    )
    info.pack(padx=30, pady=20, fill='both', expand=True)
    
    info_text = f"""Dark Mode Status: {'ENABLED' if is_dark else 'DISABLED'}

Color Palette:
• Background: {bg_color}
• Surface: {surface_color}  
• Text: {text_color}
• Primary: {primary_color}

The desktop pet's context menu and all UI components should now use these colors.

To toggle dark mode:
1. Right-click on the desktop pet
2. Select "🌙 Switch to Dark Mode" (or "☀️ Switch to Light Mode")
3. All UI elements will update automatically
"""
    
    info.insert('1.0', info_text)
    info.configure(state='disabled')
    
    # Toggle button
    def toggle_theme():
        sm.toggle_dark_mode()
        new_theme = sm.get_theme()
        is_dark_new = new_theme.is_dark_theme()
        print(f"Toggled to: {'Dark' if is_dark_new else 'Light'} mode")
        root.destroy()
        test_dark_mode()  # Restart with new theme
    
    toggle_btn = tk.Button(
        root,
        text="Toggle Dark Mode",
        command=toggle_theme,
        font=('Arial', 12),
        bg=primary_color,
        fg='white',
        relief='flat',
        padx=20,
        pady=10
    )
    toggle_btn.pack(pady=20)
    
    # Test context menu
    def test_context_menu(event):
        try:
            menu_options = [
                ("🌙 This is dark mode!", lambda: print("Dark mode item clicked")),
                ("⭐ Sample Menu Item", lambda: print("Sample item clicked")),
                ("---",),
                ("🎨 Toggle Theme", toggle_theme),
                ("❌ Close", lambda: print("Close clicked"))
            ]
            
            context_menu = ModernContextMenu(root)
            context_menu.show(event.x_root, event.y_root, menu_options)
        except Exception as e:
            print(f"Context menu error: {e}")
    
    # Bind right-click
    root.bind("<Button-3>", test_context_menu)
    
    print("Window created with theme colors. Right-click to test context menu.")
    print("Click 'Toggle Dark Mode' button to switch themes.")
    
    # Auto-close after 10 seconds for automated testing
    root.after(10000, root.destroy)
    
    root.mainloop()

if __name__ == "__main__":
    test_dark_mode()