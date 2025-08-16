# Smart Notes Auto-Start Guide

## Overview

The Smart Notes application now features an **improved auto-start system** that automatically restores all previously open instances when you restart your computer, instead of creating new empty instances.

## 🆕 **New Features & Fixes**

### ✅ **Issue 1: Standalone Instance Manager**
- **Before**: Each sticky note had its own instance manager that closed when the note closed
- **After**: **Standalone instance manager** that stays open independently
- **How to use**: Click the manager button (📋) in any sticky note header
- **File**: `standalone_instance_manager.py` + `launch_instance_manager.bat`

### ✅ **Issue 2: Checkbox System for Selective Auto-Start**
- **Before**: All instances were restored on startup
- **After**: **Checkbox system** - only checked instances auto-start
- **How to use**: 
  - In instance manager: Check/uncheck instances
  - In sticky note settings: Toggle "Enable Auto-Start for this instance"

### ✅ **Issue 3: Hidden Command Prompt on Startup**
- **Before**: Command prompt window appeared on startup
- **After**: **Silent startup** - no command prompt visible
- **File**: `startup_manager_hidden.pyw`

### ✅ **Issue 4: Minimized Widget Mode on Startup**
- **Before**: Instances opened in full size on startup
- **After**: **Minimized widget mode** - instances start small and compact
- **Behavior**: Auto-restored instances automatically minimize

## 🚀 **How the New System Works**

### **Instance Management Flow**
1. **Create Instances**: Use the standalone instance manager
2. **Set Auto-Start**: Check/uncheck instances for auto-start
3. **Computer Restart**: Only checked instances are restored
4. **Restored State**: Instances open in minimized widget mode

### **Standalone Instance Manager**
- **Independent Operation**: Stays open regardless of sticky note status
- **Centralized Control**: Manage all instances from one place
- **Auto-Start Management**: Enable/disable auto-start per instance
- **Instance Operations**: Create, rename, delete, launch instances

## 📁 **New Files Created**

- `standalone_instance_manager.py` - **Main instance manager**
- `startup_manager_hidden.pyw` - **Hidden startup manager**
- `launch_instance_manager.bat` - **Easy launcher for manager**
- `enable_auto_start.bat` - **Updated for hidden mode**

## 🔧 **Modified Files**

- `src/sticky_notes_widget.py` - Added auto-start controls and minimized mode
- `startup_manager.py` - Updated for selective auto-start

## 🎯 **How to Use**

### **1. Launch Instance Manager**
```bash
# Method 1: Double-click
launch_instance_manager.bat

# Method 2: From sticky note
Click 📋 button in header → Settings → Instance Controller

# Method 3: Command line
python standalone_instance_manager.py
```

### **2. Create and Manage Instances**
1. **Create**: Click "Create New Instance" button
2. **Rename**: Select instance → "Rename Instance"
3. **Auto-Start**: Check/uncheck the checkbox column
4. **Launch**: Select instance → "Launch Instance"
5. **Delete**: Select instance → "Delete Instance"

### **3. Enable Global Auto-Start**
1. **In Instance Manager**: Click "Enable Global Auto-Start"
2. **In Sticky Note**: Settings → "Enable Auto-start"
3. **Using Batch File**: Double-click `enable_auto_start.bat`

### **4. Per-Instance Auto-Start**
1. **In Instance Manager**: Check/uncheck instance checkbox
2. **In Sticky Note**: Settings → "Enable Auto-Start for this instance"

## 🔍 **What Happens on Restart**

1. **System Startup**: Windows loads silently
2. **Hidden Manager**: `startup_manager_hidden.pyw` runs in background
3. **Instance Filtering**: Only checked instances are processed
4. **Smart Restoration**: Instances launch with exact same IDs
5. **Minimized Mode**: All restored instances start in widget mode
6. **Data Preservation**: Notes, settings, and positions intact

## 🛠 **Technical Implementation**

### **Instance Registry Structure**
```json
{
  "instance_id": {
    "name": "Instance Name",
    "auto_start": true/false,
    "created_date": "2025-08-16T...",
    "last_modified": "2025-08-16T...",
    "theme": "dark",
    "files": { ... }
  }
}
```

### **Auto-Start Registry Entry**
- **Key**: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
- **Value**: `SmartNotes_StartupManager`
- **Data**: `"python.exe" "startup_manager_hidden.pyw"`

### **Startup Process**
1. **Hidden Execution**: `startup_manager_hidden.pyw` runs silently
2. **Registry Read**: Loads instance registry
3. **Filtering**: Only processes instances with `auto_start: true`
4. **Launch**: Uses `--instance-id` parameter for exact restoration
5. **Minimized Mode**: Detects restored instances and minimizes them

## 🎨 **User Interface**

### **Instance Manager Features**
- **Modern Dark Theme**: Consistent with sticky notes
- **Checkbox Column**: Easy auto-start management
- **Status Display**: Shows running/stopped instances
- **Action Buttons**: Launch, rename, delete operations
- **Real-time Updates**: Automatic refresh and status updates

### **Sticky Note Integration**
- **Manager Button**: 📋 button in header opens instance manager
- **Settings Panel**: Auto-start toggle in instance settings
- **Smart Detection**: Automatically detects restored instances

## 🔒 **Security & Reliability**

### **Error Handling**
- **Silent Failures**: Hidden startup manager handles errors gracefully
- **Fallback Behavior**: If auto-start fails, instances remain available
- **Logging**: Console output for debugging (when visible)

### **Data Integrity**
- **Instance Persistence**: Registry survives system restarts
- **Metadata Backup**: Instance information stored in multiple locations
- **Graceful Degradation**: System continues working even if some features fail

## 🚨 **Troubleshooting**

### **Auto-Start Not Working**
1. Check if global auto-start is enabled
2. Verify instance checkboxes are checked
3. Check Windows Event Viewer for errors
4. Test with `startup_manager_hidden.pyw --enable-auto-start`

### **Instances Not Restoring**
1. Verify instance registry exists
2. Check auto-start checkboxes in instance manager
3. Ensure instances were properly closed (not force-killed)
4. Check file permissions in home directory

### **Command Prompt Still Visible**
1. Ensure using `startup_manager_hidden.pyw`
2. Check registry entry points to correct file
3. Verify `.pyw` extension (not `.py`)

### **Performance Issues**
1. Limit number of auto-start instances (5-10 recommended)
2. Check instance note file sizes
3. Monitor system resources during startup
4. Consider increasing startup delay in hidden manager

## 🎉 **Benefits of New System**

1. **✅ Standalone Manager**: Independent operation, always accessible
2. **✅ Selective Auto-Start**: Choose which instances to restore
3. **✅ Silent Startup**: No command prompt windows
4. **✅ Smart Restoration**: Instances start in appropriate mode
5. **✅ Better UX**: Centralized management, intuitive controls
6. **✅ Data Safety**: Notes and settings always preserved
7. **✅ Performance**: Only necessary instances are restored

## 📞 **Support**

If you encounter issues:
1. **Check Console**: Look for error messages in instance manager
2. **Verify Files**: Ensure all required files are present
3. **Test Components**: Try individual features separately
4. **Check Registry**: Verify auto-start entries are correct
5. **Review Logs**: Check Windows Event Viewer for system errors

---

**Note**: This system requires Python to be installed and accessible from the system PATH. The hidden startup manager will wait 5 seconds after system startup before attempting to restore instances to ensure the system is stable. 