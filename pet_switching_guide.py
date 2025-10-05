"""
🎭 Pet Image Switching Guide

This shows you exactly where and how to switch the actual pet images.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def show_image_switching_guide():
    print("🎭 HOW TO SWITCH PET IMAGES - Complete Guide")
    print("=" * 60)
    
    print("\n🎮 METHOD 1: In-App Switching (Easiest)")
    print("   1. Run: python main.py")
    print("   2. Wait for the pet to appear on screen")
    print("   3. RIGHT-CLICK on the pet")
    print("   4. Select: Settings ►")
    print("   5. Select: Change Pet ►")
    print("   6. Choose: Ghost Pixie, Time Keeper, or Home Guardian")
    print("   7. Watch the pet change instantly!")
    
    print("\n📁 METHOD 2: Replace Image Files")
    print("   Location: react-app/public/")
    print("   Current files:")
    
    public_folder = "react-app/public/"
    images = ["ghost.png", "clock.png", "house.png"]
    
    for img in images:
        path = public_folder + img
        exists = os.path.exists(path)
        status = "✅" if exists else "❌"
        size_info = ""
        
        if exists:
            try:
                size = os.path.getsize(path)
                size_kb = size / 1024
                size_info = f" ({size_kb:.1f} KB)"
            except:
                pass
        
        print(f"   {status} {path}{size_info}")
    
    print("\n   📝 To replace images:")
    print("   • Replace ghost.png with your ghost image")
    print("   • Replace clock.png with your clock image")
    print("   • Replace house.png with your house image")
    print("   • Keep the same filenames!")
    
    print("\n⚙️  METHOD 3: Edit Configuration File")
    print("   File: config/settings.json")
    print("   Section to edit:")
    
    try:
        from src.utils.config_manager import ConfigManager
        config_manager = ConfigManager()
        settings = config_manager.load_config()
        
        available_pets = settings.get('pet', {}).get('available_pets', {})
        current_pet = settings.get('pet', {}).get('current_pet', 'ghost')
        
        print('   "available_pets": {')
        for pet_id, pet_info in available_pets.items():
            current_marker = " ← CURRENT" if pet_id == current_pet else ""
            print(f'     "{pet_id}": {{')
            print(f'       "name": "{pet_info.get("name", "Unknown")}",')
            print(f'       "image": "{pet_info.get("image", "Unknown")}",{current_marker}')
            print(f'       "personality": "{pet_info.get("personality", "Unknown")}"')
            print('     },')
        print('   }')
        
        print(f'\n   Current active pet: "{current_pet}"')
        
    except Exception as e:
        print(f"   ❌ Could not read config: {e}")
    
    print("\n🔄 METHOD 4: Command Line Switching")
    print("   Run these demo scripts:")
    print("   • python test_pet_switching_fixed.py  (Interactive)")
    print("   • python final_pet_demo.py           (Automatic)")
    
    print("\n📂 Current File Locations:")
    print("   🖼️  Images: react-app/public/*.png")
    print("   ⚙️  Config: config/settings.json")
    print("   🐾 Pet Logic: src/pet/pet_manager.py")
    
    print("\n💡 Quick Switch Tips:")
    print("   • Images auto-resize to pet window size")
    print("   • PNG format recommended for transparency")
    print("   • Changes save automatically")
    print("   • Restart pet app to see file replacements")
    
    print("\n🎯 What Happens When You Switch:")
    print("   1. Pet appearance changes immediately")
    print("   2. Personality message updates") 
    print("   3. Settings saved to config file")
    print("   4. Activity logged to CSV")
    print("   5. Speech bubble shows confirmation")

if __name__ == "__main__":
    show_image_switching_guide()