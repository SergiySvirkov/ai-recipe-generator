# scripts/scrape_recipes.py

import requests
import json
import time
from bs4 import BeautifulSoup

# --- Configuration ---
# NOTE: This is a placeholder URL. You must replace it with the actual URL 
# of a recipe category page on a website you are allowed to scrape.
BASE_URL = "[https://example-recipe-website.com/category/dinner](https://example-recipe-website.com/category/dinner)"

# --- CSS Selectors ---
# IMPORTANT: These are EXAMPLE selectors. You MUST inspect the HTML structure
# of your target website and find the correct selectors for each data point.
# Use your browser's developer tools (Right-click -> Inspect) to find them.
recipe_links_selector = "a.recipe-card-link"  # Selector to find links to individual recipe pages
title_selector = "h1.recipe-title"  # Selector for the recipe title
ingredient_selector = "li.ingredient"  # Selector for each ingredient list item
instructions_selector = "ol.instructions > li"  # Selector for each instruction step
category_selector = "a.category-link" # Selector for the category or cuisine type

# --- Output File ---
OUTPUT_FILE = "data/raw_recipes.json"

def get_recipe_urls(category_url):
    """
    Fetches the main category page and extracts URLs for individual recipes.

    Args:
        category_url (str): The URL of the page listing multiple recipes.

    Returns:
        list: A list of absolute URLs to recipe pages.
    """
    print(f"Fetching recipe links from: {category_url}")
    try:
        response = requests.get(category_url, headers={'User-Agent': 'My Recipe Scraper 1.0'})
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all anchor tags that match the selector
        links = soup.select(recipe_links_selector)
        
        # Construct absolute URLs
        base_domain = "[https://example-recipe-website.com](https://example-recipe-website.com)" # Replace with the actual domain
        recipe_urls = [base_domain + link['href'] for link in links if 'href' in link.attrs]
        
        print(f"Found {len(recipe_urls)} recipe links.")
        return recipe_urls
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {category_url}: {e}")
        return []

def parse_recipe_page(recipe_url):
    """
    Parses a single recipe page to extract its title, ingredients, and instructions.

    Args:
        recipe_url (str): The URL of the recipe page.

    Returns:
        dict: A dictionary containing the recipe data, or None if parsing fails.
    """
    print(f"  > Parsing recipe: {recipe_url}")
    try:
        response = requests.get(recipe_url, headers={'User-Agent': 'My Recipe Scraper 1.0'})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the title
        title_element = soup.select_one(title_selector)
        title = title_element.get_text(strip=True) if title_element else "No Title Found"
        
        # Find all ingredients
        ingredient_elements = soup.select(ingredient_selector)
        # Use .strip() to remove leading/trailing whitespace from each ingredient
        ingredients = [elem.get_text(strip=True) for elem in ingredient_elements]
        
        # Find all instructions
        instruction_elements = soup.select(instructions_selector)
        instructions = [elem.get_text(strip=True) for elem in instruction_elements]

        # Find the category
        category_element = soup.select_one(category_selector)
        category = category_element.get_text(strip=True) if category_element else "Uncategorized"

        # Basic validation: ensure we have the essential data
        if not title or not ingredients or not instructions:
            print(f"  > Warning: Missing essential data on {recipe_url}. Skipping.")
            return None
            
        return {
            "source_url": recipe_url,
            "title": title,
            "category": category,
            "ingredients": ingredients,
            "instructions": instructions
        }

    except requests.exceptions.RequestException as e:
        print(f"  > Error fetching recipe page {recipe_url}: {e}")
        return None
    except Exception as e:
        print(f"  > An error occurred while parsing {recipe_url}: {e}")
        return None

def main():
    """
    Main function to orchestrate the scraping process.
    """
    print("--- Starting Recipe Scraper ---")
    
    # First, get all the individual recipe URLs from the main category page
    # For this example, we'll use a placeholder list.
    # In a real scenario, you would call: recipe_urls = get_recipe_urls(BASE_URL)
    # To avoid making live requests in this example, we use a mock list.
    # REMINDER: Replace this with a call to get_recipe_urls(BASE_URL) for your project.
    mock_recipe_urls = [
        "[https://example-recipe-website.com/recipe/mock-pasta](https://example-recipe-website.com/recipe/mock-pasta)",
        "[https://example-recipe-website.com/recipe/mock-chicken-curry](https://example-recipe-website.com/recipe/mock-chicken-curry)"
    ]
    
    all_recipes = []
    
    # It's better to have a placeholder function to simulate parsing for the example
    def simulate_parsing(url):
        if "pasta" in url:
            return {
                "source_url": url, "title": "Mock Creamy Tomato Pasta", "category": "Italian",
                "ingredients": ["1 lb pasta", "1 can crushed tomatoes", "1/2 cup heavy cream", "2 cloves garlic"],
                "instructions": ["Boil pasta.", "Sauté garlic.", "Add tomatoes and cream.", "Combine with pasta."]
            }
        if "curry" in url:
            return {
                "source_url": url, "title": "Mock Simple Chicken Curry", "category": "Indian",
                "ingredients": ["1 lb chicken breast", "1 can coconut milk", "1 tbsp curry powder", "1 onion"],
                "instructions": ["Sauté onion.", "Cook chicken.", "Add coconut milk and curry powder.", "Simmer for 20 minutes."]
            }
        return None

    # Loop through each URL and parse the recipe
    for url in mock_recipe_urls:
        # In a real scenario, you would call: recipe_data = parse_recipe_page(url)
        recipe_data = simulate_parsing(url) # Using simulation for this example
        
        if recipe_data:
            all_recipes.append(recipe_data)
        
        # --- BE A RESPONSIBLE SCRAPER ---
        # Wait for a short period between requests to avoid overwhelming the server.
        print("  > Waiting 1 second before next request...")
        time.sleep(1)
        
    if not all_recipes:
        print("No recipes were scraped. Exiting.")
        return

    # Save the collected data to a JSON file
    print(f"\nScraping complete. Total recipes collected: {len(all_recipes)}")
    
    # Ensure the 'data' directory exists (though it should not be in git)
    import os
    os.makedirs('data', exist_ok=True)
    
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            # Use indent=4 for pretty-printing the JSON
            json.dump(all_recipes, f, ensure_ascii=False, indent=4)
        print(f"Successfully saved data to {OUTPUT_FILE}")
    except IOError as e:
        print(f"Error writing to file {OUTPUT_FILE}: {e}")

if __name__ == "__main__":
    main()

