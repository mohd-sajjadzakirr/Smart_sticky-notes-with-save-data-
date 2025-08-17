const { app, BrowserWindow, ipcMain, Menu, Tray, dialog, globalShortcut, screen, shell, nativeTheme } = require('electron');
const { autoUpdater } = require('electron-updater');
const path = require('path');
const Store = require('electron-store');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs').promises;

// Initialize secure store
const store = new Store({
  encryptionKey: 'smart-notes-pro-encryption-key',
  schema: {
    settings: {
      type: 'object',
      default: {}
    },
    instances: {
      type: 'object',
      default: {}
    },
    analytics: {
      type: 'object',
      default: {}
    }
  }
});

class SmartNotesProApp {
  constructor() {
    this.windows = new Map();
    this.managerWindow = null;
    this.settingsWindow = null;
    this.tray = null;
    this.isQuitting = false;
    this.settings = this.getSettings();
    this.analytics = this.getAnalytics();
    
    this.setupApp();
  }

  getSettings() {
    return store.get('settings', {
      theme: 'dark',
      autoStart: false,
      globalHotkey: 'CommandOrControl+Shift+N',
      defaultSize: { width: 400, height: 500 },
      alwaysOnTop: true,
      showInTaskbar: false,
      autoSave: true,
      autoSaveInterval: 3000,
      maxInstances: 50,
      enableMarkdown: true,
      enableSearch: true,
      enableTags: true,
      enableSync: false,
      syncProvider: 'local',
      enableAnalytics: true,
      enableSpellCheck: true,
      enableAutoComplete: true,
      enableVimMode: false,
      fontSize: 14,
      fontFamily: 'system',
      lineHeight: 1.5,
      tabSize: 2,
      wordWrap: true,
      showLineNumbers: false,
      enableMinimap: false,
      enableZenMode: false,
      opacity: 0.95,
      blurBackground: true,
      enableSounds: true,
      enableNotifications: true,
      backupInterval: 300000, // 5 minutes
      maxBackups: 10,
      exportFormat: 'markdown',
      enableEncryption: false,
      enableCollaboration: false,
      enablePlugins: true,
      customCSS: '',
      shortcuts: {
        newNote: 'CommandOrControl+N',
        saveNote: 'CommandOrControl+S',
        findInNote: 'CommandOrControl+F',
        replaceInNote: 'CommandOrControl+H',
        toggleMarkdown: 'CommandOrControl+M',
        toggleZenMode: 'F11',
        increaseFontSize: 'CommandOrControl+Plus',
        decreaseFontSize: 'CommandOrControl+-',
        resetFontSize: 'CommandOrControl+0'
      }
    });
  }

  getAnalytics() {
    return store.get('analytics', {
      totalNotes: 0,
      totalWords: 0,
      totalCharacters: 0,
      sessionsCount: 0,
      totalTimeSpent: 0,
      lastSession: null,
      createdToday: 0,
      modifiedToday: 0,
      averageNoteLength: 0,
      mostUsedTags: [],
      dailyStats: {},
      weeklyStats: {},
      monthlyStats: {}
    });
  }

  setupApp() {
    // Configure auto updater
    autoUpdater.checkForUpdatesAndNotify();

    // Handle app ready
    app.whenReady().then(() => {
      this.createTray();
      this.setupGlobalShortcuts();
      this.setupMenu();
      this.setupAutoUpdater();
      this.restoreInstances();
      this.startAnalyticsSession();
      
      // Create manager window if no instances exist
      if (this.windows.size === 0) {
        this.createManagerWindow();
      }

      // Setup periodic backups
      this.setupPeriodicBackups();
    });

    // Handle app activation (macOS)
    app.on('activate', () => {
      if (this.windows.size === 0) {
        this.createManagerWindow();
      }
    });

    // Handle before quit
    app.on('before-quit', () => {
      this.isQuitting = true;
      this.saveAllInstances();
      this.endAnalyticsSession();
      this.createBackup();
    });

    // Handle window all closed
    app.on('window-all-closed', () => {
      if (!this.isQuitting && process.platform !== 'darwin') {
        // Keep app running in system tray
      } else if (process.platform !== 'darwin') {
        app.quit();
      }
    });

    // Setup IPC handlers
    this.setupIPC();

    // Handle protocol for deep linking
    app.setAsDefaultProtocolClient('smartnotes');
  }

