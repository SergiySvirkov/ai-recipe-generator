// frontend/src/components/HomePage.js

import React, { useState } from 'react';
import RecipeGeneratorForm from './RecipeGeneratorForm';
import RecipeDisplay from './RecipeDisplay';
import { generateRecipe, saveRecipe } from '../services/api'; // Import API functions
import './styles.css';

const HomePage = () => {
  const [generatedRecipe, setGeneratedRecipe] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerateRecipe = async (formData) => {
    setIsLoading(true);
    setError(null);
    setGeneratedRecipe(null);

    try {
      const response = await generateRecipe(formData.ingredients, formData.diet);
      setGeneratedRecipe(response.data);
    } catch (err) {
      setError('Failed to generate recipe. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveRecipe = async () => {
    if (!generatedRecipe) return;

    // Check if user is logged in (by checking for a token)
    const token = localStorage.getItem('token');
    if (!token) {
      alert('Please log in to save recipes.');
      // Here you might redirect to a login page
      return;
    }

    try {
      await saveRecipe(generatedRecipe);
      alert('Recipe saved successfully!');
    } catch (err) {
      alert('Failed to save recipe.');
      console.error(err);
    }
  };

  return (
    <div className="homepage-container">
      <RecipeGeneratorForm onGenerate={handleGenerateRecipe} isLoading={isLoading} />
      {error && <p className="error-message">{error}</p>}
      <RecipeDisplay 
        recipe={generatedRecipe} 
        isLoading={isLoading} 
        onSave={handleSaveRecipe}
      />
    </div>
  );
};

export default HomePage;
