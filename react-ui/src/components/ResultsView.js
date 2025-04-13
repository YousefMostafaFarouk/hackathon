import React, { useEffect, useRef } from 'react';
import './ResultsView.css';

function ResultsView({ results }) {
  const contentRef = useRef(null);

  const isHTML = (str) => {
    return /<[a-z][\s\S]*>/i.test(str);
  };

  useEffect(() => {
    if (results && isHTML(results.response) && contentRef.current) {
      const container = contentRef.current;

      // Inject HTML content
      container.innerHTML = results.response;

      // Make canvases responsive
      const canvases = container.querySelectorAll('canvas');
      canvases.forEach(canvas => {
        if (canvas.style) {
          canvas.style.maxWidth = '100%';
          canvas.style.height = 'auto';
        }
      });

      // Ensure all tables are scrollable
      const tables = container.querySelectorAll('table');
      tables.forEach(table => {
        if (table.parentElement && !table.parentElement.classList.contains('table-wrapper')) {
          const wrapper = document.createElement('div');
          wrapper.classList.add('table-wrapper');
          wrapper.style.overflowX = 'auto';
          wrapper.style.width = '100%';
          table.parentNode.insertBefore(wrapper, table);
          wrapper.appendChild(table);
        }
      });

      // Add viewport meta tag if not present
      if (!document.querySelector('meta[name="viewport"]')) {
        const meta = document.createElement('meta');
        meta.name = 'viewport';
        meta.content = 'width=device-width, initial-scale=1.0';
        document.head.appendChild(meta);
      }

      // Execute <script> tags
      const scripts = container.querySelectorAll('script');
      scripts.forEach(oldScript => {
        const newScript = document.createElement('script');
        Array.from(oldScript.attributes).forEach(attr => {
          newScript.setAttribute(attr.name, attr.value);
        });
        newScript.text = oldScript.text;
        oldScript.replaceWith(newScript);
      });
    }
  }, [results]);

  return (
    <div className="results-container">
      <h3 className="results-title">Results</h3>

      <div className="results-content">
        {results && isHTML(results.response) ? (
          <div ref={contentRef} className="html-content-wrapper" />
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
