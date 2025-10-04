"""
Modern UI components for the Virtual Pet AI Assistant
Provides sleek, contemporary interface elements with animations and styling
"""

import tkinter as tk
from tkinter import ttk
import math
import threading
import time
from typing import Callable, Optional, Dict, Any
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import asyncio

class ModernPetWidget:
    """Modern, animated pet widget with glassmorphism effects"""
    
    def __init__(self, parent, size: tuple = (120, 120), pet_config: Dict[str, Any] = None):
        self.parent = parent
        self.size = size
        self.config = pet_config or {}
        
        # Animation state
        self.animation_frame = 0
        self.is_animating = False
        self.animation_timer = None
        self.hover_scale = 1.0
        self.target_scale = 1.0
        
        # Image handling for custom pet images
        self.pet_image = None
        self.pet_photo = None
        self.use_custom_image = False
        
        # Resizing functionality
        self.min_size = 50
        self.max_size = 500
        self.resize_step = 10
        self.current_width = size[0]
        self.current_height = size[1]
        
        # Create the widget
        self._setup_widget()
        self._create_pet_graphics()
        self._start_idle_animation()
    
    def _setup_widget(self):
        """Setup the modern pet widget with transparency and effects"""
        self.canvas = tk.Canvas(
            self.parent,
            width=self.size[0],
            height=self.size[1],
            highlightthickness=0,
            bg='#000001',  # Almost black for transparency
            bd=0
        )
        
        # Enable transparency
        self.parent.wm_attributes('-transparentcolor', '#000001')
        
        # Add subtle glow effect
        self.canvas.configure(relief='flat')
        self.canvas.pack()
        
        # Bind events
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<Enter>", self._on_hover_enter)
        self.canvas.bind("<Leave>", self._on_hover_leave)
        
        # Bind resizing events
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind("<Button-4>", self._on_mouse_wheel)  # Linux scroll up
        self.canvas.bind("<Button-5>", self._on_mouse_wheel)  # Linux scroll down
        
        # Make canvas focusable for keyboard events
        self.canvas.focus_set()
        self.canvas.bind("<KeyPress>", self._on_key_press)
        
    def _create_pet_graphics(self):
        """Create modern pet graphics with gradients and effects"""
        # Clear canvas
        self.canvas.delete("all")
        
        # Calculate center and scale
        center_x, center_y = self.size[0] // 2, self.size[1] // 2
        base_radius = min(self.size) // 3
        radius = int(base_radius * self.hover_scale)
        
        # Try to load custom image first (like Hirono)
        if self._try_load_custom_image():
            self._draw_custom_image(center_x, center_y)
            return
        
        # Create gradient background (outer glow)
        glow_radius = radius + 15
        glow_color = "#FF69B4"
        for i in range(10):
            alpha = 0.1 - (i * 0.01)
            current_radius = glow_radius + i * 2
            self.canvas.create_oval(
                center_x - current_radius, center_y - current_radius,
                center_x + current_radius, center_y + current_radius,
                fill=glow_color, outline="", stipple="gray25"
            )
        
        # Main body with gradient effect
        self._draw_gradient_circle(center_x, center_y, radius)
        
        # Eyes with animation
        self._draw_animated_eyes(center_x, center_y, radius)
        
        # Nose
        nose_y = center_y + radius * 0.1
        self.canvas.create_polygon(
            center_x - 3, nose_y + 5,
            center_x + 3, nose_y + 5,
            center_x, nose_y - 2,
            fill='#FF1493', outline='#C71585', width=1
        )
        
        # Mouth with subtle animation
        self._draw_animated_mouth(center_x, center_y, radius)
        
        # Add floating particles for magic effect
        self._add_particle_effects(center_x, center_y, radius)
    
    def _try_load_custom_image(self):
        """Try to load custom pet image (like Hirono)"""
        try:
            import os
            from pathlib import Path
            
            # Check multiple possible image paths
            possible_paths = [
                "assets/pet/hirono.png",
                "assets/pet/hirono.jpg", 
                "assets/pet/hirono.jpeg",
                "assets/pet/hirono.gif",
                "assets/pet/pet.png",
                "assets/pet/pet.jpg",
                "assets/pet/custom.png",
                "hirono.png",  # In root directory
                "pet.png"      # In root directory
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    self.pet_image = Image.open(path)
                    # Resize to fit current canvas size while maintaining aspect ratio
                    image_size = int(min(self.current_width, self.current_height) * 0.85 * self.hover_scale)
                    self.pet_image = self.pet_image.resize(
                        (image_size, image_size), 
                        Image.Resampling.LANCZOS
                    )
                    self.pet_photo = ImageTk.PhotoImage(self.pet_image)
                    self.use_custom_image = True
                    return True
            
            return False
            
        except Exception as e:
            print(f"Could not load custom pet image: {e}")
            return False
    
    def _draw_custom_image(self, center_x, center_y):
        """Draw the custom pet image (like Hirono)"""
        if self.pet_photo:
            # Add subtle glow effect around custom image (optional, can be disabled)
            glow_enabled = self.config.get('glow_effect', True)
            
            if glow_enabled:
                glow_radius = 20
                glow_colors = ["#FFE4E6", "#FFB6C1", "#FFC0CB", "#FFCCCB", "#FFD6D6"]  # Gradual pink glow
                
                for i, color in enumerate(glow_colors):
                    current_radius = glow_radius + i * 3
                    self.canvas.create_oval(
                        center_x - current_radius, center_y - current_radius,
                        center_x + current_radius, center_y + current_radius,
                        fill=color, outline=""
                    )
            
            # Draw the custom image
            self.canvas.create_image(
                center_x, center_y,
                image=self.pet_photo,
                anchor="center"
            )
            
            # Add subtle particle effects if enabled
            particles_enabled = self.config.get('particle_effects', True)
            if particles_enabled:
                self._add_particle_effects(center_x, center_y, 30)
    
    def _on_mouse_wheel(self, event):
        """Handle mouse wheel for resizing"""
        try:
            # Determine scroll direction
            if event.delta > 0 or event.num == 4:  # Scroll up = bigger
                self._resize_pet(self.resize_step)
            elif event.delta < 0 or event.num == 5:  # Scroll down = smaller
                self._resize_pet(-self.resize_step)
        except AttributeError:
            # Handle different event formats
            pass
    
    def _on_key_press(self, event):
        """Handle keyboard shortcuts for resizing"""
        if event.keysym == 'plus' or event.keysym == 'equal':  # + key
            self._resize_pet(self.resize_step)
        elif event.keysym == 'minus':  # - key
            self._resize_pet(-self.resize_step)
        elif event.keysym == '0':  # Reset to default size
            self._reset_size()
    
    def _resize_pet(self, size_change):
        """Resize the pet by the given amount"""
        new_width = max(self.min_size, min(self.max_size, self.current_width + size_change))
        new_height = max(self.min_size, min(self.max_size, self.current_height + size_change))
        
        if new_width != self.current_width or new_height != self.current_height:
            self.current_width = new_width
            self.current_height = new_height
            self.size = (self.current_width, self.current_height)
            
            # Resize the canvas
            self.canvas.configure(width=self.current_width, height=self.current_height)
            
            # Resize the parent window
            self.parent.geometry(f"{self.current_width}x{self.current_height}")
            
            # Recreate graphics with new size
            self._create_pet_graphics()
            
            # Save new size to config
            self._save_size_to_config()
    
    def _reset_size(self):
        """Reset to default size (120x120)"""
        default_size = 120
        self.current_width = default_size
        self.current_height = default_size
        self.size = (default_size, default_size)
        
        self.canvas.configure(width=default_size, height=default_size)
        self.parent.geometry(f"{default_size}x{default_size}")
        
        self._create_pet_graphics()
        self._save_size_to_config()
    
    def _save_size_to_config(self):
        """Save the current size to configuration"""
        try:
            # Update config in memory (parent widget should handle file saving)
            if hasattr(self, 'config') and self.config:
                self.config['width'] = self.current_width
                self.config['height'] = self.current_height
                
            print(f"Pet resized to: {self.current_width}x{self.current_height}")
        except Exception as e:
            print(f"Could not save size to config: {e}")
        
    def _draw_gradient_circle(self, cx: int, cy: int, radius: int):
        """Draw a gradient circle for the pet body"""
        # Create multiple overlapping circles for gradient effect
        colors = ['#FFB6C1', '#FFE4E6', '#FFF0F5', '#FFB6C1']
        
        for i, color in enumerate(colors):
            current_radius = radius - i * 5
            if current_radius > 0:
                self.canvas.create_oval(
                    cx - current_radius, cy - current_radius,
                    cx + current_radius, cy + current_radius,
                    fill=color, outline=""
                )
        
        # Add highlight
        highlight_radius = radius - 15
        self.canvas.create_oval(
            cx - highlight_radius, cy - highlight_radius - 5,
            cx + 10, cy - 5,
            fill='#FFFFFF', outline="", stipple="gray50"
        )
    
    def _draw_animated_eyes(self, cx: int, cy: int, radius: int):
        """Draw animated eyes that blink and look around"""
        # Calculate eye positions
        eye_offset_x = radius * 0.3
        eye_offset_y = radius * 0.2
        eye_size = 8
        
        left_eye_x = cx - eye_offset_x
        right_eye_x = cx + eye_offset_x
        eye_y = cy - eye_offset_y
        
        # Blinking animation
        blink_phase = (self.animation_frame // 60) % 120  # Blink every 2 seconds
        is_blinking = 110 <= blink_phase <= 120
        
        if is_blinking:
            # Closed eyes (lines)
            self.canvas.create_line(
                left_eye_x - eye_size//2, eye_y,
                left_eye_x + eye_size//2, eye_y,
                width=3, fill='#333'
            )
            self.canvas.create_line(
                right_eye_x - eye_size//2, eye_y,
                right_eye_x + eye_size//2, eye_y,
                width=3, fill='#333'
            )
        else:
            # Open eyes with pupils that move slightly
            pupil_offset = math.sin(self.animation_frame * 0.02) * 2
            
            # Eye whites
            self.canvas.create_oval(
                left_eye_x - eye_size, eye_y - eye_size//2,
                left_eye_x + eye_size, eye_y + eye_size//2,
                fill='white', outline='#ccc', width=1
            )
            self.canvas.create_oval(
                right_eye_x - eye_size, eye_y - eye_size//2,
                right_eye_x + eye_size, eye_y + eye_size//2,
                fill='white', outline='#ccc', width=1
            )
            
            # Pupils
            pupil_size = eye_size // 2
            self.canvas.create_oval(
                left_eye_x - pupil_size + pupil_offset, eye_y - pupil_size//2,
                left_eye_x + pupil_size + pupil_offset, eye_y + pupil_size//2,
                fill='#1a1a1a'
            )
            self.canvas.create_oval(
                right_eye_x - pupil_size + pupil_offset, eye_y - pupil_size//2,
                right_eye_x + pupil_size + pupil_offset, eye_y + pupil_size//2,
                fill='#1a1a1a'
            )
            
            # Eye sparkles
            sparkle_size = 2
            self.canvas.create_oval(
                left_eye_x - sparkle_size + pupil_offset, eye_y - sparkle_size,
                left_eye_x + sparkle_size + pupil_offset, eye_y + sparkle_size,
                fill='white'
            )
            self.canvas.create_oval(
                right_eye_x - sparkle_size + pupil_offset, eye_y - sparkle_size,
                right_eye_x + sparkle_size + pupil_offset, eye_y + sparkle_size,
                fill='white'
            )
    
    def _draw_animated_mouth(self, cx: int, cy: int, radius: int):
        """Draw animated mouth that changes expressions"""
        mouth_y = cy + radius * 0.4
        mouth_width = 20
        
        # Expression changes over time
        expression_phase = (self.animation_frame // 180) % 3
        
        if expression_phase == 0:  # Happy
            self.canvas.create_arc(
                cx - mouth_width//2, mouth_y - 5,
                cx + mouth_width//2, mouth_y + 10,
                start=0, extent=180, style='arc',
                outline='#FF1493', width=3
            )
        elif expression_phase == 1:  # Neutral
            self.canvas.create_line(
                cx - mouth_width//3, mouth_y,
                cx + mouth_width//3, mouth_y,
                width=2, fill='#FF1493'
            )
        else:  # Curious
            self.canvas.create_oval(
                cx - 4, mouth_y - 4,
                cx + 4, mouth_y + 4,
                fill='#FF1493', outline='#C71585'
            )
    
    def _add_particle_effects(self, cx: int, cy: int, radius: int):
        """Add floating particle effects around the pet"""
        particles = []
        for i in range(3):
            angle = (self.animation_frame + i * 120) * 0.02
            distance = radius + 20 + math.sin(angle) * 10
            
            px = cx + math.cos(angle) * distance
            py = cy + math.sin(angle) * distance
            
            # Create sparkle particles
            size = 2 + math.sin(self.animation_frame * 0.05 + i) * 1
            alpha = 0.7 + math.sin(self.animation_frame * 0.03 + i) * 0.3
            
            self.canvas.create_oval(
                px - size, py - size,
                px + size, py + size,
                fill='#FFD700', outline='', stipple='gray25'
            )
    
    def _start_idle_animation(self):
        """Start the idle animation loop"""
        self.is_animating = True
        self._animate()
    
    def _animate(self):
        """Animation loop"""
        if not self.is_animating:
            return
            
        self.animation_frame += 1
        
        # Smooth scale animation for hover effect
        scale_speed = 0.1
        if abs(self.hover_scale - self.target_scale) > 0.01:
            if self.hover_scale < self.target_scale:
                self.hover_scale += scale_speed
            else:
                self.hover_scale -= scale_speed
        else:
            self.hover_scale = self.target_scale
        
        # Redraw the pet
        self._create_pet_graphics()
        
        # Schedule next frame
        self.animation_timer = self.parent.after(50, self._animate)  # 20 FPS
    
    def _on_click(self, event):
        """Handle click with animation"""
        # Scale animation on click
        self.target_scale = 0.9
        self.parent.after(100, lambda: setattr(self, 'target_scale', 1.1))
        self.parent.after(200, lambda: setattr(self, 'target_scale', 1.0))
        
        # Trigger click event
        if hasattr(self.parent, '_on_pet_click'):
            self.parent._on_pet_click(event)
    
    def _on_drag(self, event):
        """Handle dragging"""
        if hasattr(self.parent, '_on_pet_drag'):
            self.parent._on_pet_drag(event)
    
    def _on_hover_enter(self, event):
        """Handle mouse enter with hover effect"""
        self.target_scale = 1.1
    
    def _on_hover_leave(self, event):
        """Handle mouse leave"""
        self.target_scale = 1.0
    
    def show_activity(self, active: bool = True):
        """Show activity indicator (speech bubble, etc.)"""
        if active:
            # Add a modern speech bubble
            self.canvas.create_text(
                self.size[0] // 2, 15,
                text="💭", font=("Segoe UI Emoji", 16),
                fill='#4A90E2', tags="activity"
            )
        else:
            self.canvas.delete("activity")
    
    def stop_animation(self):
        """Stop all animations"""
        self.is_animating = False
        if self.animation_timer:
            self.parent.after_cancel(self.animation_timer)


class ModernSpeechBubble:
    """Modern speech bubble that appears next to the pet"""
    
    def __init__(self, parent, pet_size: tuple = (120, 120)):
        self.parent = parent
        self.pet_size = pet_size
        self.bubble_window = None
        self.current_message = ""
        self.auto_hide_timer = None
        self.typing_timer = None
        self.typed_text = ""
        self.typing_index = 0
        self.is_visible = False
        
        # Get theme for styling
        try:
            from src.ui.theme_manager import get_theme
            self.theme = get_theme()
        except ImportError:
            self.theme = None
        
        # Animation state
        self.fade_alpha = 0.0
        self.target_alpha = 0.0
        self.fade_timer = None
        
        # Position tracking
        self.position_timer = None
        self.last_pet_x = 0
        self.last_pet_y = 0
        self.is_tracking = False
        
    def show_message(self, message: str, duration: int = 5000, typing_effect: bool = True):
        """Show a speech bubble with the given message"""
        self.current_message = message
        self.is_visible = True
        
        # Create or update bubble window
        self._create_bubble_window()
        self._position_bubble()
        
        if typing_effect:
            self._start_typing_effect()
        else:
            self.typed_text = message
            self._update_bubble_content()
        
        # Show with fade-in animation
        self.target_alpha = 0.95
        self._start_fade_animation()
        
        # Start position tracking to follow the pet
        self._start_position_tracking()
        
        # Auto-hide after duration
        if self.auto_hide_timer:
            self.parent.after_cancel(self.auto_hide_timer)
        self.auto_hide_timer = self.parent.after(duration, self.hide)
    
    def hide(self):
        """Hide the speech bubble with fade-out animation"""
        if not self.is_visible:
            return
            
        # Stop position tracking
        self._stop_position_tracking()
            
        self.target_alpha = 0.0
        self._start_fade_animation()
        
        # Actually destroy after fade animation
        self.parent.after(300, self._destroy_bubble)
    
    def _create_bubble_window(self):
        """Create the speech bubble window"""
        if self.bubble_window:
            self.bubble_window.destroy()
        
        # Create toplevel window
        self.bubble_window = tk.Toplevel(self.parent)
        self.bubble_window.overrideredirect(True)  # Remove window decorations
        self.bubble_window.wm_attributes("-topmost", True)
        self.bubble_window.wm_attributes("-transparentcolor", "#000001")
        
        # Create canvas for drawing bubble
        self.canvas = tk.Canvas(
            self.bubble_window,
            width=300,
            height=120,
            highlightthickness=0,
            bg='#000001',
            bd=0
        )
        self.canvas.pack()
        
        # Draw bubble background
        self._draw_bubble_background()
    
    def _draw_bubble_background(self):
        """Draw the speech bubble background with modern styling"""
        # Bubble dimensions
        bubble_width = 280
        bubble_height = 80
        bubble_x = 10
        bubble_y = 10
        corner_radius = 15
        
        # Get theme colors for bubble
        surface_color = self.theme.get_color("surface") if self.theme else '#ffffff'
        border_color = self.theme.get_color("border") if self.theme else '#e1e5e9'
        text_color = self.theme.get_color("text_primary") if self.theme else '#2c3e50'
        shadow_color = '#404040' if (self.theme and self.theme.is_dark_theme()) else '#d0d0d0'
        
        # Create rounded rectangle for bubble
        self._create_rounded_rectangle(
            bubble_x, bubble_y, 
            bubble_x + bubble_width, bubble_y + bubble_height,
            corner_radius, fill=surface_color, outline=border_color, width=2
        )
        
        # Add subtle shadow effect
        shadow_offset = 2
        self._create_rounded_rectangle(
            bubble_x + shadow_offset, bubble_y + shadow_offset,
            bubble_x + bubble_width + shadow_offset, bubble_y + bubble_height + shadow_offset,
            corner_radius, fill=shadow_color, outline='', stipple='gray25'
        )
        
        # Draw pointer/tail pointing to pet
        tail_points = [
            bubble_x + 30, bubble_y + bubble_height,
            bubble_x + 20, bubble_y + bubble_height + 15,
            bubble_x + 45, bubble_y + bubble_height
        ]
        self.canvas.create_polygon(tail_points, fill=surface_color, outline=border_color, width=2)
        
        # Create text area
        self.text_id = self.canvas.create_text(
            bubble_x + bubble_width // 2, bubble_y + bubble_height // 2,
            text="", font=("Segoe UI", 10), fill=text_color,
            width=bubble_width - 20, justify='left', anchor='center'
        )
    
    def _create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        """Create a rounded rectangle on the canvas"""
        points = []
        
        # Top-left corner
        for i in range(90, 180, 10):
            x = x1 + radius - radius * math.cos(math.radians(i))
            y = y1 + radius - radius * math.sin(math.radians(i))
            points.extend([x, y])
        
        # Top-right corner
        for i in range(0, 90, 10):
            x = x2 - radius + radius * math.cos(math.radians(i))
            y = y1 + radius - radius * math.sin(math.radians(i))
            points.extend([x, y])
        
        # Bottom-right corner
        for i in range(270, 360, 10):
            x = x2 - radius + radius * math.cos(math.radians(i))
            y = y2 - radius + radius * math.sin(math.radians(i))
            points.extend([x, y])
        
        # Bottom-left corner
        for i in range(180, 270, 10):
            x = x1 + radius - radius * math.cos(math.radians(i))
            y = y2 - radius + radius * math.sin(math.radians(i))
            points.extend([x, y])
        
        return self.canvas.create_polygon(points, smooth=True, **kwargs)
    
    def _position_bubble(self):
        """Position the bubble relative to the pet"""
        if not self.bubble_window:
            return
            
        # Get pet window position
        pet_x = self.parent.winfo_x()
        pet_y = self.parent.winfo_y()
        
        # Position bubble to the right and slightly above the pet
        bubble_x = pet_x + self.pet_size[0] + 10
        bubble_y = pet_y - 30
        
        # Make sure bubble stays on screen
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        # Adjust if bubble would go off-screen
        if bubble_x + 300 > screen_width:
            bubble_x = pet_x - 310  # Position to the left instead
        if bubble_y < 0:
            bubble_y = pet_y + 20
        if bubble_y + 120 > screen_height:
            bubble_y = screen_height - 140
        
        self.bubble_window.geometry(f"300x120+{bubble_x}+{bubble_y}")
    
    def _start_typing_effect(self):
        """Start the typing animation effect"""
        self.typed_text = ""
        self.typing_index = 0
        self._continue_typing()
    
    def _continue_typing(self):
        """Continue the typing animation"""
        if self.typing_index < len(self.current_message):
            self.typed_text += self.current_message[self.typing_index]
            self.typing_index += 1
            self._update_bubble_content()
            
            # Schedule next character (varies speed for more natural effect)
            delay = 30 if self.current_message[self.typing_index - 1] in '.,!?' else 50
            self.typing_timer = self.parent.after(delay, self._continue_typing)
        else:
            # Typing complete, add a subtle cursor blink effect briefly
            self.parent.after(100, lambda: self._update_bubble_content())
    
    def _update_bubble_content(self):
        """Update the bubble text content"""
        if self.bubble_window and self.text_id:
            display_text = self.typed_text
            # Add typing cursor if still typing
            if self.typing_index < len(self.current_message) and len(display_text) > 0:
                display_text += "|"
            
            self.canvas.itemconfig(self.text_id, text=display_text)
    
    def _start_fade_animation(self):
        """Start fade in/out animation"""
        self._continue_fade_animation()
    
    def _continue_fade_animation(self):
        """Continue fade animation"""
        if not self.bubble_window:
            return
            
        # Smooth animation towards target
        fade_speed = 0.05
        if abs(self.fade_alpha - self.target_alpha) > 0.01:
            if self.fade_alpha < self.target_alpha:
                self.fade_alpha += fade_speed
            else:
                self.fade_alpha -= fade_speed
            
            # Apply alpha to window
            try:
                self.bubble_window.wm_attributes("-alpha", self.fade_alpha)
            except:
                pass
            
            # Continue animation
            self.fade_timer = self.parent.after(16, self._continue_fade_animation)  # ~60fps
        else:
            self.fade_alpha = self.target_alpha
            try:
                self.bubble_window.wm_attributes("-alpha", self.fade_alpha)
            except:
                pass
    
    def _destroy_bubble(self):
        """Destroy the bubble window"""
        self.is_visible = False
        self._stop_position_tracking()
        if self.auto_hide_timer:
            self.parent.after_cancel(self.auto_hide_timer)
        if self.typing_timer:
            self.parent.after_cancel(self.typing_timer)
        if self.fade_timer:
            self.parent.after_cancel(self.fade_timer)
        if self.bubble_window:
            self.bubble_window.destroy()
            self.bubble_window = None
    
    def _start_position_tracking(self):
        """Start tracking the pet's position to follow it"""
        if self.is_tracking:
            return
            
        self.is_tracking = True
        # Store initial position
        try:
            self.last_pet_x = self.parent.winfo_x()
            self.last_pet_y = self.parent.winfo_y()
        except:
            self.last_pet_x = 0
            self.last_pet_y = 0
        
        self._track_position()
    
    def _stop_position_tracking(self):
        """Stop position tracking"""
        self.is_tracking = False
        if self.position_timer:
            self.parent.after_cancel(self.position_timer)
            self.position_timer = None
    
    def _track_position(self):
        """Continuously track pet position and update bubble location"""
        if not self.is_tracking or not self.bubble_window:
            return
        
        try:
            # Get current pet position
            current_x = self.parent.winfo_x()
            current_y = self.parent.winfo_y()
            
            # Check if position has changed
            if current_x != self.last_pet_x or current_y != self.last_pet_y:
                # Update bubble position to follow the pet
                self._position_bubble()
                self.last_pet_x = current_x
                self.last_pet_y = current_y
            
            # Schedule next position check
            self.position_timer = self.parent.after(50, self._track_position)  # Check every 50ms
            
        except Exception as e:
            # If there's an error, stop tracking
            self.is_tracking = False


class ModernChatWindow:
    """Modern chat window with glassmorphism and smooth animations"""
    
    def __init__(self, parent, title: str = "Chat with Pixie 🐱"):
        self.parent = parent
        self.window = None
        self.chat_display = None
        self.chat_input = None
        
        # Get theme for styling
        try:
            from src.ui.theme_manager import get_theme
            self.theme = get_theme()
        except ImportError:
            self.theme = None
            
        self.setup_window(title)
        
    def setup_window(self, title: str):
        """Setup modern chat window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(title)
        self.window.geometry("450x600")
        
        # Modern window styling with theme support
        bg_color = self.theme.get_color("background") if self.theme else '#f8f9fa'
        self.window.configure(bg=bg_color)
        
        # Remove default window decorations for custom styling
        # self.window.overrideredirect(True)  # Uncomment for frameless
        
        # Make window stay on top
        self.window.wm_attributes("-topmost", True)
        
        # Add subtle transparency
        self.window.wm_attributes("-alpha", 0.95)
        
        self._create_title_bar()
        self._create_chat_area()
        self._create_input_area()
        self._apply_modern_styling()
    
    def _create_title_bar(self):
        """Create modern title bar"""
        title_frame = tk.Frame(self.window, bg='#667eea', height=40)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        # Title text with theme colors
        primary_color = self.theme.get_color("primary") if self.theme else '#667eea'
        title_label = tk.Label(
            title_frame,
            text="💬 Chat with Pixie",
            font=('Segoe UI', 12, 'bold'),
            bg=primary_color,
            fg='white'
        )
        title_label.pack(side='left', padx=15, pady=10)
        
        # Close button
        close_btn = tk.Button(
            title_frame,
            text="✕",
            font=('Segoe UI', 12, 'bold'),
            bg='#667eea',
            fg='white',
            bd=0,
            padx=10,
            command=self.window.destroy
        )
        close_btn.pack(side='right', pady=5, padx=10)
        
        # Hover effects for close button
        def on_enter(e): close_btn.configure(bg='#ff4757')
        def on_leave(e): close_btn.configure(bg='#667eea')
        close_btn.bind("<Enter>", on_enter)
        close_btn.bind("<Leave>", on_leave)
    
    def _create_chat_area(self):
        """Create modern chat display area"""
        # Main chat frame with padding
        chat_container = tk.Frame(self.window, bg='#f8f9fa')
        chat_container.pack(fill='both', expand=True, padx=20, pady=(20, 10))
        
        # Chat display with modern styling and theme support
        surface_color = self.theme.get_color("surface") if self.theme else 'white'
        text_color = self.theme.get_color("text_primary") if self.theme else '#2c3e50'
        primary_color = self.theme.get_color("primary") if self.theme else '#667eea'
        
        self.chat_display = tk.Text(
            chat_container,
            wrap='word',
            state='disabled',
            bg=surface_color,
            fg=text_color,
            font=('Segoe UI', 10),
            bd=0,
            padx=15,
            pady=15,
            relief='flat',
            selectbackground='#e3f2fd',
            insertbackground=primary_color
        )
        
        # Custom scrollbar
        scrollbar = ttk.Scrollbar(chat_container, orient="vertical", command=self.chat_display.yview)
        self.chat_display.configure(yscrollcommand=scrollbar.set)
        
        self.chat_display.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Add rounded corners effect (visual)
        self.chat_display.configure(highlightthickness=1, highlightcolor='#e0e6ed')
    
    def _create_input_area(self):
        """Create modern input area"""
        # Get theme colors
        bg_color = self.theme.get_color("background") if self.theme else '#f8f9fa'
        surface_color = self.theme.get_color("surface") if self.theme else 'white'
        text_color = self.theme.get_color("text_primary") if self.theme else '#2c3e50'
        primary_color = self.theme.get_color("primary") if self.theme else '#667eea'
        
        input_container = tk.Frame(self.window, bg=bg_color)
        input_container.pack(fill='x', padx=20, pady=(0, 20))
        
        # Input text area
        input_frame = tk.Frame(input_container, bg=surface_color, relief='flat', bd=1)
        input_frame.pack(fill='x', pady=(0, 10))
        
        self.chat_input = tk.Text(
            input_frame,
            height=3,
            wrap='word',
            bg=surface_color,
            fg=text_color,
            font=('Segoe UI', 10),
            bd=0,
            padx=15,
            pady=10,
            relief='flat',
            insertbackground=primary_color
        )
        self.chat_input.pack(fill='both', expand=True)
        
        # Buttons frame
        button_frame = tk.Frame(input_container, bg=bg_color)
        button_frame.pack(fill='x')
        
        # Get button colors
        secondary_color = self.theme.get_color("secondary") if self.theme else '#48c78e'
        
        # Modern send button
        send_button = tk.Button(
            button_frame,
            text="Send Message",
            font=('Segoe UI', 10, 'bold'),
            bg=primary_color,
            fg='white',
            bd=0,
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        send_button.pack(side='right', padx=(10, 0))
        
        # Analyze button
        analyze_button = tk.Button(
            button_frame,
            text="📸 Analyze Screen",
            font=('Segoe UI', 10),
            bg=secondary_color,
            fg='white',
            bd=0,
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        analyze_button.pack(side='right')
        
        # Hover effects with theme colors
        primary_hover = self.theme.get_color("primary_hover") if self.theme else '#5a6fd8'
        secondary_hover = self.theme.get_color("secondary_hover") if self.theme else '#3ec281'
        
        self._add_button_hover_effects(send_button, primary_hover, primary_color)
        self._add_button_hover_effects(analyze_button, secondary_hover, secondary_color)
        
        return send_button, analyze_button
    
    def _add_button_hover_effects(self, button, hover_color, normal_color):
        """Add hover effects to buttons"""
        def on_enter(e): button.configure(bg=hover_color)
        def on_leave(e): button.configure(bg=normal_color)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def _apply_modern_styling(self):
        """Apply modern styling and configure tags"""
        # Configure text tags for modern message styling
        self.chat_display.tag_configure(
            "user_message", 
            font=('Segoe UI', 10, 'bold'),
            foreground='#667eea',
            spacing1=5,
            spacing3=5
        )
        
        self.chat_display.tag_configure(
            "pixie_message",
            font=('Segoe UI', 10, 'bold'),
            foreground='#48c78e',
            spacing1=5,
            spacing3=5
        )
        
        self.chat_display.tag_configure(
            "message_content",
            font=('Segoe UI', 10),
            foreground='#2c3e50',
            spacing3=10,
            lmargin1=10,
            lmargin2=10
        )
        
        self.chat_display.tag_configure(
            "timestamp",
            font=('Segoe UI', 8),
            foreground='#95a5a6',
            justify='right'
        )
    
    def add_message(self, sender: str, message: str, timestamp: str = None):
        """Add a message with modern styling"""
        self.chat_display.config(state='normal')
        
        # Add sender with styling
        sender_tag = "pixie_message" if sender == "Pixie" else "user_message"
        sender_icon = "🤖 " if sender == "Pixie" else "👤 "
        
        self.chat_display.insert('end', f"{sender_icon}{sender}\n", sender_tag)
        self.chat_display.insert('end', f"{message}\n\n", "message_content")
        
        if timestamp:
            self.chat_display.insert('end', f"{timestamp}\n", "timestamp")
        
        self.chat_display.config(state='disabled')
        self.chat_display.see('end')


class ModernContextMenu:
    """Modern context menu with animations and effects"""
    
    def __init__(self, parent):
        self.parent = parent
        self.menu_window = None
        
        # Get theme for styling
        try:
            from src.ui.theme_manager import get_theme
            self.theme = get_theme()
        except ImportError:
            self.theme = None
        
    def show(self, x: int, y: int, options: list):
        """Show modern context menu at position"""
        if self.menu_window:
            self.menu_window.destroy()
        
        self.menu_window = tk.Toplevel(self.parent)
        self.menu_window.overrideredirect(True)
        self.menu_window.wm_attributes("-topmost", True)
        self.menu_window.wm_attributes("-alpha", 0.95)
        
        # Position menu
        self.menu_window.geometry(f"+{x}+{y}")
        
        # Create menu frame with theme colors
        surface_color = self.theme.get_color("surface") if self.theme else 'white'
        border_color = self.theme.get_color("border") if self.theme else '#e0e6ed'
        
        menu_frame = tk.Frame(
            self.menu_window,
            bg=surface_color,
            relief='flat',
            bd=1,
            highlightthickness=1,
            highlightcolor=border_color
        )
        menu_frame.pack(fill='both', expand=True)
        
        # Add options with theme colors
        text_color = self.theme.get_color("text_primary") if self.theme else '#2c3e50'
        hover_color = self.theme.get_color("border") if self.theme else '#f1f3f4'
        
        for option in options:
            if option == "---":  # Separator
                separator = tk.Frame(menu_frame, height=1, bg=border_color)
                separator.pack(fill='x', padx=10, pady=2)
            else:
                label, command = option
                btn = tk.Button(
                    menu_frame,
                    text=label,
                    font=('Segoe UI', 10),
                    bg=surface_color,
                    fg=text_color,
                    bd=0,
                    padx=20,
                    pady=8,
                    relief='flat',
                    anchor='w',
                    cursor='hand2',
                    command=lambda cmd=command: self._execute_command(cmd)
                )
                btn.pack(fill='x')
                
                # Hover effects with theme colors
                def on_enter(e, button=btn): button.configure(bg=hover_color)
                def on_leave(e, button=btn): button.configure(bg=surface_color)
                btn.bind("<Enter>", on_enter)
                btn.bind("<Leave>", on_leave)
        
        # Auto-hide on focus lost
        self.menu_window.bind("<FocusOut>", lambda e: self.hide())
        self.menu_window.focus_set()
        
        # Fade in animation
        self._animate_fade_in()
    
    def _execute_command(self, command):
        """Execute command and hide menu"""
        self.hide()
        if callable(command):
            command()
    
    def _animate_fade_in(self):
        """Animate fade in effect"""
        self.menu_window.wm_attributes("-alpha", 0.0)
        
        def fade_step(alpha=0.0):
            if alpha < 0.95:
                alpha += 0.1
                self.menu_window.wm_attributes("-alpha", alpha)
                self.menu_window.after(20, lambda: fade_step(alpha))
        
        fade_step()
    
    def hide(self):
        """Hide menu"""
        if self.menu_window:
            self.menu_window.destroy()
            self.menu_window = None


class DarkModeToggle:
    """Modern dark mode toggle switch component"""
    
    def __init__(self, parent, callback=None, initial_state=False):
        self.parent = parent
        self.callback = callback
        self.is_dark = initial_state
        self.toggle_canvas = None
        self.animation_timer = None
        self.switch_x = 0
        self.target_x = 0
        self.animation_speed = 2
        
        self._setup_toggle()
        
    def _setup_toggle(self):
        """Setup the dark mode toggle switch"""
        # Container frame
        self.container = tk.Frame(
            self.parent,
            bg='transparent' if hasattr(self.parent, 'winfo_rgb') else '#f8f9fa'
        )
        
        # Toggle switch canvas
        self.toggle_canvas = tk.Canvas(
            self.container,
            width=60,
            height=30,
            highlightthickness=0,
            bd=0,
            bg='transparent' if hasattr(self.parent, 'winfo_rgb') else '#f8f9fa'
        )
        self.toggle_canvas.pack(side='left')
        
        # Label
        self.label = tk.Label(
            self.container,
            text="🌙 Dark Mode",
            font=('Segoe UI', 10),
            bg='transparent' if hasattr(self.parent, 'winfo_rgb') else '#f8f9fa',
            fg='#2c3e50'
        )
        self.label.pack(side='left', padx=(10, 0))
        
        # Bind click events
        self.toggle_canvas.bind("<Button-1>", self._on_toggle_click)
        self.label.bind("<Button-1>", self._on_toggle_click)
        
        # Initial position
        self.switch_x = 30 if self.is_dark else 5
        self.target_x = self.switch_x
        
        self._draw_toggle()
        
    def _draw_toggle(self):
        """Draw the toggle switch"""
        self.toggle_canvas.delete("all")
        
        # Background track
        track_color = "#4A90E2" if self.is_dark else "#E0E6ED"
        self.toggle_canvas.create_rounded_rectangle(
            5, 10, 55, 20, 5, fill=track_color, outline=""
        )
        
        # Switch circle
        circle_color = "#FFFFFF"
        shadow_color = "#00000020"
        
        # Draw shadow
        self.toggle_canvas.create_oval(
            self.switch_x + 1, 6, self.switch_x + 19, 24,
            fill=shadow_color, outline=""
        )
        
        # Draw main circle
        self.toggle_canvas.create_oval(
            self.switch_x, 5, self.switch_x + 18, 23,
            fill=circle_color, outline="#D0D0D0", width=1
        )
        
        # Add icon in the center
        icon = "🌙" if self.is_dark else "☀️"
        self.toggle_canvas.create_text(
            self.switch_x + 9, 14,
            text=icon, font=('Segoe UI Emoji', 8)
        )
    
    def _on_toggle_click(self, event):
        """Handle toggle click"""
        self.toggle()
    
    def toggle(self):
        """Toggle dark mode state"""
        self.is_dark = not self.is_dark
        self.target_x = 30 if self.is_dark else 5
        
        # Update label
        self.label.configure(text="🌙 Dark Mode" if self.is_dark else "☀️ Light Mode")
        
        # Start animation
        self._start_animation()
        
        # Call callback
        if self.callback:
            self.callback(self.is_dark)
    
    def set_state(self, is_dark: bool):
        """Set toggle state without triggering callback"""
        self.is_dark = is_dark
        self.switch_x = 30 if is_dark else 5
        self.target_x = self.switch_x
        
        # Update label
        self.label.configure(text="🌙 Dark Mode" if self.is_dark else "☀️ Light Mode")
        
        self._draw_toggle()
    
    def _start_animation(self):
        """Start smooth animation"""
        self._animate_step()
    
    def _animate_step(self):
        """Animate one step"""
        if abs(self.switch_x - self.target_x) > 1:
            if self.switch_x < self.target_x:
                self.switch_x += self.animation_speed
            else:
                self.switch_x -= self.animation_speed
            
            self._draw_toggle()
            self.animation_timer = self.parent.after(16, self._animate_step)
        else:
            self.switch_x = self.target_x
            self._draw_toggle()
    
    def pack(self, **kwargs):
        """Pack the toggle container"""
        self.container.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the toggle container"""
        self.container.grid(**kwargs)


# Monkey patch to add rounded rectangle to canvas
def create_rounded_rectangle(self, x1, y1, x2, y2, r, **kwargs):
    """Create a rounded rectangle on canvas"""
    points = []
    for x, y in [(x1, y1 + r), (x1, y1), (x1 + r, y1),
                 (x2 - r, y1), (x2, y1), (x2, y1 + r),
                 (x2, y2 - r), (x2, y2), (x2 - r, y2),
                 (x1 + r, y2), (x1, y2), (x1, y2 - r)]:
        points.append(x)
        points.append(y)
    return self.create_polygon(points, smooth=True, **kwargs)

tk.Canvas.create_rounded_rectangle = create_rounded_rectangle