import React, { useState, useRef } from 'react';
import {
  Box,
  Chip,
  TextField,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Add as AddIcon,
  Close as CloseIcon,
} from '@mui/icons-material';

interface TagsBarProps {
  tags: string[];
  onAddTag: (tag: string) => void;
  onRemoveTag: (tag: string) => void;
}

const TagsBar: React.FC<TagsBarProps> = ({
  tags,
  onAddTag,
  onRemoveTag,
}) => {
  const [isAddingTag, setIsAddingTag] = useState(false);
  const [newTag, setNewTag] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const handleAddTag = () => {
    if (newTag.trim() && !tags.includes(newTag.trim())) {
      onAddTag(newTag.trim());
      setNewTag('');
      setIsAddingTag(false);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      handleAddTag();
    } else if (event.key === 'Escape') {
      setNewTag('');
      setIsAddingTag(false);
    }
  };

  const startAddingTag = () => {
    setIsAddingTag(true);
    setTimeout(() => inputRef.current?.focus(), 100);
  };

  const cancelAddingTag = () => {
    setNewTag('');
    setIsAddingTag(false);
  };

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        gap: 1,
        padding: '8px 16px',
        backgroundColor: 'background.default',
        borderBottom: '1px solid',
        borderColor: 'divider',
        flexWrap: 'wrap',
        minHeight: '40px',
      }}
    >
      {/* Existing Tags */}
      {tags.map((tag) => (
        <Chip
          key={tag}
          label={tag}
          size="small"
          onDelete={() => onRemoveTag(tag)}
          deleteIcon={<CloseIcon sx={{ fontSize: 14 }} />}
          sx={{
            backgroundColor: 'primary.main',
            color: 'primary.contrastText',
            '& .MuiChip-deleteIcon': {
              color: 'primary.contrastText',
              '&:hover': {
                color: 'error.main',
              },
            },
          }}
        />
      ))}

      {/* Add Tag Input */}
      {isAddingTag ? (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
          <TextField
            ref={inputRef}
            value={newTag}
            onChange={(e) => setNewTag(e.target.value)}
            onKeyDown={handleKeyPress}
            onBlur={cancelAddingTag}
            placeholder="Tag name..."
            variant="outlined"
            size="small"
            sx={{
              width: '120px',
              '& .MuiOutlinedInput-root': {
                height: '24px',
                fontSize: '12px',
              },
            }}
          />
        </Box>
      ) : (
        <Tooltip title="Add tag">
          <IconButton
            size="small"
            onClick={startAddingTag}
            sx={{
              width: '24px',
              height: '24px',
              border: '1px dashed',
              borderColor: 'divider',
              '&:hover': {
                borderColor: 'primary.main',
                backgroundColor: 'primary.main',
                color: 'primary.contrastText',
              },
            }}
          >
            <AddIcon sx={{ fontSize: 14 }} />
          </IconButton>
        </Tooltip>
      )}
    </Box>
  );
};

export default TagsBar;