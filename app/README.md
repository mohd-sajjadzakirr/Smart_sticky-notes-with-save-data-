# 📝 Smart Notes - Multi-Instance Sticky Notes Application

A powerful desktop sticky notes application with multi-instance support, auto-start functionality, and centralized management.

## 🚀 Quick Start

### **Option 1: Simple Launch (Recommended)**
1. **Double-click** `Smart_Notes_Manager.pyw`
2. The Smart Notes Instance Manager will open
3. Click **"Create New Instance"** to create your first sticky note

### **Option 2: Alternative Launch**
- **Double-click** `Start_Smart_Notes.bat`
- Or run: `python standalone_instance_manager.py`

## 📋 Features

### **🎯 Core Features**
- ✅ **Multiple Sticky Notes** - Create unlimited instances
- ✅ **Auto-Start System** - Notes start automatically with Windows
- ✅ **Centralized Management** - Control all notes from one place
- ✅ **Persistent Storage** - Notes survive system restarts
- ✅ **Modern UI** - Clean, dark theme interface
- ✅ **Drag & Drop** - Move notes anywhere on screen
- ✅ **Resizable** - Adjust note size as needed
- ✅ **Minimize to Tray** - Keep notes hidden when not needed

### **🎛️ Instance Management**
- **Create New Instance** - Add new sticky notes
- **Enable/Disable Auto-Start** - Control which notes start automatically
- **Rename Instances** - Give notes meaningful names
- **Delete Instances** - Remove unwanted notes
- **Launch Instances** - Start stopped notes
- **Global Auto-Start** - Enable system-wide auto-start

## 🛠️ Installation & Setup

### **Prerequisites**
- **Python 3.7+** installed on your system
- **Windows 10/11** (optimized for Windows)

### **Installation Steps**

1. **Download/Extract** the application to a folder
2. **Open Command Prompt** in the app folder
3. **Install Dependencies** (if needed):
   ```bash
   pip install tkinter pillow
   ```
4. **Launch the App**:
   ```bash
   python standalone_instance_manager.py
   ```

## 📖 User Guide

### **Getting Started**

#### **1. First Launch**
1. Double-click `Smart_Notes_Manager.pyw`
2. The **Smart Notes Instance Manager** window opens
3. Click **"Create New Instance"** to create your first note
4. A sticky note window will appear

#### **2. Using Sticky Notes**
- **Type** your notes in the text area
- **Drag** the note to move it around
- **Resize** by holding Ctrl and dragging the corner
- **Minimize** using the **−** button (hides to system tray)
- **Close** using the **×** button

#### **3. Sticky Note Controls**
- **🔓 Lock/Unlock** - Prevent moving/resizing
- **⚙️ Settings** - Change transparency, themes
- **📋 Instance Manager** - Open the main manager
- **− Minimize** - Hide to system tray
- **× Close** - Close the note

### **Managing Multiple Instances**

#### **Creating New Instances**
1. In the Instance Manager, click **"Create New Instance"**
2. A new sticky note will open
3. Each instance is completely independent

#### **Enabling Auto-Start for Instances**
1. **Select** an instance from the list
2. Click **"Enable Auto-Start"**
3. The instance will now start automatically with Windows

#### **Disabling Auto-Start for Instances**
1. **Select** an instance from the list
2. Click **"Disable Auto-Start"**
3. The instance will no longer start automatically

#### **Renaming Instances**
1. **Select** an instance from the list
2. Click **"Rename Instance"**
3. Enter a new name and click OK

#### **Deleting Instances**
1. **Select** an instance from the list
2. Click **"Delete Instance"**
3. Confirm deletion (this removes the instance permanently)

### **Setting Up Global Auto-Start**

#### **Enable System-Wide Auto-Start**
1. In the Instance Manager, click **"Enable Global Auto-Start"**
2. This registers the app with Windows startup
3. **Restart your computer**
4. All auto-start enabled instances will open automatically

#### **Disable System-Wide Auto-Start**
1. In the Instance Manager, click **"Disable Global Auto-Start"**
2. The app will no longer start with Windows

## 🔧 Configuration

### **Instance Manager Interface**

The Instance Manager shows:
- **☑/☐** - Auto-start status (enabled/disabled)
- **Name** - Instance name
- **Status** - Running/Stopped
- **Created** - Creation date
- **Modified** - Last modified date
- **Auto-Start** - Auto-start status text

