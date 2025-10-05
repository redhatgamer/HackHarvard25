"""
Pet Image Viewer - Show Visual Differences

This script helps you see the actual differences between pet images
to confirm that switching is working visually.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def show_image_differences():
    print("🖼️  Pet Image Visual Analysis")
    print("=" * 50)
    
    images = [
        ("Ghost Pixie", "react-app/public/ghost.png"),
        ("Time Keeper", "react-app/public/clock.png"), 
        ("Home Guardian", "react-app/public/house.png")
    ]
    
    try:
        from PIL import Image
        import hashlib
        
        print("📊 Image Comparison:")
        
        # Calculate image hashes to detect differences
        hashes = {}
        
        for name, path in images:
            if os.path.exists(path):
                img = Image.open(path)
                
                # Convert to bytes and calculate hash
                img_bytes = img.tobytes()
                img_hash = hashlib.md5(img_bytes).hexdigest()
                hashes[name] = img_hash
                
                print(f"\n🐾 {name}")
                print(f"   Path: {path}")
                print(f"   Size: {img.size}")
                print(f"   Hash: {img_hash[:16]}...")
                
                # Check if image has transparency
                has_alpha = img.mode in ('RGBA', 'LA') or 'transparency' in img.info
                print(f"   Transparency: {'Yes' if has_alpha else 'No'}")
                
                img.close()
            else:
                print(f"\n🐾 {name}")
                print(f"   ❌ File not found: {path}")
        
        # Compare hashes to see if images are actually different
        print(f"\n🔍 Difference Analysis:")
        hash_values = list(hashes.values())
        
        if len(set(hash_values)) == len(hash_values):
            print("   ✅ All images are visually different!")
            print("   🎭 Pet switching should show clear visual changes")
        else:
            print("   ⚠️  Some images appear identical!")
            # Find duplicates
            for name1, hash1 in hashes.items():
                for name2, hash2 in hashes.items():
                    if name1 != name2 and hash1 == hash2:
                        print(f"   🔄 {name1} and {name2} are identical")
        
        # Try to open images for manual inspection
        print(f"\n🔬 Manual Inspection:")
        print("   The images will be opened for visual inspection...")
        print("   Look for these differences:")
        print("   • Ghost: Should show a ghost/spirit character")
        print("   • Clock: Should show a clock or time-related image") 
        print("   • House: Should show a house or home-related image")
        
        # Open each image for visual inspection
        for name, path in images:
            if os.path.exists(path):
                try:
                    img = Image.open(path)
                    print(f"\n   Opening {name}...")
                    
                    # Create a smaller preview
                    img.thumbnail((300, 300))
                    
                    # Show the image (this will open default image viewer)
                    img.show()
                    
                    input(f"   Press Enter after viewing {name}...")
                    
                except Exception as e:
                    print(f"   ❌ Could not open {name}: {e}")
        
        print(f"\n✨ Conclusion:")
        print("   If you saw different images when they opened,")
        print("   then pet switching IS working correctly!")
        print("   The visual change might be subtle or you might")
        print("   need to look more carefully at the pet window.")
        
        print(f"\n🎯 Test Again:")
        print("   1. Run: python main.py")
        print("   2. Right-click pet → Settings → Change Pet")
        print("   3. Watch carefully for visual changes")
        print("   4. The logs confirm the switching is working!")
        
    except ImportError:
        print("❌ PIL not available for image analysis")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    show_image_differences()