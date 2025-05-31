import React, { useState } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
  Snackbar,
} from '@mui/material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function ConcertList() {
  const [purchaseDialog, setPurchaseDialog] = useState(false);
  const [selectedConcert, setSelectedConcert] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const queryClient = useQueryClient();

  const { data: concerts = [], isLoading, error } = useQuery('concerts', async () => {
    const response = await axios.get(`${API_URL}/concerts`);
    return response.data;
  });

  const purchaseTickets = useMutation(
    async ({ concertId, quantity }) => {
      const response = await axios.post(`${API_URL}/purchase`, {
        concert_id: concertId,
        quantity: parseInt(quantity),
      });
      return response.data;
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries('concerts');
        setSnackbar({
          open: true,
          message: 'Tickets purchased successfully!',
          severity: 'success',
        });
        handleCloseDialog();
      },
      onError: (error) => {
        setSnackbar({
          open: true,
          message: error.response?.data?.detail || 'Failed to purchase tickets',
          severity: 'error',
        });
      },
    }
  );

  const handlePurchaseClick = (concert) => {
    setSelectedConcert(concert);
    setPurchaseDialog(true);
  };

  const handleCloseDialog = () => {
    setPurchaseDialog(false);
    setSelectedConcert(null);
    setQuantity(1);
  };

  const handlePurchaseConfirm = () => {
    purchaseTickets.mutate({
      concertId: selectedConcert.id,
      quantity: quantity,
    });
  };

  if (isLoading) return <Typography>Loading...</Typography>;
  if (error) return <Typography color="error">Error loading concerts</Typography>;

  return (
    <Container sx={{ py: 4 }}>
      <Grid container spacing={3}>
        {concerts.map((concert) => (
          <Grid item xs={12} sm={6} md={4} key={concert.id}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="div" gutterBottom>
                  {concert.name}
                </Typography>
                <Typography color="text.secondary" gutterBottom>
                  {new Date(concert.date).toLocaleDateString()}
                </Typography>
                <Typography variant="body2" gutterBottom>
                  Venue: {concert.venue}
                </Typography>
                <Typography variant="body2" color="primary">
                  Tickets remaining: {concert.tickets_remaining}
                </Typography>
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  sx={{ mt: 2 }}
                  onClick={() => handlePurchaseClick(concert)}
                  disabled={concert.tickets_remaining === 0}
                >
                  Purchase Tickets
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog open={purchaseDialog} onClose={handleCloseDialog}>
        <DialogTitle>Purchase Tickets</DialogTitle>
        <DialogContent>
          <Typography gutterBottom>
            Concert: {selectedConcert?.name}
          </Typography>
          <TextField
            autoFocus
            margin="dense"
            label="Quantity"
            type="number"
            fullWidth
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            inputProps={{ min: 1, max: 100 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handlePurchaseConfirm} variant="contained">
            Purchase
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert severity={snackbar.severity} onClose={() => setSnackbar({ ...snackbar, open: false })}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
}

export default ConcertList; 