  createTray() {
    const iconPath = this.getAssetPath('tray-icon.png');
    this.tray = new Tray(iconPath);
    
    const contextMenu = Menu.buildFromTemplate([
      {
        label: 'New Note',
        accelerator: 'CommandOrControl+N',
        click: () => this.createNoteWindow()
      },
      {
        label: 'Quick Note',
        accelerator: 'CommandOrControl+Shift+Q',
        click: () => this.createQuickNote()
      },
      { type: 'separator' },
      {
        label: 'Manager',
        accelerator: 'CommandOrControl+M',
        click: () => this.createManagerWindow()
      },
      {
        label: 'Settings',
        accelerator: 'CommandOrControl+,',
        click: () => this.createSettingsWindow()
      },
      { type: 'separator' },
      {
        label: 'Import Notes',
        click: () => this.importNotes()
      },
      {
        label: 'Export All Notes',
        click: () => this.exportAllNotes()
      },
      { type: 'separator' },
      {
        label: 'Analytics',
        click: () => this.showAnalytics()
      },
      { type: 'separator' },
      {
        label: 'Check for Updates',
        click: () => autoUpdater.checkForUpdatesAndNotify()
      },
      {
        label: 'About',
        click: () => this.showAbout()
      },
      { type: 'separator' },
      {
        label: 'Quit Smart Notes Pro',
        accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
        click: () => {
          this.isQuitting = true;
          app.quit();
        }
      }
    ]);

    this.tray.setContextMenu(contextMenu);
    this.tray.setToolTip('Smart Notes Pro - Advanced Sticky Notes');
    
    this.tray.on('double-click', () => {
      this.createNoteWindow();
    });

    this.tray.on('right-click', () => {
      this.tray.popUpContextMenu();
    });
  }

  setupGlobalShortcuts() {
    // Clear existing shortcuts
    globalShortcut.unregisterAll();

    // Register shortcuts from settings
    Object.entries(this.settings.shortcuts).forEach(([action, shortcut]) => {
      if (shortcut) {
        globalShortcut.register(shortcut, () => {
          this.handleGlobalShortcut(action);
        });
      }
    });

    // Register main global shortcut
    if (this.settings.globalHotkey) {
      globalShortcut.register(this.settings.globalHotkey, () => {
        this.createNoteWindow();
      });
    }
  }

  handleGlobalShortcut(action) {
    switch (action) {
      case 'newNote':
        this.createNoteWindow();
        break;
      case 'saveNote':
        this.saveActiveNote();
        break;
      case 'findInNote':
        this.triggerFindInActiveNote();
        break;
      case 'replaceInNote':
        this.triggerReplaceInActiveNote();
        break;
      case 'toggleMarkdown':
        this.toggleMarkdownInActiveNote();
        break;
      case 'toggleZenMode':
        this.toggleZenModeInActiveNote();
        break;
      default:
        console.log(`Unknown global shortcut action: ${action}`);
    }
  }

