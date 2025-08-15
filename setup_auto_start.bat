@echo off
echo ========================================
echo    Desktop Widget Auto-Start Setup
echo ========================================
echo.
echo This will set up your desktop widget to start automatically
echo when you boot your computer.
echo.
echo Press any key to continue...
pause >nul

echo.
echo Setting up auto-start...
echo.

REM Check if Python is available
python3 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python3 is not installed or not in PATH
    echo Please install Python 3.6+ and try again
    pause
    exit /b 1
)

REM Get the current directory
set "CURRENT_DIR=%~dp0"
set "WIDGET_PATH=%CURRENT_DIR%desktop_widget_simple.py"

REM Check if widget file exists
if not exist "%WIDGET_PATH%" (
    echo ERROR: Widget file not found at:
    echo %WIDGET_PATH%
    echo.
    echo Please make sure you're running this from the widget folder
    pause
    exit /b 1
)

echo Widget found at: %WIDGET_PATH%
echo.
echo Setting up auto-start in Windows Registry...
echo.

REM Create a VBS script to set registry (requires admin privileges)
echo Set WshShell = CreateObject("WScript.Shell") > "%TEMP%\setup_autostart.vbs"
echo WshShell.RegWrite "HKCU\Software\Microsoft\Windows\CurrentVersion\Run\DesktopWidget", "python3 ""%WIDGET_PATH%""", "REG_SZ" >> "%TEMP%\setup_autostart.vbs"

REM Run the VBS script
cscript //nologo "%TEMP%\setup_autostart.vbs"

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! Auto-start has been enabled.
    echo.
    echo Your desktop widget will now start automatically
    echo when you boot your computer.
    echo.
    echo To disable auto-start later:
    echo 1. Press Win + R
    echo 2. Type "msconfig" and press Enter
    echo 3. Go to Startup tab
    echo 4. Uncheck "DesktopWidget"
    echo.
    echo Cleaning up temporary files...
    del "%TEMP%\setup_autostart.vbs"
) else (
    echo.
    echo ERROR: Could not set up auto-start.
    echo This might require administrator privileges.
    echo.
    echo Alternative method:
    echo 1. Press Win + R
    echo 2. Type "shell:startup" and press Enter
    echo 3. Copy desktop_widget_simple.py to that folder
    echo.
    echo Cleaning up temporary files...
    del "%TEMP%\setup_autostart.vbs"
)

echo.
echo Setup complete! Press any key to exit...
pause >nul
