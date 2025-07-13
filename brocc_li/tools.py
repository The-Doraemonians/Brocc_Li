import json
import os
import time
from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
import urllib.parse
import urllib.request

import streamlit as st
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
import requests
from bs4 import BeautifulSoup

# Optional imports with error handling
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    webdriver = None
    By = None
    WebDriverWait = None
    EC = None
    Options = None

try:
    from fake_useragent import UserAgent
    FAKE_USERAGENT_AVAILABLE = True
except ImportError:
    FAKE_USERAGENT_AVAILABLE = False
    UserAgent = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Load environment variables
try:
    load_dotenv()
except NameError:
    pass

@dataclass
class StoreInfo:
    name: str
    address: str
    distance: float
    rating: Optional[float]
    phone: Optional[str]
    website: Optional[str]

@dataclass
class ProductInfo:
    name: str
    price: float
    store: str
    availability: bool
    unit: str
    brand: Optional[str] = None

@dataclass
class CouponInfo:
    code: str
    description: str
    discount: str
    expiry_date: Optional[str]
    store: str
    conditions: Optional[str] = None

@dataclass
class RecipeInfo:
    title: str
    ingredients: List[str]
    instructions: List[str]
    prep_time: Optional[str]
    cook_time: Optional[str]
    servings: Optional[int]
    source: str
    url: str

@dataclass
class NutritionalInfo:
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: float
    sugar: float
    sodium: float

@dataclass
class MealPlan:
    day: str
    meals: Dict[str, Dict[str, Any]]  # breakfast, lunch, dinner, snacks
    total_nutrition: NutritionalInfo
    total_cost: float

@dataclass
class ShoppingItem:
    name: str
    quantity: str
    estimated_price: float
    store: str
    category: str
    notes: Optional[str] = None

@dataclass
class DietReport:
    user_info: Dict[str, Any]
    meal_plan: List[MealPlan]
    shopping_list: List[ShoppingItem]
    total_weekly_cost: float
    nutritional_summary: Dict[str, Any]
    recommendations: List[str]
    generated_date: str

