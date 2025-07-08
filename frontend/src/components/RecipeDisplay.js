import React from 'react';
import './styles.css';

const RecipeDisplay = ({ recipe, isLoading, onSave }) => {
  if (isLoading) {
    return (
      <div className="recipe-display-container">
        <div className="loader"></div>
        <p>Generating your creative recipe...</p>
      </div>
    );
  }

  if (!recipe) {
    return (
      <div className="recipe-display-container placeholder">
        <p>Your generated recipe will appear here!</p>
      </div>
    );
  }

  return (
    <div className="recipe-display-container">
      <h2>{recipe.title}</h2>
      
      <div className="recipe-section">
        <h3>Ingredients</h3>
        <ul>
          {recipe.ingredients.map((ingredient, index) => (
            <li key={index}>{ingredient}</li>
          ))}
        </ul>
      </div>

      <div className="recipe-section">
        <h3>Instructions</h3>
        <ol>
          {recipe.instructions.map((step, index) => (
            <li key={index}>{step}</li>
          ))}
        </ol>
      </div>
      
      {/* Add a button to save the recipe */}
      <button onClick={onSave} className="save-button">
        Save Recipe
      </button>
    </div>
  );
};

export default RecipeDisplay;
