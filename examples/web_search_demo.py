#!/usr/bin/env python3
"""
Demo script showcasing the web search functionality of Brocc-Li.
This script demonstrates how to use the web search tools independently.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path to import brocc_li
sys.path.append(str(Path(__file__).parent.parent))

from brocc_li.tools import make_web_search_tools

def demo_store_search():
    """Demonstrate store search functionality."""
    print("🏪 Store Search Demo")
    print("=" * 50)
    
    web_tools = make_web_search_tools()
    search_tool = web_tools['search_nearby_stores']
    
    # Example: Search for stores in Bonn, Germany
    location = "Bonn, Germany"
    print(f"Searching for stores near: {location}")
    print("Using free OpenStreetMap services (no API key required!)")
    
    try:
        stores = search_tool.invoke({
            "location": location,
            "store_types": ['supermarket', 'grocery_store']
        })
        
        if stores and not isinstance(stores[0], dict):
            print("❌ No stores found")
            return
        
        if stores and 'error' in stores[0]:
            print(f"❌ Error: {stores[0]['error']}")
            return
        
        print(f"✅ Found {len(stores)} stores:")
        for i, store in enumerate(stores[:5], 1):  # Show top 5
            print(f"  {i}. {store['name']}")
            print(f"     Address: {store['address']}")
            print(f"     Distance: {store.get('distance', 'N/A')} km")
            print(f"     Rating: {store.get('rating', 'N/A')}")
            print()
            
    except Exception as e:
        print(f"❌ Error during store search: {e}")

def demo_recipe_search():
    """Demonstrate recipe search functionality."""
    print("👨‍🍳 Recipe Search Demo")
    print("=" * 50)
    
    web_tools = make_web_search_tools()
    search_tool = web_tools['search_recipes']
    
    # Example: Search for vegetarian pasta recipes
    query = "vegetarian pasta"
    dietary_restrictions = ["vegetarian"]
    max_time = 30  # 30 minutes
    
    print(f"Searching for recipes: {query}")
    print(f"Dietary restrictions: {dietary_restrictions}")
    print(f"Max cooking time: {max_time} minutes")
    
    try:
        recipes = search_tool.invoke({
            "query": query,
            "dietary_restrictions": dietary_restrictions,
            "max_time": max_time
        })
        
        print(f"✅ Found {len(recipes)} recipes:")
        for i, recipe in enumerate(recipes[:3], 1):  # Show top 3
            print(f"  {i}. {recipe['title']}")
            print(f"     Source: {recipe['source']}")
            print(f"     Prep time: {recipe.get('prep_time', 'N/A')}")
            print(f"     Cook time: {recipe.get('cook_time', 'N/A')}")
            print(f"     Servings: {recipe.get('servings', 'N/A')}")
            print()
            
    except Exception as e:
        print(f"❌ Error during recipe search: {e}")

def demo_coupon_search():
    """Demonstrate coupon search functionality."""
    print("🎫 Coupon Search Demo")
    print("=" * 50)
    
    web_tools = make_web_search_tools()
    search_tool = web_tools['search_coupons']
    
    # Example: Search for grocery coupons
    store_name = "Rewe"
    category = "groceries"
    
    print(f"Searching for coupons for: {store_name}")
    print(f"Category: {category}")
    
    try:
        coupons = search_tool.invoke({
            "store_name": store_name,
            "category": category
        })
        
        print(f"✅ Found {len(coupons)} coupons:")
        for i, coupon in enumerate(coupons[:3], 1):  # Show top 3
            print(f"  {i}. {coupon['description']}")
            print(f"     Code: {coupon['code']}")
            print(f"     Discount: {coupon['discount']}")
            print(f"     Store: {coupon['store']}")
            print(f"     Expires: {coupon.get('expiry_date', 'N/A')}")
            print()
            
    except Exception as e:
        print(f"❌ Error during coupon search: {e}")

def demo_price_comparison():
    """Demonstrate price comparison functionality."""
    print("💰 Price Comparison Demo")
    print("=" * 50)
    
    web_tools = make_web_search_tools()
    search_tool = web_tools['search_product_prices']
    
    # Example: Search for organic milk prices
    product_name = "organic milk"
    location = "Germany"
    
    print(f"Searching for prices: {product_name}")
    print(f"Location: {location}")
    
    try:
        products = search_tool.invoke({
            "product_name": product_name,
            "location": location
        })
        
        print(f"✅ Found {len(products)} products:")
        for i, product in enumerate(products, 1):
            print(f"  {i}. {product['name']}")
            print(f"     Store: {product['store']}")
            print(f"     Price: €{product['price']}")
            print(f"     Unit: {product['unit']}")
            print(f"     Available: {'Yes' if product['availability'] else 'No'}")
            print()
            
    except Exception as e:
        print(f"❌ Error during price search: {e}")

def demo_store_details():
    """Demonstrate store details functionality."""
    print("📍 Store Details Demo")
    print("=" * 50)
    
    web_tools = make_web_search_tools()
    search_tool = web_tools['get_store_hours_and_location']
    
    # Example: Get details for a specific store
    store_name = "Rewe"
    location = "Bonn, Germany"
    
    print(f"Getting details for: {store_name}")
    print(f"Location: {location}")
    print("Using free OpenStreetMap services")
    
    try:
        store_details = search_tool.invoke({
            "store_name": store_name,
            "location": location
        })
        
        if 'error' in store_details:
            print(f"❌ Error: {store_details['error']}")
            return
        
        print("✅ Store details:")
        print(f"  Name: {store_details.get('name', 'N/A')}")
        print(f"  Address: {store_details.get('formatted_address', 'N/A')}")
        print(f"  Phone: {store_details.get('formatted_phone_number', 'N/A')}")
        print(f"  Rating: {store_details.get('rating', 'N/A')}")
        print(f"  Website: {store_details.get('website', 'N/A')}")
        
        if 'opening_hours' in store_details:
            print("  Opening hours:")
            for period in store_details['opening_hours'].get('periods', []):
                print(f"    {period.get('open', {}).get('day', 'N/A')}: "
                      f"{period.get('open', {}).get('time', 'N/A')} - "
                      f"{period.get('close', {}).get('time', 'N/A')}")
        print()
        
    except Exception as e:
        print(f"❌ Error during store details search: {e}")

def main():
    """Run all demos."""
    print("🚀 Brocc-Li Web Search Tools Demo")
    print("=" * 60)
    print()
    print("✅ **No API keys required!** Using free mapping services.")
    print()
    
    # Run demos
    demo_store_search()
    print()
    
    demo_recipe_search()
    print()
    
    demo_coupon_search()
    print()
    
    demo_price_comparison()
    print()
    
    demo_store_details()
    print()
    
    print("✅ Demo completed!")
    print("\nTo use these tools in the full application:")
    print("1. Run: python main.py")
    print("2. Ask the agent about stores, recipes, or shopping!")
    print("3. No API keys needed - everything works with free services!")

if __name__ == "__main__":
    main() 