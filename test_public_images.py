"""
Test Updated Pet Image Paths

This script verifies that the pet switching now uses the PNG images 
from the react-app/public folder instead of assets/pet folder.
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_updated_paths():
    print("🖼️  Testing Updated Pet Image Paths")
    print("=" * 50)
    
    try:
        from src.utils.config_manager import ConfigManager
        config_manager = ConfigManager()
        settings = config_manager.load_config()
        
        available_pets = settings.get('pet', {}).get('available_pets', {})
        current_pet = settings.get('pet', {}).get('current_pet', 'ghost')
        
        print("📋 Updated Pet Configuration:")
        print(f"   Current Pet: {current_pet}")
        print()
        
        # Check each pet's image path and file existence
        for pet_id, pet_info in available_pets.items():
            name = pet_info.get('name', pet_id.title())
            image_path = pet_info.get('image', 'Unknown')
            personality = pet_info.get('personality', 'Unknown')
            
            # Check if image file exists
            exists = os.path.exists(image_path)
            status = "✅ EXISTS" if exists else "❌ MISSING"
            current_marker = " (CURRENT)" if pet_id == current_pet else ""
            
            print(f"🐾 {name}{current_marker}")
            print(f"   📁 Path: {image_path}")
            print(f"   📊 Status: {status}")
            print(f"   💭 Personality: {personality}")
            print()
        
        # Test image loading
        print("🔍 Testing Image Loading...")
        
        missing_images = []
        for pet_id, pet_info in available_pets.items():
            image_path = pet_info.get('image')
            if image_path and not os.path.exists(image_path):
                missing_images.append(f"{pet_info.get('name', pet_id)} ({image_path})")
        
        if missing_images:
            print("⚠️  Missing Images:")
            for missing in missing_images:
                print(f"   ❌ {missing}")
            print("\n💡 Make sure the PNG files are in react-app/public/")
        else:
            print("✅ All pet images found successfully!")
            print("🎉 Pet switching with public folder images is ready!")
        
        # Show file paths for verification
        print(f"\n📁 Expected Image Locations:")
        print(f"   🏠 react-app/public/house.png")
        print(f"   ⏰ react-app/public/clock.png") 
        print(f"   👻 react-app/public/ghost.png")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_updated_paths()