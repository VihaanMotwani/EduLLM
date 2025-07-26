import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [message, setMessage] = useState("Connecting to backend...");

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/')
      .then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.error('Error connecting to the backend:', error);
        setMessage('Failed to connect to the backend.');
      });
  }, []); // The empty array [] means this effect runs only once when the component loads

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