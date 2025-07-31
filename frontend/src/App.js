import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/')
      .then(response => {
        setMessage(response.data.Hello);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
        setMessage('Could not connect to backend');
      });
  }, []); // The empty array ensures this effect runs only once

  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to EduLLM</h1>
        <p>Message from backend: <strong>{message}</strong></p>
      </header>
    </div>
  );
}

export default App;