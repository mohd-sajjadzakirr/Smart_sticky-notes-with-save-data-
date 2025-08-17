@echo off
title Smart Notes Instance Manager
cd /d "%~dp0"
pythonw.exe standalone_instance_manager.py
if errorlevel 1 (
    echo Pythonw.exe not found, trying python.exe...
    python.exe standalone_instance_manager.py
)
pause 