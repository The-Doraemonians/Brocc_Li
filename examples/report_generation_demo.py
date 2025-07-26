#!/usr/bin/env python3
"""
Demo script showcasing the report generation functionality of Brocc-Li.
This script demonstrates how to generate comprehensive diet reports.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path to import brocc_li
sys.path.append(str(Path(__file__).parent.parent))

from brocc_li.tools import make_report_generation_tool
from langchain_google_genai import ChatGoogleGenerativeAI

def demo_diet_report_generation():
    """Demonstrate comprehensive diet report generation."""
    print("📊 Diet Report Generation Demo")
    print("=" * 60)
    
    # Initialize LLM (you'll need to set GOOGLE_API_KEY in environment)
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        print("   Set your Google API key to run this demo")
        return
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1,
        api_key=api_key,
    )
    
    report_tools = make_report_generation_tool(llm)
    generate_report = report_tools['generate_diet_report']
    
    # Example user preferences
    user_preferences = {
        'age': 30,
        'gender': 'female',
        'height': 165,  # cm
        'weight': 62,   # kg
        'goal': 'lose weight',
        'dietary_restrictions': ['vegetarian'],
        'allergies': ['peanuts'],
        'budget': 15,  # euros per day
        'cooking_skill': 'intermediate',
        'max_cooking_time': 30,  # minutes
        'location': 'Berlin, Germany',
        'preferences': ['Italian cuisine', 'quick meals']
    }
    
    print("Generating comprehensive diet report for:")
    print(f"  Age: {user_preferences['age']}")
    print(f"  Gender: {user_preferences['gender']}")
    print(f"  Height: {user_preferences['height']} cm")
    print(f"  Weight: {user_preferences['weight']} kg")
    print(f"  Goal: {user_preferences['goal']}")
    print(f"  Dietary restrictions: {user_preferences['dietary_restrictions']}")
    print(f"  Allergies: {user_preferences['allergies']}")
    print(f"  Daily budget: €{user_preferences['budget']}")
    print(f"  Max cooking time: {user_preferences['max_cooking_time']} minutes")
    print()
    
    try:
        report = generate_report.invoke({
            "user_preferences": user_preferences,
            "location": "Berlin, Germany"
        })
        
        if 'error' in report:
            print(f"❌ Error: {report['error']}")
            return
        
        print("✅ Diet Report Generated Successfully!")
        print()
        
        # Display user info
        print("👤 User Information:")
        user_info = report.get('user_info', {})
        print(f"  Goal: {user_info.get('goal', 'N/A')}")
        print(f"  Dietary restrictions: {user_info.get('dietary_restrictions', [])}")
        print(f"  Allergies: {user_info.get('allergies', [])}")
        print(f"  Budget: €{user_info.get('budget', 'N/A')} per day")
        print()
        
        # Display meal plan summary
        print("🍽️ Meal Plan Summary:")
        meal_plan = report.get('meal_plan', [])
        print(f"  Days planned: {len(meal_plan)}")
        
        for day_plan in meal_plan[:3]:  # Show first 3 days
            day = day_plan.get('day', 'Unknown')
            meals = day_plan.get('meals', {})
            total_cost = day_plan.get('total_cost', 0)
            nutrition = day_plan.get('total_nutrition', {})
            
            print(f"  {day}:")
            print(f"    Cost: €{total_cost:.2f}")
            print(f"    Calories: {nutrition.get('calories', 0)}")
            print(f"    Protein: {nutrition.get('protein', 0)}g")
            print(f"    Meals: {', '.join(meals.keys())}")
        print()
        
        # Display shopping list summary
        print("🛒 Shopping List Summary:")
        shopping_list = report.get('shopping_list', [])
        print(f"  Total items: {len(shopping_list)}")
        
        # Group by category
        categories = {}
        for item in shopping_list:
            category = item.get('category', 'other')
            if category not in categories:
                categories[category] = []
            categories[category].append(item)
        
        for category, items in categories.items():
            total_cost = sum(item.get('estimated_price', 0) for item in items)
            print(f"  {category.title()}: {len(items)} items (€{total_cost:.2f})")
        
        total_shopping_cost = sum(item.get('estimated_price', 0) for item in shopping_list)
        print(f"  Total shopping cost: €{total_shopping_cost:.2f}")
        print()
        
        # Display nutritional summary
        print("🔬 Nutritional Summary:")
        nutrition = report.get('nutritional_summary', {})
        print(f"  Total weekly calories: {nutrition.get('total_calories', 0):.0f}")
        print(f"  Average daily calories: {nutrition.get('avg_daily_calories', 0):.0f}")
        print(f"  Total weekly protein: {nutrition.get('total_protein', 0):.0f}g")
        print(f"  Total weekly carbs: {nutrition.get('total_carbs', 0):.0f}g")
        print(f"  Total weekly fat: {nutrition.get('total_fat', 0):.0f}g")
        print()
        
        # Display recommendations
        print("💡 Recommendations:")
        recommendations = report.get('recommendations', [])
        for i, rec in enumerate(recommendations[:5], 1):
            print(f"  {i}. {rec}")
        print()
        
        # Display cost breakdown
        print("💰 Cost Breakdown:")
        weekly_cost = report.get('total_weekly_cost', 0)
        daily_avg = weekly_cost / 7 if weekly_cost > 0 else 0
        print(f"  Weekly total: €{weekly_cost:.2f}")
        print(f"  Daily average: €{daily_avg:.2f}")
        print(f"  Shopping cost: €{total_shopping_cost:.2f}")
        print(f"  Generated on: {report.get('generated_date', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error during report generation: {e}")

def demo_shopping_list_generation():
    """Demonstrate shopping list generation."""
    print("\n🛒 Shopping List Generation Demo")
    print("=" * 50)
    
    # Initialize LLM
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        return
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1,
        api_key=api_key,
    )
    
    report_tools = make_report_generation_tool(llm)
    generate_shopping_list = report_tools['generate_shopping_list']
    
    # Sample meal plan
    sample_meal_plan = [
        {
            "day": "Monday",
            "meals": {
                "breakfast": {
                    "name": "Oatmeal with Berries",
                    "ingredients": ["oats", "berries", "honey", "milk"],
                    "nutrition": {"calories": 300, "protein": 12, "carbs": 45, "fat": 8},
                    "cost": 2.50,
                    "prep_time": "10 minutes"
                },
                "lunch": {
                    "name": "Vegetarian Pasta",
                    "ingredients": ["pasta", "tomatoes", "basil", "olive oil"],
                    "nutrition": {"calories": 450, "protein": 15, "carbs": 70, "fat": 12},
                    "cost": 3.20,
                    "prep_time": "20 minutes"
                },
                "dinner": {
                    "name": "Grilled Chicken Salad",
                    "ingredients": ["chicken breast", "lettuce", "tomatoes", "cucumber"],
                    "nutrition": {"calories": 350, "protein": 35, "carbs": 15, "fat": 18},
                    "cost": 4.80,
                    "prep_time": "25 minutes"
                }
            },
            "total_nutrition": {"calories": 1100, "protein": 62, "carbs": 130, "fat": 38},
            "total_cost": 10.50
        }
    ]
    
    print("Generating shopping list from meal plan...")
    
    try:
        shopping_result = generate_shopping_list.invoke({
            "meal_plan": sample_meal_plan,
            "location": "Berlin, Germany"
        })
        
        if 'error' in shopping_result:
            print(f"❌ Error: {shopping_result['error']}")
            return
        
        print("✅ Shopping List Generated Successfully!")
        print()
        
        print(f"Total items: {shopping_result.get('total_items', 0)}")
        print(f"Total cost: €{shopping_result.get('total_cost', 0):.2f}")
        print()
        
        # Display categorized list
        categorized_list = shopping_result.get('categorized_list', {})
        for category, items in categorized_list.items():
            print(f"{category.title()}:")
            for item in items:
                print(f"  - {item['name']}: {item['quantity']} (€{item['estimated_price']:.2f})")
            print()
        
    except Exception as e:
        print(f"❌ Error during shopping list generation: {e}")

def demo_nutritional_analysis():
    """Demonstrate nutritional analysis."""
    print("\n🔬 Nutritional Analysis Demo")
    print("=" * 40)
    
    # Initialize LLM
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        return
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1,
        api_key=api_key,
    )
    
    report_tools = make_report_generation_tool(llm)
    generate_analysis = report_tools['generate_nutritional_analysis']
    
    # Sample meal plan for analysis
    sample_meal_plan = [
        {
            "day": "Monday",
            "total_nutrition": {"calories": 1100, "protein": 62, "carbs": 130, "fat": 38}
        },
        {
            "day": "Tuesday", 
            "total_nutrition": {"calories": 1200, "protein": 58, "carbs": 140, "fat": 42}
        },
        {
            "day": "Wednesday",
            "total_nutrition": {"calories": 1150, "protein": 65, "carbs": 125, "fat": 40}
        }
    ]
    
    print("Analyzing nutritional content of meal plan...")
    
    try:
        analysis = generate_analysis.invoke({
            "meal_plan": sample_meal_plan
        })
        
        if 'error' in analysis:
            print(f"❌ Error: {analysis['error']}")
            return
        
        print("✅ Nutritional Analysis Completed!")
        print()
        
        # Display daily nutrition
        print("Daily Nutrition:")
        daily_nutrition = analysis.get('daily_nutrition', [])
        for day_data in daily_nutrition:
            day = day_data.get('day', 'Unknown')
            nutrition = day_data.get('nutrition', {})
            print(f"  {day}: {nutrition.get('calories', 0)} calories, "
                  f"{nutrition.get('protein', 0)}g protein")
        print()
        
        # Display weekly averages
        print("Weekly Averages:")
        weekly_averages = analysis.get('weekly_averages', {})
        print(f"  Calories: {weekly_averages.get('calories', 0):.0f}")
        print(f"  Protein: {weekly_averages.get('protein', 0):.0f}g")
        print(f"  Carbs: {weekly_averages.get('carbs', 0):.0f}g")
        print(f"  Fat: {weekly_averages.get('fat', 0):.0f}g")
        print()
        
        # Display recommendations
        print("Nutritional Recommendations:")
        recommendations = analysis.get('recommendations', [])
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
        
    except Exception as e:
        print(f"❌ Error during nutritional analysis: {e}")

def main():
    """Run all report generation demos."""
    print("🚀 Brocc-Li Report Generation Tools Demo")
    print("=" * 70)
    print()
    print("This demo showcases the comprehensive report generation capabilities.")
    print("You'll need to set GOOGLE_API_KEY in your environment variables.")
    print()
    
    # Run demos
    demo_diet_report_generation()
    demo_shopping_list_generation()
    demo_nutritional_analysis()
    
    print("\n✅ Demo completed!")
    print("\nTo use these tools in the full application:")
    print("1. Set GOOGLE_API_KEY in your environment")
    print("2. Run: python main.py")
    print("3. Ask the agent for a comprehensive diet report!")
    print("\nExample prompts:")
    print("- 'Generate a complete diet report for me'")
    print("- 'Create a shopping list for my meal plan'")
    print("- 'Analyze the nutrition of my diet plan'")

if __name__ == "__main__":
    main() 