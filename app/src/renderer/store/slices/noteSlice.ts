import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

const { ipcRenderer } = window.require('electron');

export interface Note {
  id: string;
  title: string;
  content: string;
  created: string;
  lastModified: string;
  tags: string[];
  isMarkdown: boolean;
  isPinned: boolean;
  isArchived: boolean;
  color: string;
  fontSize: number;
  fontFamily: string;
  bounds?: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
  settings?: {
    wordWrap: boolean;
    showLineNumbers: boolean;
    enableSpellCheck: boolean;
    enableAutoComplete: boolean;
    theme: string;
    opacity: number;
  };
}

interface NoteState {
  currentNote: Note | null;
  isLoading: boolean;
  isSaving: boolean;
  lastSaved: string | null;
  error: string | null;
  wordCount: number;
  characterCount: number;
  lineCount: number;
  cursorPosition: { line: number; column: number };
  searchQuery: string;
  searchResults: any[];
  isSearchVisible: boolean;
  isMarkdownPreview: boolean;
  isZenMode: boolean;
  isFullscreen: boolean;
}

const initialState: NoteState = {
  currentNote: null,
  isLoading: false,
  isSaving: false,
  lastSaved: null,
  error: null,
  wordCount: 0,
  characterCount: 0,
  lineCount: 1,
  cursorPosition: { line: 1, column: 1 },
  searchQuery: '',
  searchResults: [],
  isSearchVisible: false,
  isMarkdownPreview: false,
  isZenMode: false,
  isFullscreen: false,
};

// Async thunks
export const loadNote = createAsyncThunk(
  'note/loadNote',
  async (instanceId: string) => {
    const response = await ipcRenderer.invoke('load-note', instanceId);
    return response;
  }
);

export const saveNote = createAsyncThunk(
  'note/saveNote',
  async ({ instanceId, noteData }: { instanceId: string; noteData: Partial<Note> }) => {
    const response = await ipcRenderer.invoke('save-note', instanceId, noteData);
    return response;
  }
);

export const deleteNote = createAsyncThunk(
  'note/deleteNote',
  async (instanceId: string) => {
    const response = await ipcRenderer.invoke('delete-note', instanceId);
    return response;
  }
);

const noteSlice = createSlice({
  name: 'note',
  initialState,
  reducers: {
    setCurrentNote: (state, action: PayloadAction<Note>) => {
      state.currentNote = action.payload;
    },
    updateNoteContent: (state, action: PayloadAction<string>) => {
      if (state.currentNote) {
        state.currentNote.content = action.payload;
        state.currentNote.lastModified = new Date().toISOString();
        
        // Update statistics
        state.wordCount = action.payload.split(/\s+/).filter(word => word.length > 0).length;
        state.characterCount = action.payload.length;
        state.lineCount = action.payload.split('\n').length;
      }
    },
    updateNoteTitle: (state, action: PayloadAction<string>) => {
      if (state.currentNote) {
        state.currentNote.title = action.payload;
        state.currentNote.lastModified = new Date().toISOString();
      }
    },
    addTag: (state, action: PayloadAction<string>) => {
      if (state.currentNote && !state.currentNote.tags.includes(action.payload)) {
        state.currentNote.tags.push(action.payload);
        state.currentNote.lastModified = new Date().toISOString();
      }
    },
    removeTag: (state, action: PayloadAction<string>) => {
      if (state.currentNote) {
        state.currentNote.tags = state.currentNote.tags.filter(tag => tag !== action.payload);
        state.currentNote.lastModified = new Date().toISOString();
      }
    },
    toggleMarkdown: (state) => {
      if (state.currentNote) {
        state.currentNote.isMarkdown = !state.currentNote.isMarkdown;
      }
    },
    togglePin: (state) => {
      if (state.currentNote) {
        state.currentNote.isPinned = !state.currentNote.isPinned;
        state.currentNote.lastModified = new Date().toISOString();
      }
    },
    setNoteColor: (state, action: PayloadAction<string>) => {
      if (state.currentNote) {
        state.currentNote.color = action.payload;
        state.currentNote.lastModified = new Date().toISOString();
      }
    },
    setCursorPosition: (state, action: PayloadAction<{ line: number; column: number }>) => {
      state.cursorPosition = action.payload;
    },
    setSearchQuery: (state, action: PayloadAction<string>) => {
      state.searchQuery = action.payload;
    },
    setSearchResults: (state, action: PayloadAction<any[]>) => {
      state.searchResults = action.payload;
    },
    toggleSearchVisibility: (state) => {
      state.isSearchVisible = !state.isSearchVisible;
    },
    toggleMarkdownPreview: (state) => {
      state.isMarkdownPreview = !state.isMarkdownPreview;
    },
    toggleZenMode: (state) => {
      state.isZenMode = !state.isZenMode;
    },
    toggleFullscreen: (state) => {
      state.isFullscreen = !state.isFullscreen;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Load note
      .addCase(loadNote.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(loadNote.fulfilled, (state, action) => {
        state.isLoading = false;
        state.currentNote = action.payload;
        if (action.payload.content) {
          state.wordCount = action.payload.content.split(/\s+/).filter((word: string) => word.length > 0).length;
          state.characterCount = action.payload.content.length;
          state.lineCount = action.payload.content.split('\n').length;
        }
      })
      .addCase(loadNote.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to load note';
      })
      // Save note
      .addCase(saveNote.pending, (state) => {
        state.isSaving = true;
        state.error = null;
      })
      .addCase(saveNote.fulfilled, (state) => {
        state.isSaving = false;
        state.lastSaved = new Date().toISOString();
      })
      .addCase(saveNote.rejected, (state, action) => {
        state.isSaving = false;
        state.error = action.error.message || 'Failed to save note';
      })
      // Delete note
      .addCase(deleteNote.fulfilled, (state) => {
        state.currentNote = null;
      });
  },
});

export const {
  setCurrentNote,
  updateNoteContent,
  updateNoteTitle,
  addTag,
  removeTag,
  toggleMarkdown,
  togglePin,
  setNoteColor,
  setCursorPosition,
  setSearchQuery,
  setSearchResults,
  toggleSearchVisibility,
  toggleMarkdownPreview,
  toggleZenMode,
  toggleFullscreen,
  setError,
  clearError,
} = noteSlice.actions;

export default noteSlice.reducer;