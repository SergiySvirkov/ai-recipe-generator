# This file now solely handles the AI generation logic.

from flask import request, jsonify
from . import api
from .. import recipe_generator

@api.route('/generate-recipe', methods=['POST'])
def generate_recipe_endpoint():
    """API endpoint to generate a recipe."""
    data = request.get_json()
    if not data or not data.get('ingredients'):
        return jsonify({"error": "Missing or invalid 'ingredients' list"}), 400

    ingredients = data.get('ingredients')
    diet = data.get('diet', 'any')
    
    try:
        generated_recipe = recipe_generator.generate(ingredients, diet)
        return jsonify(generated_recipe), 200
    except Exception as e:
        print(f"An error occurred during recipe generation: {e}")
        return jsonify({"error": "Failed to generate recipe"}), 500
