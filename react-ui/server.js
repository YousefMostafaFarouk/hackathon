const express = require('express');
const { spawn } = require('child_process');
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');

const app = express();
const port = process.env.PORT || 5000;

// Middleware
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'build')));

// API endpoint to handle search queries
app.post('/api/search', (req, res) => {
  const { query } = req.body;
  
  if (!query) {
    return res.status(400).json({ error: 'Query is required' });
  }
  
  console.log('Received query:', query);
  
  // Spawn a Python process to execute the query
  const pythonProcess = spawn('python', [path.resolve(__dirname, '..', 'function_call.py')]);
  
  // Write the query to stdin
  pythonProcess.stdin.write(query);
  pythonProcess.stdin.end();
  
  let responseData = '';
  let errorData = '';
  
  // Collect data from stdout
  pythonProcess.stdout.on('data', (data) => {
    responseData += data.toString();
    console.log('Python output:', data.toString());
  });
  
  // Collect error data
  pythonProcess.stderr.on('data', (data) => {
    errorData += data.toString();
    console.error('Python error:', data.toString());
  });
  
  // Handle process completion
  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
    
    if (code !== 0) {
      console.error('Error data:', errorData);
      return res.status(500).json({ error: 'Query processing failed', details: errorData });
    }
    
    // Check if output.html exists and return its contents if it does
    const htmlPath = path.resolve(__dirname, 'output.html');
    console.log('Looking for output.html at:', htmlPath);
    
    if (fs.existsSync(htmlPath)) {
      console.log('Found output.html - sending HTML content to frontend');
      try {
        const htmlContent = fs.readFileSync(htmlPath, 'utf8');
        return res.json({ response: htmlContent });
      } catch (err) {
        console.error('Error reading output.html:', err);
      }
    } else {
      console.log('output.html not found at expected path:', htmlPath);
    }
    
    // Otherwise return the stdout output
    try {
      // Try to parse as JSON first
      const jsonData = JSON.parse(responseData);
      res.json({ response: jsonData });
    } catch (e) {
      // If not JSON, return as text
      res.json({ response: responseData });
    }
  });
});

// Simple test endpoint
app.get('/api/test', (req, res) => {
  res.json({ message: 'Server is running correctly' });
});

// Serve the React app for all other routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
}); 