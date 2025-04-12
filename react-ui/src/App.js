import React, { useState, useEffect } from 'react';
import './App.css';
import SearchBar from './components/SearchBar';
import ResultsView from './components/ResultsView';

// Base URL for API calls - make sure this is exactly correct
const API_BASE_URL = 'http://localhost:5000';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [serverStatus, setServerStatus] = useState(false);

  // Test connection to backend on component mount
  useEffect(() => {
    const checkServer = async () => {
      try {
        console.log('Testing connection to server at:', API_BASE_URL);
        const response = await fetch(`${API_BASE_URL}/api/test`, {
          method: 'GET',
          mode: 'cors',
          cache: 'no-cache',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          }
        });
        
        console.log('Server test response status:', response.status);
        
        if (response.ok) {
          console.log('Backend connection successful');
          setServerStatus(true);
        } else {
          console.error('Backend connection failed');
          setServerStatus(false);
        }
      } catch (err) {
        console.error('Backend connection error:', err);
        setServerStatus(false);
      }
    };
    
    checkServer();
    // Re-check server connection every 5 seconds
    const interval = setInterval(checkServer, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleSearch = async (query) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('Sending query to server:', query);
      const response = await fetch(`${API_BASE_URL}/api/search`, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      
      console.log('Response status:', response.status);
      
      const data = await response.json();
      console.log('Response data:', data);
      
      if (!response.ok) {
        // Check for rate limit errors
        if (data.details && data.details.includes('RESOURCE_EXHAUSTED')) {
          throw new Error('API rate limit exceeded. Please wait a minute and try again.');
        }
        
        if (data.response && typeof data.response === 'string' && 
            (data.response.includes('429 RESOURCE_EXHAUSTED') || 
             data.response.includes('exceeded your current quota'))) {
          throw new Error('Google API rate limit exceeded. Please wait about 60 seconds and try again.');
        }
        
        throw new Error(`Search failed with status: ${response.status}`);
      }
      
      setResults(data);
    } catch (err) {
      setError(err.message);
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Swiss Startup Explorer</h1>
        <p>Ask questions about Swiss startups and investment data</p>
        {!serverStatus && (
          <div className="server-status-warning">
            Warning: Server connection issue. Make sure the server is running at {API_BASE_URL}
          </div>
        )}
      </header>
      <main className="container">
        <SearchBar onSearch={handleSearch} />
        
        {loading && (
          <div className="text-center mt-5">
            <div className="spinner-border" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          </div>
        )}
        
        {error && (
          <div className="alert alert-danger mt-3" role="alert">
            {error.includes('rate limit') ? (
              <>
                <h4>API Rate Limit Exceeded</h4>
                <p>{error}</p>
                <p className="mt-2">The Google Gemini API has these limitations on the free tier:</p>
                <ul>
                  <li>2 requests per minute</li>
                  <li>32,000 input tokens per minute</li>
                </ul>
              </>
            ) : (
              error
            )}
          </div>
        )}
        
        {results && !loading && (
          <ResultsView results={results} />
        )}
      </main>
    </div>
  );
}

export default App; 