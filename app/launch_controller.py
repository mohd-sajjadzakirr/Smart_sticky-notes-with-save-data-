#!/usr/bin/env python3
"""
Instance Controller Launcher
This script launches the instance controller for managing multiple sticky note instances.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from instance_controller import InstanceController
    
    print("Launching Instance Controller...")
    controller = InstanceController()
    controller.show_controller()
    controller.controller_window.mainloop()
    
except ImportError as e:
    print(f"Error importing instance controller: {e}")
    print("Make sure you're running this from the project root directory.")
except Exception as e:
    print(f"Error launching instance controller: {e}") 