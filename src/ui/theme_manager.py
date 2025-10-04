"""
Theme and Style Manager for Modern UI
Provides consistent styling and theming across the application
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Tuple
import json
from pathlib import Path

class ModernTheme:
    """Modern theme configuration and styling"""
    
    # Default modern color palette
    DEFAULT_COLORS = {
        "primary": "#667eea",
        "primary_hover": "#5a6fd8", 
        "secondary": "#48c78e",
        "secondary_hover": "#3ec281",
        "accent": "#FF69B4",
        "accent_hover": "#FF1493",
        "background": "#f8f9fa",
        "surface": "#ffffff",
        "text_primary": "#2c3e50",
        "text_secondary": "#7f8c8d",
        "text_muted": "#95a5a6",
        "border": "#e0e6ed",
        "success": "#27ae60",
        "warning": "#f39c12",
        "error": "#e74c3c",
        "glow": "#FFD700"
    }
    
    # Modern fonts
    FONTS = {
        "primary": ("Segoe UI", 10),
        "heading": ("Segoe UI", 12, "bold"),
        "button": ("Segoe UI", 10, "bold"),
        "small": ("Segoe UI", 9),
        "emoji": ("Segoe UI Emoji", 12)
    }
    
    # Animation settings
    ANIMATIONS = {
        "fade_duration": 200,
        "hover_duration": 100,
        "bounce_duration": 300,
        "slide_duration": 250
    }
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.colors = self._load_colors()
        self.fonts = self._load_fonts()
        
    def _load_colors(self) -> Dict[str, str]:
        """Load colors from config or use defaults"""
        ui_config = self.config.get("ui", {})
        color_scheme = ui_config.get("color_scheme", {})
        
        # Merge with defaults
        colors = self.DEFAULT_COLORS.copy()
        colors.update(color_scheme)
        
        return colors
    
    def _load_fonts(self) -> Dict[str, Tuple]:
        """Load fonts from config or use defaults"""
        # For now, use defaults - could be extended to support custom fonts
        return self.FONTS.copy()
    
    def get_color(self, color_name: str) -> str:
        """Get color by name"""
        return self.colors.get(color_name, self.DEFAULT_COLORS.get(color_name, "#000000"))
    
    def get_font(self, font_name: str) -> Tuple:
        """Get font by name"""
        return self.fonts.get(font_name, self.FONTS["primary"])
    
    def style_button(self, button: tk.Button, style: str = "primary") -> None:
        """Apply modern styling to a button"""
        if style == "primary":
            bg_color = self.get_color("primary")
            hover_color = self.get_color("primary_hover")
        elif style == "secondary":
            bg_color = self.get_color("secondary")
            hover_color = self.get_color("secondary_hover")
        elif style == "accent":
            bg_color = self.get_color("accent")
            hover_color = self.get_color("accent_hover")
        else:
            bg_color = self.get_color("surface")
            hover_color = self.get_color("border")
        
        button.configure(
            bg=bg_color,
            fg="white" if style in ["primary", "secondary", "accent"] else self.get_color("text_primary"),
            font=self.get_font("button"),
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        
        # Add hover effects
        def on_enter(e): button.configure(bg=hover_color)
        def on_leave(e): button.configure(bg=bg_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def style_text_widget(self, text_widget: tk.Text, style: str = "default") -> None:
        """Apply modern styling to text widgets"""
        if style == "chat":
            bg_color = self.get_color("surface")
            fg_color = self.get_color("text_primary")
            select_bg = "#e3f2fd"
        else:
            bg_color = self.get_color("surface")
            fg_color = self.get_color("text_primary")
            select_bg = self.get_color("border")
        
        text_widget.configure(
            bg=bg_color,
            fg=fg_color,
            font=self.get_font("primary"),
            relief="flat",
            bd=0,
            selectbackground=select_bg,
            insertbackground=self.get_color("primary")
        )
    
    def style_frame(self, frame: tk.Frame, style: str = "default") -> None:
        """Apply modern styling to frames"""
        if style == "card":
            bg_color = self.get_color("surface")
            relief = "flat"
            bd = 1
        elif style == "container":
            bg_color = self.get_color("background")
            relief = "flat"
            bd = 0
        else:
            bg_color = self.get_color("background")
            relief = "flat"
            bd = 0
        
        frame.configure(
            bg=bg_color,
            relief=relief,
            bd=bd
        )
    
    def configure_window(self, window: tk.Toplevel) -> None:
        """Apply modern window configuration"""
        window.configure(bg=self.get_color("background"))
        
        # Set transparency if supported
        try:
            transparency = self.config.get("ui", {}).get("transparency", 0.95)
            window.wm_attributes("-alpha", transparency)
        except:
            pass
    
    def create_gradient_frame(self, parent: tk.Widget, width: int, height: int, 
                            start_color: str, end_color: str) -> tk.Canvas:
        """Create a gradient background frame"""
        canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            highlightthickness=0,
            bd=0
        )
        
        # Create gradient effect with multiple rectangles
        steps = 50
        start_rgb = self._hex_to_rgb(start_color)
        end_rgb = self._hex_to_rgb(end_color)
        
        for i in range(steps):
            ratio = i / steps
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            y1 = (height * i) // steps
            y2 = (height * (i + 1)) // steps
            
            canvas.create_rectangle(0, y1, width, y2, fill=color, outline="")
        
        return canvas
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def animate_widget_fade(self, widget: tk.Widget, fade_in: bool = True, callback=None):
        """Animate widget fade in/out effect"""
        if not hasattr(widget, 'winfo_exists') or not widget.winfo_exists():
            return
            
        steps = 10
        duration = self.ANIMATIONS["fade_duration"] // steps
        
        if fade_in:
            alpha_values = [i / steps for i in range(1, steps + 1)]
        else:
            alpha_values = [1 - (i / steps) for i in range(1, steps + 1)]
        
        def animate_step(step=0):
            if step < len(alpha_values) and widget.winfo_exists():
                try:
                    # For windows that support alpha
                    if hasattr(widget, 'wm_attributes'):
                        widget.wm_attributes("-alpha", alpha_values[step])
                    widget.after(duration, lambda: animate_step(step + 1))
                except:
                    # Fallback - just show/hide
                    if fade_in:
                        widget.configure(state='normal')
                    else:
                        widget.configure(state='disabled')
            elif callback:
                callback()
        
        animate_step()
    
    def create_modern_tooltip(self, widget: tk.Widget, text: str):
        """Create modern tooltip for widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.overrideredirect(True)
            tooltip.wm_attributes("-topmost", True)
            tooltip.configure(bg=self.get_color("text_primary"))
            
            label = tk.Label(
                tooltip,
                text=text,
                font=self.get_font("small"),
                bg=self.get_color("text_primary"),
                fg="white",
                padx=10,
                pady=5
            )
            label.pack()
            
            # Position tooltip near cursor
            x = event.x_root + 10
            y = event.y_root + 10
            tooltip.geometry(f"+{x}+{y}")
            
            # Auto-hide after 3 seconds
            tooltip.after(3000, tooltip.destroy)
            
            # Store reference to prevent garbage collection
            widget._tooltip = tooltip
        
        def hide_tooltip(event):
            if hasattr(widget, '_tooltip'):
                try:
                    widget._tooltip.destroy()
                except:
                    pass
        
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)


