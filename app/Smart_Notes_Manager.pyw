#!/usr/bin/env python3
"""
Smart Notes Instance Manager Launcher
Double-click this file to start the Smart Notes Instance Manager
"""

import os
import sys
import subprocess

def main():
    """Launch the Smart Notes Instance Manager"""
    try:
        # Get the current directory (where this file is located)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Path to the standalone instance manager
        manager_path = os.path.join(current_dir, 'standalone_instance_manager.py')
        
        # Check if the manager file exists
        if not os.path.exists(manager_path):
            print(f"Error: Instance manager not found at: {manager_path}")
            return
        
        # Launch the standalone instance manager
        # Using pythonw.exe to avoid console window
        pythonw_path = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
        
        if os.path.exists(pythonw_path):
            # Use pythonw.exe if available (no console window)
            subprocess.Popen([pythonw_path, manager_path], cwd=current_dir)
        else:
            # Fallback to regular python with hidden console
            subprocess.Popen([sys.executable, manager_path], 
                           cwd=current_dir,
                           creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
        
    except Exception as e:
        print(f"Error launching Smart Notes Manager: {e}")

if __name__ == "__main__":
    main() 