  setupMenu() {
    const template = [
      {
        label: 'File',
        submenu: [
          {
            label: 'New Note',
            accelerator: 'CmdOrCtrl+N',
            click: () => this.createNoteWindow()
          },
          {
            label: 'Quick Note',
            accelerator: 'CmdOrCtrl+Shift+Q',
            click: () => this.createQuickNote()
          },
          { type: 'separator' },
          {
            label: 'Open Manager',
            accelerator: 'CmdOrCtrl+M',
            click: () => this.createManagerWindow()
          },
          { type: 'separator' },
          {
            label: 'Import Notes...',
            accelerator: 'CmdOrCtrl+I',
            click: () => this.importNotes()
          },
          {
            label: 'Export All Notes...',
            accelerator: 'CmdOrCtrl+E',
            click: () => this.exportAllNotes()
          },
          { type: 'separator' },
          {
            label: 'Settings',
            accelerator: 'CmdOrCtrl+,',
            click: () => this.createSettingsWindow()
          },
          { type: 'separator' },
          {
            label: 'Quit',
            accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
            click: () => {
              this.isQuitting = true;
              app.quit();
            }
          }
        ]
      },
      {
        label: 'Edit',
        submenu: [
          { role: 'undo' },
          { role: 'redo' },
          { type: 'separator' },
          { role: 'cut' },
          { role: 'copy' },
          { role: 'paste' },
          { role: 'selectall' },
          { type: 'separator' },
          {
            label: 'Find',
            accelerator: 'CmdOrCtrl+F',
            click: () => this.triggerFindInActiveNote()
          },
          {
            label: 'Replace',
            accelerator: 'CmdOrCtrl+H',
            click: () => this.triggerReplaceInActiveNote()
          }
        ]
      },
      {
        label: 'View',
        submenu: [
          { role: 'reload' },
          { role: 'forceReload' },
          { role: 'toggleDevTools' },
          { type: 'separator' },
          { role: 'resetZoom' },
          { role: 'zoomIn' },
          { role: 'zoomOut' },
          { type: 'separator' },
          { role: 'togglefullscreen' },
          { type: 'separator' },
          {
            label: 'Toggle Markdown Preview',
            accelerator: 'CmdOrCtrl+Shift+M',
            click: () => this.toggleMarkdownInActiveNote()
          },
          {
            label: 'Toggle Zen Mode',
            accelerator: 'F11',
            click: () => this.toggleZenModeInActiveNote()
          }
        ]
      },
      {
        label: 'Tools',
        submenu: [
          {
            label: 'Analytics Dashboard',
            click: () => this.showAnalytics()
          },
          {
            label: 'Backup Manager',
            click: () => this.showBackupManager()
          },
          { type: 'separator' },
          {
            label: 'Plugin Manager',
            click: () => this.showPluginManager()
          },
          { type: 'separator' },
          {
            label: 'Check for Updates',
            click: () => autoUpdater.checkForUpdatesAndNotify()
          }
        ]
      },
      {
        label: 'Help',
        submenu: [
          {
            label: 'Keyboard Shortcuts',
            click: () => this.showKeyboardShortcuts()
          },
          {
            label: 'User Guide',
            click: () => shell.openExternal('https://smartnotes.com/guide')
          },
          {
            label: 'Report Issue',
            click: () => shell.openExternal('https://github.com/smartnotes/smart-notes-pro/issues')
          },
          { type: 'separator' },
          {
            label: 'About Smart Notes Pro',
            click: () => this.showAbout()
          }
        ]
      }
    ];

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
  }

  setupAutoUpdater() {
    autoUpdater.on('checking-for-update', () => {
      console.log('Checking for update...');
    });

    autoUpdater.on('update-available', (info) => {
      console.log('Update available.');
      this.showUpdateNotification(info);
    });

    autoUpdater.on('update-not-available', (info) => {
      console.log('Update not available.');
    });

    autoUpdater.on('error', (err) => {
      console.log('Error in auto-updater. ' + err);
    });

    autoUpdater.on('download-progress', (progressObj) => {
      let log_message = "Download speed: " + progressObj.bytesPerSecond;
      log_message = log_message + ' - Downloaded ' + progressObj.percent + '%';
      log_message = log_message + ' (' + progressObj.transferred + "/" + progressObj.total + ')';
      console.log(log_message);
    });

    autoUpdater.on('update-downloaded', (info) => {
      console.log('Update downloaded');
      this.showUpdateReadyNotification(info);
    });
  }

