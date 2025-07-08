import React from 'react';
import './styles.css'; // We'll create this CSS file

const Navbar = () => {
  // This is a simple presentational component for the top navigation bar.
  return (
    <nav className="navbar">
      <h1>AI Recipe Generator</h1>
      {/* In the future, this button can handle login/logout logic */}
      <button className="nav-button">Login</button>
    </nav>
  );
};

export default Navbar;
