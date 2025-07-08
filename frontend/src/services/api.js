// frontend/src/services/api.js

import axios from 'axios';

// Create an instance of axios with a base URL.
// This makes it easy to change the API endpoint in one place.
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000/api/v1', // Your Flask backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the JWT token in the headers
// for every request that requires authentication.
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['x-access-token'] = token;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// --- API Service Functions ---

export const generateRecipe = (ingredients, diet) => {
  return apiClient.post('/generate-recipe', { ingredients, diet });
};

export const loginUser = (username, password) => {
  // For login, we use Basic Authentication.
  return apiClient.post('/users/login', {}, {
    auth: {
      username,
      password,
    },
  });
};

export const registerUser = (username, password) => {
  return apiClient.post('/users/register', { username, password });
};

export const saveRecipe = (recipeData) => {
  return apiClient.post('/recipes', recipeData);
};

export const getSavedRecipes = () => {
  return apiClient.get('/recipes');
};
