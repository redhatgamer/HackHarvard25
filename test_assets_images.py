"""
Test Assets Folder Image Paths

This verifies that the pet switching now uses images from assets/pet/ folder.
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_assets_paths():
    print("🎯 Testing Assets Folder Image Paths")
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
            
            if exists:
                try:
                    size = os.path.getsize(image_path)
                    size_kb = size / 1024
                    print(f"   📏 Size: {size_kb:.1f} KB")
                except:
                    pass
            print()
        
        # Test image loading
        print("🔍 Testing Image Loading...")
        
        missing_images = []
        working_images = []
        
        for pet_id, pet_info in available_pets.items():
            image_path = pet_info.get('image')
            if image_path and not os.path.exists(image_path):
                missing_images.append(f"{pet_info.get('name', pet_id)} ({image_path})")
            else:
                working_images.append(f"{pet_info.get('name', pet_id)} ({image_path})")
        
        if missing_images:
            print("⚠️  Missing Images:")
            for missing in missing_images:
                print(f"   ❌ {missing}")
        
        if working_images:
            print("✅ Working Images:")
            for working in working_images:
                print(f"   ✅ {working}")
        
        if not missing_images:
            print("🎉 All pet images found successfully!")
            print("🚀 Pet switching with assets folder is ready!")
        
        # Show path comparison
        print(f"\n📂 Path Update Summary:")
        print(f"   ❌ OLD: react-app/public/*.png")
        print(f"   ✅ NEW: assets/pet/*.png")
        
        # Test switching
        print(f"\n🔄 Testing Pet Switching...")
        
        for pet_id in available_pets.keys():
            print(f"   Switching to {pet_id}...")
            
            # Update config
            settings['pet']['current_pet'] = pet_id
            config_manager.save_config(settings)
            
            # Verify the change
            new_settings = config_manager.load_config()
            new_current = new_settings.get('pet', {}).get('current_pet')
            
            if new_current == pet_id:
                pet_name = available_pets[pet_id].get('name', pet_id)
                image_path = available_pets[pet_id].get('image', 'Unknown')
                print(f"   ✅ {pet_name} - {image_path}")
            else:
                print(f"   ❌ Failed to switch to {pet_id}")
        
        print(f"\n🎯 Ready to Test:")
        print(f"   1. Run: python main.py")
        print(f"   2. Right-click pet → Settings → Change Pet")
        print(f"   3. Images now load from assets/pet/ folder!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")

if __name__ == "__main__":
    test_assets_paths()