  createNoteWindow(instanceId = null, options = {}) {
    const id = instanceId || uuidv4();
    
    if (this.windows.has(id)) {
      const existingWindow = this.windows.get(id);
      existingWindow.show();
      existingWindow.focus();
      return existingWindow;
    }

    const savedData = store.get(`instances.${id}`, {});
    const bounds = savedData.bounds || {
      width: this.settings.defaultSize.width,
      height: this.settings.defaultSize.height,
      x: undefined,
      y: undefined
    };

    // Smart positioning for new windows
    if (!bounds.x || !bounds.y) {
      const displays = screen.getAllDisplays();
      const primaryDisplay = screen.getPrimaryDisplay();
      const { width: screenWidth, height: screenHeight } = primaryDisplay.workAreaSize;
      
      // Cascade new windows
      const existingWindows = Array.from(this.windows.values());
      const offset = existingWindows.length * 30;
      
      bounds.x = Math.min(100 + offset, screenWidth - bounds.width - 100);
      bounds.y = Math.min(100 + offset, screenHeight - bounds.height - 100);
    }

    const window = new BrowserWindow({
      width: bounds.width,
      height: bounds.height,
      x: bounds.x,
      y: bounds.y,
      minWidth: 300,
      minHeight: 400,
      frame: false,
      alwaysOnTop: this.settings.alwaysOnTop,
      skipTaskbar: !this.settings.showInTaskbar,
      webPreferences: {
        nodeIntegration: true,
        contextIsolation: false,
        enableRemoteModule: true,
        webSecurity: false,
        allowRunningInsecureContent: true
      },
      show: false,
      transparent: true,
      hasShadow: true,
      titleBarStyle: 'hidden',
      vibrancy: this.settings.blurBackground ? 'under-window' : null,
      opacity: this.settings.opacity,
      icon: this.getAssetPath('icon.png'),
      ...options
    });

    // Load the appropriate HTML file
    const isDev = process.env.NODE_ENV === 'development';
    if (isDev) {
      window.loadURL('http://localhost:3000/index.html');
    } else {
      window.loadFile(path.join(__dirname, '../../build/index.html'));
    }
    
    window.once('ready-to-show', () => {
      window.show();
      window.webContents.send('initialize', {
        instanceId: id,
        data: savedData,
        settings: this.settings,
        analytics: this.analytics
      });
    });

    // Handle window events
    window.on('close', (event) => {
      if (!this.isQuitting) {
        event.preventDefault();
        window.hide();
      } else {
        this.saveInstance(id);
        this.windows.delete(id);
      }
    });

    window.on('moved', () => this.saveInstanceBounds(id));
    window.on('resized', () => this.saveInstanceBounds(id));
    window.on('focus', () => this.updateAnalytics('windowFocused', id));
    window.on('blur', () => this.updateAnalytics('windowBlurred', id));

    // Handle external links
    window.webContents.setWindowOpenHandler(({ url }) => {
      shell.openExternal(url);
      return { action: 'deny' };
    });

    this.windows.set(id, window);
    this.updateAnalytics('noteCreated', id);
    
    return window;
  }

  createQuickNote() {
    const quickNoteId = 'quick-note-' + Date.now();
    const window = this.createNoteWindow(quickNoteId, {
      width: 300,
      height: 200,
      alwaysOnTop: true,
      skipTaskbar: true,
      resizable: false,
      minimizable: false,
      maximizable: false
    });

    // Auto-save and close after inactivity
    setTimeout(() => {
      if (this.windows.has(quickNoteId)) {
        this.saveInstance(quickNoteId);
        window.close();
      }
    }, 300000); // 5 minutes

    return window;
  }

  createManagerWindow() {
    if (this.managerWindow && !this.managerWindow.isDestroyed()) {
      this.managerWindow.show();
      this.managerWindow.focus();
      return this.managerWindow;
    }

    this.managerWindow = new BrowserWindow({
      width: 1200,
      height: 800,
      minWidth: 900,
      minHeight: 600,
      webPreferences: {
        nodeIntegration: true,
        contextIsolation: false,
        webSecurity: false
      },
      show: false,
      icon: this.getAssetPath('icon.png'),
      titleBarStyle: 'hiddenInset',
      vibrancy: 'under-window'
    });

    const isDev = process.env.NODE_ENV === 'development';
    if (isDev) {
      this.managerWindow.loadURL('http://localhost:3000/manager.html');
    } else {
      this.managerWindow.loadFile(path.join(__dirname, '../../build/manager.html'));
    }
    
    this.managerWindow.once('ready-to-show', () => {
      this.managerWindow.show();
    });

    this.managerWindow.on('closed', () => {
      this.managerWindow = null;
    });

    return this.managerWindow;
  }

