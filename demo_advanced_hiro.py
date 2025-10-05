"""
Advanced Hiro Demo - Showcasing Complex AI Capabilities

This demonstrates advanced features that really show off Gemini's power.
"""

import asyncio
import sys
import os

def demo_advanced_capabilities():
    """Show advanced AI capabilities for live demo"""
    
    print("🚀 Hiro's Advanced AI Capabilities Demo")
    print("🎯 Perfect for Live Hackathon Presentation")
    print("=" * 60)
    
    demos = [
        {
            "title": "📸 Multi-Modal Analysis",
            "description": "Hiro can analyze screenshots + text + voice simultaneously",
            "demo_script": [
                "1. Open multiple browser tabs with different content",
                "2. Ask Hiro: 'Analyze everything on my screen and give me a productivity report'",
                "3. Show: Gemini processing visual + textual information together"
            ]
        },
        {
            "title": "🧠 Context Memory & Learning",
            "description": "Hiro remembers conversation history and builds context",
            "demo_script": [
                "1. Start conversation: 'I'm working on a hackathon project'",
                "2. Later ask: 'What was I working on earlier?'",
                "3. Show: Hiro maintains context across interactions"
            ]
        },
        {
            "title": "💡 Intelligent Code Generation",
            "description": "Ask Hiro to write code based on what it sees",
            "demo_script": [
                "1. Show a half-written function on screen",
                "2. Ask: 'Complete this function for me'",
                "3. Show: Hiro generating contextually appropriate code"
            ]
        },
        {
            "title": "🔍 Real-Time Error Detection",
            "description": "Hiro spots bugs and issues as you code",
            "demo_script": [
                "1. Write code with intentional syntax error",
                "2. Ask: 'Is there anything wrong with this code?'",
                "3. Show: Immediate bug detection and fix suggestions"
            ]
        },
        {
            "title": "📊 Data Analysis & Visualization",
            "description": "Hiro can analyze data and suggest visualizations",
            "demo_script": [
                "1. Open spreadsheet or CSV file",
                "2. Ask: 'What insights can you extract from this data?'",
                "3. Show: AI-powered data analysis and recommendations"
            ]
        },
        {
            "title": "🎯 Project Management Assistant",
            "description": "Hiro helps organize and prioritize work",
            "demo_script": [
                "1. Show your project files/folders",
                "2. Ask: 'Help me prioritize what to work on next'",
                "3. Show: Intelligent project analysis and recommendations"
            ]
        }
    ]
    
    print("\n🎭 Choose Your Demo Focus Based on Audience:")
    print("=" * 50)
    
    for i, demo in enumerate(demos, 1):
        print(f"\n{i}. {demo['title']}")
        print(f"   💫 {demo['description']}")
        print(f"   📝 Live Demo Script:")
        for step in demo['demo_script']:
            print(f"      {step}")
    
    print(f"\n🏆 Pro Tips for Maximum Impact:")
    print("=" * 50)
    print("🎯 Start with screen analysis (most visual impact)")
    print("🎤 Use voice commands (shows multi-modal AI)")
    print("💻 Demo with real code (shows practical value)")
    print("🔄 Show personality switching (unique differentiator)")
    print("📊 End with Google Sheets integration (business value)")
    
    print(f"\n💡 Backup Demos if Something Fails:")
    print("=" * 50)
    print("🎮 Steam purchase analysis (already working)")
    print("📂 File organization suggestions")
    print("💬 Simple chat conversation")
    print("🌐 React web interface (deployed and working)")
    
    return demos

def create_quick_error_file():
    """Create a file with intentional errors for live demo"""
    
    error_code = '''
def calculate_average(numbers):
    total = 0
    count = 0
    for num in numbers
        total += num
        count += 1
    return total / count  # Potential division by zero

def process_data(data):
    results = []
    for item in data:
        if item > 0
            results.append(item * 2)
    return results

# Missing function call
calculate_average([1, 2, 3, 4, 5])
'''
    
    with open("demo_error_file.py", "w") as f:
        f.write(error_code)
    
    print("📄 Created demo_error_file.py with intentional errors")
    print("💡 Use this for live bug detection demo!")

def main():
    """Run the advanced demo preparation"""
    demos = demo_advanced_capabilities()
    create_quick_error_file()
    
    print(f"\n🎉 Ready for Advanced Hiro Demo!")
    print(f"📋 You now have {len(demos)} powerful demo scenarios")
    print(f"🐛 Error file ready for bug detection demo")
    print(f"🚀 Launch Hiro with: python main.py")

if __name__ == "__main__":
    main()