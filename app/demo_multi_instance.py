#!/usr/bin/env python3
"""
Multi-Instance Demo Script
This script demonstrates the new multi-instance functionality of Smart Notes.
"""

import sys
import os
import time
import subprocess
import threading

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def print_banner():
    """Print a nice banner for the demo"""
    print("=" * 60)
    print("🚀 SMART NOTES - MULTI-INSTANCE DEMO 🚀")
    print("=" * 60)
    print()

def demo_instance_creation():
    """Demonstrate instance creation"""
    print("📝 DEMO 1: Creating Multiple Instances")
    print("-" * 40)
    
    try:
        from instance_controller import InstanceController
        
        # Create controller
        controller = InstanceController()
        
        # Create 3 demo instances
        print("Creating 3 demo instances...")
        for i in range(3):
            controller.create_instance()
            time.sleep(1)  # Small delay between creations
        
        print("✅ Created 3 demo instances successfully!")
        print("   - Each instance has its own storage and settings")
        print("   - Check your home directory for instance files")
        print()
        
        return controller
        
    except Exception as e:
        print(f"❌ Error creating instances: {e}")
        return None

def demo_instance_management(controller):
    """Demonstrate instance management features"""
    print("🔧 DEMO 2: Instance Management Features")
    print("-" * 40)
    
    if not controller:
        print("❌ Controller not available")
        return
    
    try:
        # Show instance controller
        print("Opening Instance Controller...")
        controller.show_controller()
        
        print("✅ Instance Controller opened!")
        print("   - You can now see all instances")
        print("   - Try renaming, cloning, or deleting instances")
        print("   - Each instance is completely isolated")
        print()
        
    except Exception as e:
        print(f"❌ Error opening controller: {e}")

def demo_file_structure():
    """Show the file structure created by instances"""
    print("📁 DEMO 3: Instance File Structure")
    print("-" * 40)
    
    home_dir = os.path.expanduser('~')
    instance_files = []
    
    try:
        # Scan for instance files
        for filename in os.listdir(home_dir):
            if filename.startswith('.smart_notes_') and filename.endswith('_metadata.json'):
                instance_files.append(filename)
        
        if instance_files:
            print(f"Found {len(instance_files)} instance metadata files:")
            for filename in instance_files:
                print(f"   📄 {filename}")
            
            # Show a sample metadata structure
            if instance_files:
                sample_file = os.path.join(home_dir, instance_files[0])
                try:
                    import json
                    with open(sample_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    
                    print(f"\n📋 Sample metadata from {instance_files[0]}:")
                    print(f"   Instance ID: {metadata.get('instance_id', 'N/A')[:8]}...")
                    print(f"   Name: {metadata.get('name', 'N/A')}")
                    print(f"   Created: {metadata.get('created_date', 'N/A')[:10]}")
                    print(f"   Theme: {metadata.get('theme', 'N/A')}")
                    
                except Exception as e:
                    print(f"   Could not read metadata: {e}")
        else:
            print("No instance files found yet.")
            print("Create some instances first!")
        
        print()
        
    except Exception as e:
        print(f"❌ Error scanning files: {e}")

def demo_launch_instances():
    """Demonstrate launching specific instances"""
    print("🚀 DEMO 4: Launching Specific Instances")
    print("-" * 40)
    
    home_dir = os.path.expanduser('~')
    
    try:
        # Find an instance to launch
        instance_files = [f for f in os.listdir(home_dir) 
                         if f.startswith('.smart_notes_') and f.endswith('_metadata.json')]
        
        if instance_files:
            # Launch the first instance found
            sample_file = os.path.join(home_dir, instance_files[0])
            import json
            with open(sample_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            instance_id = metadata.get('instance_id')
            instance_name = metadata.get('name', 'Unknown')
            
            print(f"Launching instance: {instance_name}")
            print(f"Instance ID: {instance_id[:8]}...")
            
            # Launch the instance
            script_path = os.path.join(os.path.dirname(__file__), 'src', 'sticky_notes_widget.py')
            subprocess.Popen([sys.executable, script_path, '--instance-id', instance_id])
            
            print("✅ Instance launched successfully!")
            print("   - This instance has its own data and settings")
            print("   - Try typing some notes - they're saved separately")
            print()
        else:
            print("No instances found to launch.")
            print("Create some instances first!")
            print()
            
    except Exception as e:
        print(f"❌ Error launching instance: {e}")

def main():
    """Main demo function"""
    print_banner()
    
    print("This demo will showcase the new multi-instance functionality!")
    print("You'll see how to create, manage, and use multiple instances.")
    print()
    
    input("Press Enter to start the demo...")
    print()
    
    # Demo 1: Instance Creation
    controller = demo_instance_creation()
    
    input("Press Enter to continue to instance management...")
    print()
    
    # Demo 2: Instance Management
    demo_instance_management(controller)
    
    input("Press Enter to see the file structure...")
    print()
    
    # Demo 3: File Structure
    demo_file_structure()
    
    input("Press Enter to launch a specific instance...")
    print()
    
    # Demo 4: Launch Specific Instance
    demo_launch_instances()
    
    print("🎉 DEMO COMPLETE!")
    print("=" * 60)
    print("You now have multiple Smart Notes instances running!")
    print("Each instance is completely independent with its own:")
    print("   - Notes storage")
    print("   - Position and size")
    print("   - Theme settings")
    print("   - Minimize widget")
    print()
    print("Use the Instance Controller (📋 button) to manage all instances.")
    print("Happy multi-instance note-taking! 🚀📝")

if __name__ == "__main__":
    main() 