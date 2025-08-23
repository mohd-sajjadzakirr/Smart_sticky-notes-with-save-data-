import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  TextField,
  IconButton,
  Tooltip,
  Typography,
  Chip,
} from '@mui/material';
import {
  Close as CloseIcon,
  KeyboardArrowUp as ArrowUpIcon,
  KeyboardArrowDown as ArrowDownIcon,
  Search as SearchIcon,
  FindReplace as ReplaceIcon,
} from '@mui/icons-material';

interface SearchBarProps {
  query: string;
  onQueryChange: (query: string) => void;
  onClose: () => void;
}

const SearchBar: React.FC<SearchBarProps> = ({
  query,
  onQueryChange,
  onClose,
}) => {
  const [replaceMode, setReplaceMode] = useState(false);
  const [replaceText, setReplaceText] = useState('');
  const [currentMatch, setCurrentMatch] = useState(0);
  const [totalMatches, setTotalMatches] = useState(0);
  const [caseSensitive, setCaseSensitive] = useState(false);
  const [wholeWord, setWholeWord] = useState(false);
  const [useRegex, setUseRegex] = useState(false);
  
  const searchInputRef = useRef<HTMLInputElement>(null);
  const replaceInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (searchInputRef.current) {
      searchInputRef.current.focus();
    }
  }, []);

  useEffect(() => {
    // Update match count when query changes
    if (query) {
      // This would typically search in the editor content
      // For now, we'll simulate finding matches
      const mockMatches = Math.floor(Math.random() * 10);
      setTotalMatches(mockMatches);
      setCurrentMatch(mockMatches > 0 ? 1 : 0);
    } else {
      setTotalMatches(0);
      setCurrentMatch(0);
    }
  }, [query, caseSensitive, wholeWord, useRegex]);

  const handleSearchKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      if (event.shiftKey) {
        handlePreviousMatch();
      } else {
        handleNextMatch();
      }
    } else if (event.key === 'Escape') {
      onClose();
    }
  };

  const handleReplaceKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      handleReplace();
    } else if (event.key === 'Escape') {
      setReplaceMode(false);
    }
  };

  const handleNextMatch = () => {
    if (totalMatches > 0) {
      setCurrentMatch((prev) => (prev >= totalMatches ? 1 : prev + 1));
    }
  };

  const handlePreviousMatch = () => {
    if (totalMatches > 0) {
      setCurrentMatch((prev) => (prev <= 1 ? totalMatches : prev - 1));
    }
  };

  const handleReplace = () => {
    // Implement replace functionality
    console.log('Replace:', query, 'with:', replaceText);
  };

  const handleReplaceAll = () => {
    // Implement replace all functionality
    console.log('Replace all:', query, 'with:', replaceText);
  };

  const toggleReplaceMode = () => {
    setReplaceMode(!replaceMode);
    if (!replaceMode && replaceInputRef.current) {
      setTimeout(() => replaceInputRef.current?.focus(), 100);
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: 'background.paper',
        borderBottom: '1px solid',
        borderColor: 'divider',
        padding: '8px 16px',
        gap: 1,
      }}
    >
      {/* Search Row */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <SearchIcon sx={{ fontSize: 18, color: 'text.secondary' }} />
        
        <TextField
          ref={searchInputRef}
          value={query}
          onChange={(e) => onQueryChange(e.target.value)}
          onKeyDown={handleSearchKeyDown}
          placeholder="Search..."
          variant="outlined"
          size="small"
          sx={{
            flex: 1,
            '& .MuiOutlinedInput-root': {
              height: '32px',
              fontSize: '14px',
            },
          }}
        />

        {totalMatches > 0 && (
          <Typography variant="caption" sx={{ color: 'text.secondary', minWidth: '60px' }}>
            {currentMatch} of {totalMatches}
          </Typography>
        )}

        <Tooltip title="Previous match (Shift+Enter)">
          <IconButton
            size="small"
            onClick={handlePreviousMatch}
            disabled={totalMatches === 0}
          >
            <ArrowUpIcon sx={{ fontSize: 16 }} />
          </IconButton>
        </Tooltip>

        <Tooltip title="Next match (Enter)">
          <IconButton
            size="small"
            onClick={handleNextMatch}
            disabled={totalMatches === 0}
          >
            <ArrowDownIcon sx={{ fontSize: 16 }} />
          </IconButton>
        </Tooltip>

        <Tooltip title="Toggle replace mode">
          <IconButton
            size="small"
            onClick={toggleReplaceMode}
            color={replaceMode ? 'primary' : 'default'}
          >
            <ReplaceIcon sx={{ fontSize: 16 }} />
          </IconButton>
        </Tooltip>

        <Tooltip title="Close search">
          <IconButton size="small" onClick={onClose}>
            <CloseIcon sx={{ fontSize: 16 }} />
          </IconButton>
        </Tooltip>
      </Box>

      {/* Replace Row */}
      {replaceMode && (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, ml: 3 }}>
          <TextField
            ref={replaceInputRef}
            value={replaceText}
            onChange={(e) => setReplaceText(e.target.value)}
            onKeyDown={handleReplaceKeyDown}
            placeholder="Replace with..."
            variant="outlined"
            size="small"
            sx={{
              flex: 1,
              '& .MuiOutlinedInput-root': {
                height: '32px',
                fontSize: '14px',
              },
            }}
          />

          <Tooltip title="Replace current match">
            <IconButton
              size="small"
              onClick={handleReplace}
              disabled={totalMatches === 0}
              sx={{ fontSize: '12px', minWidth: '60px' }}
            >
              Replace
            </IconButton>
          </Tooltip>

          <Tooltip title="Replace all matches">
            <IconButton
              size="small"
              onClick={handleReplaceAll}
              disabled={totalMatches === 0}
              sx={{ fontSize: '12px', minWidth: '70px' }}
            >
              Replace All
            </IconButton>
          </Tooltip>
        </Box>
      )}

      {/* Search Options */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, ml: 3 }}>
        <Chip
          label="Aa"
          size="small"
          variant={caseSensitive ? 'filled' : 'outlined'}
          onClick={() => setCaseSensitive(!caseSensitive)}
          sx={{ fontSize: '10px', height: '20px' }}
        />
        <Chip
          label="Ab"
          size="small"
          variant={wholeWord ? 'filled' : 'outlined'}
          onClick={() => setWholeWord(!wholeWord)}
          sx={{ fontSize: '10px', height: '20px' }}
        />
        <Chip
          label=".*"
          size="small"
          variant={useRegex ? 'filled' : 'outlined'}
          onClick={() => setUseRegex(!useRegex)}
          sx={{ fontSize: '10px', height: '20px' }}
        />
      </Box>
    </Box>
  );
};

export default SearchBar;