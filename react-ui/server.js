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
  // Extract query and backend choice from request body
  const { query, backend = 'functions' } = req.body; // Default to 'functions' if not specified
  
  if (!query) {
    return res.status(400).json({ error: 'Query is required' });
  }
  
  console.log(`Received query: "${query}" for backend: ${backend}`);
  
  // Determine which Python script to run based on backend choice
  const scriptName = backend === 'analysis' ? 'analysis.py' : 'function_call.py';
  const pythonScriptPath = path.resolve(__dirname, '..', scriptName);
  
  console.log(`Executing Python script: ${pythonScriptPath}`);
  
  // Check if the selected python script exists
  if (!fs.existsSync(pythonScriptPath)) {
    console.error(`Python script not found at: ${pythonScriptPath}`);
    return res.status(500).json({ error: `Backend script (${scriptName}) not found.` });
  }
  
  // Spawn a Python process to execute the query
  const pythonProcess = spawn('python', [pythonScriptPath]);
  
  // Write the query to stdin
  pythonProcess.stdin.write(query);
  pythonProcess.stdin.end();
  
  let responseData = '';
  let errorData = '';
  
  // Collect data from stdout
  pythonProcess.stdout.on('data', (data) => {
    responseData += data.toString();
    console.log(`[${scriptName}] output:`, data.toString());
  });
  
  // Collect error data
  pythonProcess.stderr.on('data', (data) => {
    errorData += data.toString();
    console.error(`[${scriptName}] error:`, data.toString());
  });
  
  // Handle process completion
  pythonProcess.on('close', (code) => {
    console.log(`[${scriptName}] process exited with code ${code}`);
    
    if (code !== 0) {
      console.error(`[${scriptName}] Error data:`, errorData);
      return res.status(500).json({ error: `Query processing failed with ${scriptName}`, details: errorData });
    }
    
    // Check if output.html exists and return its contents if it does
    const htmlPath = path.resolve(__dirname, 'output.html');
    console.log(`[${scriptName}] Looking for output.html at:`, htmlPath);
    
    if (fs.existsSync(htmlPath)) {
      console.log(`[${scriptName}] Found output.html - sending HTML content to frontend`);
      try {
        const htmlContent = fs.readFileSync(htmlPath, 'utf8');
        return res.json({ response: htmlContent, backend: backend });
      } catch (err) {
        console.error(`[${scriptName}] Error reading output.html:`, err);
      }
    } else {
      console.log(`[${scriptName}] output.html not found at expected path:`, htmlPath);
    }
    
    // Otherwise return the stdout output
    try {
      // Try to parse as JSON first
      const jsonData = JSON.parse(responseData);
      res.json({ response: jsonData, backend: backend });
    } catch (e) {
      // If not JSON, return as text
      res.json({ response: responseData, backend: backend });
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