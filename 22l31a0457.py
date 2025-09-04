

import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Paper } from '@mui/material';


const shortenUrlApiCall = async (url, customCode, validity) => {
  console.log("Submitting to API:", { url, customCode, validity });
  
  await new Promise(resolve => setTimeout(resolve, 1000)); 

  return { shortUrl: `https://short.est/${customCode || 'RANDOM'}` };
};


function URLForm({ onNewUrlCreated }) {
  
  const [originalUrl, setOriginalUrl] = useState('');
  const [customShortcode, setCustomShortcode] = useState('');
  const [validityPeriod, setValidityPeriod] = useState('30'); // Default to 30 minutes as per requirements

  
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent the form from reloading the page
    setError(''); // Clear previous errors

    
    if (!originalUrl.startsWith('http')) {
      setError('Please enter a valid URL (e.g., https://google.com)');
      return;
    }

    setIsLoading(true);

    try {
      
      const result = await shortenUrlApiCall(originalUrl, customShortcode, validityPeriod);
      
      onNewUrlCreated(result); 

      
      setOriginalUrl('');
      setCustomShortcode('');

    } catch (apiError) {
      setError('Failed to shorten URL. Please try again.');
      
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ padding: 4, borderRadius: 2 }}>
      <Box component="form" onSubmit={handleSubmit} noValidate>
        <Typography variant="h5" component="h2" gutterBottom>
          Create a Short URL
        </Typography>
        
        <TextField
          label="Enter Original URL"
          variant="outlined"
          fullWidth
          required
          margin="normal"
          value={originalUrl}
          onChange={(e) => setOriginalUrl(e.target.value)}
          disabled={isLoading}
        />

        <TextField
          label="Optional Custom Shortcode (4-16 characters)"
          variant="outlined"
          fullWidth
          margin="normal"
          value={customShortcode}
          onChange={(e) => setCustomShortcode(e.target.value)}
          disabled={isLoading}
        />

        <TextField
          label="Optional Validity Period (in minutes)"
          type="number"
          variant="outlined"
          fullWidth
          margin="normal"
          value={validityPeriod}
          onChange={(e) => setValidityPeriod(e.target.value)}
          disabled={isLoading}
        />

        {error && (
            <Typography color="error" variant="body2" sx={{ mt: 2 }}>
                {error}
            </Typography>
        )}

        <Button
          type="submit"
          variant="contained"
          size="large"
          fullWidth
          sx={{ mt: 2, py: 1.5 }}
          disabled={isLoading}
        >
          {isLoading ? 'Shortening...' : 'Shorten URL'}
        </Button>
      </Box>
    </Paper>
  );
}

export default URLForm;



// src/pages/HomePage.jsx

import React, { useState } from 'react';
import URLForm from '../components/URLForm';
import { Container, Typography, Box, List, ListItem, ListItemText, Paper } from '@mui/material';

function HomePage() {
  // State to hold the list of URLs created in this session
  const [createdUrls, setCreatedUrls] = useState([]);

  // This function will be called by the URLForm component when a new URL is made
  const handleNewUrl = (newUrlData) => {
    // Add the new URL to the top of our list
    setCreatedUrls(prevUrls => [newUrlData, ...prevUrls]);
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4, textAlign: 'center' }}>
        <Typography variant="h2" component="h1" gutterBottom>
          URL Shortener
        </Typography>
      </Box>

      <URLForm onNewUrlCreated={handleNewUrl} />

      {/* Section to display results */}
      {createdUrls.length > 0 && (
        <Paper sx={{ mt: 4, p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Recently Created Links:
          </Typography>
          <List>
            {createdUrls.map((url, index) => (
              <ListItem key={index}>
                <ListItemText primary={url.shortUrl} secondary="Click to copy (feature to be added)" />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}
    </Container>
  );
}

export default HomePage;