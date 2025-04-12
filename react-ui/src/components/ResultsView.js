import React from 'react';
import './ResultsView.css';

function ResultsView({ results }) {
  // Function to determine if the content includes HTML
  const isHTML = (str) => {
    return /<[a-z][\s\S]*>/i.test(str);
  };
  
  // Function to sanitize HTML content (simple version)
  const createMarkup = (content) => {
    return { __html: content };
  };

  return (
    <div className="results-container">
      <h3 className="results-title">Results</h3>
      
      <div className="results-content">
        {results && isHTML(results.response) ? (
          <div dangerouslySetInnerHTML={createMarkup(results.response)} />
        ) : (
          <div className="text-container">
            <p>{results?.response || 'No results found.'}</p>
          </div>
        )}
      </div>
      
      {results?.data && Array.isArray(results.data) && results.data.length > 0 && (
        <div className="data-table-container">
          <h4>Data Results</h4>
          <div className="table-responsive">
            <table className="table table-striped table-hover">
              <thead>
                <tr>
                  {Object.keys(results.data[0]).map((key) => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {results.data.map((item, index) => (
                  <tr key={index}>
                    {Object.values(item).map((value, idx) => (
                      <td key={idx}>{value?.toString() || '-'}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default ResultsView; 