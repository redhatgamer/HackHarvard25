"""
Demo script to test the complete pet switching functionality

This runs the pet and allows testing of:
1. Right-click menu
2. Settings submenu  
3. Pet selection submenu
4. Actual pet switching with visual updates
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def run_pet_demo():
    print("🎭 Starting Pet Switching Demo")
    print("Instructions:")
    print("1. The pet will appear on screen")
    print("2. Right-click on the pet")
    print("3. Go to Settings ► Change Pet ►")
    print("4. Choose from Ghost Pixie, Time Keeper, or Home Guardian")
    print("5. Watch the pet change appearance and personality!")
    print("\nStarting pet in 3 seconds...")
    
    await asyncio.sleep(3)
    
    # Import and run the main pet
    try:
        from main import main
        await main()
    except KeyboardInterrupt:
        print("\n👋 Pet demo ended!")
    except Exception as e:
        print(f"❌ Error running pet: {e}")

if __name__ == "__main__":
    asyncio.run(run_pet_demo())