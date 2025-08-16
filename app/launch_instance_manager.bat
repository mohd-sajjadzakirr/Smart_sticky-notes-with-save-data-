@echo off
echo Launching Smart Notes Instance Manager...
echo.

REM Get the current directory
set "CURRENT_DIR=%~dp0"
set "MANAGER=%CURRENT_DIR%standalone_instance_manager.py"

REM Check if manager exists
if not exist "%MANAGER%" (
    echo Error: Instance manager not found at %MANAGER%
    pause
    exit /b 1
)

REM Launch the instance manager
python "%MANAGER%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Instance manager launched successfully!
) else (
    echo.
    echo Error: Failed to launch instance manager.
)

echo.
pause 