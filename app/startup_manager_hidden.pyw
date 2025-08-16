#!/usr/bin/env python3
"""
Hidden Startup Manager for Smart Notes Widget
Runs without showing command prompt window
"""

import os
import json
import sys
import subprocess
import time
from pathlib import Path

def get_instance_registry():
    """Get the instance registry from file"""
    registry_file = os.path.join(os.path.expanduser('~'), '.smart_notes_instance_registry.json')
    try:
        if os.path.exists(registry_file):
            with open(registry_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        # Silent error handling for hidden mode
        pass
    return {}

def restore_instances():
    """Restore only checked instances for auto-start"""
    # Get the instance registry
    instances = get_instance_registry()
    
    if not instances:
        return
    
    # Filter only instances with auto-start enabled
    auto_start_instances = {instance_id: metadata for instance_id, metadata in instances.items() 
                           if metadata.get('auto_start', False)}
    
    if not auto_start_instances:
        return
    
    # Get the path to the sticky notes widget
    current_dir = os.path.dirname(os.path.abspath(__file__))
    widget_path = os.path.join(current_dir, 'src', 'sticky_notes_widget.py')
    
    if not os.path.exists(widget_path):
        return
    
    # Launch each auto-start enabled instance
    for instance_id, metadata in auto_start_instances.items():
        try:
            # Launch the instance with its specific ID
            cmd = [sys.executable, widget_path, '--instance-id', instance_id]
            subprocess.Popen(cmd, cwd=current_dir, 
                           creationflags=subprocess.CREATE_NO_WINDOW)  # Hide console window
            
            # Small delay between launches to avoid overwhelming the system
            time.sleep(1)
            
        except Exception as e:
            # Silent error handling for hidden mode
            pass

def enable_auto_start():
    """Enable auto-start for the application"""
    try:
        import winreg
        
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Run",
                            0, winreg.KEY_SET_VALUE)
        
        # Create auto-start entry for the HIDDEN startup manager
        current_dir = os.path.dirname(os.path.abspath(__file__))
        startup_manager_path = os.path.join(current_dir, 'startup_manager_hidden.pyw')
        auto_start_value = f'"{sys.executable}" "{startup_manager_path}"'
        winreg.SetValueEx(key, "SmartNotes_StartupManager", 0, winreg.REG_SZ, auto_start_value)
        winreg.CloseKey(key)
        
        return True
        
    except Exception as e:
        return False

def main():
    """Main entry point"""
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--enable-auto-start':
        enable_auto_start()
        return
    
    # Wait a bit for the system to fully start
    time.sleep(5)
    
    # Restore instances silently
    restore_instances()

if __name__ == "__main__":
    main() 