"""
Configuration Manager
Handles loading and saving application settings
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self):
        self.config_dir = Path(__file__).parent.parent.parent / "config"
        self.config_file = self.config_dir / "settings.json"
        self.default_config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration settings"""
        return {
            "pet": {
                "name": "Pixie",
                "personality": "helpful and friendly",
                "size": {"width": 100, "height": 100},
                "position": {"x": -1, "y": -1},  # -1 means auto-position
                "animations": {
                    "idle": "assets/pet/idle.gif",
                    "thinking": "assets/pet/thinking.gif",
                    "speaking": "assets/pet/speaking.gif"
                }
            },
            "ai": {
                "model": "gemini-1.5-flash",
                "temperature": 0.7,
                "max_tokens": 1000,
                "system_prompt": "You are a helpful virtual pet assistant. Be friendly, concise, and provide practical help based on what you see on the user's screen."
            },
            "screen": {
                "capture_interval": 2.0,  # seconds
                "max_screenshot_size": {"width": 1920, "height": 1080},
                "privacy_blur_regions": []  # List of regions to blur for privacy
            },
            "hotkeys": {
                "activate": "ctrl+alt+p",
                "screenshot": "ctrl+alt+s"
            },
            "privacy": {
                "ask_before_screenshot": False,
                "blur_sensitive_info": True,
                "exclude_apps": ["password_manager", "banking"]
            },
            "ui": {
                "transparency": 0.9,
                "always_on_top": True,
                "click_through": False
            }
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create with defaults"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Merge with defaults to ensure all keys exist
                return self._merge_config(self.default_config, config)
            else:
                # Create default config file
                self.save_config(self.default_config)
                return self.default_config.copy()
        except Exception as e:
            print(f"Error loading config: {e}. Using defaults.")
            return self.default_config.copy()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file"""
        try:
            # Ensure config directory exists
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def _merge_config(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge user config with defaults"""
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get_setting(self, path: str, config: Dict[str, Any] = None) -> Any:
        """Get a setting using dot notation (e.g., 'pet.name')"""
        if config is None:
            config = self.load_config()
        
        keys = path.split('.')
        value = config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        
        return value
    
    def set_setting(self, path: str, value: Any, config: Dict[str, Any] = None) -> bool:
        """Set a setting using dot notation"""
        if config is None:
            config = self.load_config()
        
        keys = path.split('.')
        current = config
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Set the value
        current[keys[-1]] = value
        
        return self.save_config(config)