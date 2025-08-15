@echo off
echo Creating Desktop Shortcut for Smart Notes Widget...

REM Get the current directory
set "SCRIPT_DIR=%~dp0"
set "PYW_PATH=%SCRIPT_DIR%run_no_console.pyw"

REM Create VBS script to make shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%USERPROFILE%\Desktop\Smart Notes Widget.lnk" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "pythonw.exe" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Arguments = "%PYW_PATH%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "Smart Notes Widget - Desktop Sticky Notes" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "%SCRIPT_DIR%assets\icon.png,0" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WindowStyle = 7 >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

REM Run the VBS script
cscript //nologo "%TEMP%\CreateShortcut.vbs"

REM Clean up
del "%TEMP%\CreateShortcut.vbs"

if exist "%USERPROFILE%\Desktop\Smart Notes Widget.lnk" (
    echo ✅ Desktop shortcut created successfully!
    echo 📍 Location: %USERPROFILE%\Desktop\Smart Notes Widget.lnk
) else (
    echo ❌ Failed to create desktop shortcut
)

pause 