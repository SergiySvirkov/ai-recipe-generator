import './App.css';
import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import HomePage from './components/HomePage';
import LoginPage from './components/LoginPage';

function App() {
  const [token, setToken] = useState(null);

  // Check for a token in localStorage when the app loads
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setToken(storedToken);
    }
  }, []);

  const handleLoginSuccess = (newToken) => {
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  return (
    <div className="App">
      <Navbar token={token} onLogout={handleLogout} />
      <main>
        {/* Simple routing: show login page if no token, else show homepage */}
        {!token ? (
          <LoginPage onLoginSuccess={handleLoginSuccess} />
        ) : (
          <HomePage />
        )}
      </main>
    </div>
  );
}

export default App;
