#!/usr/bin/env python3
"""
Startup Manager for Smart Notes
Launches auto-start enabled instances when the system starts
"""

import os
import sys
import subprocess
import time
from auto_start_registry import AutoStartRegistry

class StartupManager:
    def __init__(self):
        self.auto_start_registry = AutoStartRegistry()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        
    def launch_auto_start_instances(self):
        """Launch all auto-start enabled instances"""
        try:
            auto_start_instances = self.auto_start_registry.get_auto_start_instances()
            
            if not auto_start_instances:
                print("No auto-start instances found.")
                return
            
            print(f"Launching {len(auto_start_instances)} auto-start instances...")
            
            for instance_id, metadata in auto_start_instances.items():
                try:
                    self.launch_instance(instance_id, metadata)
                    # Small delay to prevent overwhelming the system
                    time.sleep(0.5)
                except Exception as e:
                    print(f"Error launching instance {instance_id}: {e}")
            
            print("Auto-start instances launched successfully!")
            
        except Exception as e:
            print(f"Error in startup manager: {e}")
    
    def launch_instance(self, instance_id, metadata):
        """Launch a single instance"""
        try:
            # Path to the sticky notes widget
            widget_path = os.path.join(self.current_dir, 'other files', 'src', 'sticky_notes_widget.py')
            
            if not os.path.exists(widget_path):
                print(f"Widget not found at: {widget_path}")
                return False
            
            # Launch the instance with the instance ID
            process = subprocess.Popen([
                sys.executable, 
                widget_path, 
                '--instance-id', 
                instance_id
            ], cwd=self.current_dir)
            
            print(f"Launched instance: {metadata.get('name', instance_id)} (PID: {process.pid})")
            return True
            
        except Exception as e:
            print(f"Error launching instance {instance_id}: {e}")
            return False
    
    def run(self):
        """Main startup process"""
        print("🚀 Smart Notes Startup Manager")
        print("=" * 40)
        
        # Wait a bit for system to fully boot
        print("Waiting for system to stabilize...")
        time.sleep(2)
        
        # Launch auto-start instances
        self.launch_auto_start_instances()
        
        print("Startup process completed.")
        
        # Keep the process running for a short time to ensure instances start
        time.sleep(5)

def main():
    """Main entry point"""
    startup_manager = StartupManager()
    startup_manager.run()

if __name__ == "__main__":
    main() 