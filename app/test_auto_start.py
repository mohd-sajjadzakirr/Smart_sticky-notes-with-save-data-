#!/usr/bin/env python3
"""
Test script to debug auto-start registry functionality
"""

from auto_start_registry import AutoStartRegistry
import os

def test_auto_start_registry():
    """Test the auto-start registry functionality"""
    print("🔍 Testing Auto-Start Registry...")
    print("=" * 50)
    
    # Create registry instance
    registry = AutoStartRegistry()
    
    # Check current state
    print(f"Registry file location: {registry.registry_file}")
    print(f"File exists: {os.path.exists(registry.registry_file)}")
    print(f"Current auto-start instances: {registry.get_auto_start_instances()}")
    print(f"Auto-start count: {registry.get_auto_start_count()}")
    
    # Test adding an instance
    print("\n📝 Testing add_instance...")
    test_metadata = {
        'name': 'Debug Test Instance',
        'created_date': '2025-08-17',
        'instance_id': 'debug-test-123'
    }
    
    success = registry.add_instance('debug-test-123', test_metadata)
    print(f"Add success: {success}")
    print(f"After add - Count: {registry.get_auto_start_count()}")
    print(f"After add - Instances: {list(registry.get_auto_start_instances().keys())}")
    
    # Test checking if enabled
    print(f"\n✅ Testing is_auto_start_enabled...")
    enabled = registry.is_auto_start_enabled('debug-test-123')
    print(f"Is enabled: {enabled}")
    
    # Test removing an instance
    print(f"\n🗑️ Testing remove_instance...")
    success = registry.remove_instance('debug-test-123')
    print(f"Remove success: {success}")
    print(f"After remove - Count: {registry.get_auto_start_count()}")
    
    # Test checking again
    enabled = registry.is_auto_start_enabled('debug-test-123')
    print(f"After remove - Is enabled: {enabled}")
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    test_auto_start_registry() 