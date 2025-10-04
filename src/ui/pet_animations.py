"""
Pet Animation and Visual Effects
Creates dynamic animations and visual effects for the modern pet UI
"""

import math
import time
import tkinter as tk
from typing import List, Tuple, Callable
from PIL import Image, ImageDraw, ImageTk
import asyncio

class PetAnimator:
    """Handles pet animations and visual effects"""
    
    def __init__(self, canvas: tk.Canvas, size: Tuple[int, int] = (120, 120)):
        self.canvas = canvas
        self.size = size
        self.animation_frame = 0
        self.is_active = False
        self.current_emotion = "happy"
        self.effects = []
        
        # Animation states
        self.blink_timer = 0
        self.idle_timer = 0
        self.breath_phase = 0
        
    def start_animations(self):
        """Start the animation loop"""
        self.is_active = True
        self._animate_loop()
    
    def stop_animations(self):
        """Stop all animations"""
        self.is_active = False
        
    def _animate_loop(self):
        """Main animation loop"""
        if not self.is_active:
            return
            
        self.animation_frame += 1
        self._update_animations()
        
        # Schedule next frame (20 FPS)
        if self.canvas.winfo_exists():
            self.canvas.after(50, self._animate_loop)
    
    def _update_animations(self):
        """Update all active animations"""
        # Update timers
        self.blink_timer += 1
        self.idle_timer += 1
        self.breath_phase = (self.animation_frame * 0.05) % (2 * math.pi)
        
        # Trigger random blinks
        if self.blink_timer > 120 and (self.animation_frame % 180) < 10:
            self.blink()
            self.blink_timer = 0
        
        # Breathing animation (subtle scale change)
        scale_factor = 1 + 0.03 * math.sin(self.breath_phase)
        self._apply_breathing_effect(scale_factor)
        
        # Update particle effects
        self._update_particle_effects()
        
        # Idle movements
        if self.idle_timer > 300:  # Every 15 seconds
            self.idle_movement()
            self.idle_timer = 0
    
    def blink(self):
        """Animate blinking"""
        # This would be implemented to modify eye sprites
        pass
    
    def idle_movement(self):
        """Random idle movements"""
        # Subtle head bobbing or looking around
        pass
    
    def _apply_breathing_effect(self, scale: float):
        """Apply subtle breathing animation"""
        # This would scale the pet slightly up and down
        pass
    
    def _update_particle_effects(self):
        """Update floating particle effects"""
        center_x, center_y = self.size[0] // 2, self.size[1] // 2
        
        # Clear old particles
        self.canvas.delete("particles")
        
        # Create floating sparkles
        for i in range(3):
            angle = (self.animation_frame + i * 120) * 0.02
            distance = 40 + math.sin(angle) * 10
            
            px = center_x + math.cos(angle) * distance
            py = center_y + math.sin(angle) * distance
            
            # Sparkle size and alpha
            size = 1.5 + math.sin(self.animation_frame * 0.05 + i) * 0.5
            
            self.canvas.create_oval(
                px - size, py - size, px + size, py + size,
                fill='#FFD700', outline='', tags="particles"
            )
    
    def set_emotion(self, emotion: str):
        """Change pet emotion (happy, sad, excited, thinking, etc.)"""
        self.current_emotion = emotion
        # Trigger emotion-specific animations
        
    def play_action_animation(self, action: str, callback: Callable = None):
        """Play a specific action animation"""
        if action == "bounce":
            self._bounce_animation(callback)
        elif action == "spin":
            self._spin_animation(callback)
        elif action == "wave":
            self._wave_animation(callback)
    
    def _bounce_animation(self, callback: Callable = None):
        """Bounce animation"""
        def bounce_step(step=0):
            if step < 20:
                # Bounce up and down
                offset = math.sin(step * 0.3) * 10
                # Apply offset to pet position
                self.canvas.after(50, lambda: bounce_step(step + 1))
            elif callback:
                callback()
        
        bounce_step()
    
    def _spin_animation(self, callback: Callable = None):
        """Spin animation"""
        # Implementation for spinning effect
        if callback:
            callback()
    
    def _wave_animation(self, callback: Callable = None):
        """Wave animation"""
        # Implementation for waving effect  
        if callback:
            callback()


