import React, { useEffect, useRef } from 'react';
import {
  Paper,
  MenuList,
  MenuItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  Cut as CutIcon,
  Copy as CopyIcon,
  Paste as PasteIcon,
  SelectAll as SelectAllIcon,
  Search as SearchIcon,
  FindReplace as ReplaceIcon,
  FormatBold as BoldIcon,
  FormatItalic as ItalicIcon,
  Code as CodeIcon,
  Link as LinkIcon,
} from '@mui/icons-material';

interface ContextMenuProps {
  position: { x: number; y: number };
  onClose: () => void;
  selectedText: string;
}

const ContextMenu: React.FC<ContextMenuProps> = ({
  position,
  onClose,
  selectedText,
}) => {
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        onClose();
      }
    };

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleEscape);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscape);
    };
  }, [onClose]);

  const handleCut = () => {
    document.execCommand('cut');
    onClose();
  };

  const handleCopy = () => {
    document.execCommand('copy');
    onClose();
  };

  const handlePaste = () => {
    document.execCommand('paste');
    onClose();
  };

  const handleSelectAll = () => {
    document.execCommand('selectAll');
    onClose();
  };

  const handleFind = () => {
    // Trigger find functionality
    onClose();
  };

  const handleReplace = () => {
    // Trigger replace functionality
    onClose();
  };

  const handleFormatBold = () => {
    // Add bold formatting to selected text
    onClose();
  };

  const handleFormatItalic = () => {
    // Add italic formatting to selected text
    onClose();
  };

  const handleFormatCode = () => {
    // Add code formatting to selected text
    onClose();
  };

  const handleCreateLink = () => {
    // Create link from selected text
    onClose();
  };

  return (
    <Paper
      ref={menuRef}
      elevation={8}
      sx={{
        position: 'fixed',
        left: position.x,
        top: position.y,
        zIndex: 9999,
        minWidth: '200px',
        maxWidth: '300px',
      }}
    >
      <MenuList dense>
        {/* Basic editing commands */}
        <MenuItem onClick={handleCut} disabled={!selectedText}>
          <ListItemIcon>
            <CutIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>Cut</ListItemText>
          <Typography variant="caption" sx={{ ml: 2, color: 'text.secondary' }}>
            Ctrl+X
          </Typography>
        </MenuItem>

        <MenuItem onClick={handleCopy} disabled={!selectedText}>
          <ListItemIcon>
            <CopyIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>Copy</ListItemText>
          <Typography variant="caption" sx={{ ml: 2, color: 'text.secondary' }}>
            Ctrl+C
          </Typography>
        </MenuItem>

        <MenuItem onClick={handlePaste}>
          <ListItemIcon>
            <PasteIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>Paste</ListItemText>
          <Typography variant="caption" sx={{ ml: 2, color: 'text.secondary' }}>
            Ctrl+V
          </Typography>
        </MenuItem>

        <MenuItem onClick={handleSelectAll}>
          <ListItemIcon>
            <SelectAllIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>Select All</ListItemText>
          <Typography variant="caption" sx={{ ml: 2, color: 'text.secondary' }}>
            Ctrl+A
          </Typography>
        </MenuItem>

        <Divider />

        {/* Search commands */}
        <MenuItem onClick={handleFind}>
          <ListItemIcon>
            <SearchIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>Find</ListItemText>
          <Typography variant="caption" sx={{ ml: 2, color: 'text.secondary' }}>
            Ctrl+F
          </Typography>
        </MenuItem>

        <MenuItem onClick={handleReplace}>
          <ListItemIcon>
            <ReplaceIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>Replace</ListItemText>
          <Typography variant="caption" sx={{ ml: 2, color: 'text.secondary' }}>
            Ctrl+H
          </Typography>
        </MenuItem>

        {/* Formatting commands (only show if text is selected) */}
        {selectedText && (
          <>
            <Divider />
            
            <MenuItem onClick={handleFormatBold}>
              <ListItemIcon>
                <BoldIcon fontSize="small" />
              </ListItemIcon>
              <ListItemText>Bold</ListItemText>
              <Typography variant="caption" sx={{ ml: 2, color: 'text.secondary' }}>
                Ctrl+B
              </Typography>
            </MenuItem>

            <MenuItem onClick={handleFormatItalic}>
              <ListItemIcon>
                <ItalicIcon fontSize="small" />
              </ListItemIcon>
              <ListItemText>Italic</ListItemText>
              <Typography variant="caption" sx={{ ml: 2, color: 'text.secondary' }}>
                Ctrl+I
              </Typography>
            </MenuItem>

            <MenuItem onClick={handleFormatCode}>
              <ListItemIcon>
                <CodeIcon fontSize="small" />
              </ListItemIcon>
              <ListItemText>Code</ListItemText>
              <Typography variant="caption" sx={{ ml: 2, color: 'text.secondary' }}>
                Ctrl+`
              </Typography>
            </MenuItem>

            <MenuItem onClick={handleCreateLink}>
              <ListItemIcon>
                <LinkIcon fontSize="small" />
              </ListItemIcon>
              <ListItemText>Create Link</ListItemText>
              <Typography variant="caption" sx={{ ml: 2, color: 'text.secondary' }}>
                Ctrl+K
              </Typography>
            </MenuItem>
          </>
        )}
      </MenuList>
    </Paper>
  );
};

export default ContextMenu;