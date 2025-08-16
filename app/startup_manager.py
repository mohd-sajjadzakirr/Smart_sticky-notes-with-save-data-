#!/usr/bin/env python3
"""
Startup Manager for Smart Notes Widget
Handles restoring all previously open instances when the computer restarts
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
        print(f"Could not load instance registry: {e}")
    return {}

def restore_instances():
    """Restore only checked instances for auto-start"""
    print("Restoring Smart Notes instances...")
    
    # Get the instance registry
    instances = get_instance_registry()
    
    if not instances:
        print("No instances to restore")
        return
    
    # Filter only instances with auto-start enabled
    auto_start_instances = {instance_id: metadata for instance_id, metadata in instances.items() 
                           if metadata.get('auto_start', False)}
    
    if not auto_start_instances:
        print("No instances with auto-start enabled")
        return
    
    print(f"Found {len(auto_start_instances)} instances with auto-start enabled")
    
    # Get the path to the sticky notes widget
    current_dir = os.path.dirname(os.path.abspath(__file__))
    widget_path = os.path.join(current_dir, 'src', 'sticky_notes_widget.py')
    
    if not os.path.exists(widget_path):
        print(f"Widget not found at: {widget_path}")
        return
    
    # Launch each auto-start enabled instance
    for instance_id, metadata in auto_start_instances.items():
        try:
            print(f"Restoring auto-start instance: {metadata.get('name', instance_id[:8])}")
            
            # Launch the instance with its specific ID
            cmd = [sys.executable, widget_path, '--instance-id', instance_id]
            subprocess.Popen(cmd, cwd=current_dir)
            
            # Small delay between launches to avoid overwhelming the system
            time.sleep(1)
            
        except Exception as e:
            print(f"Failed to restore instance {instance_id}: {e}")
    
    print("Instance restoration complete")

def enable_auto_start():
    """Enable auto-start for the application"""
    try:
        import winreg
        
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Run",
                            0, winreg.KEY_SET_VALUE)
        
        # Create auto-start entry for the startup manager
        current_dir = os.path.dirname(os.path.abspath(__file__))
        startup_manager_path = os.path.join(current_dir, 'startup_manager.py')
        auto_start_value = f'"{sys.executable}" "{startup_manager_path}"'
        winreg.SetValueEx(key, "SmartNotes_StartupManager", 0, winreg.REG_SZ, auto_start_value)
        winreg.CloseKey(key)
        
        print("Global auto-start enabled for Smart Notes")
        return True
        
    except Exception as e:
        print(f"Could not enable global auto-start: {e}")
        return False

def main():
    """Main entry point"""
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--enable-auto-start':
        if enable_auto_start():
            print("Auto-start has been successfully enabled!")
            print("Smart Notes will now automatically restore all instances when you restart your computer.")
        else:
            print("Failed to enable auto-start.")
        return
    
    print("Smart Notes Startup Manager")
    print("=" * 40)
    
    # Wait a bit for the system to fully start
    print("Waiting for system to stabilize...")
    time.sleep(5)
    
    # Restore instances
    restore_instances()
    
    print("Startup Manager finished")

if __name__ == "__main__":
    main() 