"""
Pet Switching Demo

This script demonstrates the new pet switching functionality
allowing users to choose between Ghost Pixie, Time Keeper, and Home Guardian.
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.config_manager import ConfigManager
import json

def demo_pet_switching():
    print("🎭 Pet Switching Demo")
    print("=" * 40)
    
    # Load current config
    config_manager = ConfigManager()
    settings = config_manager.load_config()
    
    # Show available pets
    available_pets = settings.get('pet', {}).get('available_pets', {})
    current_pet = settings.get('pet', {}).get('current_pet', 'ghost')
    
    print(f"\n📋 Available Pets:")
    for pet_id, pet_info in available_pets.items():
        status = " (CURRENT)" if pet_id == current_pet else ""
        print(f"  {pet_id}: {pet_info.get('name', 'Unknown')} - {pet_info.get('personality', 'No personality')}{status}")
    
    print(f"\n🎯 Current Pet: {current_pet}")
    
    # Interactive pet switching
    print("\n" + "="*40)
    print("📱 Interactive Pet Switching")
    print("Available options:")
    print("1. Ghost Pixie (mysterious and helpful)")
    print("2. Time Keeper (punctual and organized)")
    print("3. Home Guardian (cozy and protective)")
    print("4. Show current settings")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\n🔍 Enter your choice (1-5): ").strip()
            
            if choice == '1':
                switch_pet('ghost', config_manager)
            elif choice == '2':
                switch_pet('clock', config_manager)
            elif choice == '3':
                switch_pet('house', config_manager)
            elif choice == '4':
                show_current_settings(config_manager)
            elif choice == '5':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def switch_pet(pet_type, config_manager):
    """Switch to a different pet"""
    try:
        settings = config_manager.load_config()
        available_pets = settings.get('pet', {}).get('available_pets', {})
        
        if pet_type not in available_pets:
            print(f"❌ Pet type '{pet_type}' not available!")
            return
        
        # Update current pet
        old_pet = settings.get('pet', {}).get('current_pet', 'ghost')
        settings['pet']['current_pet'] = pet_type
        
        # Save settings
        config_manager.save_config(settings)
        
        # Show confirmation
        pet_info = available_pets[pet_type]
        pet_name = pet_info.get('name', pet_type.title())
        personality = pet_info.get('personality', 'helpful')
        
        print(f"✅ Successfully switched from {old_pet} to {pet_type}")
        print(f"🎭 You're now using: {pet_name}")
        print(f"💭 Personality: {personality}")
        print(f"🖼️  Image: {pet_info.get('image', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error switching pet: {e}")

def show_current_settings(config_manager):
    """Show current pet settings"""
    try:
        settings = config_manager.load_config()
        current_pet = settings.get('pet', {}).get('current_pet', 'ghost')
        available_pets = settings.get('pet', {}).get('available_pets', {})
        
        print(f"\n📊 Current Pet Settings:")
        print(f"  Active Pet: {current_pet}")
        
        if current_pet in available_pets:
            pet_info = available_pets[current_pet]
            print(f"  Name: {pet_info.get('name', 'Unknown')}")
            print(f"  Personality: {pet_info.get('personality', 'Unknown')}")
            print(f"  Image: {pet_info.get('image', 'Unknown')}")
        
        print(f"\n📋 All Available Pets:")
        for pet_id, pet_info in available_pets.items():
            status = " ✅" if pet_id == current_pet else ""
            print(f"  - {pet_id}: {pet_info.get('name', 'Unknown')}{status}")
            
    except Exception as e:
        print(f"❌ Error showing settings: {e}")

if __name__ == "__main__":
    demo_pet_switching()