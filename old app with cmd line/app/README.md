# Smart Notes Widget

A modern, feature-rich desktop sticky notes widget application built with Python and Tkinter.

## 🚀 Features

- **Modern UI**: Dark theme with sleek design
- **Drag & Drop**: Move the widget anywhere on your desktop
- **Resizable**: Custom resize handle for flexible sizing
- **Lock Functionality**: Lock position to prevent accidental movement
- **Minimize Widget**: Compact floating widget when minimized
- **Auto-Save**: Automatic saving of your notes
- **Modern Scrollbar**: Custom-designed scrollbar for better UX
- **Single Instance**: Prevents multiple instances from running
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📦 Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Quick Install
```bash
# Clone or download the project
cd app

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Development Install
```bash
# Install in development mode
pip install -e .

# Run using the console script
smart-notes
```

## 🎯 Usage

### Basic Operations
1. **Move Widget**: Click and drag anywhere on the widget
2. **Resize**: Use the resize handle (blue triangle) in the bottom-right corner
3. **Lock/Unlock**: Click the lock button (🔒/🔓) to prevent movement
4. **Minimize**: Click the minimize button (−) to hide the widget
5. **Restore**: Click the minimized widget to bring it back

### Advanced Features
- **Auto-Save**: Notes are automatically saved every 30 seconds
- **Position Memory**: Widget remembers its position between sessions
- **Size Memory**: Widget remembers its size between sessions
- **Theme Support**: Built-in dark theme with accent colors

## 🏗️ Project Structure

```
app/
├── main.py                 # Main application entry point
├── setup.py               # Package setup configuration
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── src/
│   └── sticky_notes_widget.py  # Main widget implementation
├── assets/
│   └── icon.png          # Application icon
├── dist/                 # Distribution files (generated)
└── docs/                 # Documentation (generated)
```

## 🔧 Development

### Running in Development Mode
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Building for Distribution
```bash
# Build the package
python setup.py sdist bdist_wheel

# Install from built package
pip install dist/smart-notes-widget-1.0.0.tar.gz
```

## 🎨 Customization

### Themes
The application supports custom themes. You can modify the color scheme in `src/sticky_notes_widget.py`:

```python
self.themes = {
    'dark': {
        'bg_dark': '#1e1e1e',
        'bg_medium': '#2d2d2d',
        'bg_light': '#363636',
        'text_primary': '#ffffff',
        'text_secondary': '#cccccc',
        'accent': '#007acc',
        'success': '#28a745'
    },
    # Add your custom themes here
}
```

### Icons
Replace `assets/icon.png` with your custom icon (recommended size: 64x64 pixels).

## 🐛 Troubleshooting

### Common Issues

1. **Application won't start**
   - Ensure Python 3.6+ is installed
   - Check that all dependencies are installed: `pip install -r requirements.txt`

2. **Widget not visible**
   - Check if another instance is running
   - Look for the minimized widget in the bottom-right corner

3. **Cannot move widget**
   - Check if the lock button is enabled (🔒)
   - Try clicking the unlock button (🔓)

4. **Notes not saving**
   - Check file permissions in your user directory
   - Ensure the application has write access

### Logs
The application prints helpful information to the console. Check the terminal output for error messages.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation in the `docs/` folder
- Review the troubleshooting section above

## 🔄 Version History

- **v1.0.0**: Initial release with core functionality
  - Modern UI with dark theme
  - Drag and drop functionality
  - Resize handle
  - Lock/unlock feature
  - Minimize widget
  - Auto-save functionality
  - Custom scrollbar
  - Single instance protection

---

**Made with ❤️ for productivity enthusiasts** 