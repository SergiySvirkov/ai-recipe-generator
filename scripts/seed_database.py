# scripts/seed_database.py

import json
from app import create_app, db
from app.models import Recipe, Ingredient, DietaryRestriction, User

def load_json_data(filepath):
    """Loads data from a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
        return None

def seed_database():
    """
    Fills the database with initial data from the cleaned dataset.
    This script should be run once to set up the database.
    """
    # Create a Flask application context to work with the database.
    app = create_app('development')
    with app.app_context():
        print("Starting database seeding...")

        # --- Clear existing data ---
        # This is destructive. Be careful running this on a production database.
        print("Clearing existing data from Recipe and Ingredient tables...")
        db.session.query(Recipe).delete()
        db.session.query(Ingredient).delete()
        db.session.query(DietaryRestriction).delete()
        db.session.query(User).delete()
        db.session.commit()

        # --- Seed Dietary Restrictions ---
        print("Seeding dietary restrictions...")
        restrictions = ['Vegan', 'Vegetarian', 'Gluten-Free', 'Dairy-Free']
        for name in restrictions:
            restriction = DietaryRestriction(name=name)
            db.session.add(restriction)
        db.session.commit()
        print(f"Seeded {len(restrictions)} dietary restrictions.")

        # --- Seed a default User ---
        print("Seeding a default user...")
        default_user = User(username='default_author')
        db.session.add(default_user)
        db.session.commit()

        # --- Seed Recipes and Ingredients ---
        recipes_data = load_json_data('data/train_dataset.json')
        if not recipes_data:
            print("No recipe data found. Exiting.")
            return

        print(f"Found {len(recipes_data)} recipes to seed.")
        
        # Keep a cache of ingredients to avoid querying the DB for every ingredient.
        ingredient_cache = {}

        for i, recipe_data in enumerate(recipes_data):
            print(f"Processing recipe {i+1}/{len(recipes_data)}: {recipe_data['title']}")
            
            # Create the Recipe object
            new_recipe = Recipe(
                title=recipe_data['title'],
                instructions=recipe_data['instructions'], # The setter will handle JSON conversion
                author=default_user
            )
            
            # Process ingredients
            for ingredient_name in recipe_data['ingredients']:
                # For simplicity, we extract the base name from the ingredient line.
                # A more robust solution would parse quantities and units separately.
                # Example: "1 cup flour" -> "flour"
                base_name = ingredient_name.split(' ', 1)[-1] if ' ' in ingredient_name else ingredient_name
                base_name = base_name.strip()

                if base_name in ingredient_cache:
                    ingredient = ingredient_cache[base_name]
                else:
                    ingredient = db.session.query(Ingredient).filter_by(name=base_name).first()
                    if not ingredient:
                        ingredient = Ingredient(name=base_name)
                        db.session.add(ingredient)
                    ingredient_cache[base_name] = ingredient
                
                new_recipe.ingredients.add(ingredient)
            
            db.session.add(new_recipe)

        # Commit all new records to the database
        print("Committing all new recipes and ingredients to the database...")
        db.session.commit()
        print("Database seeding complete!")

if __name__ == '__main__':
    seed_database()
