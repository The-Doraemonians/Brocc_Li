# Brocc Li

## Overview

Your Personalized Diet Management Companion.

## Setup

### Prerequisites

- Python 3.11
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/The-Doraemonians/Brocc_Li.git
   cd Brocc_Li
   ```
2. If you are using pip:
   
   ```bash
   pip install -r requirements
   ```
3. Create a virtual environment (optinal):

   ```bash
   uv venv
   ```
4. Install the required packages using `uv` (optinal):

   ```bash
   uv sync
   ```

## Running the Application

To start the Brocc Li application, run the following command:

```bash
streamlit run main.py
```

### Project Architecture

```
brocc_li/                  # Python package
├── __init__.py            # package marker
├── app.py                 # Streamlit entrypoint: orchestrates UI
├── agent.py               # Agent initialization, agent state graph, and tool factories
├── schemas.py             # Pydantic/TypedDict schemas for agent state and chat
├── state.py               # Streamlit session state helpers
├── tools.py               # Tool factory functions for agent (make_calculate_bmi_tool, etc.)
├── ui.py                  # UI composition helpers
├── utils.py               # Utility functions
└── ...                    # (other files and folders)
```

## Features

### Core Diet Assistant

- **BMI Calculation**: Calculate BMI from weight and height
- **Diet Preference Extraction**: Extract structured diet preferences from user input
- **Personalized Diet Planning**: Create customized diet plans based on preferences

### Web Search & Shopping Assistant

- **🏪 Store Discovery**: Find nearby grocery stores using free OpenStreetMap services
- **💰 Price Comparison**: Compare product prices across major German stores (Rewe, Aldi, Lidl, Edeka)
- **🎫 Coupon Search**: Find available coupons and deals from various websites
- **👨‍🍳 Recipe Search**: Search for recipes from popular cooking websites including German sites
- **🌐 Web Scraping**: Scrape product information from store websites using Selenium
- **📍 Store Details**: Get detailed store information including hours and exact location
- **⚖️ Cross-Store Comparison**: Compare prices for multiple products across different stores

### 📊 Advanced Report Generation

- **Comprehensive Diet Reports**: Generate complete 7-day meal plans with nutritional breakdown
- **Smart Shopping Lists**: Create categorized shopping lists with price estimates
- **Nutritional Analysis**: Detailed analysis of meal plans with health recommendations
- **Cost Optimization**: Budget planning and cost-saving suggestions
- **Personalized Recommendations**: AI-powered advice for diet improvements

## Test questions

to test the usage, u may use the following prompt example:

```
I am a 30-year-old female, 165 cm tall and weigh 62 kg. My goal is to lose weight.
I live in Berlin, Germany, and I don't want to travel more than 2 km for groceries.
I prefer a vegetarian diet, love Italian cuisine, and am allergic to peanuts.
I have basic cooking skills and can spend up to 30 minutes per meal.
My daily food budget is 15 euros, and I would like to prioritize deals and discounts.
```

User: "Find grocery stores near Bonn, Germany"
Agent: ✅ Uses free OpenStreetMap services to find nearby stores

User: "Compare prices for organic milk"
Agent: ✅ Searches German store websites for price comparison

User: "Find vegetarian pasta recipes"
Agent: ✅ Searches multiple recipe websites for recipes

User: "Generate a complete diet report for me"
Agent: ✅ Creates comprehensive 7-day meal plan with shopping list and nutritional analysis

## Report Generation Tools

### 🎯 Comprehensive Diet Reports

The `generate_diet_report` tool creates complete diet plans including:

#### **User Profile Analysis**

- Age, gender, height, weight, and fitness goals
- Dietary restrictions and allergies
- Budget constraints and cooking preferences
- Location-based store recommendations

#### **7-Day Meal Plan**

- **Breakfast, Lunch, Dinner, and Snacks** for each day
- **Nutritional breakdown** per meal (calories, protein, carbs, fat)
- **Cost estimates** for budget planning
- **Preparation time** for each meal
- **Ingredient lists** with quantities

#### **Smart Shopping List**

- **Categorized ingredients** (proteins, vegetables, fruits, grains, dairy, pantry)
- **Quantity calculations** based on meal plan
- **Price estimates** by food category
- **Store recommendations** for best deals
- **Budget optimization** tips

#### **Nutritional Analysis**

- **Daily and weekly totals** for all nutrients
- **Average daily intake** calculations
- **Goal-based recommendations** (weight loss, muscle gain, etc.)
- **Health insights** and improvement suggestions

#### **Personalized Recommendations**

- **Nutritional improvements** based on analysis
- **Cost savings** suggestions
- **Time management** tips
- **Shopping optimization** advice

### 🛒 Shopping List Generator

The `generate_shopping_list` tool provides:

- **Automatic ingredient extraction** from meal plans
- **Smart categorization** of food items
- **Quantity optimization** to minimize waste
- **Price estimation** based on food categories
- **Store-specific recommendations**

### 🔬 Nutritional Analysis Tool

The `generate_nutritional_analysis` tool offers:

- **Comprehensive nutrient tracking** (calories, protein, carbs, fat, fiber, sugar, sodium)
- **Daily and weekly averages**
- **Goal-based recommendations**
- **Health improvement suggestions**

## Usage Examples

### Generate Complete Diet Report

```
User: "Generate a complete diet report for me"
Agent: Creates comprehensive 7-day meal plan with:
- Personalized meal suggestions
- Nutritional breakdown
- Shopping list with prices
- Cost optimization tips
- Health recommendations
```

### Create Shopping List

```
User: "Create a shopping list for my meal plan"
Agent: Generates categorized shopping list with:
- Ingredient quantities
- Price estimates
- Store recommendations
- Budget optimization
```

### Analyze Nutrition

```
User: "Analyze the nutrition of my diet plan"
Agent: Provides detailed analysis including:
- Daily and weekly nutritional totals
- Goal-based recommendations
- Health improvement suggestions
- Nutritional balance assessment
```

### Web Search Tools

The application includes a comprehensive set of web search tools:

1. **Store Discovery** (`search_nearby_stores`):

   - Uses **OpenStreetMap Overpass API** (free)
   - Searches for supermarkets and grocery stores
   - Returns store information with addresses and contact details
   - **No API key required!**
2. **Price Comparison** (`search_product_prices`):

   - Searches major German grocery store websites
   - Supports Rewe, Aldi, Lidl, and Edeka
   - Returns product availability and pricing
3. **Coupon Search** (`search_coupons`):

   - Searches popular German coupon websites
   - Returns coupon codes, discounts, and expiry dates
4. **Recipe Search** (`search_recipes`):

   - Searches international and German recipe sites
   - Supports dietary restrictions and time constraints
   - Returns ingredients, instructions, and cooking times
5. **Web Scraping** (`scrape_store_website`):

   - Uses Selenium for dynamic content scraping
   - Handles JavaScript-rendered content
   - Extracts product information from store websites
6. **Store Details** (`get_store_hours_and_location`):

   - Gets detailed store information from OpenStreetMap
   - Returns opening hours, exact location, and contact info
   - **No API key required!**
7. **Cross-Store Comparison** (`compare_prices_across_stores`):

   - Compares multiple products across different stores
   - Identifies best deals and price differences

### Report Generation Tools

The application includes advanced report generation capabilities:

1. **Diet Report Generation** (`generate_diet_report`):

   - Creates comprehensive 7-day meal plans
   - Generates nutritional breakdown and cost analysis
   - Produces categorized shopping lists
   - Provides personalized recommendations
2. **Shopping List Generation** (`generate_shopping_list`):

   - Extracts ingredients from meal plans
   - Categorizes items by food type
   - Estimates costs and quantities
   - Optimizes for budget and efficiency
3. **Nutritional Analysis** (`generate_nutritional_analysis`):

   - Analyzes meal plan nutritional content
   - Provides daily and weekly summaries
   - Generates health recommendations
   - Tracks progress toward goals
