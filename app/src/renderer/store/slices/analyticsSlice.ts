import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

const { ipcRenderer } = window.require('electron');

export interface Analytics {
  totalNotes: number;
  totalWords: number;
  totalCharacters: number;
  sessionsCount: number;
  totalTimeSpent: number;
  lastSession: string | null;
  createdToday: number;
  modifiedToday: number;
  averageNoteLength: number;
  mostUsedTags: string[];
  dailyStats: {
    [date: string]: {
      notesCreated: number;
      notesModified: number;
      wordsWritten: number;
      timeSpent: number;
    };
  };
  weeklyStats: {
    [week: string]: {
      notesCreated: number;
      notesModified: number;
      wordsWritten: number;
      timeSpent: number;
    };
  };
  monthlyStats: {
    [month: string]: {
      notesCreated: number;
      notesModified: number;
      wordsWritten: number;
      timeSpent: number;
    };
  };
}

interface AnalyticsState {
  analytics: Analytics | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: AnalyticsState = {
  analytics: null,
  isLoading: false,
  error: null,
};

// Async thunks
export const loadAnalytics = createAsyncThunk(
  'analytics/loadAnalytics',
  async () => {
    const response = await ipcRenderer.invoke('get-analytics');
    return response;
  }
);

export const updateAnalytics = createAsyncThunk(
  'analytics/updateAnalytics',
  async ({ eventType, data }: { eventType: string; data?: any }) => {
    const response = await ipcRenderer.invoke('update-analytics', eventType, data);
    return { eventType, data };
  }
);

const analyticsSlice = createSlice({
  name: 'analytics',
  initialState,
  reducers: {
    incrementWordCount: (state, action: PayloadAction<number>) => {
      if (state.analytics) {
        state.analytics.totalWords += action.payload;
        
        const today = new Date().toISOString().split('T')[0];
        if (!state.analytics.dailyStats[today]) {
          state.analytics.dailyStats[today] = {
            notesCreated: 0,
            notesModified: 0,
            wordsWritten: 0,
            timeSpent: 0,
          };
        }
        state.analytics.dailyStats[today].wordsWritten += action.payload;
      }
    },
    incrementCharacterCount: (state, action: PayloadAction<number>) => {
      if (state.analytics) {
        state.analytics.totalCharacters += action.payload;
      }
    },
    addUsedTag: (state, action: PayloadAction<string>) => {
      if (state.analytics) {
        const existingTag = state.analytics.mostUsedTags.find(tag => tag === action.payload);
        if (!existingTag) {
          state.analytics.mostUsedTags.push(action.payload);
        }
      }
    },
    updateSessionTime: (state, action: PayloadAction<number>) => {
      if (state.analytics) {
        state.analytics.totalTimeSpent += action.payload;
        
        const today = new Date().toISOString().split('T')[0];
        if (!state.analytics.dailyStats[today]) {
          state.analytics.dailyStats[today] = {
            notesCreated: 0,
            notesModified: 0,
            wordsWritten: 0,
            timeSpent: 0,
          };
        }
        state.analytics.dailyStats[today].timeSpent += action.payload;
      }
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
      // Load analytics
      .addCase(loadAnalytics.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(loadAnalytics.fulfilled, (state, action) => {
        state.isLoading = false;
        state.analytics = action.payload;
      })
      .addCase(loadAnalytics.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to load analytics';
      })
      // Update analytics
      .addCase(updateAnalytics.fulfilled, (state, action) => {
        // Handle specific analytics updates
        const { eventType, data } = action.payload;
        
        if (state.analytics) {
          switch (eventType) {
            case 'noteCreated':
              state.analytics.totalNotes++;
              state.analytics.createdToday++;
              break;
            case 'noteModified':
              state.analytics.modifiedToday++;
              break;
            case 'wordsAdded':
              state.analytics.totalWords += data;
              break;
            case 'charactersAdded':
              state.analytics.totalCharacters += data;
              break;
          }
        }
      });
  },
});

export const {
  incrementWordCount,
  incrementCharacterCount,
  addUsedTag,
  updateSessionTime,
  setError,
  clearError,
} = analyticsSlice.actions;

export default analyticsSlice.reducer;