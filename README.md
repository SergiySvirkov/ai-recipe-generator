AI-Powered Personalized Recipe Generator

An innovative platform that generates unique recipes based on user preferences, available ingredients, and dietary restrictions using a fine-tuned generative AI model.
✨ Features

    AI-Powered Recipe Generation: Provide a list of ingredients and get a completely new, unique recipe in seconds.

    Dietary Customization: Filter recipes by dietary needs like "Vegan" or "Vegetarian".

    User Authentication: Secure user registration and login using JWT (JSON Web Tokens).

    Save Your Favorites: Logged-in users can save their favorite generated recipes to their personal collection.

    RESTful API: A well-documented backend API for easy integration and future development.

    Responsive UI: A clean and modern user interface that works seamlessly on both desktop and mobile devices.

🚀 Live Demo (Placeholder)

[A link to the live, deployed application will be here.]
🛠️ Technology Stack

Category
	

Technology

Backend
	

Python, Flask, Flask-SQLAlchemy, Flask-CORS, Gunicorn

Frontend
	

React.js, Axios

Database
	

PostgreSQL (Production), SQLite (Development)

AI / ML
	

PyTorch, Hugging Face Transformers (DistilGPT-2)

Auth
	

Flask-Bcrypt (Password Hashing), PyJWT (Tokens)

Validation
	

Flask-Marshmallow
📂 Project Structure

This project follows a monorepo-like structure:

    /: The root contains the Flask backend application and project documentation.

    /frontend: Contains the standalone React frontend application.

📋 Prerequisites

Before you begin, ensure you have the following installed on your local machine:

    Python (version 3.9 or higher)

    Node.js (version 16 or higher) and npm

    PostgreSQL (optional, for production-like setup)

⚙️ Setup and Installation

Follow these steps to get your development environment set up.
1. Backend Setup

From the project's root directory:

a. Create and activate a virtual environment:

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate

b. Install Python dependencies:

pip install -r requirements.txt

c. Set up the database:
This project uses Flask-Migrate to manage database schemas.

# Set the FLASK_APP environment variable
export FLASK_APP=manage.py # (Use 'set' on Windows)

# Initialize the migration repository (only needs to be run once)
flask db init

# Generate the initial migration script based on the models
flask db migrate -m "Initial migration"

# Apply the migration to create the database tables
flask db upgrade

d. Seed the database with initial data (optional):
The seeding script populates the database with some initial recipes and ingredients.

python scripts/seed_database.py

2. AI Model Setup

The AI model needs to be fine-tuned on the dataset. This is a one-time process that can take a while.

# This script will download the base model and fine-tune it.
# The final model will be saved in the `models/` directory (which is ignored by Git).
python scripts/fine_tune_model.py

3. Frontend Setup

Navigate to the frontend directory and install the Node.js dependencies.

cd frontend
npm install

▶️ Running the Application

You need to run the backend and frontend servers concurrently in two separate terminal windows.

1. Run the Backend Server:
Make sure you are in the root directory and your virtual environment is activated.

flask run

The Flask API will be running at http://127.0.0.1:5000.

2. Run the Frontend Server:
Make sure you are in the frontend directory.

npm start

The React application will open automatically in your browser at http://localhost:3000.

You should now be able to use the full application!
📚 API Documentation

Detailed information about the available API endpoints can be found in the documentation.

    API Endpoints Guide

    Validation and Error Handling

🔮 Future Work

    [ ] Allow users to upload their own recipes to fine-tune their personal model.

    [ ] Generate images for the created recipes using a diffusion model.

    [ ] Add more complex personalization filters (e.g., cooking time, available kitchen tools, mood).

    [ ] Implement social features like sharing recipes with other users.
