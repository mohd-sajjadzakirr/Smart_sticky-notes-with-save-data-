import React, { useEffect, useRef, useState, useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Box, Paper, IconButton, Tooltip, Chip, TextField, InputAdornment } from '@mui/material';
import {
  Close as CloseIcon,
  Minimize as MinimizeIcon,
  PushPin as PinIcon,
  Settings as SettingsIcon,
  Search as SearchIcon,
  Tag as TagIcon,
  Preview as PreviewIcon,
  Fullscreen as FullscreenIcon,
  Save as SaveIcon,
  ColorLens as ColorIcon,
} from '@mui/icons-material';
import { RootState, AppDispatch } from '../../store/store';
import {
  loadNote,
  saveNote,
  updateNoteContent,
  updateNoteTitle,
  addTag,
  removeTag,
  togglePin,
  toggleMarkdownPreview,
  toggleZenMode,
  setNoteColor,
  setCursorPosition,
  setSearchQuery,
  toggleSearchVisibility,
} from '../../store/slices/noteSlice';
import { loadSettings } from '../../store/slices/settingsSlice';
import { loadAnalytics, incrementWordCount } from '../../store/slices/analyticsSlice';
import {
  setDragging,
  setWindowBounds,
  openContextMenu,
  closeContextMenu,
  addNotification,
} from '../../store/slices/uiSlice';
import TitleBar from './TitleBar';
import Editor from './Editor';
import MarkdownPreview from './MarkdownPreview';
import SearchBar from './SearchBar';
import TagsBar from './TagsBar';
import StatusBar from './StatusBar';
import ContextMenu from './ContextMenu';
import SettingsPanel from './SettingsPanel';
import ColorPicker from './ColorPicker';
import './NoteWindow.css';

const { ipcRenderer } = window.require('electron');

