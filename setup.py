#!/usr/bin/env python3
"""
Setup script for Virtual Pet AI Assistant
This script helps users set up the project dependencies and configuration
"""

import sys
import os
import subprocess
import logging
from pathlib import Path

def setup_logging():
    """Setup basic logging for the setup script"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def check_python_version():
    """Check if Python version is compatible"""
    min_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version < min_version:
        print(f"❌ Python {min_version[0]}.{min_version[1]} or higher is required. Current version: {current_version[0]}.{current_version[1]}")
        return False
    
    print(f"✅ Python version {current_version[0]}.{current_version[1]} is compatible")
    return True

def install_requirements():
    """Install required Python packages"""
    print("\n📦 Installing Python dependencies...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found!")
        return False
    
    try:
        # Use the Python executable that's running this script
        python_exe = sys.executable
        
        cmd = [python_exe, "-m", "pip", "install", "-r", str(requirements_file)]
        
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        print("✅ Dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print(f"Error output: {e.stderr}")
        
        # Suggest manual installation
        print("\n💡 Try installing manually:")
        print(f"   {python_exe} -m pip install -r requirements.txt")
        
        return False

def setup_environment():
    """Setup environment variables"""
    print("\n🔧 Setting up environment...")
    
    env_example = Path(__file__).parent / ".env.example"
    env_file = Path(__file__).parent / ".env"
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        # Copy example to .env
        with open(env_example, 'r') as src, open(env_file, 'w') as dst:
            dst.write(src.read())
        
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env and add your Gemini API key!")
        print("   Get your free API key from: https://makersuite.google.com/app/apikey")
        return True
    else:
        print("❌ .env.example not found")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ["logs", "assets", ".cache"]
    project_root = Path(__file__).parent
    
    for dir_name in directories:
        dir_path = project_root / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"✅ Created {dir_name}/")
    
    return True

def check_system_compatibility():
    """Check system compatibility"""
    print("\n🖥️  Checking system compatibility...")
    
    # Check OS
    if os.name == 'nt':
        print("✅ Windows OS detected")
    else:
        print("⚠️  This application is primarily designed for Windows")
        print("   Some features may not work on other operating systems")
    
    # Check if running in virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
    else:
        print("⚠️  Not running in a virtual environment")
        print("   Consider using a virtual environment for better dependency management")
    
    return True

def test_dependencies():
    """Test if critical dependencies can be imported"""
    print("\n🧪 Testing dependencies...")
    
    critical_deps = [
        ('tkinter', 'GUI framework'),
        ('PIL', 'Image processing'),
        ('google.generativeai', 'Gemini AI'),
        ('psutil', 'System monitoring'),
        ('dotenv', 'Environment variables')
    ]
    
    success = True
    
    for dep_name, description in critical_deps:
        try:
            if dep_name == 'PIL':
                import PIL
            elif dep_name == 'google.generativeai':
                import google.generativeai
            elif dep_name == 'tkinter':
                import tkinter
            elif dep_name == 'psutil':
                import psutil
            elif dep_name == 'dotenv':
                import dotenv
            
            print(f"✅ {dep_name} - {description}")
            
        except ImportError as e:
            print(f"❌ {dep_name} - {description} (ImportError: {e})")
            success = False
        except Exception as e:
            print(f"⚠️  {dep_name} - {description} (Error: {e})")
    
    if os.name == 'nt':
        # Test Windows-specific dependencies
        try:
            import win32gui
            print("✅ win32gui - Windows API access")
        except ImportError:
            print("❌ win32gui - Windows API access")
            print("   Try: pip install pywin32")
            success = False
    
    return success

def display_next_steps():
    """Display what to do next"""
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Edit the .env file and add your Gemini API key")
    print("   Get it from: https://makersuite.google.com/app/apikey")
    print("2. Run the application: python main.py")
    print("3. Click on Pixie (your virtual pet) to start chatting!")
    print("\n💡 Tips:")
    print("- Right-click on Pixie for the context menu")
    print("- Use Ctrl+Alt+P to quickly activate the assistant")
    print("- The pet will analyze your screen and provide contextual help")
    
    # Check if API key is set
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            if "your_gemini_api_key_here" in content:
                print("\n⚠️  Don't forget to update your Gemini API key in .env!")

def main():
    """Main setup function"""
    print("🐱 Virtual Pet AI Assistant - Setup Script")
    print("=" * 50)
    
    setup_logging()
    
    # Run setup steps
    steps = [
        ("Checking Python version", check_python_version),
        ("Checking system compatibility", check_system_compatibility),
        ("Installing requirements", install_requirements),
        ("Setting up environment", setup_environment),
        ("Creating directories", create_directories),
        ("Testing dependencies", test_dependencies)
    ]
    
    all_success = True
    
    for step_name, step_func in steps:
        print(f"\n⏳ {step_name}...")
        try:
            success = step_func()
            if not success:
                all_success = False
                print(f"❌ {step_name} failed!")
            else:
                print(f"✅ {step_name} completed!")
        except Exception as e:
            print(f"❌ {step_name} failed with error: {e}")
            all_success = False
    
    print("\n" + "=" * 50)
    
    if all_success:
        print("🎉 Setup completed successfully!")
        display_next_steps()
    else:
        print("⚠️  Setup completed with some issues.")
        print("Please review the errors above and fix them before running the application.")
        
        print("\n🆘 Common solutions:")
        print("- Make sure you're using Python 3.8 or higher")
        print("- Run this script in a virtual environment")
        print("- On Windows, you might need to install Visual C++ Build Tools")
        print("- Try running as administrator if you get permission errors")
    
    return 0 if all_success else 1

if __name__ == "__main__":
    sys.exit(main())