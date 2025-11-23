import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './AIChat.css';

import { API_URL } from './config';

function AIChat({ isBackendOnline }) {
    const [messages, setMessages] = useState([
        { role: 'assistant', content: '👋 Hi! I\'m your ADAS AI Assistant. Ask me about alerts, driving safety, or get suggestions!' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [suggestions, setSuggestions] = useState([]);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Fetch AI suggestions on mount
    useEffect(() => {
        if (isBackendOnline) {
            fetchSuggestions();
        }
    }, [isBackendOnline]);

    const fetchSuggestions = async () => {
        try {
            const response = await axios.get(`${API_URL}/api/chat/suggestions`);
            setSuggestions(response.data.suggestions || []);
        } catch (error) {
            console.error('Error fetching suggestions:', error);
        }
    };

    const sendMessage = async () => {
        if (!input.trim() || loading) return;

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setLoading(true);

        try {
            if (!isBackendOnline) {
                // Offline mode - provide helpful response
                setMessages(prev => [...prev, {
                    role: 'assistant',
                    content: '🔌 Backend is offline. Start the backend server to chat with AI! In the meantime, here are some general safety tips: Always maintain safe distance, check blind spots, and stay alert.'
                }]);
                setLoading(false);
                return;
            }

            const response = await axios.post(`${API_URL}/api/chat`, {
                message: userMessage
            });

            setMessages(prev => [...prev, {
                role: 'assistant',
                content: response.data.response
            }]);
        } catch (error) {
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: '❌ Sorry, I encountered an error. Please try again or check if the backend is running.'
            }]);
        } finally {
            setLoading(false);
        }
    };

    const quickQuestions = [
        "What alerts did I get recently?",
        "Give me safety tips",
        "Explain the last alert",
        "How can I improve my driving?"
    ];

    return (
        <div className="ai-chat-container">
            <div className="chat-header">
                <div className="chat-title">
                    <span className="ai-icon">🤖</span>
                    <span>AI Assistant</span>
                </div>
                <div className={`ai-status ${isBackendOnline ? 'online' : 'offline'}`}>
                    {isBackendOnline ? '● Online' : '○ Offline'}
                </div>
            </div>

            {suggestions.length > 0 && (
                <div className="suggestions-banner">
                    <div className="suggestion-title">💡 AI Suggestions:</div>
                    {suggestions.map((suggestion, idx) => (
                        <div key={idx} className="suggestion-item">{suggestion}</div>
                    ))}
                </div>
            )}

            <div className="chat-messages">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`message ${msg.role}`}>
                        <div className="message-avatar">
                            {msg.role === 'user' ? '👤' : '🤖'}
                        </div>
                        <div className="message-content">
                            {msg.content}
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="message assistant">
                        <div className="message-avatar">🤖</div>
                        <div className="message-content typing">
                            <span></span><span></span><span></span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="quick-questions">
                {quickQuestions.map((q, idx) => (
                    <button
                        key={idx}
                        onClick={() => {
                            setInput(q);
                            setTimeout(() => sendMessage(), 100);
                        }}
                        className="quick-question-btn"
                        disabled={loading}
                    >
                        {q}
                    </button>
                ))}
            </div>

            <div className="chat-input-container">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Ask me anything about driving safety..."
                    className="chat-input"
                    disabled={loading}
                />
                <button
                    onClick={sendMessage}
                    disabled={loading || !input.trim()}
                    className="send-btn"
                >
                    {loading ? '⏳' : '→'}
                </button>
            </div>
        </div>
    );
}

export default AIChat;
