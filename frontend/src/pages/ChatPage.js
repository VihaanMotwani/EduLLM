import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import TextareaAutosize from 'react-textarea-autosize';
import { FiSend, FiPlus, FiLogOut } from 'react-icons/fi';
import api from '../api'; // Your configured axios instance
import '../App.css'; // We can reuse the existing CSS

function ChatPage() {
  const navigate = useNavigate();
  const messagesEndRef = useRef(null);

  // State Management
  const [chats, setChats] = useState([]); // List of all chat threads for the sidebar
  const [currentChatId, setCurrentChatId] = useState(null); // ID of the currently active chat
  const [messages, setMessages] = useState([]); // Messages of the active chat
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // --- Data Fetching Effects ---

  // Effect to fetch the list of chats when the component mounts
  useEffect(() => {
    const fetchChats = async () => {
      try {
        const response = await api.get('/chats');
        setChats(response.data);
        // If there are chats, select the most recent one
        if (response.data.length > 0) {
          setCurrentChatId(response.data[0].id);
        }
      } catch (error) {
        console.error('Failed to fetch chats:', error);
      }
    };
    fetchChats();
  }, []);

  // Effect to fetch messages whenever the currentChatId changes
  useEffect(() => {
    if (!currentChatId) return;

    const fetchMessages = async () => {
      setIsLoading(true);
      try {
        const response = await api.get(`/chats/${currentChatId}/messages`);
        setMessages(response.data.map(msg => ({
          sender: msg.role,
          text: msg.content
        })));
      } catch (error) {
        console.error('Failed to fetch messages:', error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchMessages();
  }, [currentChatId]);

  // --- Event Handlers ---

  const handleNewChat = async () => {
    try {
      const response = await api.post('/chats');
      const newChat = response.data;
      setChats([newChat, ...chats]); // Add new chat to the top of the list
      setCurrentChatId(newChat.id);
      setMessages([]); // Start with an empty message list
    } catch (error) {
      console.error('Failed to create new chat:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading || !currentChatId) return;

    const userMessage = { sender: 'human', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await api.post('/chat', {
        question: input,
        chat_id: currentChatId,
        model: "gpt-4.1-mini"
      });

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

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    navigate('/login');
  };
  
  // Auto-scroll to the latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // --- Rendering ---

  return (
    <div className="app-container">
      <aside className="sidebar open">
        <div className="sidebar-header">
          <h1>EduLLM Chats</h1>
          <button onClick={handleNewChat} className="new-chat-button">
            <FiPlus /> New Chat
          </button>
        </div>
        <div className="chat-list">
          {chats.map(chat => (
            <div
              key={chat.id}
              className={`chat-list-item ${chat.id === currentChatId ? 'active' : ''}`}
              onClick={() => setCurrentChatId(chat.id)}
            >
              {chat.title}
            </div>
          ))}
        </div>
        <div className="sidebar-footer">
            <button onClick={handleLogout} className="logout-button">
                <FiLogOut /> Logout
            </button>
        </div>
      </aside>

      <main className="main-chat-panel">
        <div className="chat-history">
          {messages.map((msg, index) => (
            <div key={index} className={`message-wrapper ${msg.sender}`}>
              {msg.sender === 'human' ? (
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
              placeholder="Ask anything..."
              disabled={isLoading || !currentChatId}
              onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) handleSubmit(e); }}
            />
            <button type="submit" className="send-button" disabled={!input.trim() || isLoading || !currentChatId}>
              <FiSend />
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}

export default ChatPage;