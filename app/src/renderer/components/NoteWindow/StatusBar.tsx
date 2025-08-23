import React from 'react';
import { Box, Typography, Chip } from '@mui/material';
import { formatDistanceToNow } from 'date-fns';

interface StatusBarProps {
  wordCount: number;
  characterCount: number;
  lineCount: number;
  cursorPosition: { line: number; column: number };
  lastSaved?: string;
  isSaving: boolean;
}

const StatusBar: React.FC<StatusBarProps> = ({
  wordCount,
  characterCount,
  lineCount,
  cursorPosition,
  lastSaved,
  isSaving,
}) => {
  const formatLastSaved = (timestamp?: string) => {
    if (!timestamp) return 'Never saved';
    try {
      return `Saved ${formatDistanceToNow(new Date(timestamp), { addSuffix: true })}`;
    } catch {
      return 'Saved recently';
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '4px 16px',
        backgroundColor: 'background.default',
        borderTop: '1px solid',
        borderColor: 'divider',
        minHeight: '28px',
      }}
    >
      {/* Left Section - Cursor Position */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <Typography variant="caption" sx={{ color: 'text.secondary' }}>
          Line {cursorPosition.line}, Column {cursorPosition.column}
        </Typography>
      </Box>

      {/* Center Section - Statistics */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <Typography variant="caption" sx={{ color: 'text.secondary' }}>
          {wordCount} words
        </Typography>
        <Typography variant="caption" sx={{ color: 'text.secondary' }}>
          {characterCount} chars
        </Typography>
        <Typography variant="caption" sx={{ color: 'text.secondary' }}>
          {lineCount} lines
        </Typography>
      </Box>

      {/* Right Section - Save Status */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        {isSaving ? (
          <Chip
            label="Saving..."
            size="small"
            color="primary"
            variant="outlined"
            sx={{ height: '20px', fontSize: '10px' }}
          />
        ) : (
          <Typography variant="caption" sx={{ color: 'text.secondary' }}>
            {formatLastSaved(lastSaved)}
          </Typography>
        )}
      </Box>
    </Box>
  );
};

export default StatusBar;