  createSettingsWindow() {
    if (this.settingsWindow && !this.settingsWindow.isDestroyed()) {
      this.settingsWindow.show();
      this.settingsWindow.focus();
      return this.settingsWindow;
    }

    this.settingsWindow = new BrowserWindow({
      width: 800,
      height: 700,
      minWidth: 700,
      minHeight: 600,
      resizable: true,
      webPreferences: {
        nodeIntegration: true,
        contextIsolation: false,
        webSecurity: false
      },
      show: false,
      parent: this.managerWindow,
      modal: false,
      icon: this.getAssetPath('icon.png'),
      titleBarStyle: 'hiddenInset'
    });

    const isDev = process.env.NODE_ENV === 'development';
    if (isDev) {
      this.settingsWindow.loadURL('http://localhost:3000/settings.html');
    } else {
      this.settingsWindow.loadFile(path.join(__dirname, '../../build/settings.html'));
    }
    
    this.settingsWindow.once('ready-to-show', () => {
      this.settingsWindow.show();
    });

    this.settingsWindow.on('closed', () => {
      this.settingsWindow = null;
    });

    return this.settingsWindow;
  }

  getAssetPath(filename) {
    if (process.env.NODE_ENV === 'development') {
      return path.join(__dirname, '../../assets', filename);
    }
    return path.join(process.resourcesPath, 'assets', filename);
  }

  saveInstance(instanceId) {
    const window = this.windows.get(instanceId);
    if (window && !window.isDestroyed()) {
      window.webContents.send('save-request');
    }
  }

  saveInstanceBounds(instanceId) {
    const window = this.windows.get(instanceId);
    if (window && !window.isDestroyed()) {
      const bounds = window.getBounds();
      const currentData = store.get(`instances.${instanceId}`, {});
      store.set(`instances.${instanceId}`, {
        ...currentData,
        bounds: bounds,
        lastModified: new Date().toISOString()
      });
    }
  }

  saveAllInstances() {
    this.windows.forEach((window, instanceId) => {
      this.saveInstance(instanceId);
    });
  }

  restoreInstances() {
    const instances = store.get('instances', {});
    Object.keys(instances).forEach(instanceId => {
      const instanceData = instances[instanceId];
      if (instanceData.autoRestore !== false && !instanceData.isQuickNote) {
        setTimeout(() => {
          this.createNoteWindow(instanceId);
        }, 100 * Object.keys(instances).indexOf(instanceId)); // Stagger window creation
      }
    });
  }

  // Analytics methods
  startAnalyticsSession() {
    if (!this.settings.enableAnalytics) return;

    this.analytics.sessionsCount++;
    this.analytics.lastSession = new Date().toISOString();
    this.sessionStartTime = Date.now();
    
    store.set('analytics', this.analytics);
  }

  endAnalyticsSession() {
    if (!this.settings.enableAnalytics || !this.sessionStartTime) return;

    const sessionDuration = Date.now() - this.sessionStartTime;
    this.analytics.totalTimeSpent += sessionDuration;
    
    store.set('analytics', this.analytics);
  }

  updateAnalytics(event, data = null) {
    if (!this.settings.enableAnalytics) return;

    const today = new Date().toISOString().split('T')[0];
    
    if (!this.analytics.dailyStats[today]) {
      this.analytics.dailyStats[today] = {
        notesCreated: 0,
        notesModified: 0,
        wordsWritten: 0,
        timeSpent: 0
      };
    }

    switch (event) {
      case 'noteCreated':
        this.analytics.totalNotes++;
        this.analytics.createdToday++;
        this.analytics.dailyStats[today].notesCreated++;
        break;
      case 'noteModified':
        this.analytics.modifiedToday++;
        this.analytics.dailyStats[today].notesModified++;
        break;
      case 'wordsAdded':
        this.analytics.totalWords += data;
        this.analytics.dailyStats[today].wordsWritten += data;
        break;
      case 'charactersAdded':
        this.analytics.totalCharacters += data;
        break;
    }

    store.set('analytics', this.analytics);
  }

