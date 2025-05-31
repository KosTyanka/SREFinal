import React, { useState, useEffect } from 'react';
import { Container, Typography, Card, CardContent, Button, Grid } from '@mui/material';

function App() {
  const [concerts, setConcerts] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchConcerts();
  }, []);

  const fetchConcerts = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/concerts', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setConcerts(data);
      setError(null);
    } catch (error) {
      console.error('Error fetching concerts:', error);
      setError('Failed to load concerts. Please try again later.');
    }
  };

  const purchaseTicket = async (concertId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/concerts/${concertId}/tickets`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      await fetchConcerts(); // Refresh concert list
      setError(null);
    } catch (error) {
      console.error('Error purchasing ticket:', error);
      setError('Failed to purchase ticket. Please try again later.');
    }
  };

  return (
    <Container maxWidth="md" style={{ marginTop: '2rem' }}>
      <Typography variant="h3" component="h1" gutterBottom>
        Concert Ticketing System
      </Typography>
      
      {error && (
        <Typography color="error" style={{ marginBottom: '1rem' }}>
          {error}
        </Typography>
      )}

      <Grid container spacing={3}>
        {concerts.map((concert) => (
          <Grid item xs={12} sm={6} md={4} key={concert.id}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="h2">
                  {concert.name}
                </Typography>
                <Typography color="textSecondary">
                  {new Date(concert.date).toLocaleDateString()}
                </Typography>
                <Typography variant="body2" component="p">
                  Venue: {concert.venue}
                </Typography>
                <Typography variant="body2" component="p">
                  Available Tickets: {concert.available_tickets}
                </Typography>
                <Typography variant="body2" component="p">
                  Price: ${concert.price}
                </Typography>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => purchaseTicket(concert.id)}
                  disabled={concert.available_tickets <= 0}
                  style={{ marginTop: '1rem' }}
                >
                  {concert.available_tickets > 0 ? 'Purchase Ticket' : 'Sold Out'}
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}

export default App; 