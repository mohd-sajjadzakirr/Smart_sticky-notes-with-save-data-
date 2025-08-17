#!/usr/bin/env python3
"""
Simple launcher for the Smart Notes Instance Manager
"""

import subprocess
import os
import sys

def main():
    """Launch the standalone instance manager"""
    try:
        # Get the current directory (should be the app folder)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        manager_path = os.path.join(current_dir, 'standalone_instance_manager.py')
        
        # Check if the manager file exists
        if not os.path.exists(manager_path):
            print(f"Error: Instance manager not found at: {manager_path}")
            return
        
        # Launch the standalone instance manager (hidden console)
        print("🚀 Launching Smart Notes Instance Manager...")
        subprocess.Popen([sys.executable, manager_path], 
                        cwd=current_dir,
                        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        
    except Exception as e:
        print(f"Error launching instance manager: {e}")

if __name__ == "__main__":
    main() 