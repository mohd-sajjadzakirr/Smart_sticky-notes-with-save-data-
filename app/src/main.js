const { app, BrowserWindow, ipcMain, Menu, Tray, dialog, globalShortcut, screen } = require('electron');
const path = require('path');
const Store = require('electron-store');
const { v4: uuidv4 } = require('uuid');

// Initialize store
const store = new Store();

class SmartNotesApp {
    constructor() {
        this.windows = new Map();
        this.tray = null;
        this.isQuitting = false;
        this.settings = store.get('settings', this.getDefaultSettings());
        
        this.setupApp();
    }

    getDefaultSettings() {
        return {
            theme: 'dark',
            autoStart: false,
            globalHotkey: 'CommandOrControl+Shift+N',
            defaultSize: { width: 350, height: 450 },
            alwaysOnTop: true,
            showInTaskbar: false,
            autoSave: true,
            autoSaveInterval: 5000,
            maxInstances: 20,
            enableMarkdown: true,
            enableSearch: true,
            enableTags: true,
            enableSync: false
        };
    }

    setupApp() {
        // Handle app ready
        app.whenReady().then(() => {
            this.createTray();
            this.setupGlobalShortcuts();
            this.setupMenu();
            this.restoreInstances();
            
            // Create manager window if no instances exist
            if (this.windows.size === 0) {
                this.createManagerWindow();
            }
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
    }

    createTray() {
        const iconPath = path.join(__dirname, '../assets/tray-icon.png');
        this.tray = new Tray(iconPath);
        
        const contextMenu = Menu.buildFromTemplate([
            {
                label: 'New Note',
                click: () => this.createNoteWindow()
            },
            {
                label: 'Manager',
                click: () => this.createManagerWindow()
            },
            { type: 'separator' },
            {
                label: 'Settings',
                click: () => this.createSettingsWindow()
            },
            { type: 'separator' },
            {
                label: 'Quit',
                click: () => {
                    this.isQuitting = true;
                    app.quit();
                }
            }
        ]);

        this.tray.setContextMenu(contextMenu);
        this.tray.setToolTip('Smart Notes Enhanced');
        
        this.tray.on('double-click', () => {
            this.createNoteWindow();
        });
    }

    setupGlobalShortcuts() {
        if (this.settings.globalHotkey) {
            globalShortcut.register(this.settings.globalHotkey, () => {
                this.createNoteWindow();
            });
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
                        label: 'Manager',
                        accelerator: 'CmdOrCtrl+M',
                        click: () => this.createManagerWindow()
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
                    { role: 'selectall' }
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
                    { role: 'togglefullscreen' }
                ]
            }
        ];

        const menu = Menu.buildFromTemplate(template);
        Menu.setApplicationMenu(menu);
    }