  // Backup methods
  setupPeriodicBackups() {
    if (!this.settings.backupInterval) return;

    setInterval(() => {
      this.createBackup();
    }, this.settings.backupInterval);
  }

  async createBackup() {
    try {
      const backupData = {
        timestamp: new Date().toISOString(),
        version: app.getVersion(),
        instances: store.get('instances', {}),
        settings: this.settings,
        analytics: this.analytics
      };

      const backupsDir = path.join(app.getPath('userData'), 'backups');
      await fs.mkdir(backupsDir, { recursive: true });

      const backupFile = path.join(backupsDir, `backup-${Date.now()}.json`);
      await fs.writeFile(backupFile, JSON.stringify(backupData, null, 2));

      // Clean old backups
      await this.cleanOldBackups(backupsDir);

      console.log('Backup created:', backupFile);
    } catch (error) {
      console.error('Failed to create backup:', error);
    }
  }

  async cleanOldBackups(backupsDir) {
    try {
      const files = await fs.readdir(backupsDir);
      const backupFiles = files
        .filter(file => file.startsWith('backup-') && file.endsWith('.json'))
        .map(file => ({
          name: file,
          path: path.join(backupsDir, file),
          timestamp: parseInt(file.replace('backup-', '').replace('.json', ''))
        }))
        .sort((a, b) => b.timestamp - a.timestamp);

      // Keep only the latest backups
      const filesToDelete = backupFiles.slice(this.settings.maxBackups);
      
      for (const file of filesToDelete) {
        await fs.unlink(file.path);
      }
    } catch (error) {
      console.error('Failed to clean old backups:', error);
    }
  }

  // Import/Export methods
  async importNotes() {
    const result = await dialog.showOpenDialog({
      title: 'Import Notes',
      filters: [
        { name: 'JSON Files', extensions: ['json'] },
        { name: 'Markdown Files', extensions: ['md', 'markdown'] },
        { name: 'Text Files', extensions: ['txt'] },
        { name: 'All Files', extensions: ['*'] }
      ],
      properties: ['openFile', 'multiSelections']
    });

    if (result.canceled) return { success: false };

    try {
      let importedCount = 0;
      
      for (const filePath of result.filePaths) {
        const content = await fs.readFile(filePath, 'utf8');
        const ext = path.extname(filePath).toLowerCase();
        
        if (ext === '.json') {
          const data = JSON.parse(content);
          if (data.instances) {
            // Import from backup
            Object.entries(data.instances).forEach(([id, instanceData]) => {
              store.set(`instances.${id}`, instanceData);
              importedCount++;
            });
          } else {
            // Import single note
            const instanceId = uuidv4();
            store.set(`instances.${instanceId}`, {
              id: instanceId,
              title: path.basename(filePath, ext),
              content: content,
              created: new Date().toISOString(),
              lastModified: new Date().toISOString(),
              tags: [],
              isMarkdown: true
            });
            importedCount++;
          }
        } else {
          // Import as text/markdown
          const instanceId = uuidv4();
          store.set(`instances.${instanceId}`, {
            id: instanceId,
            title: path.basename(filePath, ext),
            content: content,
            created: new Date().toISOString(),
            lastModified: new Date().toISOString(),
            tags: [],
            isMarkdown: ext === '.md' || ext === '.markdown'
          });
          importedCount++;
        }
      }

      return { success: true, count: importedCount };
    } catch (error) {
      console.error('Import failed:', error);
      return { success: false, error: error.message };
    }
  }

