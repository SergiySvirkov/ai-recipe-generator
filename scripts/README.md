# Scripts

<!-- This directory contains various helper scripts for the project, primarily for data processing tasks. -->

This directory holds standalone Python scripts used for various data-related tasks that are not part of the main Flask application logic.

## Scripts Overview

- **`scrape_recipes.py`**: A script to scrape recipe data from websites. This is the first step in building our dataset. **Note:** This script must be adapted for the specific structure of the target website.
- **`clean_data.py`** (to be created later): A script for cleaning and standardizing the raw scraped data before it's used to train the AI model.

## How to Run Scripts

Ensure you have the necessary dependencies installed. You can run any script from the root directory of the project, for example:

```bash
# Activate your virtual environment first
source venv/bin/activate

# Run the scraping script
python scripts/scrape_recipes.py
