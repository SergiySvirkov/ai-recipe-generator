import React from 'react';
import './styles.css';

const Navbar = ({ token, onLogout }) => {
  return (
    <nav className="navbar">
      <h1>AI Recipe Generator</h1>
      {token ? (
        <button onClick={onLogout} className="nav-button logout">Logout</button>
      ) : (
        // In a real app, this might link to the login page
        <p className="nav-login-prompt">Login to save recipes</p>
      )}
    </nav>
  );
};

export default Navbar;