  async exportAllNotes() {
    const result = await dialog.showSaveDialog({
      title: 'Export All Notes',
      defaultPath: `smart-notes-export-${new Date().toISOString().split('T')[0]}.json`,
      filters: [
        { name: 'JSON Files', extensions: ['json'] },
        { name: 'ZIP Archive', extensions: ['zip'] }
      ]
    });

    if (result.canceled) return { success: false };

    try {
      const instances = store.get('instances', {});
      const exportData = {
        exportDate: new Date().toISOString(),
        version: app.getVersion(),
        totalNotes: Object.keys(instances).length,
        instances: instances
      };

      await fs.writeFile(result.filePath, JSON.stringify(exportData, null, 2));
      return { success: true, path: result.filePath, count: Object.keys(instances).length };
    } catch (error) {
      console.error('Export failed:', error);
      return { success: false, error: error.message };
    }
  }

  // Utility methods for active window operations
  getActiveNoteWindow() {
    const focusedWindow = BrowserWindow.getFocusedWindow();
    if (focusedWindow && this.windows.has(focusedWindow.id)) {
      return focusedWindow;
    }
    return null;
  }

  saveActiveNote() {
    const activeWindow = this.getActiveNoteWindow();
    if (activeWindow) {
      activeWindow.webContents.send('save-request');
    }
  }

  triggerFindInActiveNote() {
    const activeWindow = this.getActiveNoteWindow();
    if (activeWindow) {
      activeWindow.webContents.send('trigger-find');
    }
  }

  triggerReplaceInActiveNote() {
    const activeWindow = this.getActiveNoteWindow();
    if (activeWindow) {
      activeWindow.webContents.send('trigger-replace');
    }
  }

  toggleMarkdownInActiveNote() {
    const activeWindow = this.getActiveNoteWindow();
    if (activeWindow) {
      activeWindow.webContents.send('toggle-markdown');
    }
  }

  toggleZenModeInActiveNote() {
    const activeWindow = this.getActiveNoteWindow();
    if (activeWindow) {
      activeWindow.webContents.send('toggle-zen-mode');
    }
  }

  // Notification methods
  showUpdateNotification(info) {
    // Implementation for update notification
  }

  showUpdateReadyNotification(info) {
    // Implementation for update ready notification
  }

  showAnalytics() {
    // Implementation for analytics dashboard
  }

  showBackupManager() {
    // Implementation for backup manager
  }

  showPluginManager() {
    // Implementation for plugin manager
  }

  showKeyboardShortcuts() {
    // Implementation for keyboard shortcuts help
  }

  showAbout() {
    dialog.showMessageBox({
      type: 'info',
      title: 'About Smart Notes Pro',
      message: 'Smart Notes Pro',
      detail: `Version: ${app.getVersion()}\nA powerful, feature-rich sticky notes application.\n\nDeveloped with ❤️ by Smart Notes Team`,
      buttons: ['OK']
    });
  }

