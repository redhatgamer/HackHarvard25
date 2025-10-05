"""
Pet Image Switching Diagnostic Tool

This script helps diagnose why the pet image might not be changing visually.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def run_image_switch_diagnostic():
    print("🔍 Pet Image Switching Diagnostic")
    print("=" * 50)
    
    try:
        from src.utils.config_manager import ConfigManager
        config_manager = ConfigManager()
        settings = config_manager.load_config()
        
        current_pet = settings.get('pet', {}).get('current_pet', 'ghost')
        available_pets = settings.get('pet', {}).get('available_pets', {})
        
        print(f"📋 Current Configuration:")
        print(f"   Active Pet: {current_pet}")
        
        # Check each pet's image
        print(f"\n🖼️  Image File Analysis:")
        for pet_id, pet_info in available_pets.items():
            name = pet_info.get('name', pet_id.title())
            image_path = pet_info.get('image', 'Unknown')
            
            # Check file existence and properties
            exists = os.path.exists(image_path)
            status = "✅ EXISTS" if exists else "❌ MISSING"
            current_marker = " (CURRENT)" if pet_id == current_pet else ""
            
            print(f"\n   🐾 {name}{current_marker}")
            print(f"      Path: {image_path}")
            print(f"      Status: {status}")
            
            if exists:
                try:
                    size = os.path.getsize(image_path)
                    size_kb = size / 1024
                    print(f"      Size: {size_kb:.1f} KB")
                    
                    # Try to load with PIL
                    from PIL import Image
                    img = Image.open(image_path)
                    print(f"      Dimensions: {img.size[0]}x{img.size[1]}")
                    print(f"      Format: {img.format}")
                    print(f"      Mode: {img.mode}")
                    img.close()
                    
                except Exception as e:
                    print(f"      ❌ PIL Error: {e}")
        
        # Test image switching
        print(f"\n🔄 Testing Pet Switching...")
        
        # Switch to each pet and verify
        for pet_id in available_pets.keys():
            print(f"\n   Switching to {pet_id}...")
            
            # Update config
            settings['pet']['current_pet'] = pet_id
            config_manager.save_config(settings)
            
            # Verify the change
            new_settings = config_manager.load_config()
            new_current = new_settings.get('pet', {}).get('current_pet')
            
            if new_current == pet_id:
                print(f"   ✅ Config updated successfully")
            else:
                print(f"   ❌ Config update failed: expected {pet_id}, got {new_current}")
        
        print(f"\n💡 Diagnostic Results:")
        
        # Check for common issues
        issues_found = []
        
        # Check if all images exist
        missing_images = []
        for pet_id, pet_info in available_pets.items():
            image_path = pet_info.get('image')
            if not os.path.exists(image_path):
                missing_images.append(f"{pet_info.get('name', pet_id)} ({image_path})")
        
        if missing_images:
            issues_found.append("Missing image files")
            print(f"   ❌ Missing Images:")
            for missing in missing_images:
                print(f"      - {missing}")
        
        # Check image format
        for pet_id, pet_info in available_pets.items():
            image_path = pet_info.get('image')
            if os.path.exists(image_path):
                try:
                    from PIL import Image
                    img = Image.open(image_path)
                    if img.mode not in ['RGB', 'RGBA']:
                        issues_found.append(f"Image {pet_id} has unsupported mode: {img.mode}")
                    img.close()
                except Exception as e:
                    issues_found.append(f"Image {pet_id} cannot be loaded: {e}")
        
        if not issues_found:
            print(f"   ✅ No obvious issues found")
            print(f"   💡 Try running the pet app and check the logs for errors")
        else:
            print(f"   ⚠️  Issues found:")
            for issue in issues_found:
                print(f"      - {issue}")
        
        print(f"\n🚀 Quick Fix Suggestions:")
        print(f"   1. Make sure all PNG files exist in react-app/public/")
        print(f"   2. Restart the pet application after changes")
        print(f"   3. Check the console logs for detailed error messages")
        print(f"   4. Try switching pets through the right-click menu")
        
    except Exception as e:
        print(f"❌ Diagnostic failed: {e}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")

if __name__ == "__main__":
    run_image_switch_diagnostic()