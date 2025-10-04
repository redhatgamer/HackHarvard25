"""
Utility functions for the virtual pet assistant
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import hashlib
import time

def get_project_root() -> Path:
    """Get the project root directory"""
    return Path(__file__).parent.parent.parent

def ensure_directory(path: Path) -> bool:
    """Ensure a directory exists, create if it doesn't"""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Failed to create directory {path}: {e}")
        return False

def get_cache_path() -> Path:
    """Get the cache directory path"""
    cache_dir = get_project_root() / ".cache"
    ensure_directory(cache_dir)
    return cache_dir

def get_logs_path() -> Path:
    """Get the logs directory path"""
    logs_dir = get_project_root() / "logs"
    ensure_directory(logs_dir)
    return logs_dir

def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing invalid characters"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename[:255]  # Limit length

def hash_string(text: str) -> str:
    """Generate a hash for a string"""
    return hashlib.md5(text.encode()).hexdigest()

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    size_index = 0
    
    while size_bytes >= 1024 and size_index < len(size_names) - 1:
        size_bytes /= 1024.0
        size_index += 1
    
    return f"{size_bytes:.1f} {size_names[size_index]}"

def get_system_info() -> Dict[str, Any]:
    """Get basic system information"""
    import platform
    import psutil
    
    return {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "cpu_count": psutil.cpu_count(),
        "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "disk_usage": psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent
    }

def is_admin() -> bool:
    """Check if running with administrator privileges (Windows)"""
    if os.name != 'nt':
        return os.geteuid() == 0
    
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def measure_performance(func_name: str = ""):
    """Decorator to measure function performance"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            duration = end_time - start_time
            logging.debug(f"Performance [{func_name or func.__name__}]: {duration:.3f}s")
            
            return result
        return wrapper
    return decorator

class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, max_calls: int, time_window: float):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
    
    def can_proceed(self) -> bool:
        """Check if a new call can be made"""
        current_time = time.time()
        
        # Remove old calls outside the time window
        self.calls = [call_time for call_time in self.calls 
                     if current_time - call_time < self.time_window]
        
        # Check if we can make a new call
        if len(self.calls) < self.max_calls:
            self.calls.append(current_time)
            return True
        
        return False
    
    def time_until_next_call(self) -> float:
        """Get time until next call is allowed"""
        if not self.calls:
            return 0.0
        
        oldest_call = min(self.calls)
        current_time = time.time()
        
        return max(0.0, self.time_window - (current_time - oldest_call))

def check_dependencies() -> Dict[str, bool]:
    """Check if all required dependencies are installed"""
    dependencies = {
        'PIL': False,
        'google.generativeai': False,
        'psutil': False,
        'win32gui': False,
        'dotenv': False,
        'tkinter': False
    }
    
    for dep in dependencies:
        try:
            if dep == 'PIL':
                import PIL
            elif dep == 'google.generativeai':
                import google.generativeai
            elif dep == 'psutil':
                import psutil
            elif dep == 'win32gui':
                import win32gui
            elif dep == 'dotenv':
                import dotenv
            elif dep == 'tkinter':
                import tkinter
            
            dependencies[dep] = True
        except ImportError:
            dependencies[dep] = False
    
    return dependencies

def get_missing_dependencies() -> list:
    """Get list of missing dependencies"""
    deps = check_dependencies()
    return [dep for dep, installed in deps.items() if not installed]