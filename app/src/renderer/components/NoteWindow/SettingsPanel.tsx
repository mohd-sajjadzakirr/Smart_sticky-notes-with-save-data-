import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Paper,
  Typography,
  IconButton,
  Tabs,
  Tab,
  Switch,
  Slider,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  TextField,
  Button,
  Divider,
} from '@mui/material';
import {
  Close as CloseIcon,
  Palette as PaletteIcon,
  TextFields as TextIcon,
  Settings as SettingsIcon,
  Keyboard as KeyboardIcon,
} from '@mui/icons-material';
import { RootState, AppDispatch } from '../../store/store';
import { updateSetting, saveSettings } from '../../store/slices/settingsSlice';
import { setActiveTab } from '../../store/slices/uiSlice';

interface SettingsPanelProps {
  onClose: () => void;
}

const SettingsPanel: React.FC<SettingsPanelProps> = ({ onClose }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { settings } = useSelector((state: RootState) => state.settings);
  const { activeTab } = useSelector((state: RootState) => state.ui);

  const handleTabChange = (event: React.SyntheticEvent, newValue: string) => {
    dispatch(setActiveTab(newValue));
  };

  const handleSettingChange = (key: string, value: any) => {
    dispatch(updateSetting({ key, value }));
  };

  const handleSave = () => {
    if (settings) {
      dispatch(saveSettings(settings));
    }
    onClose();
  };

  if (!settings) return null;

  return (
    <Paper
      elevation={8}
      sx={{
        position: 'fixed',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: '500px',
        height: '600px',
        zIndex: 9999,
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Header */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '16px',
          borderBottom: '1px solid',
          borderColor: 'divider',
        }}
      >
        <Typography variant="h6">Note Settings</Typography>
        <IconButton onClick={onClose}>
          <CloseIcon />
        </IconButton>
      </Box>

      {/* Tabs */}
      <Tabs
        value={activeTab}
        onChange={handleTabChange}
        sx={{ borderBottom: '1px solid', borderColor: 'divider' }}
      >
        <Tab label="General" value="general" icon={<SettingsIcon />} />
        <Tab label="Appearance" value="appearance" icon={<PaletteIcon />} />
        <Tab label="Editor" value="editor" icon={<TextIcon />} />
        <Tab label="Shortcuts" value="shortcuts" icon={<KeyboardIcon />} />
      </Tabs>

      {/* Content */}
      <Box sx={{ flex: 1, overflow: 'auto', padding: '16px' }}>
        {activeTab === 'general' && (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Auto-save
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Switch
                  checked={settings.autoSave}
                  onChange={(e) => handleSettingChange('autoSave', e.target.checked)}
                />
                <Typography variant="body2">
                  Automatically save changes
                </Typography>
              </Box>
              {settings.autoSave && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="body2" gutterBottom>
                    Auto-save interval: {settings.autoSaveInterval / 1000}s
                  </Typography>
                  <Slider
                    value={settings.autoSaveInterval}
                    onChange={(e, value) => handleSettingChange('autoSaveInterval', value)}
                    min={1000}
                    max={30000}
                    step={1000}
                    marks={[
                      { value: 1000, label: '1s' },
                      { value: 5000, label: '5s' },
                      { value: 10000, label: '10s' },
                      { value: 30000, label: '30s' },
                    ]}
                  />
                </Box>
              )}
            </Box>

            <Divider />

            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Window Behavior
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Switch
                    checked={settings.alwaysOnTop}
                    onChange={(e) => handleSettingChange('alwaysOnTop', e.target.checked)}
                  />
                  <Typography variant="body2">Always on top</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Switch
                    checked={settings.showInTaskbar}
                    onChange={(e) => handleSettingChange('showInTaskbar', e.target.checked)}
                  />
                  <Typography variant="body2">Show in taskbar</Typography>
                </Box>
              </Box>
            </Box>

            <Divider />

            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Features
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Switch
                    checked={settings.enableMarkdown}
                    onChange={(e) => handleSettingChange('enableMarkdown', e.target.checked)}
                  />
                  <Typography variant="body2">Enable Markdown</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Switch
                    checked={settings.enableSpellCheck}
                    onChange={(e) => handleSettingChange('enableSpellCheck', e.target.checked)}
                  />
                  <Typography variant="body2">Spell check</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Switch
                    checked={settings.enableAutoComplete}
                    onChange={(e) => handleSettingChange('enableAutoComplete', e.target.checked)}
                  />
                  <Typography variant="body2">Auto-complete</Typography>
                </Box>
              </Box>
            </Box>
          </Box>
        )}

        {activeTab === 'appearance' && (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Theme
              </Typography>
              <FormControl fullWidth size="small">
                <Select
                  value={settings.theme}
                  onChange={(e) => handleSettingChange('theme', e.target.value)}
                >
                  <MenuItem value="dark">Dark</MenuItem>
                  <MenuItem value="light">Light</MenuItem>
                  <MenuItem value="blue">Blue</MenuItem>
                  <MenuItem value="green">Green</MenuItem>
                </Select>
              </FormControl>
            </Box>

            <Divider />

            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Opacity: {Math.round(settings.opacity * 100)}%
              </Typography>
              <Slider
                value={settings.opacity}
                onChange={(e, value) => handleSettingChange('opacity', value)}
                min={0.3}
                max={1}
                step={0.1}
                marks={[
                  { value: 0.3, label: '30%' },
                  { value: 0.5, label: '50%' },
                  { value: 0.8, label: '80%' },
                  { value: 1, label: '100%' },
                ]}
              />
            </Box>

            <Divider />

            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Effects
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Switch
                    checked={settings.blurBackground}
                    onChange={(e) => handleSettingChange('blurBackground', e.target.checked)}
                  />
                  <Typography variant="body2">Blur background</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Switch
                    checked={settings.enableSounds}
                    onChange={(e) => handleSettingChange('enableSounds', e.target.checked)}
                  />
                  <Typography variant="body2">Sound effects</Typography>
                </Box>
              </Box>
            </Box>
          </Box>
        )}

        {activeTab === 'editor' && (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Font Settings
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <FormControl fullWidth size="small">
                  <InputLabel>Font Family</InputLabel>
                  <Select
                    value={settings.fontFamily}
                    onChange={(e) => handleSettingChange('fontFamily', e.target.value)}
                    label="Font Family"
                  >
                    <MenuItem value="system">System Default</MenuItem>
                    <MenuItem value="monospace">Monospace</MenuItem>
                    <MenuItem value="serif">Serif</MenuItem>
                    <MenuItem value="sans-serif">Sans Serif</MenuItem>
                  </Select>
                </FormControl>

                <Box>
                  <Typography variant="body2" gutterBottom>
                    Font Size: {settings.fontSize}px
                  </Typography>
                  <Slider
                    value={settings.fontSize}
                    onChange={(e, value) => handleSettingChange('fontSize', value)}
                    min={10}
                    max={24}
                    step={1}
                    marks={[
                      { value: 10, label: '10px' },
                      { value: 14, label: '14px' },
                      { value: 18, label: '18px' },
                      { value: 24, label: '24px' },
                    ]}
                  />
                </Box>

                <Box>
                  <Typography variant="body2" gutterBottom>
                    Line Height: {settings.lineHeight}
                  </Typography>
                  <Slider
                    value={settings.lineHeight}
                    onChange={(e, value) => handleSettingChange('lineHeight', value)}
                    min={1.2}
                    max={2.0}
                    step={0.1}
                    marks={[
                      { value: 1.2, label: '1.2' },
                      { value: 1.5, label: '1.5' },
                      { value: 1.8, label: '1.8' },
                      { value: 2.0, label: '2.0' },
                    ]}
                  />
                </Box>
              </Box>
            </Box>

            <Divider />

            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Editor Options
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Switch
                    checked={settings.wordWrap}
                    onChange={(e) => handleSettingChange('wordWrap', e.target.checked)}
                  />
                  <Typography variant="body2">Word wrap</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Switch
                    checked={settings.showLineNumbers}
                    onChange={(e) => handleSettingChange('showLineNumbers', e.target.checked)}
                  />
                  <Typography variant="body2">Show line numbers</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Switch
                    checked={settings.enableVimMode}
                    onChange={(e) => handleSettingChange('enableVimMode', e.target.checked)}
                  />
                  <Typography variant="body2">Vim mode</Typography>
                </Box>
              </Box>
            </Box>

            <Divider />

            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Tab Size: {settings.tabSize} spaces
              </Typography>
              <Slider
                value={settings.tabSize}
                onChange={(e, value) => handleSettingChange('tabSize', value)}
                min={2}
                max={8}
                step={1}
                marks={[
                  { value: 2, label: '2' },
                  { value: 4, label: '4' },
                  { value: 6, label: '6' },
                  { value: 8, label: '8' },
                ]}
              />
            </Box>
          </Box>
        )}

        {activeTab === 'shortcuts' && (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              Keyboard Shortcuts
            </Typography>
            {Object.entries(settings.shortcuts).map(([action, shortcut]) => (
              <Box key={action} sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Typography variant="body2" sx={{ minWidth: '120px' }}>
                  {action.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}:
                </Typography>
                <TextField
                  value={shortcut}
                  onChange={(e) => handleSettingChange(`shortcuts.${action}`, e.target.value)}
                  size="small"
                  sx={{ flex: 1 }}
                />
              </Box>
            ))}
          </Box>
        )}
      </Box>

      {/* Footer */}
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'flex-end',
          gap: 2,
          padding: '16px',
          borderTop: '1px solid',
          borderColor: 'divider',
        }}
      >
        <Button onClick={onClose}>Cancel</Button>
        <Button variant="contained" onClick={handleSave}>
          Save Changes
        </Button>
      </Box>
    </Paper>
  );
};

export default SettingsPanel;