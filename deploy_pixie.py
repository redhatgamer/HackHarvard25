"""
Pixie Pet Deployment Script
Creates an executable (.exe) file from the Python project
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_executable():
    """Create executable using PyInstaller with optimal settings for Pixie"""
    
    print("🦎 Starting Pixie Pet Deployment...")
    print("=" * 50)
    
    # Get current directory
    project_dir = Path(__file__).parent
    main_script = project_dir / "main.py"
    
    if not main_script.exists():
        print("❌ Error: main.py not found!")
        return False
    
    # PyInstaller command with optimized settings for Pixie
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window (GUI app)
        "--name=PixiePet",              # Name of the executable
        "--icon=assets/pet/ghost.png",  # Use ghost as icon (if available)
        
        # Include data files and directories
        "--add-data", "assets;assets",
        "--add-data", "config;config", 
        "--add-data", "src;src",
        
        # Include hidden imports that PyInstaller might miss
        "--hidden-import", "PIL._tkinter_finder",
        "--hidden-import", "google.generativeai",
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.ttk",
        "--hidden-import", "pystray",
        "--hidden-import", "dotenv",
        
        # Exclude unnecessary modules to reduce size
        "--exclude-module", "matplotlib",
        "--exclude-module", "numpy",
        "--exclude-module", "scipy",
        
        # Main script
        str(main_script)
    ]
    
    print("🔧 Building executable with PyInstaller...")
    print("Command:", " ".join(cmd[:5]) + " ...")
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_dir)
        
        if result.returncode == 0:
            print("✅ Build completed successfully!")
            
            # Check if executable was created
            exe_path = project_dir / "dist" / "PixiePet.exe"
            if exe_path.exists():
                exe_size = exe_path.stat().st_size / (1024 * 1024)  # MB
                print(f"📦 Executable created: {exe_path}")
                print(f"📏 File size: {exe_size:.1f} MB")
                
                # Copy important files to dist folder
                dist_dir = project_dir / "dist"
                
                # Copy assets if not included properly
                if not (dist_dir / "assets").exists() and (project_dir / "assets").exists():
                    shutil.copytree(project_dir / "assets", dist_dir / "assets")
                    print("📂 Copied assets folder")
                
                # Copy config if not included properly  
                if not (dist_dir / "config").exists() and (project_dir / "config").exists():
                    shutil.copytree(project_dir / "config", dist_dir / "config")
                    print("⚙️ Copied config folder")
                
                # Create a simple README for distribution
                readme_content = """🦎 Pixie Pet - Your AI Desktop Companion

INSTALLATION:
1. Make sure PixiePet.exe, assets/, and config/ folders are in the same directory
2. Double-click PixiePet.exe to run
3. Right-click on Pixie for context menu options

REQUIREMENTS:
- Windows 7 or later
- Internet connection for AI features
- Gemini API key (configure in config/settings.json)

TROUBLESHOOTING:
- If Pixie doesn't appear, check Windows Defender/antivirus
- For AI features, make sure GEMINI_API_KEY environment variable is set
- Config files are in the config/ folder

Enjoy your new desktop companion! 🎉
"""
                
                with open(dist_dir / "README.txt", "w") as f:
                    f.write(readme_content)
                
                print("📋 Created README.txt")
                print("\n🎉 Deployment complete!")
                print(f"📍 Find your executable at: {dist_dir}")
                print("\n💡 Distribution tips:")
                print("   • Include the entire 'dist' folder when sharing")
                print("   • Users need the assets and config folders")
                print("   • Consider creating an installer for easier distribution")
                
                return True
            else:
                print("❌ Executable not found after build")
                return False
        else:
            print("❌ Build failed!")
            print("Error output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error during build: {e}")
        return False

def create_installer_script():
    """Create an NSIS installer script for professional distribution"""
    
    installer_script = '''
; Pixie Pet Installer Script (NSIS)
!define APPNAME "Pixie Pet"
!define COMPANYNAME "Your Company"
!define DESCRIPTION "AI-Powered Desktop Companion"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define HELPURL "https://github.com/yourusername/pixie-pet"
!define UPDATEURL "https://github.com/yourusername/pixie-pet/releases"
!define ABOUTURL "https://github.com/yourusername/pixie-pet"
!define INSTALLSIZE 50000  # Estimate size in KB

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\\${APPNAME}"
Name "${APPNAME}"
outFile "PixiePetInstaller.exe"
 
page directory
page instfiles
 
section "install"
    setOutPath $INSTDIR
    file /r "dist\\*.*"
    
    # Create desktop shortcut
    createShortCut "$DESKTOP\\${APPNAME}.lnk" "$INSTDIR\\PixiePet.exe"
    
    # Create start menu shortcut  
    createDirectory "$SMPROGRAMS\\${APPNAME}"
    createShortCut "$SMPROGRAMS\\${APPNAME}\\${APPNAME}.lnk" "$INSTDIR\\PixiePet.exe"
    createShortCut "$SMPROGRAMS\\${APPNAME}\\Uninstall.lnk" "$INSTDIR\\uninstall.exe"
    
    # Registry info for add/remove programs
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "DisplayName" "${APPNAME} - ${DESCRIPTION}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "UninstallString" "$INSTDIR\\uninstall.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "DisplayIcon" "$INSTDIR\\PixiePet.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "Publisher" "${COMPANYNAME}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "HelpLink" "${HELPURL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "URLUpdateInfo" "${UPDATEURL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "URLInfoAbout" "${ABOUTURL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}"
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "VersionMinor" ${VERSIONMINOR}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "EstimatedSize" ${INSTALLSIZE}
    
    writeUninstaller "$INSTDIR\\uninstall.exe"
sectionEnd

section "uninstall"
    delete "$DESKTOP\\${APPNAME}.lnk"
    rmDir /r "$SMPROGRAMS\\${APPNAME}"
    rmDir /r "$INSTDIR"
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}"
sectionEnd
'''
    
    with open("pixie_installer.nsi", "w") as f:
        f.write(installer_script)
    
    print("📝 Created installer script: pixie_installer.nsi")
    print("💡 To build installer:")
    print("   1. Install NSIS (Nullsoft Scriptable Install System)")
    print("   2. Right-click pixie_installer.nsi → 'Compile NSIS Script'")

if __name__ == "__main__":
    print("🦎 Pixie Pet Deployment Tool")
    print("Choose an option:")
    print("1. Create executable (.exe)")
    print("2. Create installer script (.nsi)")
    print("3. Both")
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    if choice in ["1", "3"]:
        success = create_executable()
        if not success:
            sys.exit(1)
    
    if choice in ["2", "3"]:
        create_installer_script()
    
    print("\n🎉 Deployment process complete!")