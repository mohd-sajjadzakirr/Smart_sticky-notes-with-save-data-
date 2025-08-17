import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

const { ipcRenderer } = window.require('electron');

export interface Settings {
  theme: string;
  autoStart: boolean;
  globalHotkey: string;
  defaultSize: { width: number; height: number };
  alwaysOnTop: boolean;
  showInTaskbar: boolean;
  autoSave: boolean;
  autoSaveInterval: number;
  maxInstances: number;
  enableMarkdown: boolean;
  enableSearch: boolean;
  enableTags: boolean;
  enableSync: boolean;
  syncProvider: string;
  enableAnalytics: boolean;
  enableSpellCheck: boolean;
  enableAutoComplete: boolean;
  enableVimMode: boolean;
  fontSize: number;
  fontFamily: string;
  lineHeight: number;
  tabSize: number;
  wordWrap: boolean;
  showLineNumbers: boolean;
  enableMinimap: boolean;
  enableZenMode: boolean;
  opacity: number;
  blurBackground: boolean;
  enableSounds: boolean;
  enableNotifications: boolean;
  backupInterval: number;
  maxBackups: number;
  exportFormat: string;
  enableEncryption: boolean;
  enableCollaboration: boolean;
  enablePlugins: boolean;
  customCSS: string;
  shortcuts: {
    [key: string]: string;
  };
}

interface SettingsState {
  settings: Settings | null;
  isLoading: boolean;
  isSaving: boolean;
  error: string | null;
}

const initialState: SettingsState = {
  settings: null,
  isLoading: false,
  isSaving: false,
  error: null,
};

// Async thunks
export const loadSettings = createAsyncThunk(
  'settings/loadSettings',
  async () => {
    const response = await ipcRenderer.invoke('get-settings');
    return response;
  }
);

export const saveSettings = createAsyncThunk(
  'settings/saveSettings',
  async (settings: Partial<Settings>) => {
    const response = await ipcRenderer.invoke('save-settings', settings);
    return settings;
  }
);

const settingsSlice = createSlice({
  name: 'settings',
  initialState,
  reducers: {
    updateSetting: (state, action: PayloadAction<{ key: string; value: any }>) => {
      if (state.settings) {
        (state.settings as any)[action.payload.key] = action.payload.value;
      }
    },
    updateShortcut: (state, action: PayloadAction<{ action: string; shortcut: string }>) => {
      if (state.settings) {
        state.settings.shortcuts[action.payload.action] = action.payload.shortcut;
      }
    },
    resetSettings: (state) => {
      // Reset to default settings
      state.settings = null;
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
      // Load settings
      .addCase(loadSettings.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(loadSettings.fulfilled, (state, action) => {
        state.isLoading = false;
        state.settings = action.payload;
      })
      .addCase(loadSettings.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to load settings';
      })
      // Save settings
      .addCase(saveSettings.pending, (state) => {
        state.isSaving = true;
        state.error = null;
      })
      .addCase(saveSettings.fulfilled, (state, action) => {
        state.isSaving = false;
        if (state.settings) {
          state.settings = { ...state.settings, ...action.payload };
        }
      })
      .addCase(saveSettings.rejected, (state, action) => {
        state.isSaving = false;
        state.error = action.error.message || 'Failed to save settings';
      });
  },
});

export const {
  updateSetting,
  updateShortcut,
  resetSettings,
  setError,
  clearError,
} = settingsSlice.actions;

export default settingsSlice.reducer;