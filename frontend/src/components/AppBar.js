import React from 'react';
import {
  AppBar as MuiAppBar,
  Toolbar,
  Typography,
  Box,
} from '@mui/material';
import ConfirmationNumberIcon from '@mui/icons-material/ConfirmationNumber';

function AppBar() {
  return (
    <MuiAppBar position="static">
      <Toolbar>
        <Box display="flex" alignItems="center">
          <ConfirmationNumberIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div">
            Concert Ticketing
          </Typography>
        </Box>
      </Toolbar>
    </MuiAppBar>
  );
}

export default AppBar; 