    createNoteWindow(instanceId = null) {
        const id = instanceId || uuidv4();
        
        if (this.windows.has(id)) {
            this.windows.get(id).focus();
            return;
        }

        const savedData = store.get(`instances.${id}`, {});
        const bounds = savedData.bounds || {
            width: this.settings.defaultSize.width,
            height: this.settings.defaultSize.height,
            x: undefined,
            y: undefined
        };

        const window = new BrowserWindow({
            width: bounds.width,
            height: bounds.height,
            x: bounds.x,
            y: bounds.y,
            minWidth: 250,
            minHeight: 300,
            frame: false,
            alwaysOnTop: this.settings.alwaysOnTop,
            skipTaskbar: !this.settings.showInTaskbar,
            webPreferences: {
                nodeIntegration: true,
                contextIsolation: false,
                enableRemoteModule: true
            },
            show: false,
            transparent: true,
            hasShadow: true
        });

        window.loadFile(path.join(__dirname, 'note-window.html'));
        
        window.once('ready-to-show', () => {
            window.show();
            window.webContents.send('initialize', {
                instanceId: id,
                data: savedData,
                settings: this.settings
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

        this.windows.set(id, window);
        return window;
    }

    createManagerWindow() {
        if (this.managerWindow && !this.managerWindow.isDestroyed()) {
            this.managerWindow.focus();
            return;
        }

        this.managerWindow = new BrowserWindow({
            width: 900,
            height: 700,
            minWidth: 800,
            minHeight: 600,
            webPreferences: {
                nodeIntegration: true,
                contextIsolation: false
            },
            show: false,
            icon: path.join(__dirname, '../assets/icon.png')
        });

        this.managerWindow.loadFile(path.join(__dirname, 'manager-window.html'));
        
        this.managerWindow.once('ready-to-show', () => {
            this.managerWindow.show();
        });

        this.managerWindow.on('closed', () => {
            this.managerWindow = null;
        });
    }

    createSettingsWindow() {
        if (this.settingsWindow && !this.settingsWindow.isDestroyed()) {
            this.settingsWindow.focus();
            return;
        }

        this.settingsWindow = new BrowserWindow({
            width: 600,
            height: 500,
            resizable: false,
            webPreferences: {
                nodeIntegration: true,
                contextIsolation: false
            },
            show: false,
            parent: this.managerWindow,
            modal: true
        });

        this.settingsWindow.loadFile(path.join(__dirname, 'settings-window.html'));
        
        this.settingsWindow.once('ready-to-show', () => {
            this.settingsWindow.show();
        });

        this.settingsWindow.on('closed', () => {
            this.settingsWindow = null;
        });
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
                bounds: bounds
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
            if (instances[instanceId].autoRestore !== false) {
                this.createNoteWindow(instanceId);
            }
        });
    }

    setupIPC() {
        // Note operations
        ipcMain.handle('save-note', (event, instanceId, data) => {
            const currentData = store.get(`instances.${instanceId}`, {});
            store.set(`instances.${instanceId}`, {
                ...currentData,
                ...data,
                lastModified: new Date().toISOString()
            });
        });

        ipcMain.handle('load-note', (event, instanceId) => {
            return store.get(`instances.${instanceId}`, {});
        });

        ipcMain.handle('delete-note', (event, instanceId) => {
            store.delete(`instances.${instanceId}`);
            const window = this.windows.get(instanceId);
            if (window) {
                window.close();
                this.windows.delete(instanceId);
            }
        });

        // Manager operations
        ipcMain.handle('get-all-instances', () => {
            const instances = store.get('instances', {});
            return Object.keys(instances).map(id => ({
                id,
                ...instances[id]
            }));
        });

        ipcMain.handle('create-new-note', () => {
            const window = this.createNoteWindow();
            return window.id;
        });

        ipcMain.handle('show-note', (event, instanceId) => {
            const window = this.windows.get(instanceId);
            if (window) {
                window.show();
                window.focus();
            } else {
                this.createNoteWindow(instanceId);
            }
        });

        // Settings operations
        ipcMain.handle('get-settings', () => {
            return this.settings;
        });

        ipcMain.handle('save-settings', (event, newSettings) => {
            this.settings = { ...this.settings, ...newSettings };
            store.set('settings', this.settings);
            
            // Apply settings
            this.applySettings();
        });

        // Window operations
        ipcMain.handle('minimize-window', (event) => {
            const window = BrowserWindow.fromWebContents(event.sender);
            window.hide();
        });

        ipcMain.handle('close-window', (event) => {
            const window = BrowserWindow.fromWebContents(event.sender);
            window.close();
        });

        ipcMain.handle('toggle-always-on-top', (event) => {
            const window = BrowserWindow.fromWebContents(event.sender);
            const isOnTop = window.isAlwaysOnTop();
            window.setAlwaysOnTop(!isOnTop);
            return !isOnTop;
        });

        // Export/Import
        ipcMain.handle('export-notes', async () => {
            const result = await dialog.showSaveDialog({
                filters: [
                    { name: 'JSON Files', extensions: ['json'] },
                    { name: 'All Files', extensions: ['*'] }
                ]
            });

            if (!result.canceled) {
                const instances = store.get('instances', {});
                const fs = require('fs');
                fs.writeFileSync(result.filePath, JSON.stringify(instances, null, 2));
                return { success: true, path: result.filePath };
            }
            return { success: false };
        });

        ipcMain.handle('import-notes', async () => {
            const result = await dialog.showOpenDialog({
                filters: [
                    { name: 'JSON Files', extensions: ['json'] },
                    { name: 'All Files', extensions: ['*'] }
                ]
            });

            if (!result.canceled) {
                const fs = require('fs');
                try {
                    const data = JSON.parse(fs.readFileSync(result.filePaths[0], 'utf8'));
                    const currentInstances = store.get('instances', {});
                    store.set('instances', { ...currentInstances, ...data });
                    return { success: true, count: Object.keys(data).length };
                } catch (error) {
                    return { success: false, error: error.message };
                }
            }
            return { success: false };
        });
    }

    applySettings() {
        // Update global shortcut
        globalShortcut.unregisterAll();
        if (this.settings.globalHotkey) {
            globalShortcut.register(this.settings.globalHotkey, () => {
                this.createNoteWindow();
            });
        }

        // Update all windows
        this.windows.forEach(window => {
            window.setAlwaysOnTop(this.settings.alwaysOnTop);
            window.setSkipTaskbar(!this.settings.showInTaskbar);
            window.webContents.send('settings-updated', this.settings);
        });
    }
}

// Create app instance
new SmartNotesApp();