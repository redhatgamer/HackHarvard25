#!/usr/bin/env python3
"""
Simple development mode without file watching
Use this if you prefer manual restarts or if watchdog doesn't work
"""

import sys
import os
import subprocess
from pathlib import Path

def run_with_restart():
    """Run the application with easy restart capability"""
    
    project_root = Path(__file__).parent
    
    print("🐱 Virtual Pet AI Assistant - Simple Development Mode")
    print("=" * 50)
    print("- 🚀 Quick restart: Press Ctrl+C then Enter")
    print("- 🛑 Exit: Press Ctrl+C twice quickly") 
    print("- 📝 Edit files normally, restart manually when needed")
    print("=" * 50)
    print()
    
    restart_count = 0
    
    while True:
        restart_count += 1
        print(f"🔄 Starting application (restart #{restart_count})...")
        
        try:
            # Run the main application
            result = subprocess.run(
                [sys.executable, "main.py"],
                cwd=project_root
            )
            
            if result.returncode == 0:
                print("👋 Application exited normally")
                break
            else:
                print(f"⚠️  Application exited with code: {result.returncode}")
            
        except KeyboardInterrupt:
            print("\n🔄 Restart requested...")
            
            try:
                restart = input("Press Enter to restart, or Ctrl+C again to exit: ")
                print()
                continue
            except KeyboardInterrupt:
                print("\n👋 Exiting development mode")
                break
        
        except Exception as e:
            print(f"❌ Error running application: {e}")
            break

def main():
    """Main entry point"""
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ main.py not found in current directory")
        print("Please run this script from the project root directory")
        return 1
    
    run_with_restart()
    return 0

if __name__ == "__main__":
    sys.exit(main())