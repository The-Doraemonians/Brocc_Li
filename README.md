# Brocc Li

## Overview

Your Personalized Diet Management Companion.

## Setup

### Prerequisites

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
