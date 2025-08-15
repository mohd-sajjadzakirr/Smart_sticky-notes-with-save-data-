#!/usr/bin/env python3
"""
Build script for Smart Notes Widget
Creates a Windows executable that runs without showing command prompt
"""

import os
import sys
import subprocess
import shutil

def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building Smart Notes Widget executable...")
    
    # Change to app directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window (GUI only)
        "--name=SmartNotesWidget",      # Executable name
        "--icon=assets/icon.png",       # Application icon
        "--add-data=assets;assets",     # Include assets folder
        "--hidden-import=PIL._tkinter_finder",  # Include PIL
        "--hidden-import=tkinter",      # Include tkinter
        "--hidden-import=tkinter.ttk",  # Include ttk
        "--hidden-import=json",         # Include json
        "--hidden-import=os",           # Include os
        "--hidden-import=sys",          # Include sys
        "--hidden-import=threading",    # Include threading
        "--hidden-import=time",         # Include time
        "--clean",                      # Clean build cache
        "main.py"                       # Main script
    ]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build completed successfully!")
        
        # Check if executable was created
        exe_path = os.path.join("dist", "SmartNotesWidget.exe")
        if os.path.exists(exe_path):
            print(f"📦 Executable created: {exe_path}")
            print(f"📏 File size: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
            
            # Create a launcher script
            create_launcher_script()
            
            return True
        else:
            print("❌ Executable not found!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def create_launcher_script():
    """Create a simple launcher script"""
    launcher_content = '''@echo off
echo Starting Smart Notes Widget...
start "" "dist\\SmartNotesWidget.exe"
'''
    
    with open("launch_exe.bat", "w") as f:
        f.write(launcher_content)
    
    print("📄 Created launcher script: launch_exe.bat")

def clean_build():
    """Clean build artifacts"""
    print("🧹 Cleaning build artifacts...")
    
    dirs_to_clean = ["build", "__pycache__"]
    files_to_clean = ["SmartNotesWidget.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🗑️  Removed {dir_name}")
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"🗑️  Removed {file_name}")

if __name__ == "__main__":
    print("🚀 Smart Notes Widget - Build Script")
    print("=" * 50)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"✅ PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller not found!")
        print("Please install it with: pip install pyinstaller")
        sys.exit(1)
    
    # Clean previous builds
    clean_build()
    
    # Build executable
    if build_executable():
        print("\n🎉 Build completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run: launch_exe.bat")
        print("2. Or double-click: dist/SmartNotesWidget.exe")
        print("3. The app will run without showing a command prompt")
    else:
        print("\n❌ Build failed!")
        sys.exit(1) 