"""
Final Pet Switching Demo

Shows the complete pet switching workflow from configuration to visual change.
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def demo_config_switching():
    print("🎭 Final Pet Switching Demo")
    print("=" * 50)
    
    try:
        from src.utils.config_manager import ConfigManager
        config_manager = ConfigManager()
        
        print("📋 Testing all pet switches...\n")
        
        # Test switching to each pet
        pets = ['ghost', 'clock', 'house']
        
        for i, pet in enumerate(pets, 1):
            print(f"{i}. Switching to {pet}...")
            
            # Load current settings
            settings = config_manager.load_config()
            old_pet = settings.get('pet', {}).get('current_pet', 'unknown')
            
            # Switch pet
            settings['pet']['current_pet'] = pet
            config_manager.save_config(settings)
            
            # Verify the change
            new_settings = config_manager.load_config()
            current_pet = new_settings.get('pet', {}).get('current_pet')
            
            if current_pet == pet:
                pet_info = new_settings.get('pet', {}).get('available_pets', {}).get(pet, {})
                pet_name = pet_info.get('name', pet.title())
                personality = pet_info.get('personality', 'Unknown')
                image = pet_info.get('image', 'Unknown')
                
                print(f"   ✅ Success! Changed from '{old_pet}' to '{pet}'")
                print(f"   🎭 Name: {pet_name}")
                print(f"   💭 Personality: {personality}")
                print(f"   🖼️  Image: {image}")
            else:
                print(f"   ❌ Failed to switch to {pet}")
            
            print()
        
        print("🎉 All pet switching tests completed!")
        print("\n🚀 Ready to use with the pet application!")
        print("\n💡 Usage: Right-click pet → Settings ► Change Pet ► Choose your favorite!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    demo_config_switching()