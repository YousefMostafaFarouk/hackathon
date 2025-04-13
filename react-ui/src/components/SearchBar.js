import React, { useState } from 'react';
import './SearchBar.css';

const predefinedSearches = [
  { 
    id: 1, 
    name: 'Biotech startups in Zürich', 
    query: 'Show me all Biotech startups in Zürich' 
  },
  { 
    id: 2, 
    name: 'Early stage investments in ICT', 
    query: 'What is the total amount of early stage investments in ICT?' 
  },
  { 
    id: 3, 
    name: 'Top investors in Medtech', 
    query: 'Who are the top investors in medtech startups?' 
  },
  { 
    id: 4, 
    name: 'Female-led startups', 
    query: 'List all startups with female CEOs' 
  },
  { 
    id: 5, 
    name: 'Recent deals in Cleantech', 
    query: 'Show me the most recent funding deals in cleantech' 
  }
];

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('');
  const [backend, setBackend] = useState('functions');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch({ query, backend });
    }
  };
  
  const handlePredefinedSearch = (predefinedQuery) => {
    setQuery(predefinedQuery);
    onSearch({ query: predefinedQuery, backend });
  };
  
  return (
    <div className="search-container">
      <form onSubmit={handleSubmit}>
        <div className="input-group mb-3">
          <input
            type="text"
            className="form-control form-control-lg"
            placeholder="Ask a question about Swiss startups..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            aria-label="Search query"
          />
          <button 
            className="btn btn-primary" 
            type="submit"
            disabled={!query.trim()}
          >
            Search
          </button>
        </div>
        
        {/* Mode Selection */}
        <div className="backend-selection mb-3">
          <label className="form-label d-block text-center mb-2">Choose which mode:</label>
          <div className="d-flex justify-content-center gap-2">
            <button
              type="button"
              className={`btn ${backend === 'functions' ? 'btn-success' : 'btn-outline-secondary'} flex-grow-1`}
              onClick={() => setBackend('functions')}
              style={{ minWidth: '150px', height: '60px' }}
            >
              Analysis
            </button>
            <button
              type="button"
              className={`btn ${backend === 'analysis' ? 'btn-success' : 'btn-outline-secondary'} flex-grow-1`}
              onClick={() => setBackend('analysis')}
              title="May provide creative but occasionally inaccurate responses"
              style={{ minWidth: '150px', height: '60px' }}
            >
              Advanced Analysis
              <small className="d-block text-warning">May hallucinate</small>
            </button>
          </div>
        </div>
      </form>
      
      <div className="predefined-searches">
        <h5>Popular Searches:</h5>
        <div className="d-flex flex-wrap gap-2 justify-content-center">
          {predefinedSearches.map((search) => (
            <button
              key={search.id}
              className="btn btn-outline-secondary"
              onClick={() => handlePredefinedSearch(search.query)}
            >
              {search.name}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default SearchBar; 