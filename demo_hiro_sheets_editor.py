"""
Hiro's Smart Google Sheets Editing Demo

This shows how Hiro can intelligently reorganize, clean up, and enhance 
existing Google Sheets data with AI-powered suggestions and automated fixes.
"""

import csv
import os
from datetime import datetime, timedelta

class HiroSheetsEditor:
    """Demonstrates Hiro's intelligent Google Sheets editing capabilities"""
    
    def __init__(self, input_file="hiro_steam_analysis.csv"):
        self.input_file = input_file
        self.output_file = "hiro_organized_steam_data.csv"
        self.original_data = []
        self.organized_data = []
    
    def load_existing_data(self):
        """Load the existing Steam data from Google Sheets export"""
        print("📊 Hiro is analyzing your Google Sheets data...")
        print("=" * 50)
        
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.original_data = list(reader)
            
            print(f"✅ Loaded {len(self.original_data)} entries from Google Sheets")
            return True
        except FileNotFoundError:
            print(f"❌ Could not find {self.input_file}")
            return False
    
    def analyze_and_reorganize(self):
        """Hiro analyzes the data and applies intelligent reorganization"""
        
        print(f"\n🤖 Hiro's AI Analysis & Reorganization:")
        print("=" * 50)
        
        # Sort by different criteria and add new insights
        print("🔄 Step 1: Smart Sorting & Categorization")
        
        # Sort by value (worst to best deals)
        sorted_by_value = sorted(self.original_data, key=lambda x: self._extract_price_per_hour(x), reverse=True)
        
        print("   📈 Sorting by cost-effectiveness (worst to best deals)")
        print("   📊 Adding spending priority recommendations")
        print("   🎯 Categorizing purchase patterns")
        
        # Add Hiro's enhanced analysis
        for i, item in enumerate(sorted_by_value):
            # Add priority score
            priority = self._calculate_priority_score(item)
            item['Hiro_Priority'] = priority
            
            # Add category insights
            item['Spending_Pattern'] = self._analyze_spending_pattern(item)
            
            # Add action recommendations
            item['Action_Needed'] = self._get_action_recommendation(item)
            
            # Add financial impact
            item['Financial_Impact'] = self._calculate_financial_impact(item)
        
        self.organized_data = sorted_by_value
        
        print("✅ Data reorganized with AI insights")
    
    def _extract_price_per_hour(self, item):
        """Extract numeric price per hour for sorting"""
        pph = item.get('Price per Hour', 'N/A')
        if 'N/A' in pph or '$inf' in pph:
            return 999999  # Put infinite/no-play items at top
        try:
            return float(pph.replace('$', '').replace('/h', ''))
        except:
            return 0
    
    def _calculate_priority_score(self, item):
        """Hiro calculates a priority score for each purchase"""
        hours = float(item.get('Hours Played', '0h').replace('h', ''))
        price = float(item.get('Price', '$0').replace('$', ''))
        
        if hours < 1 and price > 30:
            return "🚨 HIGH - Refund Candidate"
        elif hours < 5 and price > 50:
            return "⚠️ MEDIUM - Buyer's Remorse Risk"
        elif hours > 100:
            return "⭐ ADDICTION - Monitor Time"
        elif price == 0 and hours > 20:
            return "💎 EXCELLENT - Free Value Winner"
        elif hours > 0 and (price / hours) < 1:
            return "✅ GOOD - Solid Investment"
        else:
            return "📊 NORMAL - Standard Purchase"
    
    def _analyze_spending_pattern(self, item):
        """Analyze spending patterns"""
        category = item.get('Category', '')
        price = float(item.get('Price', '$0').replace('$', ''))
        
        if 'Cosmetic' in item.get('Purchase Type', ''):
            return "💸 Cosmetic Spender"
        elif category == 'RPG' and price > 40:
            return "🐉 RPG Enthusiast"
        elif category == 'FPS' and price == 0:
            return "🎯 F2P FPS Player"
        elif price > 60:
            return "💰 Premium Buyer"
        elif price < 15:
            return "💵 Budget Conscious"
        else:
            return "🎮 Balanced Gamer"
    
    def _get_action_recommendation(self, item):
        """Hiro's specific action recommendations"""
        hours = float(item.get('Hours Played', '0h').replace('h', ''))
        price = float(item.get('Price', '$0').replace('$', ''))
        category = item.get('Category', '')
        
        if hours < 1 and price > 30:
            return "Request Steam refund (within 14 days)"
        elif hours < 5 and price > 50:
            return "Play 2+ hours to evaluate or refund"
        elif category == 'RPG' and hours > 50:
            return "Look for similar RPGs on sale"
        elif 'Cosmetic' in item.get('Purchase Type', '') and price > 20:
            return "Set monthly cosmetic budget limit"
        elif hours > 100:
            return "Consider time management tools"
        elif price == 0 and hours > 50:
            return "Support developer with DLC purchase"
        else:
            return "Monitor for future sale patterns"
    
    def _calculate_financial_impact(self, item):
        """Calculate the financial impact and potential savings"""
        hours = float(item.get('Hours Played', '0h').replace('h', ''))
        price = float(item.get('Price', '$0').replace('$', ''))
        
        if hours < 1 and price > 30:
            return f"-${price:.2f} (Potential refund)"
        elif hours < 5 and price > 50:
            return f"-${price*0.7:.2f} (Likely regret purchase)"
        elif hours > 0 and (price / hours) < 0.5:
            return f"+${price*2:.2f} (Exceptional value received)"
        elif hours > 50:
            return f"+${hours*0.5:.2f} (Entertainment value delivered)"
        else:
            return f"${0:.2f} (Neutral impact)"
    
    def create_organized_spreadsheet(self):
        """Create the new organized spreadsheet with Hiro's enhancements"""
        
        print(f"\n📋 Creating Hiro's Organized Spreadsheet:")
        print("=" * 50)
        
        # New enhanced headers
        headers = [
            'Rank', 'Game/Item', 'Price', 'Hours Played', 'Price per Hour',
            'Category', 'Hiro_Priority', 'Spending_Pattern', 'Action_Needed',
            'Financial_Impact', 'Original_Analysis', 'Enhanced_Recommendations'
        ]
        
        with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            
            for i, item in enumerate(self.organized_data, 1):
                # Enhanced recommendations based on all data
                enhanced_rec = self._generate_enhanced_recommendation(item, i)
                
                writer.writerow([
                    f"#{i}",
                    item.get('Game/Item', ''),
                    item.get('Price', ''),
                    item.get('Hours Played', ''),
                    item.get('Price per Hour', ''),
                    item.get('Category', ''),
                    item.get('Hiro_Priority', ''),
                    item.get('Spending_Pattern', ''),
                    item.get('Action_Needed', ''),
                    item.get('Financial_Impact', ''),
                    item.get('Hiro Analysis', ''),
                    enhanced_rec
                ])
        
        print(f"✅ Created organized spreadsheet: {self.output_file}")
    
    def _generate_enhanced_recommendation(self, item, rank):
        """Generate enhanced recommendations based on ranking and patterns"""
        
        if rank <= 3:
            return "🚨 TOP PRIORITY: Address immediately to improve spending efficiency"
        elif rank <= 5:
            return "⚠️ HIGH PRIORITY: Review and take corrective action"
        elif 'EXCELLENT' in item.get('Hiro_Priority', ''):
            return "💎 MAINTAIN PATTERN: This category works well for you"
        elif 'RPG' in item.get('Category', ''):
            return "🐉 RPG LOVER: Consider Witcher series, Mass Effect, or Divinity games"
        elif 'FPS' in item.get('Category', ''):
            return "🎯 FPS FOCUS: Try Apex Legends, Valorant, or Overwatch 2"
        else:
            return "📊 MONITOR: Track future purchases in this category"
    
    def show_hiro_improvements(self):
        """Display what Hiro improved in the organization"""
        
        print(f"\n🎯 Hiro's Smart Improvements:")
        print("=" * 50)
        
        improvements = [
            "📊 Ranked all purchases by cost-effectiveness (worst first)",
            "🎯 Added priority scoring system for immediate action items",
            "💡 Identified spending patterns across categories",
            "🚨 Flagged refund opportunities and buyer's remorse risks",
            "💎 Highlighted exceptional value purchases to repeat",
            "📈 Calculated financial impact of each decision",
            "🤖 Generated personalized action recommendations",
            "🎮 Added gaming behavior insights and addiction warnings"
        ]
        
        for improvement in improvements:
            print(f"   {improvement}")
        
        print(f"\n💰 Financial Insights Hiro Added:")
        
        # Calculate summary statistics
        total_waste = sum(float(item.get('Price', '$0').replace('$', '')) 
                         for item in self.organized_data 
                         if '🚨 HIGH' in item.get('Hiro_Priority', ''))
        
        excellent_games = len([item for item in self.organized_data 
                              if 'EXCELLENT' in item.get('Hiro_Priority', '')])
        
        print(f"   💸 Potential refund value: ${total_waste:.2f}")
        print(f"   💎 Excellent value games found: {excellent_games}")
        print(f"   🎯 Actionable recommendations: {len(self.organized_data)}")
    
    def show_google_sheets_instructions(self):
        """Show how to import the improved data back to Google Sheets"""
        
        print(f"\n📊 Import Hiro's Improvements to Google Sheets:")
        print("=" * 50)
        print(f"📂 New organized file: {self.output_file}")
        print(f"🌐 Steps:")
        print(f"   1. Go back to your Google Sheet")
        print(f"   2. Create a new tab called 'Hiro Organized'")
        print(f"   3. Drag and drop '{self.output_file}' into the new tab")
        print(f"   4. See Hiro's AI organization and recommendations!")
        
        print(f"\n✨ New Features You'll See:")
        print(f"   📊 Rank column - prioritized by urgency")
        print(f"   🎯 Priority scores - immediate action items")
        print(f"   💡 Spending patterns - understand your habits")
        print(f"   🚨 Action needed - specific next steps")
        print(f"   💰 Financial impact - money saved/wasted")
        print(f"   🤖 Enhanced recommendations - personalized advice")

def main():
    """Run Hiro's Google Sheets editing demo"""
    
    print("🤖 Hiro's Smart Google Sheets Editor")
    print("🎯 Demonstrating AI-Powered Data Organization")
    print("=" * 60)
    
    editor = HiroSheetsEditor()
    
    # Load and analyze existing data
    if not editor.load_existing_data():
        print("❌ Please make sure hiro_steam_analysis.csv exists first!")
        return
    
    # Show Hiro analyzing and reorganizing
    editor.analyze_and_reorganize()
    
    # Create the improved spreadsheet
    editor.create_organized_spreadsheet()
    
    # Show what Hiro improved
    editor.show_hiro_improvements()
    
    # Show Google Sheets integration
    editor.show_google_sheets_instructions()
    
    print(f"\n🎉 Demo Complete!")
    print(f"🤖 Hiro transformed your raw data into actionable business intelligence")
    print(f"📊 Ready to show judges how AI can actively improve spreadsheet organization!")

if __name__ == "__main__":
    main()