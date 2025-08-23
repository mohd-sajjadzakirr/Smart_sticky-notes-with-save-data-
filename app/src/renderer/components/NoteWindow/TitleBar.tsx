import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Typography,
  IconButton,
  Tooltip,
  TextField,
  Chip,
} from '@mui/material';
import {
  Close as CloseIcon,
  Minimize as MinimizeIcon,
  PushPin as PinIcon,
  PushPinOutlined as PinOutlinedIcon,
  Settings as SettingsIcon,
  Search as SearchIcon,
  Preview as PreviewIcon,
  Fullscreen as FullscreenIcon,
  Save as SaveIcon,
  ColorLens as ColorIcon,
  DragIndicator as DragIcon,
} from '@mui/icons-material';

interface TitleBarProps {
  title: string;
  onTitleChange: (title: string) => void;
  isPinned: boolean;
  isSaving: boolean;
  onPin: () => void;
  onMinimize: () => void;
  onClose: () => void;
  onSettings: () => void;
  onColorPicker: () => void;
  onSearch: () => void;
  onMarkdownToggle: () => void;
  onZenMode: () => void;
}

const TitleBar: React.FC<TitleBarProps> = ({
  title,
  onTitleChange,
  isPinned,
  isSaving,
  onPin,
  onMinimize,
  onClose,
  onSettings,
  onColorPicker,
  onSearch,
  onMarkdownToggle,
  onZenMode,
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(title);
  const titleInputRef = useRef<HTMLInputElement>(null);
  const titleBarRef = useRef<HTMLDivElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  useEffect(() => {
    setEditTitle(title);
  }, [title]);

  useEffect(() => {
    if (isEditing && titleInputRef.current) {
      titleInputRef.current.focus();
      titleInputRef.current.select();
    }
  }, [isEditing]);

  const handleTitleClick = () => {
    setIsEditing(true);
  };

  const handleTitleSubmit = () => {
    setIsEditing(false);
    if (editTitle.trim() !== title) {
      onTitleChange(editTitle.trim() || 'Untitled Note');
    }
  };

  const handleTitleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      handleTitleSubmit();
    } else if (event.key === 'Escape') {
      setEditTitle(title);
      setIsEditing(false);
    }
  };

  const handleMouseDown = (event: React.MouseEvent) => {
    if (event.target === titleBarRef.current || (event.target as Element).closest('.drag-handle')) {
      setIsDragging(true);
      setDragStart({
        x: event.clientX,
        y: event.clientY,
      });
      
      const handleMouseMove = (e: MouseEvent) => {
        if (isDragging) {
          const deltaX = e.clientX - dragStart.x;
          const deltaY = e.clientY - dragStart.y;
          
          // Send drag info to main process
          window.electronAPI?.moveWindow?.(deltaX, deltaY);
        }
      };

      const handleMouseUp = () => {
        setIsDragging(false);
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
      };

      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }
  };

  return (
    <Box
      ref={titleBarRef}
      className="title-bar"
      onMouseDown={handleMouseDown}
      sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '8px 16px',
        backgroundColor: 'background.paper',
        borderBottom: '1px solid',
        borderColor: 'divider',
        minHeight: '48px',
        cursor: isDragging ? 'grabbing' : 'grab',
        userSelect: 'none',
        '-webkit-app-region': 'drag',
      }}
    >
      {/* Left Section - Title and Status */}
      <Box sx={{ display: 'flex', alignItems: 'center', flex: 1, minWidth: 0 }}>
        <Box className="drag-handle" sx={{ mr: 1, cursor: 'grab' }}>
          <DragIcon sx={{ fontSize: 16, color: 'text.secondary' }} />
        </Box>
        
        {isEditing ? (
          <TextField
            ref={titleInputRef}
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            onBlur={handleTitleSubmit}
            onKeyDown={handleTitleKeyPress}
            variant="standard"
            size="small"
            sx={{
              flex: 1,
              maxWidth: '300px',
              '& .MuiInput-underline:before': {
                borderBottomColor: 'transparent',
              },
              '& .MuiInput-underline:hover:before': {
                borderBottomColor: 'primary.main',
              },
              '& .MuiInputBase-input': {
                fontSize: '14px',
                fontWeight: 500,
                padding: '4px 0',
              },
            }}
          />
        ) : (
          <Typography
            variant="subtitle2"
            onClick={handleTitleClick}
            sx={{
              cursor: 'pointer',
              fontWeight: 500,
              color: 'text.primary',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap',
              maxWidth: '300px',
              '&:hover': {
                backgroundColor: 'action.hover',
                borderRadius: 1,
                padding: '2px 4px',
                margin: '-2px -4px',
              },
            }}
          >
            {title || 'Untitled Note'}
          </Typography>
        )}

        {isSaving && (
          <Chip
            label="Saving..."
            size="small"
            color="primary"
            variant="outlined"
            sx={{ ml: 1, height: 20, fontSize: '10px' }}
          />
        )}
      </Box>

      {/* Right Section - Controls */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          gap: 0.5,
          '-webkit-app-region': 'no-drag',
        }}
      >
        <Tooltip title="Search in note">
          <IconButton size="small" onClick={onSearch}>
            <SearchIcon sx={{ fontSize: 16 }} />
          </IconButton>
        </Tooltip>

        <Tooltip title="Toggle markdown preview">
          <IconButton size="small" onClick={onMarkdownToggle}>
            <PreviewIcon sx={{ fontSize: 16 }} />
          </IconButton>
        </Tooltip>

        <Tooltip title="Change color">
          <IconButton size="small" onClick={onColorPicker}>
            <ColorIcon sx={{ fontSize: 16 }} />
          </IconButton>
        </Tooltip>

        <Tooltip title="Zen mode">
          <IconButton size="small" onClick={onZenMode}>
            <FullscreenIcon sx={{ fontSize: 16 }} />
          </IconButton>
        </Tooltip>

        <Tooltip title={isPinned ? 'Unpin from top' : 'Pin to top'}>
          <IconButton size="small" onClick={onPin} color={isPinned ? 'primary' : 'default'}>
            {isPinned ? <PinIcon sx={{ fontSize: 16 }} /> : <PinOutlinedIcon sx={{ fontSize: 16 }} />}
          </IconButton>
        </Tooltip>

        <Tooltip title="Settings">
          <IconButton size="small" onClick={onSettings}>
            <SettingsIcon sx={{ fontSize: 16 }} />
          </IconButton>
        </Tooltip>

        <Tooltip title="Minimize">
          <IconButton size="small" onClick={onMinimize}>
            <MinimizeIcon sx={{ fontSize: 16 }} />
          </IconButton>
        </Tooltip>

        <Tooltip title="Close">
          <IconButton size="small" onClick={onClose} sx={{ color: 'error.main' }}>
            <CloseIcon sx={{ fontSize: 16 }} />
          </IconButton>
        </Tooltip>
      </Box>
    </Box>
  );
};

export default TitleBar;