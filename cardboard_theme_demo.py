"""
Cardboard Theme Demo
A simple script to demonstrate the cardboard theme functionality
"""

import tkinter as tk
from src.ui.modern_components import CardboardContextMenu, ModernContextMenu

def demo_cardboard_theme():
    """Demo the cardboard theme vs modern theme"""
    
    root = tk.Tk()
    root.title("Cardboard vs Modern Theme Demo")
    root.geometry("400x300")
    root.configure(bg='#F5F5DC')  # Beige background
    
    # Instructions
    instruction_label = tk.Label(
        root,
        text="Click the buttons to see different theme menus:",
        font=('Arial', 12, 'bold'),
        bg='#F5F5DC',
        fg='#8B4513'
    )
    instruction_label.pack(pady=20)
    
    # Cardboard theme button
    def show_cardboard_menu():
        if CardboardContextMenu:
            menu_options = [
                ("🛠️ Code Tools", lambda: print("Code Tools clicked")),
                ("📊 Google Sheets", lambda: print("Sheets clicked")),
                ("🎭 Pet Options", lambda: print("Pet options clicked")),
                "---",
                ("⚙️ Settings", lambda: print("Settings clicked")),
                ("❌ Exit", lambda: root.quit())
            ]
            
            cardboard_menu = CardboardContextMenu(root)
            cardboard_menu.show(200, 150, menu_options)
    
    cardboard_btn = tk.Button(
        root,
        text="🧳 Show Cardboard Menu",
        font=('Courier New', 11, 'bold'),
        bg='#D2B48C',
        fg='#8B4513',
        relief='raised',
        bd=3,
        padx=20,
        pady=8,
        cursor='hand2',
        command=show_cardboard_menu
    )
    cardboard_btn.pack(pady=10)
    
    # Modern theme button  
    def show_modern_menu():
        if ModernContextMenu:
            menu_options = [
                ("🛠️ Code Tools", lambda: print("Code Tools clicked")),
                ("📊 Google Sheets", lambda: print("Sheets clicked")),
                ("🎭 Pet Options", lambda: print("Pet options clicked")),
                "---",
                ("⚙️ Settings", lambda: print("Settings clicked")),
                ("❌ Exit", lambda: root.quit())
            ]
            
            modern_menu = ModernContextMenu(root)
            modern_menu.show(200, 200, menu_options)
    
    modern_btn = tk.Button(
        root,
        text="✨ Show Modern Menu",
        font=('Segoe UI', 11),
        bg='#2D2D2D',
        fg='white',
        relief='flat',
        bd=0,
        padx=20,
        pady=8,
        cursor='hand2',
        command=show_modern_menu
    )
    modern_btn.pack(pady=10)
    
    # Theme comparison info
    info_text = """
Cardboard Theme Features:
• Brown/tan color palette  
• Rustic typewriter font
• Raised borders & texture effects
• Subtle entrance animation with wobble
• Weathered, handcrafted appearance

Modern Theme Features:
• Dark/light adaptive colors
• Clean sans-serif font
• Smooth gradients & shadows
• Elegant fade transitions
• Contemporary, professional look
    """
    
    info_label = tk.Label(
        root,
        text=info_text.strip(),
        font=('Arial', 9),
        bg='#F5F5DC',
        fg='#654321',
        justify='left'
    )
    info_label.pack(pady=15)
    
    root.mainloop()

if __name__ == "__main__":
    demo_cardboard_theme()