"""
Screen Monitor
Handles screen capture and active window detection
"""

import logging
import asyncio
import time
from typing import Optional, Dict, Any, Tuple
from PIL import Image, ImageGrab
import psutil
import win32gui
import win32process

class ScreenMonitor:
    """Monitors screen activity and captures screenshots"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.last_screenshot = None
        self.last_active_window = None
        self.monitoring = False
    
    def get_screenshot(self, region: Optional[Tuple[int, int, int, int]] = None) -> Image.Image:
        """
        Capture a screenshot of the screen or specified region
        
        Args:
            region: Tuple of (left, top, right, bottom) to capture specific region
        
        Returns:
            PIL Image of the screenshot
        """
        try:
            screenshot = ImageGrab.grab(bbox=region)
            self.last_screenshot = screenshot
            return screenshot
        except Exception as e:
            self.logger.error(f"Error capturing screenshot: {e}")
            raise
    
    def get_active_window_info(self) -> Dict[str, Any]:
        """
        Get information about the currently active window
        
        Returns:
            Dictionary with window information
        """
        try:
            hwnd = win32gui.GetForegroundWindow()
            
            if hwnd == 0:
                return {"title": "Unknown", "app_name": "Unknown", "hwnd": 0}
            
            # Get window title
            window_title = win32gui.GetWindowText(hwnd)
            
            # Get process info
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                process = psutil.Process(pid)
                app_name = process.name()
                exe_path = process.exe()
            except (psutil.NoSuchProcess, psutil.AccessDenied, OSError):
                app_name = "Unknown"
                exe_path = ""
            
            # Get window position and size
            try:
                rect = win32gui.GetWindowRect(hwnd)
                window_rect = {
                    "left": rect[0],
                    "top": rect[1], 
                    "right": rect[2],
                    "bottom": rect[3],
                    "width": rect[2] - rect[0],
                    "height": rect[3] - rect[1]
                }
            except Exception:
                window_rect = None
            
            window_info = {
                "title": window_title,
                "app_name": app_name,
                "exe_path": exe_path,
                "hwnd": hwnd,
                "pid": pid if 'pid' in locals() else 0,
                "rect": window_rect
            }
            
            self.last_active_window = window_info
            return window_info
            
        except Exception as e:
            self.logger.error(f"Error getting active window info: {e}")
            return {"title": "Error", "app_name": "Error", "hwnd": 0}
    
    def detect_application_type(self, window_info: Dict[str, Any]) -> str:
        """
        Detect the type of application based on window info
        
        Args:
            window_info: Window information dictionary
        
        Returns:
            Application type string
        """
        app_name = window_info.get("app_name", "").lower()
        window_title = window_info.get("title", "").lower()
        
        # VS Code
        if "code" in app_name or "visual studio code" in window_title:
            return "vscode"
        
        # Excel
        if "excel" in app_name or "excel" in window_title:
            return "excel"
        
        # Word
        if "winword" in app_name or "word" in window_title:
            return "word"
        
        # PowerPoint
        if "powerpnt" in app_name or "powerpoint" in window_title:
            return "powerpoint"
        
        # Web browsers
        if any(browser in app_name for browser in ["chrome", "firefox", "edge", "safari", "opera"]):
            return "browser"
        
        # IDEs
        if any(ide in app_name for ide in ["pycharm", "intellij", "eclipse", "netbeans", "atom", "sublime"]):
            return "ide"
        
        # Command line
        if any(terminal in app_name for terminal in ["cmd", "powershell", "terminal", "wt"]):
            return "terminal"
        
        # File explorer
        if "explorer" in app_name:
            return "file_explorer"
        
        # Photo/Image editors
        if any(editor in app_name for editor in ["photoshop", "gimp", "paint", "mspaint"]):
            return "image_editor"
        
        # Video players
        if any(player in app_name for player in ["vlc", "mpc", "wmplayer", "quicktime"]):
            return "video_player"
        
        # Games
        if any(game_indicator in app_name for game_indicator in ["steam", "origin", "uplay", "epic"]):
            return "game"
        
        return "unknown"
    
    def get_screen_context(self) -> Dict[str, Any]:
        """
        Get comprehensive context about the current screen state
        
        Returns:
            Dictionary with screen context information
        """
        window_info = self.get_active_window_info()
        app_type = self.detect_application_type(window_info)
        
        context = {
            "timestamp": time.time(),
            "active_window": window_info,
            "app_type": app_type,
            "has_screenshot": self.last_screenshot is not None
        }
        
        # Add application-specific context
        if app_type == "vscode":
            context["suggestions"] = [
                "Code assistance and debugging",
                "Syntax explanations",
                "Best practices and refactoring tips"
            ]
        elif app_type == "excel":
            context["suggestions"] = [
                "Formula help and explanations", 
                "Data analysis tips",
                "Chart and visualization suggestions"
            ]
        elif app_type == "browser":
            context["suggestions"] = [
                "Web page summarization",
                "Research assistance", 
                "Link and content analysis"
            ]
        
        return context
    
    async def start_monitoring(self, callback=None, interval: float = 2.0):
        """
        Start monitoring screen changes
        
        Args:
            callback: Function to call when screen changes detected
            interval: Monitoring interval in seconds
        """
        self.monitoring = True
        self.logger.info("Started screen monitoring")
        
        last_window_title = None
        
        try:
            while self.monitoring:
                current_window = self.get_active_window_info()
                current_title = current_window.get("title", "")
                
                # Check if active window changed
                if current_title != last_window_title:
                    self.logger.debug(f"Active window changed to: {current_title}")
                    
                    if callback:
                        try:
                            await callback(current_window)
                        except Exception as e:
                            self.logger.error(f"Error in monitoring callback: {e}")
                    
                    last_window_title = current_title
                
                await asyncio.sleep(interval)
                
        except Exception as e:
            self.logger.error(f"Error in screen monitoring: {e}")
        finally:
            self.monitoring = False
            self.logger.info("Stopped screen monitoring")
    
    def stop_monitoring(self):
        """Stop screen monitoring"""
        self.monitoring = False
        self.logger.info("Requested screen monitoring stop")
    
    def capture_window_screenshot(self, window_info: Dict[str, Any]) -> Optional[Image.Image]:
        """
        Capture screenshot of a specific window
        
        Args:
            window_info: Window information dictionary
        
        Returns:
            PIL Image of the window or None if failed
        """
        try:
            rect = window_info.get("rect")
            if not rect:
                return None
            
            # Capture the window region
            screenshot = ImageGrab.grab(bbox=(
                rect["left"], 
                rect["top"],
                rect["right"], 
                rect["bottom"]
            ))
            
            return screenshot
            
        except Exception as e:
            self.logger.error(f"Error capturing window screenshot: {e}")
            return None