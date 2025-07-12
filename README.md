# Brocc-Li: Intelligent Diet Assistant

An artificial Dietitian that's actually intelligent, now with comprehensive web search capabilities for grocery shopping, recipe finding, and store discovery.

## Features

### Core Diet Assistant
- **BMI Calculation**: Calculate BMI from weight and height
- **Diet Preference Extraction**: Extract structured diet preferences from user input
- **Personalized Diet Planning**: Create customized diet plans based on preferences

### Web Search & Shopping Assistant
- **🏪 Store Discovery**: Find nearby grocery stores using Google Maps API
- **💰 Price Comparison**: Compare product prices across major German stores (Rewe, Aldi, Lidl, Edeka)
- **🎫 Coupon Search**: Find available coupons and deals from various websites
- **👨‍🍳 Recipe Search**: Search for recipes from popular cooking websites including German sites
- **🌐 Web Scraping**: Scrape product information from store websites using Selenium
- **📍 Store Details**: Get detailed store information including hours and exact location
- **⚖️ Cross-Store Comparison**: Compare prices for multiple products across different stores

- Python 3.11
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/The-Doraemonians/Brocc_Li.git
    cd Brocc_Li
    ```

2.  Create a virtual environment (recommended):

    ```bash
    uv venv
    ```

3.  Install the required packages using `uv`:

    ```bash
    uv sync
    ```

## Running the Application

To start the Brocc Li application, run the following command:

```bash
streamlit run main.py
```


#### Store Discovery
```
User: "Find grocery stores near Bonn, Germany"
Agent: Uses search_nearby_stores to find nearby supermarkets
```

#### Price Comparison
```
User: "Compare prices for organic milk across stores"
Agent: Uses search_product_prices and compare_prices_across_stores
```

#### Recipe Search
```
User: "Find vegetarian pasta recipes under 30 minutes"
Agent: Uses search_recipes with dietary restrictions and time constraints
```

#### Coupon Search
```
User: "Find coupons for Rewe"
Agent: Uses search_coupons to find available deals
```

## Architecture

### Web Search Tools

The application includes a comprehensive set of web search tools:

1. **Store Discovery** (`search_nearby_stores`):
   - Uses Google Maps Places API
   - Searches for supermarkets and grocery stores
   - Returns store information with ratings and contact details

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
   - Gets detailed store information from Google Maps
   - Returns opening hours, exact location, and contact info

7. **Cross-Store Comparison** (`compare_prices_across_stores`):
   - Compares multiple products across different stores
   - Identifies best deals and price differences
