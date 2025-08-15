#!/usr/bin/env python3
"""
Smart Notes Widget - Desktop Sticky Notes Application
Main entry point for the application
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import threading
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from sticky_notes_widget import DesktopWidget
except ImportError as e:
    print(f"Error importing DesktopWidget: {e}")
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
    # Only show console output if running in console mode
    if sys.stdout and sys.stdout.isatty():
        print("🚀 Starting Smart Notes Widget...")
    
    # Check for single instance
    if check_single_instance():
        if sys.stdout and sys.stdout.isatty():
            print("⚠️  Another instance is already running. Bringing it to front.")
        return
    
    try:
        # Create and run the widget
        if sys.stdout and sys.stdout.isatty():
            print("📝 Initializing Smart Notes Widget...")
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
        
        if sys.stdout and sys.stdout.isatty():
            print("✅ Smart Notes Widget is ready!")
            print("💡 Tips:")
            print("   - Click and drag to move the widget")
            print("   - Use the resize handle (bottom-right) to resize")
            print("   - Click the lock button to prevent movement")
            print("   - Click minimize to hide the widget")
            print("   - Your notes are automatically saved")
        
        # Start the main event loop
        widget.run()
        
    except Exception as e:
        error_msg = f"Failed to start Smart Notes Widget:\n{e}"
        if sys.stdout and sys.stdout.isatty():
            print(f"❌ Error starting Smart Notes Widget: {e}")
        messagebox.showerror("Error", error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main() 