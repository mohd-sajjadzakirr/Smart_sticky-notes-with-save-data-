@echo off
echo Installing Smart Notes Widget...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.6+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo.
echo To run Smart Notes Widget:
echo   1. Double-click launch.bat
echo   2. Or run: python main.py
echo.
echo To install as a system command:
echo   pip install -e .
echo.
pause 