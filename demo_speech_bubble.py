"""
Demo of the new speech bubble functionality
Shows h    # Add instructions label
    instruction_frame = tk.Frame(root, bg='lightblue')
    instruction_frame.pack(pady=10)
    
    tk.Label(instruction_frame, text="🖱️ Click pet for speech bubbles!", 
             bg='lightblue', font=("Arial", 10)).pack()
    tk.Label(instruction_frame, text="💫 Drag window to see bubble follow!", 
             bg='lightblue', font=("Arial", 9), fg='darkblue').pack()
    tk.Label(instruction_frame, text="Speech bubbles now move with pet! 💭", 
             bg='lightblue', font=("Arial", 9), fg='gray').pack()et now speaks in bubbles instead of opening a chat window
"""

import tkinter as tk
from src.ui.modern_components import ModernSpeechBubble

def create_demo():
    """Create a demo of speech bubbles"""
    
    # Create main window
    root = tk.Tk()
    root.title("Speech Bubble Demo")
    root.geometry("200x200+100+100")
    root.configure(bg='lightblue')
    
    # Create a fake pet (just a circle)
    canvas = tk.Canvas(root, width=200, height=200, bg='lightblue')
    canvas.pack()
    
    # Draw a simple pet
    canvas.create_oval(75, 75, 125, 125, fill='pink', outline='purple', width=3)
    canvas.create_oval(85, 85, 95, 95, fill='black')  # Left eye
    canvas.create_oval(105, 85, 115, 95, fill='black')  # Right eye
    canvas.create_arc(85, 105, 115, 120, start=0, extent=180, style='arc', outline='red', width=2)  # Mouth
    
    # Add instructions
    canvas.create_text(100, 30, text="Click the pet!", font=("Arial", 12), fill='darkblue')
    
    # Create speech bubble system
    speech_bubble = ModernSpeechBubble(root, pet_size=(50, 50))
    
    messages = [
        "Hello! I'm your AI pet! 🐱",
        "Click me to see me talk! 💬",
        "I can show messages instead of opening windows! ✨",
        "Much more natural, don't you think? 😊",
        "Double-click for analysis! 🔍",
        "Right-click for options! 📋",
        "I love chatting this way! 💕"
    ]
    
    message_index = 0
    
    def show_message():
        nonlocal message_index
        message = messages[message_index]
        message_index = (message_index + 1) % len(messages)
        speech_bubble.show_message(message, duration=4000, typing_effect=True)
    
    # Bind click to show speech bubble
    canvas.bind("<Button-1>", lambda e: show_message())
    
    # Auto-show first message
    root.after(1000, show_message)
    
    # Instructions label
    instruction_frame = tk.Frame(root, bg='lightblue')
    instruction_frame.pack(pady=10)
    
    tk.Label(instruction_frame, text="🖱️ Click the pet to see speech bubbles!", 
             bg='lightblue', font=("Arial", 10)).pack()
    tk.Label(instruction_frame, text="This is how the pet talks now! 💭", 
             bg='lightblue', font=("Arial", 9), fg='gray').pack()
    
    return root

if __name__ == "__main__":
    try:
        demo = create_demo()
        demo.mainloop()
    except Exception as e:
        print(f"Error running demo: {e}")
        import traceback
        traceback.print_exc()