class ParticleSystem:
    """Particle system for magical effects"""
    
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.particles = []
        
    class Particle:
        def __init__(self, x, y, vx, vy, life, color="#FFD700", size=2):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.life = life
            self.max_life = life
            self.color = color
            self.size = size
            
        def update(self):
            self.x += self.vx
            self.y += self.vy
            self.vy += 0.1  # Gravity
            self.life -= 1
            
            # Fade out over time
            alpha = self.life / self.max_life
            return self.life > 0, alpha
    
    def emit_burst(self, x, y, count=10, colors=None):
        """Emit a burst of particles"""
        if colors is None:
            colors = ["#FFD700", "#FF69B4", "#87CEEB", "#98FB98"]
            
        for _ in range(count):
            import random
            vx = random.uniform(-3, 3)
            vy = random.uniform(-5, -1)
            life = random.randint(30, 60)
            color = random.choice(colors)
            
            particle = self.Particle(x, y, vx, vy, life, color)
            self.particles.append(particle)
    
    def update(self):
        """Update all particles"""
        self.canvas.delete("particles")
        
        active_particles = []
        for particle in self.particles:
            alive, alpha = particle.update()
            
            if alive:
                # Draw particle with fading
                size = particle.size * alpha
                self.canvas.create_oval(
                    particle.x - size, particle.y - size,
                    particle.x + size, particle.y + size,
                    fill=particle.color, outline="", tags="particles"
                )
                active_particles.append(particle)
        
        self.particles = active_particles


class VisualEffects:
    """Collection of visual effects for the modern UI"""
    
    @staticmethod
    def create_glow_effect(canvas: tk.Canvas, x: int, y: int, radius: int, color: str = "#FF69B4"):
        """Create a glow effect around a point"""
        for i in range(5):
            glow_radius = radius + i * 5
            alpha = 0.3 - (i * 0.05)
            canvas.create_oval(
                x - glow_radius, y - glow_radius,
                x + glow_radius, y + glow_radius,
                fill=color, outline="", stipple="gray25", tags="glow"
            )
    
    @staticmethod
    def create_ripple_effect(canvas: tk.Canvas, x: int, y: int, max_radius: int = 50):
        """Create an expanding ripple effect"""
        def animate_ripple(radius=5):
            if radius < max_radius:
                canvas.delete("ripple")
                alpha = 1 - (radius / max_radius)
                
                canvas.create_oval(
                    x - radius, y - radius, x + radius, y + radius,
                    outline="#4A90E2", width=2, tags="ripple"
                )
                
                canvas.after(50, lambda: animate_ripple(radius + 5))
            else:
                canvas.delete("ripple")
        
        animate_ripple()
    
    @staticmethod  
    def pulse_effect(widget: tk.Widget, color_start: str, color_end: str, duration: int = 1000):
        """Create a pulsing color effect"""
        def pulse_step(step=0, direction=1):
            if step < 20:
                # Interpolate between colors
                ratio = (step / 20) * direction
                ratio = max(0, min(1, ratio))
                
                # Simple interpolation (would need proper color interpolation)
                try:
                    widget.configure(bg=color_start if ratio < 0.5 else color_end)
                except:
                    pass
                    
                next_step = step + 1 if direction == 1 else step - 1
                next_direction = -1 if step >= 19 and direction == 1 else (1 if step <= 0 and direction == -1 else direction)
                
                widget.after(duration // 40, lambda: pulse_step(next_step, next_direction))
        
        pulse_step()
    
    @staticmethod
    def shake_effect(widget: tk.Widget, intensity: int = 5, duration: int = 500):
        """Create a shake effect"""
        if not hasattr(widget, 'winfo_x'):
            return
            
        original_x = widget.winfo_x()
        original_y = widget.winfo_y()
        
        def shake_step(step=0):
            if step < 20:
                import random
                offset_x = random.randint(-intensity, intensity)
                offset_y = random.randint(-intensity, intensity)
                
                try:
                    widget.place(x=original_x + offset_x, y=original_y + offset_y)
                except:
                    pass
                
                widget.after(duration // 20, lambda: shake_step(step + 1))
            else:
                # Return to original position
                try:
                    widget.place(x=original_x, y=original_y)
                except:
                    pass
        
        shake_step()


class EmotionExpressions:
    """Different emotional expressions for the pet"""
    
    EXPRESSIONS = {
        "happy": {
            "eyes": "normal",
            "mouth": "smile", 
            "color_tint": "#FFB6C1",
            "particles": True
        },
        "excited": {
            "eyes": "wide",
            "mouth": "big_smile",
            "color_tint": "#FF69B4", 
            "particles": True,
            "bounce": True
        },
        "thinking": {
            "eyes": "looking_up",
            "mouth": "neutral",
            "color_tint": "#E6E6FA",
            "thought_bubble": True
        },
        "sleepy": {
            "eyes": "sleepy",
            "mouth": "small",
            "color_tint": "#B0C4DE",
            "particles": False
        },
        "confused": {
            "eyes": "crossed",
            "mouth": "wavy",
            "color_tint": "#DDA0DD",
            "question_mark": True
        }
    }
    
    @staticmethod
    def get_expression(emotion: str) -> dict:
        """Get expression configuration for emotion"""
        return EmotionExpressions.EXPRESSIONS.get(emotion, EmotionExpressions.EXPRESSIONS["happy"])