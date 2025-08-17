import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  IconButton,
  Grid,
} from '@mui/material';
import {
  Close as CloseIcon,
  Check as CheckIcon,
} from '@mui/icons-material';

interface ColorPickerProps {
  currentColor: string;
  onColorChange: (color: string) => void;
  onClose: () => void;
}

const predefinedColors = [
  { name: 'Default', value: '#2d2d2d' },
  { name: 'Blue', value: '#1976d2' },
  { name: 'Green', value: '#388e3c' },
  { name: 'Orange', value: '#f57c00' },
  { name: 'Red', value: '#d32f2f' },
  { name: 'Purple', value: '#7b1fa2' },
  { name: 'Teal', value: '#00796b' },
  { name: 'Pink', value: '#c2185b' },
  { name: 'Indigo', value: '#303f9f' },
  { name: 'Brown', value: '#5d4037' },
  { name: 'Grey', value: '#616161' },
  { name: 'Black', value: '#212121' },
];

const ColorPicker: React.FC<ColorPickerProps> = ({
  currentColor,
  onColorChange,
  onClose,
}) => {
  const [selectedColor, setSelectedColor] = useState(currentColor);

  const handleColorSelect = (color: string) => {
    setSelectedColor(color);
    onColorChange(color);
  };

  return (
    <Paper
      elevation={8}
      sx={{
        position: 'fixed',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: '300px',
        zIndex: 9999,
        padding: '16px',
      }}
    >
      {/* Header */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: '16px',
        }}
      >
        <Typography variant="h6">Choose Color</Typography>
        <IconButton onClick={onClose} size="small">
          <CloseIcon />
        </IconButton>
      </Box>

      {/* Color Grid */}
      <Grid container spacing={1}>
        {predefinedColors.map((color) => (
          <Grid item xs={3} key={color.value}>
            <Box
              onClick={() => handleColorSelect(color.value)}
              sx={{
                width: '100%',
                height: '48px',
                backgroundColor: color.value,
                borderRadius: '8px',
                cursor: 'pointer',
                border: selectedColor === color.value ? '3px solid' : '2px solid transparent',
                borderColor: selectedColor === color.value ? 'primary.main' : 'transparent',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                transition: 'all 0.2s ease',
                '&:hover': {
                  transform: 'scale(1.05)',
                  boxShadow: 2,
                },
              }}
            >
              {selectedColor === color.value && (
                <CheckIcon
                  sx={{
                    color: color.value === '#212121' || color.value === '#2d2d2d' ? 'white' : 'white',
                    fontSize: '20px',
                  }}
                />
              )}
            </Box>
            <Typography
              variant="caption"
              sx={{
                display: 'block',
                textAlign: 'center',
                marginTop: '4px',
                fontSize: '10px',
              }}
            >
              {color.name}
            </Typography>
          </Grid>
        ))}
      </Grid>

      {/* Custom Color Input */}
      <Box sx={{ marginTop: '16px' }}>
        <Typography variant="body2" gutterBottom>
          Custom Color:
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <input
            type="color"
            value={selectedColor}
            onChange={(e) => handleColorSelect(e.target.value)}
            style={{
              width: '40px',
              height: '40px',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
            }}
          />
          <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
            {selectedColor}
          </Typography>
        </Box>
      </Box>
    </Paper>
  );
};

export default ColorPicker;