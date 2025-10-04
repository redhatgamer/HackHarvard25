#!/usr/bin/env python3
"""
Modern UI Demo Script
Test all the new modern UI components and features
"""

import sys
import os
import asyncio
import tkinter as tk
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.ui.modern_components import ModernPetWidget, ModernChatWindow, ModernContextMenu
    from src.ui.theme_manager import get_theme, get_style_manager
    from src.ui.pet_animations import PetAnimator, ParticleSystem, VisualEffects
    print("✅ Modern UI components imported successfully")
except ImportError as e:
    print(f"❌ Failed to import modern UI components: {e}")
    sys.exit(1)

class ModernUIDemo:
    """Demo application for modern UI features"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window
        
        # Initialize theme
        self.style_manager = get_style_manager()
        self.theme = self.style_manager.get_theme()
        
        # Apply global styles
        self.style_manager.apply_global_styles(self.root)
        
        # Demo components
        self.pet_window = None
        self.chat_window = None
        
        print("🎨 Modern UI Demo initialized")
    
    def create_demo_pet(self):
        """Create demo pet window with modern styling"""
        self.pet_window = tk.Toplevel(self.root)
        self.pet_window.title("Modern Pixie Demo")
        self.pet_window.geometry("140x140")
        
        # Modern window styling
        self.pet_window.wm_attributes("-topmost", True)
        self.pet_window.wm_attributes("-alpha", 0.95)
        self.pet_window.overrideredirect(True)
        self.pet_window.configure(bg='#000001')
        
        # Position in center of screen
        screen_width = self.pet_window.winfo_screenwidth()
        screen_height = self.pet_window.winfo_screenheight()
        x = (screen_width // 2) - 70
        y = (screen_height // 2) - 70
        self.pet_window.geometry(f"+{x}+{y}")
        
        # Create modern pet widget
        self.pet_widget = ModernPetWidget(
            self.pet_window,
            size=(140, 140),
            pet_config={"name": "Demo Pixie"}
        )
        
        # Bind events
        self.pet_widget.canvas.bind("<Button-1>", self.on_pet_click)
        self.pet_widget.canvas.bind("<Button-3>", self.on_pet_right_click)
        self.pet_widget.canvas.bind("<B1-Motion>", self.on_pet_drag)
        
        print("🐱 Modern pet window created")
        return self.pet_window
    
    def on_pet_click(self, event):
        """Handle pet click - open chat"""
        print("👆 Pet clicked - opening modern chat")
        self.create_demo_chat()
        
        # Show activity indicator
        self.pet_widget.show_activity(True)
        
        # Hide activity after 2 seconds
        self.pet_window.after(2000, lambda: self.pet_widget.show_activity(False))
    
    def on_pet_right_click(self, event):
        """Handle right click - show modern context menu"""
        print("👆 Pet right-clicked - showing context menu")
        
        menu_options = [
            ("💬 Open Chat", self.create_demo_chat),
            ("🎨 Change Color", self.change_pet_color),
            ("🎭 Show Emotion", self.demo_emotions),
            "---",  # Separator
            ("📸 Demo Effects", self.demo_effects),
            ("⚙️ Settings", lambda: print("Settings clicked")),
            ("❌ Close", self.close_demo)
        ]
        
        modern_menu = ModernContextMenu(self.pet_window)
        modern_menu.show(event.x_root, event.y_root, menu_options)
    
    def on_pet_drag(self, event):
        """Handle pet dragging"""
        x = self.pet_window.winfo_pointerx() - 70
        y = self.pet_window.winfo_pointery() - 70
        self.pet_window.geometry(f"+{x}+{y}")
    
    def create_demo_chat(self):
        """Create demo chat window"""
        if hasattr(self, 'chat_demo') and self.chat_demo.window.winfo_exists():
            self.chat_demo.window.lift()
            return
        
        self.chat_demo = ModernChatWindow(self.root, "Modern UI Demo Chat 🚀")
        
        # Add some demo messages
        self.chat_demo.add_message("Pixie", "Welcome to the Modern UI Demo! ✨")
        self.chat_demo.add_message("You", "Wow, this looks amazing!")
        self.chat_demo.add_message("Pixie", "I've got a fresh new look with smooth animations, better colors, and lots of visual effects! 🎨")
        self.chat_demo.add_message("Pixie", "Try right-clicking on me to see the modern context menu, or just drag me around the screen!")
        
        print("💬 Modern chat window created")
    
    def change_pet_color(self):
        """Demo color changing"""
        print("🎨 Changing pet colors")
        # This would change the pet's color scheme
        
    def demo_emotions(self):
        """Demo different emotions"""
        print("🎭 Demonstrating emotions")
        emotions = ["happy", "excited", "thinking", "sleepy"]
        
        def cycle_emotion(index=0):
            if index < len(emotions):
                emotion = emotions[index]
                print(f"   Showing emotion: {emotion}")
                # This would change the pet's expression
                self.pet_window.after(1500, lambda: cycle_emotion(index + 1))
        
        cycle_emotion()
    
    def demo_effects(self):
        """Demo visual effects"""
        print("✨ Demonstrating visual effects")
        
        # Pulse effect
        canvas = self.pet_widget.canvas
        center_x, center_y = 70, 70
        
        # Create ripple effect
        VisualEffects.create_ripple_effect(canvas, center_x, center_y, 60)
        
        # Add some particle bursts
        def create_burst():
            from src.ui.pet_animations import ParticleSystem
            particles = ParticleSystem(canvas)
            particles.emit_burst(center_x, center_y, 15)
            
            # Update particles for a few frames
            def update_particles(count=0):
                if count < 60:  # 3 seconds at 20 FPS
                    particles.update()
                    canvas.after(50, lambda: update_particles(count + 1))
            
            update_particles()
        
        self.pet_window.after(500, create_burst)
    
    def close_demo(self):
        """Close the demo"""
        print("👋 Closing Modern UI Demo")
        self.root.quit()
    
    def run_demo(self):
        """Run the demo"""
        print("🚀 Starting Modern UI Demo")
        print("=" * 40)
        print("Features to test:")
        print("- 🐱 Modern animated pet widget")
        print("- 💬 Glassmorphism chat interface") 
        print("- 🎨 Modern color schemes and fonts")
        print("- ✨ Particle effects and animations")
        print("- 📱 Context menus with hover effects")
        print("- 🎭 Emotional expressions")
        print("=" * 40)
        print()
        
        # Create pet window
        self.create_demo_pet()
        
        # Start the UI loop
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted by user")

def main():
    """Main demo function"""
    print("🎨 Modern UI Demo for Pixie")
    print("Testing new modern interface components")
    print()
    
    # Check dependencies
    try:
        import PIL
        import tkinter
        print("✅ Basic dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return 1
    
    # Run demo
    demo = ModernUIDemo()
    demo.run_demo()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())