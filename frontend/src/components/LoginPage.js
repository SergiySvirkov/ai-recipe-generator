import React, { useState } from 'react';
import { loginUser, registerUser } from '../services/api';
import './styles.css';

const LoginPage = ({ onLoginSuccess }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      if (isLogin) {
        // Handle Login
        const response = await loginUser(username, password);
        const token = response.data.token;
        localStorage.setItem('token', token); // Store token in localStorage
        onLoginSuccess(token); // Notify parent component
      } else {
        // Handle Register
        await registerUser(username, password);
        alert('Registration successful! Please log in.');
        setIsLogin(true); // Switch to login form
      }
    } catch (err) {
      setError(err.response?.data?.message || 'An error occurred.');
      console.error(err);
    }
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>{isLogin ? 'Login' : 'Register'}</h2>
        {error && <p className="error-message">{error}</p>}
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit" className="generate-button">
          {isLogin ? 'Login' : 'Register'}
        </button>
        <button type="button" className="toggle-auth" onClick={() => setIsLogin(!isLogin)}>
          {isLogin ? 'Need an account? Register' : 'Have an account? Login'}
        </button>
      </form>
    </div>
  );
};

export default LoginPage;
