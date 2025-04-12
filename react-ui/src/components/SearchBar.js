import React, { useState } from 'react';
import './SearchBar.css';

const predefinedSearches = [
  { 
    id: 1, 
    name: 'Biotech startups in Zurich', 
    query: 'Show me all Biotech startups in Zurich' 
  },
  { 
    id: 2, 
    name: 'Early stage investments in ICT', 
    query: 'What is the total amount of early stage investments in ICT?' 
  },
  { 
    id: 3, 
    name: 'Top investors in Medtech', 
    query: 'Who are the top investors in Medtech startups?' 
  },
  { 
    id: 4, 
    name: 'Female-led startups', 
    query: 'List all startups with female CEOs' 
  },
  { 
    id: 5, 
    name: 'Recent deals in Cleantech', 
    query: 'Show me the most recent funding deals in Cleantech' 
  }
];

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  };
  
  const handlePredefinedSearch = (predefinedQuery) => {
    setQuery(predefinedQuery);
    onSearch(predefinedQuery);
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