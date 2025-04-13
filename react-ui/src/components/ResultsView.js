import React, { useEffect, useRef } from 'react';
import './ResultsView.css';

function ResultsView({ results }) {
  const contentRef = useRef(null);
  
  // Function to determine if the content includes HTML
  const isHTML = (str) => {
    return /<[a-z][\s\S]*>/i.test(str);
  };
  
  // Function to sanitize HTML content (simple version)
  const createMarkup = (content) => {
    return { __html: content };
  };

  // Effect to make charts responsive after they're inserted into the DOM
  useEffect(() => {
    if (results && isHTML(results.response) && contentRef.current) {
      // Find all canvases and make them responsive
      const canvases = contentRef.current.querySelectorAll('canvas');
      canvases.forEach(canvas => {
        // Ensure canvas is responsive
        if (canvas.style) {
          canvas.style.maxWidth = '100%';
          canvas.style.height = 'auto';
        }
      });

      // Add viewport meta tag if not present
      if (!document.querySelector('meta[name="viewport"]')) {
        const meta = document.createElement('meta');
        meta.name = 'viewport';
        meta.content = 'width=device-width, initial-scale=1.0';
        document.head.appendChild(meta);
      }
      
      // Ensure all tables are scrollable
      const tables = contentRef.current.querySelectorAll('table');
      tables.forEach(table => {
        // Wrap table in a div with overflow auto if not already
        if (table.parentElement && !table.parentElement.classList.contains('table-wrapper')) {
          const wrapper = document.createElement('div');
          wrapper.classList.add('table-wrapper');
          wrapper.style.overflowX = 'auto';
          wrapper.style.width = '100%';
          table.parentNode.insertBefore(wrapper, table);
          wrapper.appendChild(table);
        }
      });
    }
  }, [results]);

  return (
    <div className="results-container">
      <h3 className="results-title">Results</h3>
      
      <div className="results-content">
        {results && isHTML(results.response) ? (
          <div ref={contentRef} className="html-content-wrapper" dangerouslySetInnerHTML={createMarkup(results.response)} />
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