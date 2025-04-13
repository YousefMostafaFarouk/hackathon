const http = require('http');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const PORT = 5000;

// Get the absolute path to the function_call.py file
const PYTHON_SCRIPT_PATH = path.resolve(__dirname, '..', 'function_call.py');
console.log(`Python script path: ${PYTHON_SCRIPT_PATH}`);

// Check if system_prompt.txt exists
const SYSTEM_PROMPT_PATH = path.resolve(__dirname, '..', 'system_prompt.txt');
console.log(`System prompt path: ${SYSTEM_PROMPT_PATH}`);
console.log(`System prompt exists: ${fs.existsSync(SYSTEM_PROMPT_PATH)}`);

const server = http.createServer((req, res) => {
  // Handle CORS - improve CORS support
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type,Authorization');
  res.setHeader('Access-Control-Allow-Credentials', true);
  
  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }
  
  console.log(`${req.method} ${req.url}`);
  
  // Test endpoint
  if (req.url === '/api/test' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ message: 'Server is running correctly' }));
    return;
  }
  
  // Handle search API
  if (req.url === '/api/search' && req.method === 'POST') {
    let body = '';
    
    req.on('data', (chunk) => {
      body += chunk.toString();
    });
    
    req.on('end', () => {
      try {
        const { query } = JSON.parse(body);
        
        if (!query) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Query is required' }));
          return;
        }
        
        console.log('Received query:', query);
        
        // Spawn Python process with explicit path
        const pythonProcess = spawn('python', [PYTHON_SCRIPT_PATH]);
        
        // Write query to stdin
        pythonProcess.stdin.write(query);
        pythonProcess.stdin.end();
        
        let responseData = '';
        let errorData = '';
        
        pythonProcess.stdout.on('data', (data) => {
          responseData += data.toString();
          console.log('Python output:', data.toString());
        });
        
        pythonProcess.stderr.on('data', (data) => {
          errorData += data.toString();
          console.error('Python error:', data.toString());
        });
        
        pythonProcess.on('close', (code) => {
          console.log(`Python process exited with code ${code}`);
          
          if (code !== 0) {
            console.error('Error data:', errorData);
            
            // Check for rate limit errors
            if (responseData.includes('429 RESOURCE_EXHAUSTED') || 
                responseData.includes('exceeded your current quota')) {
              
              res.writeHead(429, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({ 
                error: 'Google API rate limit exceeded', 
                details: 'The free tier of Google Gemini API has limits of 2 requests per minute and 32,000 tokens per minute',
                response: responseData,
                retryAfter: 60 // suggest retry after 60 seconds
              }));
              return;
            }
            
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Query processing failed', details: errorData, response: responseData }));
            return;
          }
          
          // Check if output.html exists
          const htmlPath = path.resolve(__dirname, 'output.html');
          if (fs.existsSync(htmlPath)) {
            try {
              const htmlContent = fs.readFileSync(htmlPath, 'utf8');
              res.writeHead(200, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({ response: htmlContent }));
              return;
            } catch (err) {
              console.error('Error reading output.html:', err);
            }
          }
          
          // Return stdout output
          try {
            // Try to parse as JSON first
            const jsonData = JSON.parse(responseData);
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ response: jsonData }));
          } catch (e) {
            // Return as text
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ response: responseData }));
          }
        });
      } catch (error) {
        console.error('Error parsing request:', error);
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Invalid request format' }));
      }
    });
    
    return;
  }
  
  // Default response for unknown endpoints
  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'Not found' }));
});

server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}/`);
}); 