class FreeMapServices:
    """Free mapping services that don't require API keys."""
    
    @staticmethod
    def geocode_location(location: str) -> Optional[Dict[str, float]]:
        """Geocode location using OpenStreetMap Nominatim (free)."""
        try:
            # Use Nominatim for geocoding
            base_url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': location,
                'format': 'json',
                'limit': 1
            }
            
            url = f"{base_url}?{urllib.parse.urlencode(params)}"
            
            # Add proper headers to avoid being blocked
            headers = {
                'User-Agent': 'Brocc-Li Diet Assistant/1.0'
            }
            
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as response:
                data = json.loads(response.read().decode())
                
                if data:
                    result = data[0]
                    return {
                        'lat': float(result['lat']),
                        'lon': float(result['lon'])
                    }
        except Exception as e:
            st.warning(f"Geocoding failed: {e}")
        
        return None
    
    @staticmethod
    def search_nearby_places(location: str, query: str, radius: int = 5000) -> List[Dict]:
        """Search for nearby places using OpenStreetMap Overpass API (free)."""
        try:
            # First geocode the location
            coords = FreeMapServices.geocode_location(location)
            if not coords:
                return []
            
            # Use Overpass API to search for places
            overpass_url = "https://overpass-api.de/api/interpreter"
            
            # Search for supermarkets and grocery stores
            overpass_query = f"""
            [out:json][timeout:25];
            (
              node["shop"="supermarket"](around:{radius},{coords['lat']},{coords['lon']});
              node["shop"="convenience"](around:{radius},{coords['lat']},{coords['lon']});
              way["shop"="supermarket"](around:{radius},{coords['lat']},{coords['lon']});
              way["shop"="convenience"](around:{radius},{coords['lat']},{coords['lon']});
            );
            out body;
            >;
            out skel qt;
            """
            
            headers = {
                'User-Agent': 'Brocc-Li Diet Assistant/1.0'
            }
            
            response = requests.post(overpass_url, data=overpass_query, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                places = []
                
                for element in data.get('elements', []):
                    if element['type'] == 'node' and 'tags' in element:
                        tags = element['tags']
                        if 'name' in tags:
                            # Calculate approximate distance (simplified)
                            distance = FreeMapServices._calculate_distance(
                                coords['lat'], coords['lon'],
                                element['lat'], element['lon']
                            )
                            
                            place_info = {
                                'name': tags.get('name', 'Unknown Store'),
                                'address': tags.get('addr:street', '') + ' ' + tags.get('addr:housenumber', ''),
                                'distance': distance,
                                'rating': None,  # Not available in OSM
                                'phone': tags.get('phone'),
                                'website': tags.get('website'),
                                'opening_hours': tags.get('opening_hours'),
                                'brand': tags.get('brand')
                            }
                            places.append(place_info)
                
                return places[:10]  # Return top 10 results
                
        except Exception as e:
            st.warning(f"Place search failed: {e}")
        
        return []
    
    @staticmethod
    def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula."""
        import math
        
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c

class WebSearchTools:
    def __init__(self):
        self.driver = None
        self.ua = None
        self.session = requests.Session()
        
        # Initialize UserAgent if available
        if FAKE_USERAGENT_AVAILABLE and UserAgent:
            try:
                self.ua = UserAgent()
                self.session.headers.update({'User-Agent': self.ua.random})
            except Exception:
                self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        else:
            self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        
        # Store data cache
        self.store_cache = {}
        self.coupon_cache = {}
        self.recipe_cache = {}
        
    def _get_selenium_driver(self):
        """Initialize Selenium WebDriver with headless options."""
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium is not available. Please install it with: pip install selenium")
        
        if self.driver is None:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            if self.ua:
                chrome_options.add_argument(f"--user-agent={self.ua.random}")
            self.driver = webdriver.Chrome(options=chrome_options)
        return self.driver
    
    def _cleanup_driver(self):
        """Clean up Selenium driver."""
        if self.driver:
            self.driver.quit()
            self.driver = None

def make_web_search_tools():
    """Create comprehensive web search tools."""
    web_tools = WebSearchTools()
    
    @tool
    def search_nearby_stores(location: str, store_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Search for nearby grocery stores using free mapping services.
        
        Args:
            location: Address or coordinates to search from
            store_types: List of store types to search for (e.g., ['supermarket', 'grocery_store'])
        """
        if store_types is None:
            store_types = ['supermarket', 'grocery_store']
        
        stores = []
        
        # Use free mapping services
        places = FreeMapServices.search_nearby_places(location, "supermarket")
        
        for place in places:
            store_info = StoreInfo(
                name=place['name'],
                address=place['address'],
                distance=place['distance'],
                rating=place['rating'],
                phone=place['phone'],
                website=place['website']
            )
            stores.append(store_info.__dict__)
        
        # If no results from OSM, provide some sample data
        if not stores:
            stores = [
                {
                    'name': 'Rewe',
                    'address': 'Friedenspl. 1-3, 53111 Bonn',
                    'rating': 4.2,
                    'phone': '+49 0228 68446914',
                    'website': 'https://www.rewe.de'
                },
                {
                    'name': 'Aldi Süd',
                    'address': 'Endenicher Str. 104, 53115 Bonn',
                    'rating': 4.0,
                    'phone': '+49 0800 8002534',
                    'website': 'https://www.aldi-sued.de'
                }
            ]
        
        return stores[:10]  # Return top 10 results
    
    @tool
    def search_product_prices(product_name: str, location: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for product prices across different stores.
        
        Args:
            product_name: Name of the product to search for
            location: Optional location for local store search
        """
        products = []
        
        # List of German grocery store websites
        store_urls = {
            'Rewe': 'https://shop.rewe.de',
            'Aldi': 'https://www.aldi-sued.de',
            'Lidl': 'https://www.lidl.de',
            'Edeka': 'https://www.edeka.de'
        }
        
        for store_name, base_url in store_urls.items():
            try:
                # This is a simplified example - actual implementation would need
                # specific selectors for each store's website
                search_url = f"{base_url}/search?q={product_name}"
                
                response = web_tools.session.get(search_url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract product information (this would need to be customized per store)
                    product_info = ProductInfo(
                        name=product_name,
                        price=0.0,  # Would extract actual price
                        store=store_name,
                        availability=True,  # Would check actual availability
                        unit="piece"
                    )
                    products.append(product_info.__dict__)
                    
            except Exception as e:
                st.warning(f"Could not search {store_name}: {str(e)}")
        
        return products
    
    @tool
    def search_coupons(store_name: Optional[str] = None, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for available coupons and deals.
        
        Args:
            store_name: Specific store to search for coupons
            category: Category of products (e.g., 'groceries', 'dairy')
        """
        coupons = []
        
        # Example coupon websites
        coupon_sites = [
            'https://www.rabattcode.de',
            'https://www.gutscheine.de',
            'https://www.sparwelt.de'
        ]
        
        for site in coupon_sites:
            try:
                response = web_tools.session.get(site, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract coupon information (simplified)
                    coupon_info = CouponInfo(
                        code="EXAMPLE123",
                        description="Sample discount",
                        discount="10% off",
                        expiry_date=(datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                        store="Sample Store",
                        conditions="Minimum purchase required"
                    )
                    coupons.append(coupon_info.__dict__)
                    
            except Exception as e:
                st.warning(f"Could not search {site}: {str(e)}")
        
        return coupons
    
    @tool
    def search_recipes(query: str, dietary_restrictions: Optional[List[str]] = None, 
                      max_time: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Search for recipes from popular cooking websites.
        
        Args:
            query: Recipe search query
            dietary_restrictions: List of dietary restrictions (e.g., ['vegetarian', 'gluten-free'])
            max_time: Maximum cooking time in minutes
        """
        recipes = []
        
        # Popular recipe websites
        recipe_sites = [
            'https://www.allrecipes.com',
            'https://www.foodnetwork.com',
            'https://www.epicurious.com',
            'https://www.chefkoch.de',  # German recipe site
            'https://www.lecker.de'     # German recipe site
        ]
        
        for site in recipe_sites:
            try:
                search_url = f"{site}/search?q={query}"
                response = web_tools.session.get(search_url, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract recipe information (simplified)
                    recipe_info = RecipeInfo(
                        title=f"Sample Recipe from {site}",
                        ingredients=["ingredient 1", "ingredient 2", "ingredient 3"],
                        instructions=["Step 1", "Step 2", "Step 3"],
                        prep_time="15 minutes",
                        cook_time="30 minutes",
                        servings=4,
                        source=site,
                        url=search_url
                    )
                    recipes.append(recipe_info.__dict__)
                    
            except Exception as e:
                st.warning(f"Could not search {site}: {str(e)}")
        
        return recipes
    
    @tool
    def scrape_store_website(store_url: str, product_search: Optional[str] = None) -> Dict[str, Any]:
        """
        Scrape product information from a specific store website.
        
        Args:
            store_url: URL of the store website
            product_search: Optional product to search for
        """
        try:
            driver = web_tools._get_selenium_driver()
            driver.get(store_url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Extract page information
            page_info = {
                'title': driver.title,
                'url': store_url,
                'products_found': [],
                'scraping_time': datetime.now().isoformat()
            }
            
            if product_search:
                # This would implement actual product search logic
                # specific to each store's website structure
                page_info['search_query'] = product_search
                page_info['products_found'] = [
                    {
                        'name': 'Sample Product',
                        'price': '€2.99',
                        'availability': True
                    }
                ]
            
            return page_info
            
        except Exception as e:
            return {"error": f"Failed to scrape {store_url}: {str(e)}"}
    
    @tool
    def get_store_hours_and_location(store_name: str, location: str) -> Dict[str, Any]:
        """
        Get detailed store information including hours and exact location.
        
        Args:
            store_name: Name of the store
            location: General location/area
        """
        try:
            # Search for the specific store using free services
            search_query = f"{store_name} {location}"
            places = FreeMapServices.search_nearby_places(location, store_name)
            
            if places:
                place = places[0]  # Get the first result
                return {
                    'name': place['name'],
                    'formatted_address': place['address'],
                    'formatted_phone_number': place['phone'],
                    'opening_hours': place.get('opening_hours'),
                    'rating': place['rating'],
                    'website': place['website']
                }
            else:
                return {"error": f"Store '{store_name}' not found in {location}"}
                
        except Exception as e:
            return {"error": f"Failed to get store information: {str(e)}"}
    
    @tool
    def compare_prices_across_stores(product_list: List[str], location: str) -> Dict[str, Any]:
        """
        Compare prices for multiple products across different stores.
        
        Args:
            product_list: List of products to compare
            location: Location for store search
        """
        comparison_results = {
            'location': location,
            'products': {},
            'store_comparison': {},
            'best_deals': []
        }
        
        # Get nearby stores
        stores = search_nearby_stores(location)
        
        for product in product_list:
            comparison_results['products'][product] = {}
            
            # Search for product in each store
            for store in stores[:5]:  # Top 5 stores
                if isinstance(store, dict) and 'name' in store:
                    store_name = store['name']
                    products = search_product_prices(product)
                    
                    for product_info in products:
                        if isinstance(product_info, dict) and product_info.get('store') == store_name:
                            comparison_results['products'][product][store_name] = product_info
                            break
        
        # Find best deals
        for product, store_prices in comparison_results['products'].items():
            if store_prices:
                best_price = min(store_prices.values(), key=lambda x: x.get('price', float('inf')))
                comparison_results['best_deals'].append({
                    'product': product,
                    'store': best_price.get('store', 'Unknown'),
                    'price': best_price.get('price', 0.0)
                })
        
        return comparison_results
    
    return {
        'search_nearby_stores': search_nearby_stores,
        'search_product_prices': search_product_prices,
        'search_coupons': search_coupons,
        'search_recipes': search_recipes,
        'scrape_store_website': scrape_store_website,
        'get_store_hours_and_location': get_store_hours_and_location,
        'compare_prices_across_stores': compare_prices_across_stores
    }

def make_report_generation_tool(llm: ChatGoogleGenerativeAI):
    """Create a comprehensive report generation tool."""
    
    @tool
    def generate_diet_report(user_preferences: dict, location: str = "Germany") -> Dict[str, Any]:
        """
        Generate a comprehensive diet report with meal plan, nutritional breakdown, costs, and shopping list.
        
        Args:
            user_preferences: User's diet preferences and constraints
            location: User's location for store recommendations
        """
        try:
            # Extract user information
            user_info = {
                'age': user_preferences.get('age'),
                'gender': user_preferences.get('gender'),
                'height': user_preferences.get('height'),
                'weight': user_preferences.get('weight'),
                'goal': user_preferences.get('goal'),
                'dietary_restrictions': user_preferences.get('dietary_restrictions', []),
                'allergies': user_preferences.get('allergies', []),
                'budget': user_preferences.get('budget'),
                'cooking_skill': user_preferences.get('cooking_skill', 'intermediate'),
                'max_cooking_time': user_preferences.get('max_cooking_time', 30)
            }
            
            # Generate meal plan using LLM
            meal_plan_prompt = f"""
            Create a 7-day meal plan for a user with these preferences: {user_preferences}
            
            Return a JSON object with this structure:
            {{
                "meal_plan": [
                    {{
                        "day": "Monday",
                        "meals": {{
                            "breakfast": {{
                                "name": "meal name",
                                "ingredients": ["ingredient 1", "ingredient 2"],
                                "nutrition": {{"calories": 300, "protein": 15, "carbs": 30, "fat": 10}},
                                "cost": 2.50,
                                "prep_time": "10 minutes"
                            }},
                            "lunch": {{...}},
                            "dinner": {{...}},
                            "snacks": [{{...}}]
                        }},
                        "total_nutrition": {{"calories": 1800, "protein": 80, "carbs": 200, "fat": 60}},
                        "total_cost": 12.50
                    }}
                ]
            }}
            
            Ensure the plan meets the user's dietary restrictions, budget, and cooking time constraints.
            """
            
            meal_plan_response = llm.invoke(meal_plan_prompt)
            meal_plan_content = meal_plan_response.content
            
            # Parse meal plan
            if isinstance(meal_plan_content, list):
                meal_plan_content = meal_plan_content[0] if meal_plan_content else ""
            meal_plan_content = str(meal_plan_content).strip()
            
            # Extract JSON from response
            if "```json" in meal_plan_content:
                start = meal_plan_content.find("```json") + 7
                end = meal_plan_content.find("```", start)
                meal_plan_content = meal_plan_content[start:end].strip()
            
            try:
                meal_plan_data = json.loads(meal_plan_content)
            except json.JSONDecodeError:
                # Fallback meal plan
                meal_plan_data = {
                    "meal_plan": [
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
                }
            
            # Generate shopping list
            shopping_list = []
            all_ingredients = set()
            
            for day_plan in meal_plan_data.get("meal_plan", []):
                for meal_type, meal in day_plan.get("meals", {}).items():
                    if isinstance(meal, dict) and "ingredients" in meal:
                        for ingredient in meal["ingredients"]:
                            all_ingredients.add(ingredient.lower())
            
            # Categorize ingredients and estimate prices
            ingredient_categories = {
                "proteins": ["chicken", "fish", "eggs", "tofu", "beans", "lentils"],
                "vegetables": ["tomatoes", "lettuce", "cucumber", "carrots", "onions", "garlic"],
                "fruits": ["berries", "apples", "bananas", "oranges"],
                "grains": ["oats", "pasta", "rice", "bread"],
                "dairy": ["milk", "cheese", "yogurt"],
                "pantry": ["olive oil", "honey", "salt", "pepper", "basil"]
            }
            
            for ingredient in all_ingredients:
                category = "other"
                for cat, items in ingredient_categories.items():
                    if ingredient in items:
                        category = cat
                        break
                
                # Estimate price based on category
                price_estimates = {
                    "proteins": 3.50,
                    "vegetables": 1.20,
                    "fruits": 2.00,
                    "grains": 1.50,
                    "dairy": 2.50,
                    "pantry": 1.00,
                    "other": 1.50
                }
                
                shopping_item = ShoppingItem(
                    name=ingredient.title(),
                    quantity="1 unit",
                    estimated_price=price_estimates.get(category, 1.50),
                    store="Rewe",
                    category=category,
                    notes=f"Category: {category}"
                )
                shopping_list.append(shopping_item.__dict__)
            
            # Calculate totals
            total_weekly_cost = sum(day.get("total_cost", 0) for day in meal_plan_data.get("meal_plan", []))
            total_shopping_cost = sum(item["estimated_price"] for item in shopping_list)
            
            # Generate nutritional summary
            weekly_nutrition = {
                "total_calories": sum(day.get("total_nutrition", {}).get("calories", 0) for day in meal_plan_data.get("meal_plan", [])),
                "avg_daily_calories": sum(day.get("total_nutrition", {}).get("calories", 0) for day in meal_plan_data.get("meal_plan", [])) / 7,
                "total_protein": sum(day.get("total_nutrition", {}).get("protein", 0) for day in meal_plan_data.get("meal_plan", [])),
                "total_carbs": sum(day.get("total_nutrition", {}).get("carbs", 0) for day in meal_plan_data.get("meal_plan", [])),
                "total_fat": sum(day.get("total_nutrition", {}).get("fat", 0) for day in meal_plan_data.get("meal_plan", []))
            }
            
            # Generate recommendations
            recommendations_prompt = f"""
            Based on this user profile: {user_preferences}
            And this meal plan: {meal_plan_data}
            
            Provide 3-5 specific, actionable recommendations for:
            1. Nutritional improvements
            2. Cost savings
            3. Time management
            4. Shopping tips
            
            Return as a JSON array of strings.
            """
            
            recommendations_response = llm.invoke(recommendations_prompt)
            recommendations_content = recommendations_response.content
            
            if isinstance(recommendations_content, list):
                recommendations_content = recommendations_content[0] if recommendations_content else ""
            recommendations_content = str(recommendations_content).strip()
            
            try:
                if "[" in recommendations_content and "]" in recommendations_content:
                    start = recommendations_content.find("[")
                    end = recommendations_content.rfind("]") + 1
                    recommendations = json.loads(recommendations_content[start:end])
                else:
                    recommendations = [
                        "Consider meal prepping on weekends to save time during the week",
                        "Buy ingredients in bulk when possible to reduce costs",
                        "Plan meals around seasonal produce for better prices",
                        "Use leftovers creatively to minimize food waste"
                    ]
            except json.JSONDecodeError:
                recommendations = [
                    "Consider meal prepping on weekends to save time during the week",
                    "Buy ingredients in bulk when possible to reduce costs",
                    "Plan meals around seasonal produce for better prices",
                    "Use leftovers creatively to minimize food waste"
                ]
            
            # Create final report
            report = DietReport(
                user_info=user_info,
                meal_plan=meal_plan_data.get("meal_plan", []),
                shopping_list=shopping_list,
                total_weekly_cost=total_weekly_cost,
                nutritional_summary=weekly_nutrition,
                recommendations=recommendations,
                generated_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            return report.__dict__
            
        except Exception as e:
            st.error(f"Error generating diet report: {str(e)}")
            return {"error": f"Failed to generate diet report: {str(e)}"}
    
    @tool
    def generate_shopping_list(meal_plan: List[Dict], location: str = "Germany") -> Dict[str, Any]:
        """
        Generate a detailed shopping list from a meal plan with prices and store recommendations.
        
        Args:
            meal_plan: List of daily meal plans
            location: User's location for store recommendations
        """
        try:
            # Extract all ingredients from meal plan
            all_ingredients = {}
            
            for day in meal_plan:
                for meal_type, meal in day.get("meals", {}).items():
                    if isinstance(meal, dict) and "ingredients" in meal:
                        for ingredient in meal["ingredients"]:
                            ingredient_lower = ingredient.lower()
                            if ingredient_lower in all_ingredients:
                                all_ingredients[ingredient_lower]["quantity"] += 1
                            else:
                                all_ingredients[ingredient_lower] = {
                                    "name": ingredient.title(),
                                    "quantity": 1,
                                    "category": "other"
                                }
            
            # Categorize ingredients
            ingredient_categories = {
                "proteins": ["chicken", "fish", "eggs", "tofu", "beans", "lentils", "beef", "pork"],
                "vegetables": ["tomatoes", "lettuce", "cucumber", "carrots", "onions", "garlic", "spinach", "broccoli"],
                "fruits": ["berries", "apples", "bananas", "oranges", "grapes", "strawberries"],
                "grains": ["oats", "pasta", "rice", "bread", "quinoa", "couscous"],
                "dairy": ["milk", "cheese", "yogurt", "butter", "cream"],
                "pantry": ["olive oil", "honey", "salt", "pepper", "basil", "oregano", "flour", "sugar"]
            }
            
            for ingredient, info in all_ingredients.items():
                for category, items in ingredient_categories.items():
                    if ingredient in items:
                        info["category"] = category
                        break
            
            # Estimate prices and create shopping list
            price_estimates = {
                "proteins": 3.50,
                "vegetables": 1.20,
                "fruits": 2.00,
                "grains": 1.50,
                "dairy": 2.50,
                "pantry": 1.00,
                "other": 1.50
            }
            
            shopping_list = []
            total_cost = 0
            
            for ingredient, info in all_ingredients.items():
                category = info["category"]
                price = price_estimates.get(category, 1.50) * info["quantity"]
                total_cost += price
                
                shopping_item = ShoppingItem(
                    name=info["name"],
                    quantity=f"{info['quantity']} units",
                    estimated_price=price,
                    store="Rewe",
                    category=category,
                    notes=f"Category: {category}"
                )
                shopping_list.append(shopping_item.__dict__)
            
            # Group by category
            categorized_list = {}
            for item in shopping_list:
                category = item["category"]
                if category not in categorized_list:
                    categorized_list[category] = []
                categorized_list[category].append(item)
            
            return {
                "shopping_list": shopping_list,
                "categorized_list": categorized_list,
                "total_cost": total_cost,
                "total_items": len(shopping_list),
                "generated_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            st.error(f"Error generating shopping list: {str(e)}")
            return {"error": f"Failed to generate shopping list: {str(e)}"}
    
    @tool
    def generate_nutritional_analysis(meal_plan: List[Dict]) -> Dict[str, Any]:
        """
        Generate detailed nutritional analysis of a meal plan.
        
        Args:
            meal_plan: List of daily meal plans
        """
        try:
            daily_nutrition = []
            weekly_totals = {
                "calories": 0,
                "protein": 0,
                "carbs": 0,
                "fat": 0,
                "fiber": 0,
                "sugar": 0,
                "sodium": 0
            }
            
            for day in meal_plan:
                day_nutrition = day.get("total_nutrition", {})
                daily_nutrition.append({
                    "day": day.get("day", "Unknown"),
                    "nutrition": day_nutrition
                })
                
                for nutrient, value in day_nutrition.items():
                    if nutrient in weekly_totals:
                        weekly_totals[nutrient] += value
            
            # Calculate averages
            num_days = len(daily_nutrition)
            weekly_averages = {
                nutrient: total / num_days if num_days > 0 else 0
                for nutrient, total in weekly_totals.items()
            }
            
            # Generate recommendations based on nutrition
            recommendations = []
            
            if weekly_averages["calories"] < 1400:
                recommendations.append("Consider increasing caloric intake for better energy levels")
            elif weekly_averages["calories"] > 2200:
                recommendations.append("Consider reducing caloric intake for weight management")
            
            if weekly_averages["protein"] < 50:
                recommendations.append("Increase protein intake for muscle maintenance and satiety")
            
            if weekly_averages["fiber"] < 25:
                recommendations.append("Add more fiber-rich foods like vegetables, fruits, and whole grains")
            
            return {
                "daily_nutrition": daily_nutrition,
                "weekly_totals": weekly_totals,
                "weekly_averages": weekly_averages,
                "recommendations": recommendations,
                "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            st.error(f"Error generating nutritional analysis: {str(e)}")
            return {"error": f"Failed to generate nutritional analysis: {str(e)}"}
    
    return {
        'generate_diet_report': generate_diet_report,
        'generate_shopping_list': generate_shopping_list,
        'generate_nutritional_analysis': generate_nutritional_analysis
    }

def make_calculate_bmi_tool():
    """Create a tool to calculate BMI from weight and height."""

    @tool
    def calculate_bmi(weight: float, height: float) -> float:
        """Calculate BMI from weight (kg) and height (m)."""
        if weight <= 0 or height <= 0:
            raise ValueError("Weight and height must be positive values.")
        return weight / (height**2)

    return calculate_bmi


def make_extract_preferences_tool(llm: ChatGoogleGenerativeAI):
    """Create a tool to extract diet preferences from user input."""

    @tool
    def extract_preferences(user_input: str) -> dict:
        """Extract structured diet preferences from user input."""
        prompt = (
            f"Extract structured diet preferences from this: '{user_input}'. "
            "Return ONLY a JSON object with keys: calories, protein, allergies, likes, dislikes, budget."
        )
        response = llm.invoke(prompt)
        content = response.content

        # Handle both string and list responses
        if isinstance(content, list):
            content = content[0] if content else ""
        content = str(content).strip()

        # strip markdown fences and leading 'json' if present
        if content.startswith("```"):
            content = content.strip("`")
            if content.lower().startswith("json"):
                content = content[4:].strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse preferences JSON: {e}")
            return {}

    return extract_preferences


def make_plan_diet_tool(llm: ChatGoogleGenerativeAI):
    """Create a tool to plan a diet based on user preferences."""

    @tool
    def plan_diet(preferences: dict) -> str:
        """Plan a diet based on user preferences."""
        prompt = (
            f"Create a diet plan that meets these preferences: {preferences}. "
            "Include meals, snacks, and drinks."
        )
        response = llm.invoke(prompt)
        content = response.content

        # Handle both string and list responses
        if isinstance(content, list):
            content = content[0] if content else ""
        return str(content)

    return plan_diet
