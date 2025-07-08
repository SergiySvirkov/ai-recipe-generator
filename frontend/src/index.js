import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

// Create a root instance for rendering the React application.
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the main App component inside React's StrictMode.
// StrictMode is a tool for highlighting potential problems in an application.
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
