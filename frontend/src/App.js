import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState("Connecting to backend...");

  useEffect(() => {
    // Simulating a successful connection for now
    setMessage("Backend connection will be here.");
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to EduLLM</h1>
        <p>{message}</p>
      </header>
    </div>
  );
}

export default App;