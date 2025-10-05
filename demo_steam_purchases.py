"""
Steam Purchase Analysis Demo with Hiro AI

This creates fake Steam purchase data and shows how Hiro can analyze spending patterns,
detect issues, and provide intelligent recommendations.
"""

import csv
import os
from datetime import datetime, timedelta
import random
import webbrowser

class SteamPurchaseAnalyzer:
    """Generate fake Steam data and show Hiro's AI analysis capabilities"""
    
    def __init__(self):
        self.filename = "hiro_steam_analysis.csv"
        self.games_data = [
            {"name": "Cyberpunk 2077", "price": 59.99, "category": "RPG", "hours_played": 0.2},
            {"name": "Counter-Strike 2", "price": 0.00, "category": "FPS", "hours_played": 150.5},
            {"name": "Baldur's Gate 3", "price": 59.99, "category": "RPG", "hours_played": 89.3},
            {"name": "Call of Duty: MW3", "price": 69.99, "category": "FPS", "hours_played": 12.1},
            {"name": "Factorio", "price": 35.00, "category": "Strategy", "hours_played": 234.7},
            {"name": "The Witcher 3", "price": 9.99, "category": "RPG", "hours_played": 95.2},
            {"name": "Destiny 2 DLC", "price": 39.99, "category": "FPS", "hours_played": 2.3},
            {"name": "Stardew Valley", "price": 14.99, "category": "Simulation", "hours_played": 67.8},
            {"name": "Red Dead Redemption 2", "price": 29.99, "category": "Action", "hours_played": 5.1},
            {"name": "Hades", "price": 24.99, "category": "Roguelike", "hours_played": 45.6},
            {"name": "Among Us", "price": 4.99, "category": "Social", "hours_played": 0.8},
            {"name": "Fall Guys", "price": 0.00, "category": "Battle Royale", "hours_played": 3.2},
            {"name": "Elden Ring", "price": 59.99, "category": "RPG", "hours_played": 78.9},
            {"name": "CS:GO Skins", "price": 127.50, "category": "Cosmetic", "hours_played": 0.0},
            {"name": "Dota 2 Battle Pass", "price": 29.99, "category": "MOBA", "hours_played": 0.5}
        ]
    
    def generate_purchase_data(self):
        """Generate realistic Steam purchase history with some problematic patterns"""
        
        # Create CSV with headers
        with open(self.filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Date', 'Game/Item', 'Price', 'Category', 'Hours Played', 
                'Price per Hour', 'Purchase Type', 'Hiro Analysis', 'Recommendations'
            ])
        
        print("🎮 Generating Steam Purchase Data...")
        print("=" * 50)
        
        # Generate purchases over the last 6 months
        base_date = datetime.now() - timedelta(days=180)
        
        for i, game in enumerate(self.games_data):
            # Random purchase date
            purchase_date = base_date + timedelta(days=random.randint(0, 180))
            
            # Calculate value metrics
            hours = game['hours_played']
            price_per_hour = game['price'] / hours if hours > 0 else float('inf')
            
            # Determine purchase type
            if game['price'] == 0:
                purchase_type = "Free to Play"
            elif "DLC" in game['name'] or "Skins" in game['name'] or "Battle Pass" in game['name']:
                purchase_type = "DLC/Cosmetic"
            else:
                purchase_type = "Full Game"
            
            # Hiro's AI Analysis
            analysis = self._generate_hiro_analysis(game, hours, price_per_hour, purchase_type)
            recommendations = self._generate_hiro_recommendations(game, hours, price_per_hour)
            
            # Write to CSV
            with open(self.filename, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    purchase_date.strftime('%Y-%m-%d'),
                    game['name'],
                    f"${game['price']:.2f}",
                    game['category'],
                    f"{hours:.1f}h",
                    f"${price_per_hour:.2f}/h" if price_per_hour != float('inf') else "N/A",
                    purchase_type,
                    analysis,
                    recommendations
                ])
            
            print(f"   📦 {game['name']} - ${game['price']:.2f} - {analysis}")
    
    def _generate_hiro_analysis(self, game, hours, price_per_hour, purchase_type):
        """Generate Hiro's intelligent analysis of each purchase"""
        
        if hours < 1 and game['price'] > 30:
            return "🚨 Poor Value: Expensive game with minimal playtime"
        elif hours < 5 and game['price'] > 50:
            return "⚠️ Buyer's Remorse Risk: High-cost, low-engagement purchase"
        elif price_per_hour < 1:
            return "💎 Excellent Value: High playtime per dollar spent"
        elif price_per_hour < 2:
            return "👍 Good Value: Reasonable cost per entertainment hour"
        elif "Cosmetic" in purchase_type and hours == 0:
            return "💸 Cosmetic Spending: No gameplay impact, aesthetic only"
        elif game['price'] == 0 and hours > 50:
            return "🎯 Smart Choice: Free game with high engagement"
        elif hours > 100:
            return "🏆 Addiction Alert: Extremely high playtime detected"
        elif hours > 50:
            return "🎮 Great Investment: Substantial entertainment value"
        else:
            return "📊 Standard Purchase: Normal gaming purchase pattern"
    
    def _generate_hiro_recommendations(self, game, hours, price_per_hour):
        """Generate Hiro's AI-powered recommendations"""
        
        if hours < 1 and game['price'] > 30:
            return "Try playing for 2+ hours or request refund within 14 days"
        elif hours < 5 and game['price'] > 50:
            return "Consider if this genre matches your preferences before similar purchases"
        elif price_per_hour < 1:
            return "Look for similar games in this genre - great ROI category for you"
        elif "Cosmetic" in game['category'] and game['price'] > 50:
            return "Set monthly cosmetic spending limits to avoid overspending"
        elif game['category'] == "RPG" and hours > 50:
            return "You love RPGs! Consider Divinity: Original Sin 2, Persona 5"
        elif game['category'] == "Strategy" and hours > 100:
            return "Strategy addiction detected! Try Civilization VI, Age of Empires IV"
        elif hours == 0:
            return "Game in backlog - schedule dedicated time or consider refund"
        else:
            return "Monitor future purchases in this category based on play patterns"
    
    def generate_summary_analysis(self):
        """Generate Hiro's overall spending analysis"""
        
        total_spent = sum(game['price'] for game in self.games_data)
        total_hours = sum(game['hours_played'] for game in self.games_data)
        avg_price_per_hour = total_spent / total_hours if total_hours > 0 else 0
        
        # Count categories
        categories = {}
        for game in self.games_data:
            categories[game['category']] = categories.get(game['category'], 0) + game['price']
        
        print(f"\n🤖 Hiro's AI Analysis Summary:")
        print("=" * 50)
        print(f"💰 Total Steam Spending: ${total_spent:.2f}")
        print(f"⏰ Total Gaming Hours: {total_hours:.1f}h")
        print(f"📊 Average Cost Per Hour: ${avg_price_per_hour:.2f}/h")
        print(f"🎮 Most Expensive Category: {max(categories, key=categories.get)} (${max(categories.values()):.2f})")
        
        print(f"\n🧠 Hiro's Smart Recommendations:")
        print("=" * 50)
        
        # Analyze spending patterns
        expensive_unused = [g for g in self.games_data if g['price'] > 30 and g['hours_played'] < 5]
        best_value = [g for g in self.games_data if g['hours_played'] > 0 and (g['price'] / g['hours_played']) < 1]
        
        if expensive_unused:
            print(f"🚨 {len(expensive_unused)} expensive games barely played - consider refund policy")
        if best_value:
            print(f"💎 {len(best_value)} games offer excellent value - buy similar genres")
        
        print(f"📈 Predicted next purchase: RPG genre (based on {sum(1 for g in self.games_data if g['category'] == 'RPG')} RPG purchases)")
        print(f"💡 Recommended spending limit: $40/month (current rate: ${total_spent/6:.2f}/month)")
        
        return {
            'total_spent': total_spent,
            'total_hours': total_hours,
            'avg_cost_per_hour': avg_price_per_hour,
            'expensive_unused': len(expensive_unused),
            'best_value': len(best_value)
        }
    
    def show_google_sheets_integration(self):
        """Show how to import this into Google Sheets"""
        
        print(f"\n📊 Google Sheets Integration:")
        print("=" * 50)
        print(f"📂 File created: {self.filename}")
        print(f"🌐 Import to Google Sheets:")
        print(f"   1. Go to https://sheets.google.com")
        print(f"   2. Create new sheet or open existing")
        print(f"   3. Drag and drop '{self.filename}' into the sheet")
        print(f"   4. Hiro's analysis will appear in columns H & I!")
        
        print(f"\n✨ What makes this special:")
        print(f"   🤖 AI-powered spending analysis")
        print(f"   📈 Value-per-hour calculations")
        print(f"   🎯 Personalized game recommendations")
        print(f"   🚨 Automatic problem detection")
        print(f"   💡 Smart budget suggestions")

def main():
    """Run the Steam purchase analysis demo"""
    
    print("🎮 Hiro's Steam Purchase Analysis Demo")
    print("🤖 Showcasing AI-Powered Gaming Insights")
    print("=" * 60)
    
    analyzer = SteamPurchaseAnalyzer()
    
    # Generate the data
    analyzer.generate_purchase_data()
    
    # Show summary analysis
    summary = analyzer.generate_summary_analysis()
    
    # Show Google Sheets integration
    analyzer.show_google_sheets_integration()
    
    print(f"\n🎯 Demo Complete!")
    print(f"📊 Ready for Google Sheets import: hiro_steam_analysis.csv")
    print(f"🤖 Hiro found {summary['expensive_unused']} potential money-wasting purchases")
    print(f"💎 Hiro identified {summary['best_value']} excellent value games")

if __name__ == "__main__":
    main()