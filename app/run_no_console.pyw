#!/usr/bin/env python3
"""
Smart Notes Widget - No Console Version
This file runs without showing a command prompt window
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from sticky_notes_widget import DesktopWidget
    import tkinter as tk
    from tkinter import messagebox
    import threading
    import time
except ImportError as e:
    # Show error in a GUI dialog since there's no console
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("Import Error", f"Failed to import required modules:\n{e}")
    sys.exit(1)

def check_single_instance():
    """Check if another instance is already running"""
    try:
        import win32gui
        import win32con
        
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if "Smart Notes" in window_text:
                    windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if len(windows) > 0:
            # Bring existing window to front
            hwnd = windows[0]
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            return True
        return False
        
    except ImportError:
        # win32gui not available, continue anyway
        return False

def main():
    """Main application entry point"""
    # Check for single instance
    if check_single_instance():
        return
    
    try:
        # Create and run the widget
        widget = DesktopWidget()
        
        # Set up auto-save in background thread
        def auto_save_worker():
            while True:
                try:
                    if hasattr(widget, 'save_notes'):
                        widget.save_notes()
                    time.sleep(30)  # Save every 30 seconds
                except:
                    break
        
        auto_save_thread = threading.Thread(target=auto_save_worker, daemon=True)
        auto_save_thread.start()
        
        # Start the main event loop
        widget.run()
        
    except Exception as e:
        error_msg = f"Failed to start Smart Notes Widget:\n{e}"
        messagebox.showerror("Error", error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main() 