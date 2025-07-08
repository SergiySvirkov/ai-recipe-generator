# scripts/clean_data.py

import json
import re
import random
import os

# --- Configuration ---
# Input file from the scraping step
RAW_DATA_PATH = "data/raw_recipes.json"

# Output files for the cleaned and split data
CLEANED_TRAIN_PATH = "data/train_dataset.json"
CLEANED_VALIDATION_PATH = "data/validation_dataset.json"

# Percentage of data to use for the validation set
VALIDATION_SPLIT_RATIO = 0.2

# --- Normalization Dictionaries ---
# This approach makes it easy to add more normalization rules later.

# Dictionary for standardizing units of measurement
UNIT_NORMALIZATION_MAP = {
    # Weight
    r'\b(grams?|gr?)\b': 'g',
    r'\b(kilograms?|kg)\b': 'kg',
    r'\b(ounces?|oz)\b': 'oz',
    r'\b(pounds?|lbs?)\b': 'lb',
    # Volume
    r'\b(milliliters?|ml)\b': 'ml',
    r'\b(liters?|l)\b': 'l',
    r'\b(teaspoons?|tsp)\b': 'tsp',
    r'\b(tablespoons?|tbsp)\b': 'tbsp',
    r'\b(cups?|c)\b': 'cup',
    # Other common terms
    r'\b(cloves?)\b': 'clove',
}

# Dictionary for standardizing ingredient names
# This is a simple example. A more advanced system might use lemmatization.
INGREDIENT_NORMALIZATION_MAP = {
    r'large onion': 'onion',
    r'red onion': 'onion',
    r'yellow onion': 'onion',
    r'garlic clove': 'garlic',
    r'chicken breasts?': 'chicken breast',
    r'crushed tomatoes?': 'canned tomatoes',
    r'olive oil': 'olive oil', # To handle cases like 'extra virgin olive oil'
}


def load_json_data(filepath):
    """Loads data from a JSON file."""
    print(f"Loading data from {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found. Please run the scraping script first.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}. The file might be corrupted or empty.")
        return None

def save_json_data(data, filepath):
    """Saves data to a JSON file."""
    print(f"Saving {len(data)} items to {filepath}...")
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Save successful.")
    except IOError as e:
        print(f"Error writing to file {filepath}: {e}")

def normalize_ingredient_line(line):
    """Normalizes a single ingredient line for units and names."""
    line = line.lower() # Convert to lowercase for consistent matching
    
    # Normalize units
    for pattern, replacement in UNIT_NORMALIZATION_MAP.items():
        line = re.sub(pattern, replacement, line)
        
    # Normalize ingredient names
    for pattern, replacement in INGREDIENT_NORMALIZATION_MAP.items():
        line = re.sub(pattern, replacement, line)
        
    # Remove extra whitespace
    line = re.sub(r'\s+', ' ', line).strip()
    
    return line

def clean_recipe(recipe):
    """
    Cleans a single recipe object by normalizing its ingredients
    and performing basic validation.
    """
    # Normalize title and category
    recipe['title'] = recipe.get('title', 'Untitled').strip()
    recipe['category'] = recipe.get('category', 'Uncategorized').strip()

    # Normalize ingredients
    original_ingredients = recipe.get('ingredients', [])
    if not original_ingredients:
        return None # Skip recipes with no ingredients
    
    cleaned_ingredients = [normalize_ingredient_line(ing) for ing in original_ingredients]
    recipe['ingredients'] = cleaned_ingredients
    
    # Validate instructions
    instructions = recipe.get('instructions', [])
    if not instructions or len(instructions) < 2:
        return None # Skip recipes with no or very few instructions

    recipe['instructions'] = [inst.strip() for inst in instructions]

    return recipe


def main():
    """Main function to orchestrate the cleaning and splitting process."""
    print("--- Starting Data Cleaning and Normalization Script ---")
    
    raw_recipes = load_json_data(RAW_DATA_PATH)
    if raw_recipes is None:
        return # Exit if data loading failed

    print(f"Loaded {len(raw_recipes)} raw recipes.")
    
    cleaned_recipes = []
    seen_titles = set()

    for recipe in raw_recipes:
        # 1. Remove duplicates based on title
        title = recipe.get('title', '').strip().lower()
        if not title or title in seen_titles:
            continue
        seen_titles.add(title)
        
        # 2. Clean and normalize the recipe
        cleaned = clean_recipe(recipe)
        
        # 3. Add to our list if it's a valid, cleaned recipe
        if cleaned:
            cleaned_recipes.append(cleaned)
            
    print(f"Finished cleaning. Kept {len(cleaned_recipes)} unique and valid recipes.")
    
    # 4. Shuffle the data for random splitting
    random.shuffle(cleaned_recipes)
    
    # 5. Split the data into training and validation sets
    split_index = int(len(cleaned_recipes) * (1 - VALIDATION_SPLIT_RATIO))
    train_data = cleaned_recipes[:split_index]
    validation_data = cleaned_recipes[split_index:]
    
    print(f"Splitting data into {len(train_data)} training samples and {len(validation_data)} validation samples.")
    
    # 6. Save the processed datasets
    save_json_data(train_data, CLEANED_TRAIN_PATH)
    save_json_data(validation_data, CLEANED_VALIDATION_PATH)
    
    print("\n--- Data cleaning process complete! ---")
    print(f"Training data saved to: {CLEANED_TRAIN_PATH}")
    print(f"Validation data saved to: {CLEANED_VALIDATION_PATH}")


if __name__ == "__main__":
    main()

