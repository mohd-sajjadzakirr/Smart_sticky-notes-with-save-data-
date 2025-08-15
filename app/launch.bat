@echo off
echo Starting Smart Notes Widget...
cd /d "%~dp0"
start /min pythonw main.py
if errorlevel 1 (
    echo Trying with python instead...
    start /min python main.py
) 