# Swiss Startup Explorer

A React.js user interface for querying Swiss startup data using natural language. This application allows users to ask questions about Swiss startups and their investments and get results from the data.

## Features

- Natural language search interface
- Predefined popular search queries
- Display of data in formatted tables
- Support for HTML response visualization

## Setup

### Prerequisites

- Node.js (v14+)
- npm or yarn
- Python 3.8+
- Required Python packages: pandas, pandasql, google-generativeai

### Installation

1. Clone the repository
2. Install frontend dependencies:
   ```
   cd react-ui
   npm install
   ```
3. Install server dependencies:
   ```
   npm install express body-parser --save
   ```

### Configuration

Ensure that your Python backend is properly set up with the required API keys and data files.

## Development

Start the development server with:

```
cd react-ui
npm run dev
```

This will start both the React frontend and Express backend servers.

## Building for Production

```
cd react-ui
npm run build
```

The build will be created in the `build` directory.

## Usage

1. Enter a question in the search bar or select a predefined query
2. View the results in the results section
3. Results may be displayed as text or formatted HTML depending on the response

## Examples of Queries

- "Show me all Biotech startups in Zurich"
- "What is the total amount of early stage investments in ICT?"
- "Who are the top investors in Medtech startups?"
- "List all startups with female CEOs"
- "Show me the most recent funding deals in Cleantech" 