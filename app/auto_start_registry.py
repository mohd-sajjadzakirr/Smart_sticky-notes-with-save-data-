#!/usr/bin/env python3
"""
Auto-Start Registry Manager for Smart Notes
Manages instances that should start automatically with the system
"""

import json
import os
import sys
from datetime import datetime

class AutoStartRegistry:
    def __init__(self):
        self.registry_file = os.path.join(os.path.expanduser('~'), '.smart_notes_auto_start.json')
        self.auto_start_instances = {}
        self.load_registry()
    
    def load_registry(self):
        """Load auto-start registry from file"""
        try:
            if os.path.exists(self.registry_file):
                with open(self.registry_file, 'r', encoding='utf-8') as f:
                    self.auto_start_instances = json.load(f)
            else:
                self.auto_start_instances = {}
        except Exception as e:
            print(f"Error loading auto-start registry: {e}")
            self.auto_start_instances = {}
    
    def save_registry(self):
        """Save auto-start registry to file"""
        try:
            with open(self.registry_file, 'w', encoding='utf-8') as f:
                json.dump(self.auto_start_instances, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving auto-start registry: {e}")
            return False
    
    def add_instance(self, instance_id, instance_metadata):
        """Add an instance to auto-start registry"""
        try:
            # Add timestamp for when auto-start was enabled
            instance_metadata['auto_start_enabled'] = datetime.now().isoformat()
            self.auto_start_instances[instance_id] = instance_metadata
            return self.save_registry()
        except Exception as e:
            print(f"Error adding instance to auto-start: {e}")
            return False
    
    def remove_instance(self, instance_id):
        """Remove an instance from auto-start registry"""
        try:
            if instance_id in self.auto_start_instances:
                del self.auto_start_instances[instance_id]
                return self.save_registry()
            return True
        except Exception as e:
            print(f"Error removing instance from auto-start: {e}")
            return False
    
    def is_auto_start_enabled(self, instance_id):
        """Check if an instance has auto-start enabled"""
        return instance_id in self.auto_start_instances
    
    def get_auto_start_instances(self):
        """Get all auto-start enabled instances"""
        return self.auto_start_instances.copy()
    
    def get_auto_start_count(self):
        """Get count of auto-start enabled instances"""
        return len(self.auto_start_instances)
    
    def clear_all(self):
        """Clear all auto-start instances"""
        try:
            self.auto_start_instances = {}
            return self.save_registry()
        except Exception as e:
            print(f"Error clearing auto-start registry: {e}")
            return False
    
    def update_instance_metadata(self, instance_id, new_metadata):
        """Update metadata for an auto-start instance"""
        try:
            if instance_id in self.auto_start_instances:
                # Preserve auto-start timestamp
                auto_start_enabled = self.auto_start_instances[instance_id].get('auto_start_enabled')
                self.auto_start_instances[instance_id] = new_metadata
                if auto_start_enabled:
                    self.auto_start_instances[instance_id]['auto_start_enabled'] = auto_start_enabled
                return self.save_registry()
            return False
        except Exception as e:
            print(f"Error updating auto-start instance metadata: {e}")
            return False

def main():
    """Test the auto-start registry"""
    registry = AutoStartRegistry()
    
    # Test adding an instance
    test_instance = {
        'name': 'Test Instance',
        'created': '2025-08-17',
        'position': {'x': 100, 'y': 200},
        'size': {'width': 300, 'height': 400}
    }
    
    registry.add_instance('test-123', test_instance)
    print(f"Auto-start instances: {registry.get_auto_start_instances()}")
    print(f"Count: {registry.get_auto_start_count()}")
    
    # Test removing an instance
    registry.remove_instance('test-123')
    print(f"After removal - Count: {registry.get_auto_start_count()}")

if __name__ == "__main__":
    main() 