class StyleManager:
    """Manages styling across the application"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.theme = ModernTheme(self.config)
        
    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """Load configuration from file"""
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Try default config location
        try:
            default_config = Path(__file__).parent.parent.parent / "config" / "settings.json"
            if default_config.exists():
                with open(default_config, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {}
    
    def get_theme(self) -> ModernTheme:
        """Get the current theme"""
        return self.theme
    
    def apply_global_styles(self, root: tk.Tk):
        """Apply global styles to the application"""
        # Configure ttk styles
        style = ttk.Style()
        
        # Configure modern button style
        style.configure(
            "Modern.TButton",
            font=self.theme.get_font("button"),
            foreground="white",
            background=self.theme.get_color("primary"),
            borderwidth=0,
            focuscolor="none"
        )
        
        style.map(
            "Modern.TButton",
            background=[
                ("active", self.theme.get_color("primary_hover")),
                ("pressed", self.theme.get_color("primary"))
            ]
        )
        
        # Configure modern frame style
        style.configure(
            "Modern.TFrame",
            background=self.theme.get_color("background"),
            borderwidth=0
        )
        
        # Set default font
        root.option_add("*Font", self.theme.get_font("primary"))


# Global style manager instance
_style_manager = None

def get_style_manager() -> StyleManager:
    """Get the global style manager instance"""
    global _style_manager
    if _style_manager is None:
        _style_manager = StyleManager()
    return _style_manager

def get_theme() -> ModernTheme:
    """Get the current theme"""
    return get_style_manager().get_theme()