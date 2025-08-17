#!/usr/bin/env python3
"""
Diagnostic script to check auto-start registry and instance manager
"""

from auto_start_registry import AutoStartRegistry
import json
import os

def diagnose_auto_start():
    """Diagnose auto-start registry issues"""
    print("🔍 DIAGNOSING AUTO-START REGISTRY")
    print("=" * 60)
    
    # Check auto-start registry
    registry = AutoStartRegistry()
    
    print("\n📋 AUTO-START REGISTRY STATUS:")
    print(f"Registry file: {registry.registry_file}")
    print(f"File exists: {os.path.exists(registry.registry_file)}")
    print(f"Auto-start instances: {registry.get_auto_start_instances()}")
    print(f"Auto-start count: {registry.get_auto_start_count()}")
    
    # Check each auto-start instance
    print("\n📝 AUTO-START INSTANCES DETAILS:")
    auto_start_instances = registry.get_auto_start_instances()
    for instance_id, metadata in auto_start_instances.items():
        print(f"  Instance ID: {instance_id}")
        print(f"    Name: {metadata.get('name', 'Unknown')}")
        print(f"    Auto-start enabled: {metadata.get('auto_start_enabled', 'Unknown')}")
        print(f"    Created: {metadata.get('created_date', 'Unknown')}")
        print()
    
    # Check if instance metadata files exist
    print("📁 CHECKING INSTANCE METADATA FILES:")
    home_dir = os.path.expanduser('~')
    instance_files = []
    
    for filename in os.listdir(home_dir):
        if filename.startswith('.smart_notes_') and filename.endswith('_metadata.json'):
            instance_files.append(filename)
            print(f"  Found: {filename}")
    
    print(f"Total instance files found: {len(instance_files)}")
    
    # Check if auto-start instances have corresponding metadata files
    print("\n🔗 CHECKING AUTO-START vs METADATA FILES:")
    for instance_id in auto_start_instances.keys():
        metadata_file = f'.smart_notes_{instance_id}_metadata.json'
        metadata_path = os.path.join(home_dir, metadata_file)
        
        if os.path.exists(metadata_path):
            print(f"  ✅ {instance_id} - Metadata file exists")
        else:
            print(f"  ❌ {instance_id} - Metadata file MISSING")
    
    # Test auto-start registry functions
    print("\n🧪 TESTING AUTO-START REGISTRY FUNCTIONS:")
    for instance_id in auto_start_instances.keys():
        is_enabled = registry.is_auto_start_enabled(instance_id)
        print(f"  {instance_id}: is_auto_start_enabled() = {is_enabled}")
    
    print("\n✅ DIAGNOSIS COMPLETE!")

if __name__ == "__main__":
    diagnose_auto_start() 