import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UIState {
  isDragging: boolean;
  isResizing: boolean;
  dragOffset: { x: number; y: number };
  windowBounds: { x: number; y: number; width: number; height: number };
  isContextMenuOpen: boolean;
  contextMenuPosition: { x: number; y: number };
  selectedText: string;
  isSettingsPanelOpen: boolean;
  activeTab: string;
  notifications: Array<{
    id: string;
    type: 'success' | 'error' | 'warning' | 'info';
    message: string;
    timestamp: number;
    duration?: number;
  }>;
  isOnline: boolean;
  lastSync: string | null;
  syncStatus: 'idle' | 'syncing' | 'error';
}

const initialState: UIState = {
  isDragging: false,
  isResizing: false,
  dragOffset: { x: 0, y: 0 },
  windowBounds: { x: 0, y: 0, width: 400, height: 500 },
  isContextMenuOpen: false,
  contextMenuPosition: { x: 0, y: 0 },
  selectedText: '',
  isSettingsPanelOpen: false,
  activeTab: 'general',
  notifications: [],
  isOnline: navigator.onLine,
  lastSync: null,
  syncStatus: 'idle',
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    setDragging: (state, action: PayloadAction<boolean>) => {
      state.isDragging = action.payload;
    },
    setResizing: (state, action: PayloadAction<boolean>) => {
      state.isResizing = action.payload;
    },
    setDragOffset: (state, action: PayloadAction<{ x: number; y: number }>) => {
      state.dragOffset = action.payload;
    },
    setWindowBounds: (state, action: PayloadAction<{ x: number; y: number; width: number; height: number }>) => {
      state.windowBounds = action.payload;
    },
    openContextMenu: (state, action: PayloadAction<{ x: number; y: number }>) => {
      state.isContextMenuOpen = true;
      state.contextMenuPosition = action.payload;
    },
    closeContextMenu: (state) => {
      state.isContextMenuOpen = false;
    },
    setSelectedText: (state, action: PayloadAction<string>) => {
      state.selectedText = action.payload;
    },
    toggleSettingsPanel: (state) => {
      state.isSettingsPanelOpen = !state.isSettingsPanelOpen;
    },
    setActiveTab: (state, action: PayloadAction<string>) => {
      state.activeTab = action.payload;
    },
    addNotification: (state, action: PayloadAction<{
      type: 'success' | 'error' | 'warning' | 'info';
      message: string;
      duration?: number;
    }>) => {
      const notification = {
        id: Date.now().toString(),
        timestamp: Date.now(),
        ...action.payload,
      };
      state.notifications.push(notification);
    },
    removeNotification: (state, action: PayloadAction<string>) => {
      state.notifications = state.notifications.filter(n => n.id !== action.payload);
    },
    clearNotifications: (state) => {
      state.notifications = [];
    },
    setOnlineStatus: (state, action: PayloadAction<boolean>) => {
      state.isOnline = action.payload;
    },
    setLastSync: (state, action: PayloadAction<string>) => {
      state.lastSync = action.payload;
    },
    setSyncStatus: (state, action: PayloadAction<'idle' | 'syncing' | 'error'>) => {
      state.syncStatus = action.payload;
    },
  },
});

export const {
  setDragging,
  setResizing,
  setDragOffset,
  setWindowBounds,
  openContextMenu,
  closeContextMenu,
  setSelectedText,
  toggleSettingsPanel,
  setActiveTab,
  addNotification,
  removeNotification,
  clearNotifications,
  setOnlineStatus,
  setLastSync,
  setSyncStatus,
} = uiSlice.actions;

export default uiSlice.reducer;