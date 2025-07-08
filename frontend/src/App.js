import './App.css';
import React from 'react';
import Navbar from './components/Navbar';
import HomePage from './components/HomePage';
// import LoginPage from './components/LoginPage'; // Uncomment to use login page

function App() {
  // For now, we will just display the HomePage.
  // In a real app, you would have routing logic here to switch
  // between HomePage, LoginPage, etc.
  return (
    <div className="App">
      <Navbar />
      <main>
        <HomePage />
        {/* <LoginPage /> */}
      </main>
    </div>
  );
}

export default App;
