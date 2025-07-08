# manage.py

import os
from app import create_app, db
from app.models import User, Recipe, Ingredient, DietaryRestriction

# Create the Flask application instance using the factory function.
# We use the 'development' configuration by default.
# The FLASK_APP environment variable should be set to this file (manage.py)
# for the 'flask' command-line interface to work.
app = create_app(os.getenv('FLASK_CONFIG') or 'development')

@app.shell_context_processor
def make_shell_context():
    """
    Creates a shell context that automatically imports the app, database,
    and models when 'flask shell' is run. This makes debugging and testing
    in the interactive shell easier.
    """
    return dict(
        db=db,
        User=User,
        Recipe=Recipe,
        Ingredient=Ingredient,
        DietaryRestriction=DietaryRestriction
    )

if __name__ == '__main__':
    # This block allows you to run the application directly using 'python manage.py'.
    # It's useful for starting the development server.
    # The host='0.0.0.0' makes the server accessible on your local network.
    app.run(host='0.0.0.0')
