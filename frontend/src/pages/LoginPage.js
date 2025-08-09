// src/pages/LoginPage.js
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { FiLogIn, FiBookOpen } from 'react-icons/fi';
import api from '../api';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await api.post('/token', formData);
      localStorage.setItem('accessToken', response.data.access_token);
      navigate('/');
    } catch (err) {
      setError('Invalid username or password.');
    }
  };

  return (
    <div className="auth-page-container">
      <div className="auth-branding-section">
        <FiBookOpen className="icon" />
        <h1>Welcome Back to EduLLM</h1>
        <p>Your personal AI/ML tutor, ready to help you learn and explore.</p>
      </div>

      <div className="auth-form-section">
        <form onSubmit={handleSubmit} className="auth-form">
          <h2>Sign In</h2>
          <div className="input-group">
            <label htmlFor="username">Username</label>
            <input id="username" type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
          </div>
          <div className="input-group">
            <label htmlFor="password">Password</label>
            <input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          {error && <p className="error-message">{error}</p>}
          <button type="submit" className="auth-submit-button">Login</button>
          <p className="form-footer">
            Don't have an account? <Link to="/register">Register here</Link>
          </p>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;