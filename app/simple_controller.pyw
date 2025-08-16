#!/usr/bin/env pythonw
"""
Simple Instance Controller (.pyw version)
Direct launch without console window
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run
from instance_controller import InstanceController

controller = InstanceController()
controller.show_controller()
controller.controller_window.mainloop() 