const NoteWindow: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { currentNote, isLoading, isSaving, isMarkdownPreview, isZenMode, isSearchVisible } = useSelector((state: RootState) => state.note);
  const { settings } = useSelector((state: RootState) => state.settings);
  const { isContextMenuOpen, contextMenuPosition, isSettingsPanelOpen } = useSelector((state: RootState) => state.ui);
  
  const [instanceId, setInstanceId] = useState<string>('');
  const [isColorPickerOpen, setIsColorPickerOpen] = useState(false);
  const [autoSaveTimer, setAutoSaveTimer] = useState<NodeJS.Timeout | null>(null);
  const noteWindowRef = useRef<HTMLDivElement>(null);
  const editorRef = useRef<HTMLTextAreaElement>(null);

  // Initialize note window
  useEffect(() => {
    const handleInitialize = (event: any, data: any) => {
      setInstanceId(data.instanceId);
      dispatch(loadNote(data.instanceId));
      dispatch(loadSettings());
      dispatch(loadAnalytics());
    };

    const handleSaveRequest = () => {
      if (currentNote && instanceId) {
        dispatch(saveNote({ instanceId, noteData: currentNote }));
      }
    };

    const handleSettingsUpdated = (event: any, newSettings: any) => {
      // Apply new settings to the window
      applySettings(newSettings);
    };

    ipcRenderer.on('initialize', handleInitialize);
    ipcRenderer.on('save-request', handleSaveRequest);
    ipcRenderer.on('settings-updated', handleSettingsUpdated);
    ipcRenderer.on('trigger-find', () => dispatch(toggleSearchVisibility()));
    ipcRenderer.on('toggle-markdown', () => dispatch(toggleMarkdownPreview()));
    ipcRenderer.on('toggle-zen-mode', () => dispatch(toggleZenMode()));

    return () => {
      ipcRenderer.removeAllListeners('initialize');
      ipcRenderer.removeAllListeners('save-request');
      ipcRenderer.removeAllListeners('settings-updated');
      ipcRenderer.removeAllListeners('trigger-find');
      ipcRenderer.removeAllListeners('toggle-markdown');
      ipcRenderer.removeAllListeners('toggle-zen-mode');
    };
  }, [dispatch, currentNote, instanceId]);

  // Auto-save functionality
  useEffect(() => {
    if (settings?.autoSave && currentNote && instanceId) {
      if (autoSaveTimer) {
        clearTimeout(autoSaveTimer);
      }

      const timer = setTimeout(() => {
        dispatch(saveNote({ instanceId, noteData: currentNote }));
      }, settings.autoSaveInterval || 3000);

      setAutoSaveTimer(timer);
    }

    return () => {
      if (autoSaveTimer) {
        clearTimeout(autoSaveTimer);
      }
    };
  }, [currentNote, settings, instanceId, dispatch]);

  // Apply settings to window
  const applySettings = useCallback((newSettings: any) => {
    if (noteWindowRef.current) {
      const element = noteWindowRef.current;
      element.style.opacity = newSettings.opacity?.toString() || '1';
      element.style.fontSize = `${newSettings.fontSize || 14}px`;
      element.style.fontFamily = newSettings.fontFamily || 'Inter, sans-serif';
    }
  }, []);

  // Handle content change
  const handleContentChange = useCallback((content: string) => {
    dispatch(updateNoteContent(content));
    
    // Update word count analytics
    const wordCount = content.split(/\s+/).filter(word => word.length > 0).length;
    dispatch(incrementWordCount(wordCount));
  }, [dispatch]);

  // Handle title change
  const handleTitleChange = useCallback((title: string) => {
    dispatch(updateNoteTitle(title));
  }, [dispatch]);

  // Handle tag operations
  const handleAddTag = useCallback((tag: string) => {
    dispatch(addTag(tag));
  }, [dispatch]);

  const handleRemoveTag = useCallback((tag: string) => {
    dispatch(removeTag(tag));
  }, [dispatch]);

  // Handle window controls
  const handleMinimize = useCallback(async () => {
    await ipcRenderer.invoke('minimize-window');
  }, []);

  const handleClose = useCallback(async () => {
    if (currentNote && instanceId) {
      await dispatch(saveNote({ instanceId, noteData: currentNote }));
    }
    await ipcRenderer.invoke('close-window');
  }, [currentNote, instanceId, dispatch]);

  const handlePin = useCallback(async () => {
    const result = await ipcRenderer.invoke('toggle-always-on-top');
    if (result.success) {
      dispatch(togglePin());
      dispatch(addNotification({
        type: 'info',
        message: result.isOnTop ? 'Note pinned to top' : 'Note unpinned',
        duration: 2000,
      }));
    }
  }, [dispatch]);

  // Handle color change
  const handleColorChange = useCallback((color: string) => {
    dispatch(setNoteColor(color));
    setIsColorPickerOpen(false);
  }, [dispatch]);

  // Handle context menu
  const handleContextMenu = useCallback((event: React.MouseEvent) => {
    event.preventDefault();
    dispatch(openContextMenu({ x: event.clientX, y: event.clientY }));
  }, [dispatch]);

  // Handle click outside to close menus
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (isContextMenuOpen) {
        dispatch(closeContextMenu());
      }
      if (isColorPickerOpen) {
        setIsColorPickerOpen(false);
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, [isContextMenuOpen, isColorPickerOpen, dispatch]);

  if (isLoading) {
    return (
      <Box className="note-window loading" display="flex" alignItems="center" justifyContent="center">
        <div className="loading-spinner">Loading...</div>
      </Box>
    );
  }

  return (
    <Box
      ref={noteWindowRef}
      className={`note-window ${isZenMode ? 'zen-mode' : ''} ${currentNote?.color || 'default'}`}
      onContextMenu={handleContextMenu}
      sx={{
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: currentNote?.color || 'background.paper',
        borderRadius: isZenMode ? 0 : 2,
        overflow: 'hidden',
        boxShadow: isZenMode ? 'none' : 3,
      }}
    >
      {/* Title Bar */}
      {!isZenMode && (
        <TitleBar
          title={currentNote?.title || 'Untitled Note'}
          onTitleChange={handleTitleChange}
          isPinned={currentNote?.isPinned || false}
          isSaving={isSaving}
          onPin={handlePin}
          onMinimize={handleMinimize}
          onClose={handleClose}
          onSettings={() => dispatch({ type: 'ui/toggleSettingsPanel' })}
          onColorPicker={() => setIsColorPickerOpen(true)}
          onSearch={() => dispatch(toggleSearchVisibility())}
          onMarkdownToggle={() => dispatch(toggleMarkdownPreview())}
          onZenMode={() => dispatch(toggleZenMode())}
        />
      )}

      {/* Search Bar */}
      {isSearchVisible && (
        <SearchBar
          query=""
          onQueryChange={(query) => dispatch(setSearchQuery(query))}
          onClose={() => dispatch(toggleSearchVisibility())}
        />
      )}

      {/* Tags Bar */}
      {currentNote?.tags && currentNote.tags.length > 0 && (
        <TagsBar
          tags={currentNote.tags}
          onAddTag={handleAddTag}
          onRemoveTag={handleRemoveTag}
        />
      )}

      {/* Main Content */}
      <Box sx={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {isMarkdownPreview ? (
          <MarkdownPreview content={currentNote?.content || ''} />
        ) : (
          <Editor
            ref={editorRef}
            content={currentNote?.content || ''}
            onChange={handleContentChange}
            settings={settings}
            onCursorPositionChange={(line, column) => dispatch(setCursorPosition({ line, column }))}
          />
        )}
      </Box>

      {/* Status Bar */}
      {!isZenMode && (
        <StatusBar
          wordCount={currentNote?.content?.split(/\s+/).filter(word => word.length > 0).length || 0}
          characterCount={currentNote?.content?.length || 0}
          lineCount={currentNote?.content?.split('\n').length || 1}
          cursorPosition={{ line: 1, column: 1 }}
          lastSaved={currentNote?.lastModified}
          isSaving={isSaving}
        />
      )}

      {/* Context Menu */}
      {isContextMenuOpen && (
        <ContextMenu
          position={contextMenuPosition}
          onClose={() => dispatch(closeContextMenu())}
          selectedText=""
        />
      )}

      {/* Settings Panel */}
      {isSettingsPanelOpen && (
        <SettingsPanel
          onClose={() => dispatch({ type: 'ui/toggleSettingsPanel' })}
        />
      )}

      {/* Color Picker */}
      {isColorPickerOpen && (
        <ColorPicker
          currentColor={currentNote?.color || '#2d2d2d'}
          onColorChange={handleColorChange}
          onClose={() => setIsColorPickerOpen(false)}
        />
      )}
    </Box>
  );
};

export default NoteWindow;