# 🚀 Smart Notes - Quick Setup Guide

## ⚡ 5-Minute Setup

### **Step 1: Launch the App**
1. **Double-click** `Smart_Notes_Manager.pyw`
2. The Smart Notes Instance Manager opens

### **Step 2: Create Your First Note**
1. Click **"Create New Instance"**
2. A sticky note window appears
3. Start typing your notes!

### **Step 3: Enable Auto-Start (Optional)**
1. **Select** your note from the list
2. Click **"Enable Auto-Start"**
3. Click **"Enable Global Auto-Start"**
4. **Restart your computer**
5. Your notes will open automatically!

---

## 📋 What Each File Does

| File | Purpose | When to Use |
|------|---------|-------------|
| `Smart_Notes_Manager.pyw` | **Main Launcher** | **Double-click this to start!** |
| `Start_Smart_Notes.bat` | Alternative Launcher | If .pyw doesn't work |
| `standalone_instance_manager.py` | Core Application | Command line launch |
| `auto_start_registry.py` | Auto-Start Manager | Manages which notes auto-start |
| `startup_manager.py` | System Startup | Handles Windows boot |
| `README.md` | Full Documentation | Complete user guide |

---

## 🎯 Essential Actions

### **Creating Notes**
- Click **"Create New Instance"** in the manager
- Each note is completely independent

### **Managing Notes**
- **Select** a note from the list
- Use buttons: **Enable/Disable Auto-Start**, **Rename**, **Delete**

### **Auto-Start Setup**
1. **Individual Notes**: Select note → "Enable Auto-Start"
2. **System-Wide**: Click "Enable Global Auto-Start"
3. **Restart Computer**: Notes will open automatically

---

## 🔧 Troubleshooting

### **App Won't Start?**
- Try `Start_Smart_Notes.bat` instead
- Check if Python is installed: `python --version`

### **Auto-Start Not Working?**
- Enable **Global Auto-Start** in the manager
- **Restart computer** (not just log out)
- Check Windows startup settings

### **Notes Not Showing?**
- Refresh the instance list
- Restart the application
- Check file permissions

---

## 📁 Your Data Location

All your notes are stored in:
```
C:\Users\[YourUsername]\
```

Files:
- `.smart_notes_*_notes.txt` - Your note content
- `.smart_notes_*_metadata.json` - Note settings
- `.smart_notes_auto_start.json` - Auto-start list

---

## 🎉 You're Ready!

**Quick Start Checklist:**
- ✅ App launches successfully
- ✅ Can create new notes
- ✅ Notes save automatically
- ✅ Auto-start enabled (optional)
- ✅ Notes open on boot (if auto-start enabled)

**Next Steps:**
1. Create your first note
2. Enable auto-start for important notes
3. Enable global auto-start
4. Restart computer to test
5. Enjoy your automatic sticky notes!

---

**Need Help?** Check the full `README.md` for detailed instructions. 