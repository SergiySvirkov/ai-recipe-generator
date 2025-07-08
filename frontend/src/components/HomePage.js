import React, { useState } from 'react';
import RecipeGeneratorForm from './RecipeGeneratorForm';
import RecipeDisplay from './RecipeDisplay';
import './styles.css';

const HomePage = () => {
  // This component will manage the state for the main page.
  // 'generatedRecipe' will hold the recipe object returned from the API.
  const [generatedRecipe, setGeneratedRecipe] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // This function will be passed down to the form component.
  // It will be called when the form is submitted.
  const handleGenerateRecipe = (formData) => {
    console.log("Form data received in HomePage:", formData);
    setIsLoading(true);
    setGeneratedRecipe(null); // Clear previous recipe

    // Simulate an API call
    setTimeout(() => {
      const mockRecipe = {
        title: "Mock Creamy Chicken Pasta",
        ingredients: ["1 lb chicken breast", "2 cups pasta", "1 cup heavy cream", "3 cloves garlic"],
        instructions: [
          "Cook the pasta according to package directions.",
          "While pasta is cooking, sauté chicken and garlic in a pan.",
          "Reduce heat, stir in heavy cream, and simmer for 5 minutes.",
          "Combine pasta with the chicken and sauce, and serve immediately."
        ]
      };
      setGeneratedRecipe(mockRecipe);
      setIsLoading(false);
    }, 2000); // 2-second delay to simulate network latency
  };

  return (
    <div className="homepage-container">
      <RecipeGeneratorForm onGenerate={handleGenerateRecipe} isLoading={isLoading} />
      <RecipeDisplay recipe={generatedRecipe} isLoading={isLoading} />
    </div>
  );
};

export default HomePage;