### **Status Bar**
Shows real-time information:
- **Total** - Number of instances
- **Running** - Currently active instances
- **Auto-Start** - Instances set to auto-start

## 📁 File Structure

```
Smart_Notes/
├── Smart_Notes_Manager.pyw          # Main launcher (double-click this!)
├── Start_Smart_Notes.bat            # Alternative launcher
├── standalone_instance_manager.py   # Main application
├── auto_start_registry.py           # Auto-start management
├── startup_manager.py               # System startup handler
├── launch_manager.py                # Additional launcher
└── other files/
    ├── src/
    │   └── sticky_notes_widget.py   # Individual note widget
    └── assets/
        └── icon.png                 # Application icon
```

## 🔍 Troubleshooting

### **Common Issues**

#### **App Won't Start**
- **Check Python installation**: `python --version`
- **Try alternative launcher**: `Start_Smart_Notes.bat`
- **Check file permissions**: Run as administrator if needed

#### **Auto-Start Not Working**
1. **Enable Global Auto-Start** in Instance Manager
2. **Restart computer** (not just log out)
3. **Check Windows startup settings**:
   - Press `Win + R`, type `msconfig`
   - Go to "Startup" tab
   - Ensure Smart Notes is enabled

#### **Instances Not Showing**
- **Refresh the list**: Close and reopen Instance Manager
- **Check file permissions**: Ensure app can write to user directory
- **Restart the app**: Sometimes instances need to be reloaded

#### **Notes Not Saving**
- **Check disk space**: Ensure sufficient free space
- **Check file permissions**: App needs write access to user directory
- **Restart the app**: Sometimes file handles get locked

### **Debug Information**

#### **Enable Debug Mode**
Run from command line to see debug output:
```bash
python standalone_instance_manager.py
```

#### **Check Auto-Start Status**
Run the diagnostic script:
```bash
python diagnose_auto_start.py
```

## 🎨 Customization

### **Changing Themes**
1. Open a sticky note
2. Click the **⚙️ Settings** button
3. Adjust transparency and other settings

### **Keyboard Shortcuts**
- **Ctrl + Drag** - Resize note
- **Drag** - Move note
- **Click and drag** - Select text

## 🔒 Data Storage

### **Where Your Data is Stored**
- **User Directory**: `C:\Users\[YourUsername]\`
- **Instance Metadata**: `.smart_notes_[instance-id]_metadata.json`
- **Note Content**: `.smart_notes_[instance-id]_notes.txt`
- **Settings**: `.smart_notes_[instance-id]_settings.json`
- **Positions**: `.smart_notes_[instance-id]_position.json`
- **Auto-Start Registry**: `.smart_notes_auto_start.json`

### **Backup Your Notes**
To backup all your notes:
1. Copy the `.smart_notes_*` files from your user directory
2. Store them in a safe location
3. Restore by copying them back

## 🆘 Support

### **Getting Help**
1. **Check this README** for common solutions
2. **Run diagnostic scripts** to identify issues
3. **Check console output** for error messages
4. **Restart the application** if issues persist

### **Known Limitations**
- **Windows Only** - Optimized for Windows 10/11
- **Single User** - Not designed for multi-user systems
- **Local Storage** - Notes stored locally, not in cloud

## 📝 Version History

### **Current Version Features**
- ✅ Multi-instance sticky notes
- ✅ Auto-start system
- ✅ Centralized management
- ✅ Persistent storage
- ✅ Modern UI
- ✅ Drag & drop support
- ✅ Minimize to tray
- ✅ Settings customization

---

## 🎉 Quick Reference

### **Essential Commands**
```bash
# Launch the app
python standalone_instance_manager.py

# Check auto-start status
python diagnose_auto_start.py

# Test auto-start registry
python test_auto_start.py
```

### **File Locations**
- **Main App**: `Smart_Notes_Manager.pyw` (double-click to start)
- **Data**: `C:\Users\[YourUsername]\` (hidden files)
- **Auto-Start**: Windows Registry + `.smart_notes_auto_start.json`

### **Quick Setup**
1. Double-click `Smart_Notes_Manager.pyw`
2. Click "Create New Instance"
3. Click "Enable Global Auto-Start"
4. Restart computer
5. Enjoy automatic sticky notes!

---

**Happy Note-Taking! 📝✨** 