  setupIPC() {
    // Note operations
    ipcMain.handle('save-note', async (event, instanceId, data) => {
      const currentData = store.get(`instances.${instanceId}`, {});
      const updatedData = {
        ...currentData,
        ...data,
        lastModified: new Date().toISOString()
      };
      
      store.set(`instances.${instanceId}`, updatedData);
      this.updateAnalytics('noteModified', instanceId);
      
      return { success: true };
    });

    ipcMain.handle('load-note', async (event, instanceId) => {
      return store.get(`instances.${instanceId}`, {});
    });

    ipcMain.handle('delete-note', async (event, instanceId) => {
      store.delete(`instances.${instanceId}`);
      const window = this.windows.get(instanceId);
      if (window && !window.isDestroyed()) {
        window.close();
        this.windows.delete(instanceId);
      }
      return { success: true };
    });

    // Manager operations
    ipcMain.handle('get-all-instances', async () => {
      const instances = store.get('instances', {});
      return Object.keys(instances).map(id => ({
        id,
        ...instances[id]
      }));
    });

    ipcMain.handle('create-new-note', async () => {
      const window = this.createNoteWindow();
      return { success: true, instanceId: window.id };
    });

    ipcMain.handle('show-note', async (event, instanceId) => {
      const window = this.windows.get(instanceId);
      if (window && !window.isDestroyed()) {
        window.show();
        window.focus();
      } else {
        this.createNoteWindow(instanceId);
      }
      return { success: true };
    });

    // Settings operations
    ipcMain.handle('get-settings', async () => {
      return this.settings;
    });

    ipcMain.handle('save-settings', async (event, newSettings) => {
      this.settings = { ...this.settings, ...newSettings };
      store.set('settings', this.settings);
      this.applySettings();
      return { success: true };
    });

    // Analytics operations
    ipcMain.handle('get-analytics', async () => {
      return this.analytics;
    });

    ipcMain.handle('update-analytics', async (event, eventType, data) => {
      this.updateAnalytics(eventType, data);
      return { success: true };
    });

    // Window operations
    ipcMain.handle('minimize-window', async (event) => {
      const window = BrowserWindow.fromWebContents(event.sender);
      if (window) {
        window.hide();
      }
      return { success: true };
    });

    ipcMain.handle('close-window', async (event) => {
      const window = BrowserWindow.fromWebContents(event.sender);
      if (window) {
        window.close();
      }
      return { success: true };
    });

    ipcMain.handle('toggle-always-on-top', async (event) => {
      const window = BrowserWindow.fromWebContents(event.sender);
      if (window) {
        const isOnTop = window.isAlwaysOnTop();
        window.setAlwaysOnTop(!isOnTop);
        return { success: true, isOnTop: !isOnTop };
      }
      return { success: false };
    });

    // Import/Export operations
    ipcMain.handle('import-notes', async () => {
      return await this.importNotes();
    });

    ipcMain.handle('export-notes', async () => {
      return await this.exportAllNotes();
    });

    // Backup operations
    ipcMain.handle('create-backup', async () => {
      await this.createBackup();
      return { success: true };
    });

    ipcMain.handle('restore-backup', async (event, backupPath) => {
      try {
        const backupData = JSON.parse(await fs.readFile(backupPath, 'utf8'));
        if (backupData.instances) {
          store.set('instances', backupData.instances);
        }
        if (backupData.settings) {
          this.settings = backupData.settings;
          store.set('settings', this.settings);
        }
        return { success: true };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    // System operations
    ipcMain.handle('get-system-info', async () => {
      return {
        platform: process.platform,
        arch: process.arch,
        version: app.getVersion(),
        electronVersion: process.versions.electron,
        nodeVersion: process.versions.node,
        chromeVersion: process.versions.chrome
      };
    });

    ipcMain.handle('open-external', async (event, url) => {
      shell.openExternal(url);
      return { success: true };
    });

    ipcMain.handle('show-item-in-folder', async (event, path) => {
      shell.showItemInFolder(path);
      return { success: true };
    });
  }

  applySettings() {
    // Update global shortcuts
    this.setupGlobalShortcuts();

    // Update all windows
    this.windows.forEach(window => {
      if (!window.isDestroyed()) {
        window.setAlwaysOnTop(this.settings.alwaysOnTop);
        window.setSkipTaskbar(!this.settings.showInTaskbar);
        window.setOpacity(this.settings.opacity);
        window.webContents.send('settings-updated', this.settings);
      }
    });

    // Update tray
    if (this.tray) {
      this.createTray(); // Recreate tray with updated menu
    }
  }
}

// Create app instance
const smartNotesApp = new SmartNotesProApp();

// Handle deep linking
app.on('open-url', (event, url) => {
  event.preventDefault();
  // Handle smartnotes:// protocol
  console.log('Deep link:', url);
});

// Prevent multiple instances
const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', (event, commandLine, workingDirectory) => {
    // Someone tried to run a second instance, focus our window instead
    if (smartNotesApp.managerWindow) {
      if (smartNotesApp.managerWindow.isMinimized()) {
        smartNotesApp.managerWindow.restore();
      }
      smartNotesApp.managerWindow.focus();
    } else {
      smartNotesApp.createManagerWindow();
    }
  });
}