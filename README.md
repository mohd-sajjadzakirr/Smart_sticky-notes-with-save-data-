# 📝 Sticky Notes App

A lightweight, always-on-top sticky notes application built with Python and Tkinter. Perfect for keeping important notes visible on your desktop at all times.

## ✨ Features

- **Always on Top**: Stays visible above all other windows
- **Auto-Save**: Automatically saves your notes every 2 seconds after you stop typing
- **Draggable**: Click and drag the title bar to move the note anywhere on your screen
- **Customizable**: Change colors, fonts, and sizes to match your preferences
- **Persistent**: Notes are saved locally and restored when you restart the app
- **Minimal UI**: Clean, distraction-free interface
- **Right-Click Menu**: Quick access to copy, paste, cut, and clear functions

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher (comes pre-installed on most systems)
- No external packages required - uses only Python standard library

### Installation & Usage

1. **Download the files** to your desired folder
2. **Open a terminal/command prompt** in that folder
3. **Run the app**:
   ```bash
   python sticky_notes.py
   ```

That's it! The sticky note will appear on your screen and stay on top of all other windows.

## 🎨 Customization

Click the **⚙️** button in the title bar to open settings:

### Colors
- **Background**: Change the main note background color
- **Title Bar**: Customize the top bar color
- **Text**: Set your preferred text color

### Fonts
- **Font Family**: Choose from Arial, Times New Roman, Courier New, Verdana, or Georgia
- **Font Size**: Adjust from 8 to 24 points

## 💾 Data Storage

The app creates two local files:
- `sticky_notes.txt` - Your actual notes content
- `sticky_settings.json` - Your customization preferences

These files are saved in the same folder as the app and persist between sessions.

## 🔧 Advanced Features

### Auto-Save
- Notes are automatically saved 2 seconds after you stop typing
- Status bar shows when notes are being saved or have been saved
- Manual save option available in the right-click menu

### Window Management
- **Move**: Click and drag the title bar to reposition
- **Close**: Click the red ✕ button (notes are automatically saved)
- **Always on Top**: The note stays visible above all other applications

### Context Menu
Right-click anywhere in the text area for:
- Copy, Paste, Cut
- Clear All (with confirmation)
- Save Now (manual save)

## 🖥️ System Compatibility

- **Windows**: ✅ Fully supported
- **macOS**: ✅ Should work (may need minor adjustments)
- **Linux**: ✅ Should work with most distributions

## 🚀 Make It Start Automatically

### Windows
1. Press `Win + R`, type `shell:startup`, press Enter
2. Create a shortcut to `sticky_notes.py` in the startup folder
3. Or create a `.bat` file with: `python "C:\path\to\sticky_notes.py"`

### macOS
1. System Preferences → Users & Groups → Login Items
2. Add the sticky notes app

### Linux
1. Add to your desktop environment's startup applications
2. Or add to `~/.config/autostart/`

## 🐛 Troubleshooting

### Common Issues

**App won't start:**
- Ensure Python is installed and in your PATH
- Try running `python --version` in terminal

**Notes not saving:**
- Check if the app has write permissions in its folder
- Look for error messages in the status bar

**Window positioning issues:**
- The note remembers its last position
- If it's off-screen, delete the settings file to reset position

### Reset to Defaults
Delete both `sticky_notes.txt` and `sticky_settings.json` files to restore default settings.

## 📱 Tips for Best Experience

1. **Position strategically**: Place the note where it won't interfere with your work but remains visible
2. **Use colors**: Customize colors to match your desktop theme
3. **Font size**: Choose a size that's comfortable to read from your typical viewing distance
4. **Regular backups**: The notes file is plain text - easy to backup or sync

## 🤝 Contributing

Feel free to modify and improve the app! Some ideas for enhancements:
- Multiple notes support
- Rich text formatting
- Cloud sync integration
- Keyboard shortcuts
- Export to different formats

## 📄 License

This project is open source and available under the MIT License.

---

**Enjoy your sticky notes!** 🎉
