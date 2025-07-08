import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import {  Form, Button, Nav } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  
  // Add state for active source
  const [activeSource, setActiveSource] = useState(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSearch = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) return;
    
    // Add user message
    setMessages(prev => [...prev, { type: 'user', content: query }]);
    setLoading(true);
    setActiveSource(null); // Reset active source
    
    const currentQuery = query;
    setQuery(''); // Clear input field

    try {
      const response = await axios.post('http://localhost:5000/mr', {
        query: currentQuery
      });
      
      // Add assistant message
      setMessages(prev => [...prev, { 
        type: 'assistant', 
        content: response.data.response || "I couldn't find any information on that topic." 
      }]);
      
      // Set the first source as active if available
      if (response.data.response && 
          response.data.response.sources && 
          response.data.response.sources.length > 0) {
        setActiveSource(0);
      }
    } catch (err) {
      console.error('Error fetching results:', err);
      setMessages(prev => [...prev, { 
        type: 'assistant', 
        content: "I'm sorry, I encountered an error while searching. Please try again." 
      }]);
    } finally {
      setLoading(false);
    }
  };

  // Function to render source navigation
  const renderSourceNavigation = (sources) => {
    if (!sources || sources.length === 0) return null;
    
    return (
      <Nav variant="pills" className="source-navigation">
        {sources.map((source, index) => (
          <Nav.Item key={index}>
            <Nav.Link 
              active={activeSource === index}
              onClick={() => setActiveSource(index)}
              className="source-button"
            >
              {source.name}
            </Nav.Link>
          </Nav.Item>
        ))}
        <Nav.Item>
          <Nav.Link 
            active={activeSource === 'all'}
            onClick={() => setActiveSource('all')}
            className="source-button"
          >
            All Sources
          </Nav.Link>
        </Nav.Item>
      </Nav>
    );
  };

  // Function to render the active source content
  const renderSourceContent = (response) => {
    if (!response || !response.sources) return null;
    
    if (activeSource === 'all') {
      // Show all sources
      return (
        <div className="all-sources">
          <h3>Summary</h3>
          <p>{response.summary}</p>
          
          <h3>All Sources</h3>
          {response.sources.map((source, index) => (
            <div key={index} className="source-content">
              <h4>{source.name}</h4>
              <p>{source.description}</p>
              <a href={source.url} target="_blank" rel="noopener noreferrer">
                Read more
              </a>
            </div>
          ))}
          
          {renderImagesAndVideos(response)}
        </div>
      );
    } else if (activeSource !== null && response.sources[activeSource]) {
      // Show specific source
      const source = response.sources[activeSource];
      return (
        <div className="single-source">
          <h3>{source.name}</h3>
          <p>{source.description}</p>
          <a href={source.url} target="_blank" rel="noopener noreferrer" className="source-link">
            Read full article
          </a>
          
          {renderImagesAndVideos(response)}
        </div>
      );
    }
    
    return null;
  };

  // Function to render images and videos
  const renderImagesAndVideos = (response) => {
    return (
      <>
        {response.images && response.images.length > 0 && (
          <div className="response-images">
            <h3>Images</h3>
            <div className="image-gallery">
              {response.images.map((image, index) => (
                <div key={index} className="image-container">
                  <img src={image} alt={`Result ${index + 1}`} />
                </div>
              ))}
            </div>
          </div>
        )}
        
        {response.videos && response.videos.length > 0 && (
          <div className="response-videos">
            <h3>Videos</h3>
            <ul>
              {response.videos.map((video, index) => (
                <li key={index}>
                  <a href={video} target="_blank" rel="noopener noreferrer">
                    Video {index + 1}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </>
    );
  };

  // Function to render structured response
  const renderStructuredResponse = (response) => {
    if (typeof response === 'string') {
      return <ReactMarkdown>{response}</ReactMarkdown>;
    }
    
    return (
      <div className="structured-response">
        {response.title && <h2 className="response-title">{response.title}</h2>}
        
        {response.summary && (
          <div className="response-summary">
            <p>{response.summary}</p>
          </div>
        )}
        
        {response.sources && response.sources.length > 0 && (
          <>
            {renderSourceNavigation(response.sources)}
            {renderSourceContent(response)}
          </>
        )}
      </div>
    );
  };

  return (
    <div className="weave-app">
      <div className="sidebar">
        <div className="logo-container">
          <div className="logo">W</div>
          <h1>Weave</h1>
        </div>
        <button className="new-chat-btn" onClick={() => {
          setMessages([]);
          setActiveSource(null);
        }}>
          <span>+</span> New Search
        </button>
        <div className="sidebar-footer">
          <p>Powered by Groq</p>
        </div>
      </div>
      
      <div className="main-content">
        <div className="chat-container">
          {messages.length === 0 ? (
            <div className="welcome-container">
              <h1>Weave</h1>
              <p>Your AI-powered web search assistant</p>
              <div className="examples">
                <h3>Try asking about:</h3>
                <div className="example-grid">
                  <div className="example-card" onClick={() => setQuery("What is Retrieval Augmented Generation (RAG)?")}>
                   What is Retrieval Augmented Generation (RAG)?
                  </div>
                  <div className="example-card" onClick={() => setQuery("Latest news about GenAI")}>
                    Latest news about GenAI
                  </div>
                  <div className="example-card" onClick={() => setQuery("How to learn Artificial Intelligence?")}>
                   How to learn Artificial Intelligence?
                  </div>
                  <div className="example-card" onClick={() => setQuery("Types of AI")}>
                    Types  of AI
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="messages">
              {messages.map((message, index) => (
                <div key={index} className={`message ${message.type}`}>
                  <div className="message-avatar">
                    {message.type === 'user' ? '👤' : 'W'}
                  </div>
                  <div className="message-content">
                    {message.type === 'user' ? (
                      <p>{message.content}</p>
                    ) : (
                      renderStructuredResponse(message.content)
                    )}
                  </div>
                </div>
              ))}
              {loading && (
                <div className="message assistant">
                  <div className="message-avatar">V</div>
                  <div className="message-content">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
        
        <div className="input-container">
          <Form onSubmit={handleSearch}>
            <div className="input-wrapper">
              <Form.Control
                type="text"
                placeholder="Ask me anything..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                disabled={loading}
              />
              <Button type="submit" disabled={loading || !query.trim()}>
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22 2L11 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </Button>
            </div>
          </Form>
          <p className="input-footer">
            Weave searches the web to find the most relevant information
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
