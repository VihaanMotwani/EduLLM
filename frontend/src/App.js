import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import TextareaAutosize from 'react-textarea-autosize';
// Import new icons
import { FiSend } from 'react-icons/fi';
import { BsArrowBarLeft, BsArrowBarRight } from 'react-icons/bs';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const messagesEndRef = useRef(null);
  // At the top of your App component, with the other state variables
  const [sessionId, setSessionId] = useState(null);

  useEffect(() => {
    // Generate a unique session ID when the component mounts
    setSessionId(Date.now().toString());
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const newUserMessage = { sender: 'user', text: input };
    const updatedMessages = [...messages, newUserMessage];

    setMessages(updatedMessages);
    setInput('');
    setIsLoading(true);

    try {
      // --- THIS IS THE KEY CHANGE ---
      // The endpoint is now '/chat'
      const response = await axios.post('http://127.0.0.1:8000/chat', {
        question: input, // Send only the latest user input as the question
        session_id: sessionId,
        model: "gpt-4.1-mini" // Or whichever model you intend to use
      });

      // The backend returns the answer directly in the 'answer' field
      const aiMessage = { sender: 'ai', text: response.data.answer };
      setMessages(prev => [...prev, aiMessage]);

    } catch (error) {
      console.error('Error communicating with the agent:', error);
      const errorMessage = { sender: 'ai', text: 'Sorry, I ran into an error.' };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* --- Left Sidebar --- */}
      <aside className={`sidebar ${isSidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <h1>EduLLM</h1>
          <p className="tagline">Your personal AI/ML tutor</p>
        </div>
      </aside>

      {/* --- Main Chat Panel --- */}
      <main className="main-chat-panel">
        <header className="chat-panel-header">
          <button className="menu-button" onClick={() => setIsSidebarOpen(!isSidebarOpen)}>
            {isSidebarOpen ? <BsArrowBarLeft /> : <BsArrowBarRight />}
          </button>
        </header>
        <div className="chat-history">
          {messages.map((msg, index) => (
            <div key={index} className={`message-wrapper ${msg.sender}`}>
              {msg.sender === 'user' ? (
                <div className="user-prompt">{msg.text}</div>
              ) : (
                <div className="ai-response">
                  <ReactMarkdown>{msg.text}</ReactMarkdown>
                </div>
              )}
            </div>
          ))}
          {isLoading && (
              <div className="message-wrapper ai">
                <div className="ai-response thinking">...</div>
              </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-area">
          <form className="input-form" onSubmit={handleSubmit}>
            <TextareaAutosize
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask EduLLM anything..."
              disabled={isLoading}
              maxRows={5}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
            />
            <button type="submit" className="send-button" aria-label="Send message" disabled={!input.trim() || isLoading}>
              <FiSend />
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}

export default App;