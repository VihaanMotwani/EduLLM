// src/pages/RegisterPage.js
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { FiUserPlus, FiBookOpen } from 'react-icons/fi';
import api from '../api';

function RegisterPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await api.post('/register', { username, password });
      navigate('/login');
    } catch (err) {
      setError('Username may already be taken. Please try another.');
    }
  };

  return (
    <div className="auth-page-container">
      <div className="auth-branding-section">
        <FiBookOpen className="icon" />
        <h1>Join EduLLM</h1>
        <p>Create your account to start your personalized learning journey.</p>
      </div>
      <div className="auth-form-section">
        <form onSubmit={handleSubmit} className="auth-form">
          <h2>Create Account</h2>
          <div className="input-group">
            <label htmlFor="username">Username</label>
            <input id="username" type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
          </div>
          <div className="input-group">
            <label htmlFor="password">Password</label>
            <input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          {error && <p className="error-message">{error}</p>}
          <button type="submit" className="auth-submit-button">Register</button>
          <p className="form-footer">
            Already have an account? <Link to="/login">Sign in</Link>
          </p>
        </form>
      </div>
    </div>
  );
}

export default RegisterPage;