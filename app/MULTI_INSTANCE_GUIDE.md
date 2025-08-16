# 🚀 Multi-Instance Feature Guide

## Overview
The Smart Notes app now supports multiple instances! Each instance is completely isolated with its own:
- Notes storage
- Position settings
- Theme preferences
- Minimize widget
- Instance-specific metadata

## 🎯 Key Features

### 1. **Instance Controller**
- **Access**: Click the 📋 button in any instance's header
- **Functions**: Create, delete, open, clone, and manage instances
- **Persistent**: All instances are saved between app restarts

### 2. **Instance Isolation**
- Each instance has unique file storage
- Independent themes and settings
- Separate minimize widgets
- No data sharing between instances

### 3. **Instance Management**
- **Naming**: Custom names for each instance
- **Cloning**: Duplicate existing instances with their content
- **Deletion**: Remove instances and all associated data
- **Organization**: View all instances in one place

## 🛠️ How to Use

### **Launching the Instance Controller**

#### Option 1: From Any Instance
1. Open any Smart Notes instance
2. Click the 📋 button in the header
3. The Instance Controller window will open

#### Option 2: Direct Launch
```bash
# From project root
python launch_controller.py

# Or use the batch file (Windows)
launch_controller.bat
```

### **Creating a New Instance**
1. Open the Instance Controller
2. Click the **"+ New Instance"** button
3. A new instance will be created and launched automatically
4. The new instance gets a default name (e.g., "New Instance 1")

### **Managing Instances**

#### **Opening an Instance**
- Double-click any instance in the controller list
- Or click the instance name to focus it

#### **Renaming an Instance**
1. Open the Instance Controller
2. Double-click the instance name
3. Enter a new name
4. Press Enter or click outside to save

#### **Cloning an Instance**
1. Select an instance in the controller
2. Click the **"Clone"** button
3. A new instance will be created with the same content
4. The clone gets "(Copy)" added to its name

#### **Deleting an Instance**
1. Select an instance in the controller
2. Click the **"Delete"** button
3. Confirm the deletion
4. All instance data will be permanently removed

### **Instance Settings**
Each instance has its own settings accessible via the ⚙️ button:
- **Instance Management**: Rename the current instance
- **Theme Selection**: Choose from Dark, Light, or Blue themes
- **Transparency**: Adjust window opacity
- **Auto-start**: Enable/disable startup with Windows

## 📁 File Structure

Each instance creates these files in your home directory:
```
~/.smart_notes_{instance_id}_metadata.json    # Instance info
~/.smart_notes_{instance_id}_notes.txt        # Notes content
~/.smart_notes_{instance_id}_settings.json    # Theme & preferences
~/.smart_notes_{instance_id}_position.json    # Window position & size
~/.smart_notes_{instance_id}_mini_position.json # Minimize widget position
```

## 🔧 Technical Details

### **Instance IDs**
- Each instance gets a unique UUID
- Instance IDs are used in filenames and metadata
- IDs are persistent and never change

### **Instance Metadata**
```json
{
  "instance_id": "uuid-string",
  "name": "Instance Name",
  "created_date": "2024-01-01T00:00:00",
  "last_modified": "2024-01-01T00:00:00",
  "theme": "dark",
  "files": {
    "settings": "~/.smart_notes_{id}_settings.json",
    "notes": "~/.smart_notes_{id}_notes.txt",
    "position": "~/.smart_notes_{id}_position.json",
    "mini_position": "~/.smart_notes_{id}_mini_position.json"
  }
}
```

### **Command Line Launch**
You can launch a specific instance directly:
```bash
python src/sticky_notes_widget.py --instance-id <instance_id>
```

## 🎨 Customization

### **Instance Themes**
- Each instance can have different themes
- Themes are saved per-instance
- Available themes: Dark, Light, Blue

### **Instance Names**
- Custom names for easy identification
- Names are displayed in window titles
- Names are saved in instance metadata

## 🚨 Important Notes

### **Data Safety**
- **Deleting an instance permanently removes all data**
- **No recovery option** - deletion is irreversible
- Always backup important notes before deleting instances

### **Performance**
- Multiple instances use more system resources
- Each instance runs independently
- No limit on the number of instances

### **File Management**
- Instance files are stored in your home directory
- Files are automatically created when needed
- Don't manually delete instance files

## 🐛 Troubleshooting

### **Instance Controller Won't Open**
- Check if Python is properly installed
- Ensure all required files are present
- Try launching directly: `python launch_controller.py`

### **Instances Not Loading**
- Check file permissions in your home directory
- Verify metadata files exist and are readable
- Try refreshing the controller (🔄 button)

### **Instance Names Not Saving**
- Check if the home directory is writable
- Verify JSON file permissions
- Try renaming again

### **Lost Instance Data**
- Check if instance files still exist
- Verify file paths are correct
- Restart the app to reload instances

## 🔮 Future Enhancements

Potential features for future versions:
- Instance grouping and categories
- Instance templates
- Data export/import between instances
- Instance backup and restore
- Instance sharing (optional)
- Instance search and filtering

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all files are present
3. Check Python and tkinter installation
4. Review error messages in the console

---

**Happy Note-Taking! 📝✨** 