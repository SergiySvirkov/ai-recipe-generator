# app/api/routes.py

from flask import request, jsonify
from . import api
from .. import recipe_generator # Import the shared instance of the generator

@api.route('/generate-recipe', methods=['POST'])
def generate_recipe_endpoint():
    """
    API endpoint to generate a recipe.
    Expects a JSON payload with 'ingredients' and an optional 'diet'.
    """
    # Get the JSON data from the request.
    data = request.get_json()
    
    # --- Input Validation ---
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
        
    ingredients = data.get('ingredients')
    if not ingredients or not isinstance(ingredients, list) or len(ingredients) == 0:
        return jsonify({"error": "Missing or invalid 'ingredients' list"}), 400

    diet = data.get('diet', 'any') # Default to 'any' if not provided

    print(f"Received request to generate recipe with ingredients: {ingredients}, diet: {diet}")

    # --- Call the AI Service ---
    # Use the pre-loaded recipe_generator instance to generate the recipe.
    try:
        generated_recipe = recipe_generator.generate(ingredients, diet)
        return jsonify(generated_recipe), 200
    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred during recipe generation: {e}")
        return jsonify({"error": "Failed to generate recipe"}), 500

