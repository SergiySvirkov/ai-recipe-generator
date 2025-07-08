# scripts/test_generator.py

import sys
import os

# Add the root directory of the project to the Python path.
# This allows us to import modules from the 'app' package.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.ai_service import RecipeGenerator

def main():
    """
    A simple script to test the RecipeGenerator service independently.
    """
    print("--- Testing Recipe Generator ---")

    # Check if the model directory exists.
    model_path = "models/recipe-generator-distilgpt2"
    if not os.path.isdir(model_path):
        print(f"Error: Model directory not found at '{model_path}'")
        print("Please run the fine-tuning script first: python scripts/fine_tune_model.py")
        return

    # Initialize the generator. This will load the model into memory.
    try:
        generator = RecipeGenerator(model_path=model_path)
    except Exception as e:
        print(f"Failed to initialize RecipeGenerator: {e}")
        return

    # --- Test Case 1: Simple Dinner ---
    print("\n--- Test Case 1: Simple Dinner ---")
    ingredients1 = ["chicken breast", "mushrooms", "cream"]
    print(f"Input Ingredients: {ingredients1}")
    
    recipe1 = generator.generate(ingredients1)
    
    print("\n--- Generated Recipe ---")
    print(f"Title: {recipe1.get('title')}")
    print("\nIngredients:")
    for ing in recipe1.get('ingredients', []):
        print(f"- {ing}")
    print("\nInstructions:")
    for i, inst in enumerate(recipe1.get('instructions', [])):
        print(f"{i+1}. {inst}")
    print("-" * 25)

    # --- Test Case 2: Vegan Option ---
    print("\n--- Test Case 2: Vegan Option ---")
    ingredients2 = ["lentils", "carrots", "celery", "canned tomatoes"]
    diet2 = "vegan"
    print(f"Input Ingredients: {ingredients2}")
    print(f"Dietary Preference: {diet2}")
    
    recipe2 = generator.generate(ingredients2, diet=diet2)
    
    print("\n--- Generated Recipe ---")
    print(f"Title: {recipe2.get('title')}")
    print("\nIngredients:")
    for ing in recipe2.get('ingredients', []):
        print(f"- {ing}")
    print("\nInstructions:")
    for i, inst in enumerate(recipe2.get('instructions', [])):
        print(f"{i+1}. {inst}")
    print("-" * 25)


if __name__ == "__main__":
    main()
