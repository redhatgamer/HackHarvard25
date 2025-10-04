#!/usr/bin/env python3
"""
Development script with hot-reload functionality
Automatically restarts the application when source files change
"""

import sys
import os
import time
import subprocess
import signal
from pathlib import Path
from threading import Thread, Event
import logging

# Check if watchdog is available, install if not
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("📦 Installing watchdog for hot-reload functionality...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "watchdog"])
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

class HotReloadHandler(FileSystemEventHandler):
    """Handler for file system events that triggers app restart"""
    
    def __init__(self, restart_callback):
        self.restart_callback = restart_callback
        self.last_restart = 0
        # Debounce restarts to avoid multiple triggers
        self.debounce_time = 1.0  # seconds
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        # Only watch Python files and config files
        if not (event.src_path.endswith(('.py', '.json', '.env'))):
            return
            
        # Ignore __pycache__ and log files
        if '__pycache__' in event.src_path or event.src_path.endswith('.log'):
            return
            
        current_time = time.time()
        if current_time - self.last_restart > self.debounce_time:
            print(f"🔄 File changed: {event.src_path}")
            self.restart_callback()
            self.last_restart = current_time

class DevServer:
    """Development server with hot-reload capabilities"""
    
    def __init__(self):
        self.process = None
        self.observer = None
        self.running = False
        self.restart_event = Event()
        self.project_root = Path(__file__).parent
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='[DEV] %(asctime)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
        
    def start_app(self):
        """Start the main application"""
        if self.process and self.process.poll() is None:
            self.logger.info("🛑 Stopping existing application...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
        
        self.logger.info("🚀 Starting Virtual Pet AI Assistant...")
        
        # Start the application
        try:
            self.process = subprocess.Popen(
                [sys.executable, "main.py"],
                cwd=self.project_root,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            
            self.logger.info(f"✅ Application started (PID: {self.process.pid})")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start application: {e}")
    
    def restart_app(self):
        """Trigger app restart"""
        self.restart_event.set()
    
    def setup_file_watcher(self):
        """Setup file system watcher for hot-reload"""
        handler = HotReloadHandler(self.restart_app)
        self.observer = Observer()
        
        # Watch the src directory for changes
        src_path = self.project_root / "src"
        if src_path.exists():
            self.observer.schedule(handler, str(src_path), recursive=True)
            self.logger.info(f"👁️  Watching for changes in: {src_path}")
        
        # Watch config directory
        config_path = self.project_root / "config"
        if config_path.exists():
            self.observer.schedule(handler, str(config_path), recursive=True)
            self.logger.info(f"👁️  Watching for changes in: {config_path}")
        
        # Watch main files
        main_files = ["main.py", ".env"]
        for file in main_files:
            file_path = self.project_root / file
            if file_path.exists():
                self.observer.schedule(handler, str(file_path.parent), recursive=False)
        
        self.observer.start()
        self.logger.info("🔍 File watcher started")
    
    def run(self):
        """Run the development server"""
        self.running = True
        
        print("🐱 Virtual Pet AI Assistant - Development Mode")
        print("=" * 50)
        print("Features:")
        print("- 🔄 Hot-reload on file changes")
        print("- 📝 Real-time development feedback")
        print("- 🚀 Automatic application restart")
        print()
        print("Press Ctrl+C to stop the development server")
        print("=" * 50)
        
        try:
            # Setup file watcher
            self.setup_file_watcher()
            
            # Start the application
            self.start_app()
            
            # Main loop
            while self.running:
                if self.restart_event.wait(timeout=1.0):
                    self.restart_event.clear()
                    self.start_app()
                
                # Check if process is still running
                if self.process and self.process.poll() is not None:
                    exit_code = self.process.poll()
                    if exit_code != 0:
                        self.logger.error(f"❌ Application exited with code: {exit_code}")
                        # Don't auto-restart on error, wait for file changes
                    else:
                        self.logger.info("👋 Application exited normally")
                        break
        
        except KeyboardInterrupt:
            self.logger.info("🛑 Development server interrupted by user")
        
        except Exception as e:
            self.logger.error(f"💥 Development server error: {e}")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.running = False
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.logger.info("🔍 File watcher stopped")
        
        if self.process and self.process.poll() is None:
            self.logger.info("🛑 Stopping application...")
            
            if os.name == 'nt':  # Windows
                # Gracefully terminate on Windows
                try:
                    self.process.terminate()
                    self.process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    self.process.kill()
            else:  # Unix-like
                try:
                    self.process.send_signal(signal.SIGTERM)
                    self.process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    self.process.kill()
        
        self.logger.info("👋 Development server stopped")

def main():
    """Main entry point for development mode"""
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ main.py not found in current directory")
        print("Please run this script from the project root directory")
        return 1
    
    # Check dependencies
    try:
        # Test imports to ensure the app can run
        import PIL
        import tkinter
        print("✅ Basic dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return 1
    
    # Check API key
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("⚠️  Warning: Gemini API key not configured")
        print("The AI features won't work without a valid API key")
        print("Add your key to the .env file to enable AI functionality")
    else:
        print("✅ Gemini API key configured")
    
    print()
    
    # Start development server
    dev_server = DevServer()
    dev_server.run()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())