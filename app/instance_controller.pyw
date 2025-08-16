#!/usr/bin/env pythonw
"""
Instance Controller (.pyw version)
This script launches the instance controller for managing multiple sticky note instances.
No console window will be displayed.
"""

import sys
import os

# Add the src directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

try:
    # Import the instance controller
    from instance_controller import InstanceController
    
    # Create and show the controller
    controller = InstanceController()
    controller.show_controller()
    
    # Start the main event loop
    controller.controller_window.mainloop()
    
except ImportError as e:
    # If import fails, show error in a message box
    import tkinter as tk
    from tkinter import messagebox
    
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Import Error", 
                        f"Could not import instance controller: {e}\n\n"
                        f"Current directory: {current_dir}\n"
                        f"Looking for src directory: {src_dir}\n\n"
                        "Make sure you're running this from the project root directory.")
    root.destroy()
    
except Exception as e:
    # If any other error occurs, show error in a message box
    import tkinter as tk
    from tkinter import messagebox
    
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Runtime Error", 
                        f"Error launching instance controller: {e}")
    root.destroy() 