// src/pages/ChatPage.js
import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import TextareaAutosize from 'react-textarea-autosize';
import { FiSend, FiPlus, FiLogOut, FiEdit2, FiMessageSquare } from 'react-icons/fi';
import api from '../api';
import '../App.css';

function ChatPage() {
  const navigate = useNavigate();
  const { chatId } = useParams();
  const messagesEndRef = useRef(null);

  // --- State Management ---
  const [chats, setChats] = useState([]);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [editingChatId, setEditingChatId] = useState(null);
  const [editingTitle, setEditingTitle] = useState("");

  // --- Core Functions & Handlers ---

  const handleLogout = useCallback(() => {
    localStorage.removeItem('accessToken');
    navigate('/login');
  }, [navigate]);

  const fetchChats = useCallback(() => {
    api.get('/chats')
      .then(response => setChats(response.data))
      .catch(error => {
        console.error('Failed to fetch chats:', error);
        if (error.response && error.response.status === 401) handleLogout();
      });
  }, [handleLogout]);

  const handleNewChat = async () => {
    try {
      const { data: newChat } = await api.post('/chats');
      // After creating, navigate to the new chat's page
      // The sidebar will update automatically because a new chat has been added
      fetchChats(); // Refresh the chat list
      navigate(`/chat/${newChat.id}`);
    } catch (error) {
      console.error('Failed to create new chat:', error);
    }
  };
  
  const handleStartEditing = (chat) => {
    setEditingChatId(chat.id);
    setEditingTitle(chat.title);
  };

  const handleSaveRename = async (chatIdToRename) => {
    if (!editingTitle.trim()) {
        setEditingChatId(null); // Cancel edit if title is empty
        return;
    }
    try {
      await api.put(`/chats/${chatIdToRename}`, { title: editingTitle });
      setChats(prev => prev.map(c => 
        c.id === chatIdToRename ? { ...c, title: editingTitle } : c
      ));
    } catch (error) {
      console.error("Failed to rename chat:", error);
    } finally {
      setEditingChatId(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading || !chatId) return;

    const currentChat = chats.find(c => c.id === parseInt(chatId));
    const isNewChat = currentChat?.title === "New Chat";

    const userMessage = { sender: 'human', text: input };
    setMessages(prev => [...prev, userMessage]);
    const currentInput = input;
    setInput('');
    setIsLoading(true);

    try {
      const response = await api.post('/chat', {
        question: currentInput,
        chat_id: parseInt(chatId),
        model: "gpt-4.1-mini"
      });
      const aiMessage = { sender: 'ai', text: response.data.answer };
      setMessages(prev => [...prev, aiMessage]);
      
      if (isNewChat) {
        fetchChats(); // Refresh list to show auto-generated title
      }
    } catch (error) {
      console.error('Error communicating with the agent:', error);
      const errorMessage = { sender: 'ai', text: 'Sorry, I ran into an error.' };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };
  
  // --- Effects ---

  useEffect(() => {
    fetchChats();
  }, [fetchChats]);

  useEffect(() => {
    if (!chatId) {
        setMessages([]);
        return;
    }
    setIsLoading(true);
    setMessages([]);
    api.get(`/chats/${chatId}/messages`)
      .then(response => {
        setMessages(response.data.map(msg => ({
          sender: msg.role,
          text: msg.content
        })));
      })
      .catch(error => console.error('Failed to fetch messages for chat ID:', chatId, error))
      .finally(() => setIsLoading(false));
  }, [chatId]);
  
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // --- Rendering ---

  return (
    <div className="app-container">
      <aside className="sidebar open">
        <div className="sidebar-header">
          <button onClick={handleNewChat} className="new-chat-button">
            <FiPlus /> New Chat
          </button>
        </div>
        <div className="chat-list">
          {chats.map(chat => (
            <div key={chat.id} className="chat-list-item-wrapper">
              {editingChatId === chat.id ? (
                <input
                  type="text"
                  value={editingTitle}
                  onChange={(e) => setEditingTitle(e.target.value)}
                  onBlur={() => handleSaveRename(chat.id)}
                  onKeyDown={(e) => { if (e.key === 'Enter') handleSaveRename(chat.id); }}
                  className="title-edit-input"
                  autoFocus
                />
              ) : (
                <Link to={`/chat/${chat.id}`} className={`chat-list-item ${chat.id === parseInt(chatId) ? 'active' : ''}`}>
                  {chat.title}
                  <button className="edit-icon" onClick={(e) => { e.preventDefault(); handleStartEditing(chat); }}>
                    <FiEdit2 size={14} />
                  </button>
                </Link>
              )}
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
        {!chatId ? (
          <div className="start-chat-container">
            <FiMessageSquare className="icon" />
            <h2>Welcome to EduLLM</h2>
            <p>Select a conversation or start a new one.</p>
          </div>
        ) : (
          <>
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
              {isLoading && ( <div className="message-wrapper ai"><div className="ai-response thinking">...</div></div> )}
              <div ref={messagesEndRef} />
            </div>
            <div className="chat-input-area">
              <form className="input-form" onSubmit={handleSubmit}>
                <TextareaAutosize
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask anything..."
                  disabled={isLoading}
                  onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSubmit(e); } }}
                />
                <button type="submit" className="send-button" disabled={!input.trim() || isLoading}>
                  <FiSend />
                </button>
              </form>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default ChatPage;