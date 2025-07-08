import React, { useState } from 'react';
import './styles.css';

const RecipeGeneratorForm = ({ onGenerate, isLoading }) => {
  // State for the form inputs
  const [ingredients, setIngredients] = useState('');
  const [diet, setDiet] = useState('any'); // Default diet option

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevent default form submission behavior
    
    // Basic validation
    if (!ingredients.trim()) {
      alert("Please enter at least one ingredient.");
      return;
    }

    // Pass the form data up to the parent component (HomePage)
    onGenerate({
      // Split ingredients by comma and trim whitespace
      ingredients: ingredients.split(',').map(ing => ing.trim()),
      diet: diet
    });
  };

  return (
    <div className="form-container">
      <h2>Generate a New Recipe</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="ingredients">Ingredients (comma separated):</label>
          <input
            type="text"
            id="ingredients"
            value={ingredients}
            onChange={(e) => setIngredients(e.target.value)}
            placeholder="e.g., chicken, potatoes, carrots"
          />
        </div>
        <div className="form-group">
          <label htmlFor="diet">Dietary Preference:</label>
          <select id="diet" value={diet} onChange={(e) => setDiet(e.target.value)}>
            <option value="any">Any</option>
            <option value="vegetarian">Vegetarian</option>
            <option value="vegan">Vegan</option>
          </select>
        </div>
        <button type="submit" className="generate-button" disabled={isLoading}>
          {isLoading ? 'Generating...' : 'Generate Recipe'}
        </button>
      </form>
    </div>
  );
};

export default RecipeGeneratorForm;
