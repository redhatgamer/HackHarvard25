#!/usr/bin/env python3
"""
Deployment preparation script
Prepares the Virtual Pet AI Assistant for deployment
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Check if all deployment requirements are met"""
    print("🔍 Checking deployment requirements...")
    
    # Check if API key is available
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("   Make sure to set it in GitHub Secrets or your environment")
        return False
    else:
        print("✅ GEMINI_API_KEY found")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required, found {sys.version}")
        return False
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} OK")
    
    return True

def install_build_tools():
    """Install tools needed for building executables"""
    print("📦 Installing build tools...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], 
                      check=True, capture_output=True)
        print("✅ PyInstaller installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install PyInstaller: {e}")
        return False

def build_executable():
    """Build standalone executable"""
    print("🏗️  Building executable...")
    
    try:
        # PyInstaller command for Windows GUI app
        cmd = [
            'pyinstaller',
            '--onefile',          # Single executable file
            '--windowed',         # No console window
            '--name', 'VirtualPetAI',
            '--icon', 'assets/icon.ico' if Path('assets/icon.ico').exists() else None,
            '--add-data', 'config;config',
            '--add-data', 'assets;assets',
            '--hidden-import', 'PIL._tkinter_finder',
            'main.py'
        ]
        
        # Remove None values
        cmd = [arg for arg in cmd if arg is not None]
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Executable built successfully")
        print(f"   Location: dist/VirtualPetAI.exe")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"   Output: {e.stdout}")
        print(f"   Error: {e.stderr}")
        return False

def create_distribution_package():
    """Create a distribution package"""
    print("📦 Creating distribution package...")
    
    try:
        # Create dist directory structure
        dist_dir = Path('distribution')
        dist_dir.mkdir(exist_ok=True)
        
        # Copy executable
        if Path('dist/VirtualPetAI.exe').exists():
            shutil.copy('dist/VirtualPetAI.exe', dist_dir)
        
        # Copy essential files
        files_to_copy = [
            'README.md',
            'QUICKSTART.md', 
            'LICENSE',
            '.env.example'
        ]
        
        for file in files_to_copy:
            if Path(file).exists():
                shutil.copy(file, dist_dir)
        
        # Copy directories
        dirs_to_copy = ['config', 'assets']
        for dir_name in dirs_to_copy:
            if Path(dir_name).exists():
                shutil.copytree(dir_name, dist_dir / dir_name, dirs_exist_ok=True)
        
        print("✅ Distribution package created in 'distribution/' folder")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create distribution: {e}")
        return False

def main():
    """Main deployment preparation function"""
    print("🚀 Virtual Pet AI Assistant - Deployment Preparation")
    print("=" * 55)
    
    steps = [
        ("Checking requirements", check_requirements),
        ("Installing build tools", install_build_tools), 
        ("Building executable", build_executable),
        ("Creating distribution package", create_distribution_package)
    ]
    
    for step_name, step_func in steps:
        print(f"\n⏳ {step_name}...")
        success = step_func()
        
        if not success:
            print(f"\n❌ Deployment preparation failed at: {step_name}")
            return 1
    
    print("\n" + "=" * 55)
    print("🎉 Deployment preparation completed successfully!")
    print("\n📁 Files ready for distribution:")
    print("   - distribution/VirtualPetAI.exe (Standalone executable)")
    print("   - distribution/README.md (Instructions)")
    print("   - distribution/QUICKSTART.md (Quick setup guide)")
    print("   - distribution/.env.example (Environment template)")
    print("\n💡 Next steps:")
    print("   1. Test the executable: distribution/VirtualPetAI.exe")
    print("   2. Distribute the entire 'distribution/' folder")
    print("   3. Users just need to add their API key to .env")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())